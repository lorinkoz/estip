# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import View, RedirectView, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import six

from braces.views import SetHeadlineMixin

from . import models, forms
from apps.audit.models import Trace
from common.mixins import ConsultorRequiredMixin, StaffRequiredMixin, MethodPreventMixin


class PaymentList(StaffRequiredMixin, SetHeadlineMixin, ListView):
    model = models.Payment
    paginate_by = 25
    page_kwarg = 'p'
    headline = 'Pagos'
    template_name = 'payments/payment_list.html'

    def get_queryset(self):
        queryset = super(PaymentList, self).get_queryset()
        query = self.request.GET.get('q','').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class PaymentCurrent(RedirectView):
    permanent = False

    def get_redirect_url(self):
        current = models.Payment.objects.filter(date_closed=None).first()
        if current:
            return reverse('payment_details', args=[current.slug])
        else:
            return reverse('payment_list')


class PaymentDetails(StaffRequiredMixin, SetHeadlineMixin, DetailView):
    model = models.Payment
    template_name = 'payments/payment_details.html'

    def get_headline(self):
        return self.get_object()

    def get_context_data(self, **kwargs):
        from apps.students.models import Student
        context = super(PaymentDetails, self).get_context_data(**kwargs)
        headers, data = self.get_object().tabulate(self.request.GET.get('q', ''), 10)
        context['headers'] = headers
        context['data'] = data
        context['total_amount'] = models.PaymentRecord.objects.filter(row__payment=self.get_object()).aggregate(total=Sum('amount'))['total']
        return context


class PaymentCreate(StaffRequiredMixin, MethodPreventMixin, SetHeadlineMixin, CreateView):
    model = models.Payment
    fields = ('name', 'description')
    headline = 'Inicializar pago'
    template_name = 'payments/payment_form.html'

    def prevent_all(self, request):
        return models.Payment.objects.filter(date_closed=None).exists()

    def get_success_url(self):
        return reverse('payment_details', args=[self.object.slug])

    def form_valid(self, form):
        payment = form.save(commit=False)
        Trace.log('{} inicializó el pago {}'.format(self.request.user.traceable_name, payment), self.request.user)
        return super(PaymentCreate, self).form_valid(form)


class PaymentUpdate(StaffRequiredMixin, SetHeadlineMixin, UpdateView):
    model = models.Payment
    fields = ('name', 'description')
    headline = 'Editar pago %s'
    template_name = 'payments/payment_form.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('payment_list'))

    def form_valid(self, form):
        payment = form.save(commit=False)
        Trace.log('{} editó el pago {}'.format(self.request.user.traceable_name, payment), self.request.user)
        return super(PaymentUpdate, self).form_valid(form)


class PaymentGenerate(StaffRequiredMixin, MethodPreventMixin, SetHeadlineMixin, DetailView):
    model = models.Payment
    headline = 'Calcular pago %s'
    template_name = 'payments/payment_generate.html'

    def prevent_all(self, request):
        return not self.get_object().can_generate

    def get_headline(self):
        return self.headline % self.get_object()

    def post(self, request, *args, **kwargs):
        from threading import Thread
        payment = self.get_object()
        form = forms.PaymentGenerationForm(request.POST)
        if form.is_valid():
            t = Thread(target=payment.generate, args=(form.cleaned_data, self.request.user.get_full_name()))
            t.start()
            Trace.log('{} inició el cálculo del pago {}'.format(request.user.traceable_name, payment), request.user)
            return redirect('payment_details', payment.slug)
        else:
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentGenerate, self).get_context_data(**kwargs)
        context['form'] = forms.PaymentGenerationForm()
        return context


class PaymentClose(StaffRequiredMixin, MethodPreventMixin, SetHeadlineMixin, UpdateView):
    model = models.Payment
    fields = ()
    headline = 'Cerrar pago %s'
    template_name = 'payments/payment_close.html'

    def prevent_all(self, request):
        return not self.get_object().can_close
    
    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('payment_list'))

    def form_valid(self, form):
        payment = form.save(commit=False)
        payment.close()
        Trace.log('{} cerró el pago {}'.format(self.request.user.traceable_name, payment), self.request.user)
        return super(PaymentClose, self).form_valid(form)


class PaymentDelete(StaffRequiredMixin, MethodPreventMixin, SetHeadlineMixin, DeleteView):
    model = models.Payment
    headline = 'Eliminar pago %s'
    template_name = 'payments/payment_delete.html'

    def prevent_all(self, request):
        return not self.get_object().can_delete

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return reverse('payment_list')

    def delete(self, request, *args, **kwargs):
        pass


class PaymentPrint(StaffRequiredMixin, View):
    max_page = 0

    def render_pdf(self, stream, payment, headers, data, title):
        from django.template.defaultfilters import floatformat
        from reportlab.lib import pagesizes, colors
        from reportlab.lib.units import inch
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph, PageBreak
        from apps.core.models import School
        ###
        school = School.objects.get()
        ###
        margin = margin = 0.5 * inch
        page_height, page_width = pagesizes.LETTER
        payment_column_width = 0.7 * inch
        name_column_width = page_width - 2*margin - payment_column_width*(len(headers)+3)
        ###
        stylesheet = getSampleStyleSheet()
        normalStyle = stylesheet['Normal']
        ###
        def make_totalizer():
            totalizer = []
            for header in headers + ['Total']:
                totalizer.append(0.0)
            return totalizer
        def parse_totalizer(title, totalizer, prefix=''):
            if prefix: prefix += ': '
            return ['', prefix.upper() + six.text_type(title)] + [floatformat(x, 2) for x in totalizer] + ['']
        def get_headers():
            return ['CODIGO', 'NOMBRE Y APELLIDOS'] + [x.get_alias() for x in headers] + ['TOTAL', 'FIRMA']
        def append_section_heading(main_story, container):
            main_story.append(Paragraph('<b>%s de %s<br/>Facultad de %s</b>' % (container.year, container.specialty, container.specialty.faculty), normalStyle))
            main_story.append(Spacer(0, 0.2*inch))
        def append_table(main_story, local_grid, final_rows):
            styles = [x for x in base_styles]
            styles.append(('LINEABOVE', (0,-final_rows), (-1,-final_rows), 1, colors.black))
            styles.append(('TOPPADDING', (0,1), (-1,-final_rows-1), 0.05*inch))
            styles.append(('BOTTOMPADDING', (0,1), (-1,-final_rows-1), 0.05*inch))
            main_story.append(Table(
                local_grid, style=TableStyle(styles), repeatRows=1,
                colWidths=[payment_column_width]+[name_column_width]+[payment_column_width]*(len(headers)+2)
            ))
        ###
        def global_page_template(c, d):
            c.saveState()
            image_width = 0
            if school.logo:
                image_width = school.logo.width*25/school.logo.height
                c.drawImage(school.logo.path, margin, page_height-margin*0.8-16, height=25, width=image_width)
            c.setFont('Times-Roman', 11)
            c.drawString(margin+image_width+10, page_height-margin*0.8, school.name)
            c.drawString(margin+image_width+10, page_height-margin*0.8-14, 'Estipendio Estudiantil - {}'.format(payment))
            c.setFont('Times-Roman', 10)
            c.drawString(page_width-margin-inch, page_height-margin*0.8, 'Calculado')
            c.drawString(page_width-margin-inch, page_height-margin*0.8-14, '{}'.format((payment.date_generated or payment.date_created).date()))
            page = c.getPageNumber()
            self.max_page = max(self.max_page, page)
            if payment.generated_by:
                c.drawString(margin, margin/2, 'Hecho por: {}'.format(payment.generated_by))
            c.drawString(page_width-margin-inch, margin/2, 'Página {} de {}'.format(page, self.max_page))
            c.restoreState()
        ###
        doc = SimpleDocTemplate(
            stream,
            pagesize=pagesizes.landscape(pagesizes.LETTER),
            leftMargin=margin,
            rightMargin=margin,
            topMargin=margin*1.5,
            bottomMargin=margin,
            title = title,
        )
        doc.title = title
        story = []
        base_styles = [
            ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
            ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
            ('ALIGN', (0,0), (0,-1), 'RIGHT'),
            # ('FONTNAME', (2, 1), (-1, -1), 'Courier'),
        ]
        if data:
            first = data[0]
            total = make_totalizer()
            faculty = (first.specialty.faculty, make_totalizer())
            specialty = (first.specialty, make_totalizer())
            year = (first.year, make_totalizer())
            grid = [get_headers()]
            append_section_heading(story, first)
            for row in data:
                breaker = 0
                if row.specialty.faculty != faculty[0]:
                    breaker = 3
                    grid.append(parse_totalizer(prefix='Total año', *year))
                    grid.append(parse_totalizer(prefix='Total especialidad', *specialty))
                    grid.append(parse_totalizer(prefix='Total facultad', *faculty))
                    year = (row.year, make_totalizer())
                    specialty = (row.specialty, make_totalizer())
                    faculty = (row.specialty.faculty, make_totalizer())
                elif row.specialty != specialty[0]:
                    breaker = 2
                    grid.append(parse_totalizer(prefix='Total año', *year))
                    grid.append(parse_totalizer(prefix='Total especialidad', *specialty))
                    year = (row.year, make_totalizer())
                    specialty = (row.specialty, make_totalizer())
                elif row.year != year[0]:
                    breaker = 1
                    grid.append(parse_totalizer(prefix='Total año', *year))
                    year = (row.year, make_totalizer())
                if breaker:
                    append_table(story, grid, breaker)
                    grid = [get_headers()]
                    story.append(PageBreak())
                    append_section_heading(story, row)
                grid.append([row.student.sid, row.student.full_name] + [floatformat(x, 2) for x in row.payments] + [floatformat(row.total, 2), '_'*8])
                for i in range(len(row.payments)):
                    year[1][i] += float(float(row.payments[i]))
                    specialty[1][i] += float(row.payments[i])
                    faculty[1][i] += float(row.payments[i])
                    total[i] += float(row.payments[i])
                year[1][-1] += float(row.total)
                specialty[1][-1] += float(row.total)
                faculty[1][-1] += float(row.total)
                total[-1] += float(row.total)
            grid.append(parse_totalizer(prefix='Total año', *year))
            grid.append(parse_totalizer(prefix='Total especialidad', *specialty))
            grid.append(parse_totalizer(prefix='Total facultad', *faculty))
            grid.append(parse_totalizer('TOTAL GENERAL', total))
            append_table(story, grid, 4)
        doc.build(story, onFirstPage=global_page_template, onLaterPages=global_page_template)
        return stream

    def get(self, request, slug):
        from StringIO import StringIO
        self.payment = get_object_or_404(models.Payment, slug=slug, status__gte=2)
        headers, data = self.payment.tabulate(limit=None)
        filename = '%s %s' % ('Estipendio', six.text_type(self.payment))
        self.render_pdf(StringIO(), self.payment, headers, data, filename)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="%s.pdf"' % filename
        return self.render_pdf(response, self.payment, headers, data, filename)

    def get_context_data(self, **kwargs):
        context = super(PaymentPrint, self).get_context_data(**kwargs)
        context['object'] = self.payment
        return context


class PaymentRecords(StaffRequiredMixin, MethodPreventMixin, SetHeadlineMixin, TemplateView):
    headline = 'Detalles de pago'
    template_name = 'payments/payment_records.html'

    def dispatch(self, request, slug, sid):
        from apps.students.models import Student
        self.payment = get_object_or_404(models.Payment, slug=slug)
        self.student = get_object_or_404(Student, sid=sid)
        self.row = get_object_or_404(models.PaymentRow, payment=self.payment, student=self.student)
        return super(PaymentRecords, self).dispatch(request, slug, sid)

    def prevent_all(self, request):
        return self.payment.is_closed

    def get(self, request, *args, **kwargs):
        data = {}
        for record in models.PaymentRecord.objects.filter(row=self.row):
            data[record.payment_type.slug] = record.amount
        self.form = forms.PaymentRecordsForm(initial=data)
        return super(PaymentRecords, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        from apps.core.models import PaymentType
        self.form = forms.PaymentRecordsForm(request.POST)
        if self.form.is_valid():
            deletion_list = []
            for payment_type in PaymentType.objects.all():
                amount = self.form.cleaned_data[payment_type.slug]
                if amount:
                    models.PaymentRecord.objects.update_or_create(
                        row=self.row, payment_type=payment_type,
                        defaults={'amount': amount})
                else:
                    deletion_list.append(payment_type)
            models.PaymentRecord.objects.filter(row=self.row, payment_type__in=deletion_list).delete()
            return redirect(self.request.GET.get('volver', reverse('payment_details', args=[self.payment.slug])))
        return super(PaymentRecords, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentRecords, self).get_context_data(**kwargs)
        context['payment'] = self.payment
        context['student'] = self.student
        context['row'] = self.row
        context['form'] = self.form
        return context