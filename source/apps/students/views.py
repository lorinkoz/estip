# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from braces.views import SetHeadlineMixin

from . import models, forms
from apps.core.models import PaymentRule
from common.mixins import StaffRequiredMixin, MethodPreventMixin


class StudentList(StaffRequiredMixin, SetHeadlineMixin, ListView):
    model = models.Student
    paginate_by = 25
    page_kwarg = 'p'
    headline = 'Estudiantes'
    template_name = 'students/student_list.html'

    def get_queryset(self):
        qs = super(StudentList, self).get_queryset().select_related('status', 'status__student_type', 'status__specialty', 'status__specialty__faculty')
        self.filter_form = forms.StudentFilterForm(self.request.GET)
        return self.filter_form.filter(qs)

    def get_context_data(self, **kwargs):
        context = super(StudentList, self).get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context


class ActiveStudentList(StudentList):
    headline = 'Estudiantes activos'
    queryset = models.Student.objects.exclude(status=None)


class InactiveStudentList(StudentList):
    headline = 'Estudiantes inactivos'
    queryset = models.Student.objects.filter(status=None)


class UnruledStudentList(StudentList):
    headline = 'Estudiantes sin reglas de pago'
    queryset = models.Student.objects.exclude(status=None).annotate(rules=Count('status__rules__pk')).filter(rules=0)


class StudentCreate(StaffRequiredMixin, SetHeadlineMixin, CreateView):
    model = models.Student
    headline = 'Nuevo estudiante'
    form_class = forms.StudentForm
    slug_url_kwarg = slug_field = 'sid'
    template_name = 'students/student_form.html'

    def get(self, request, *args, **kwargs):
        self.form2 = forms.StudentStatusForm()
        return super(StudentCreate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form2 = forms.StudentStatusForm(request.POST)
        return super(StudentCreate, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('student_list'))

    def form_valid(self, form):
        if self.form2.is_valid():
            status = self.form2.save()
            instance = form.save(commit=False)
            instance.status = status
            return super(StudentCreate, self).form_valid(form)
        return super(StudentCreate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(StudentCreate, self).get_context_data(**kwargs)
        context['show_form2'] = True
        context['form2'] = self.form2
        return context


class StudentUpdate(StaffRequiredMixin, SetHeadlineMixin, UpdateView):
    model = models.Student
    headline = 'Editar estudiante %s'
    form_class = forms.StudentForm
    slug_url_kwarg = slug_field = 'sid'
    template_name = 'students/student_form.html'

    def get(self, request, *args, **kwargs):
        self.instance2 = self.get_object().status
        self.form2 = forms.StudentStatusForm(instance=self.instance2)
        return super(StudentUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.instance2 = self.get_object().status
        self.form2 = forms.StudentStatusForm(request.POST, instance=self.instance2)
        return super(StudentUpdate, self).post(request, *args, **kwargs)
    
    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('student_list'))

    def form_valid(self, form):
        if self.instance2:
            if self.form2.is_valid():
                status = self.form2.save()
                instance = form.save(commit=False)
                instance.status = status
                return super(StudentUpdate, self).form_valid(form)
            else:
                return super(StudentUpdate, self).form_invalid(form)
        else:
            return super(StudentUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(StudentUpdate, self).get_context_data(**kwargs)
        context['show_form2'] = self.instance2 is not None
        context['form2'] = self.form2
        return context


class StudentDelete(StaffRequiredMixin, SetHeadlineMixin, DeleteView):
    model = models.Student
    headline = 'Eliminar estudiante %s'
    slug_url_kwarg = 'sid'
    slug_field = 'sid'
    template_name = 'students/student_delete.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('student_list'))


class StudentActivate(StaffRequiredMixin, SetHeadlineMixin, MethodPreventMixin, CreateView):
    model = models.StudentStatus
    form_class = forms.StudentStatusForm
    headline = 'Activar estudiante %s'
    template_name = 'students/student_activate.html'

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(models.Student, sid=self.kwargs['sid'])
        return super(StudentActivate, self).dispatch(request, *args, **kwargs)

    def prevent_all(self, request):
        return self.student.status is not None

    def get_headline(self):
        return self.headline % self.student

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('student_list'))

    def form_valid(self, form):
        instance = form.save()
        self.student.status = instance
        self.student.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(StudentActivate, self).get_context_data(**kwargs)
        context['student'] = self.student
        return context


class StudentDeactivate(StaffRequiredMixin, SetHeadlineMixin, MethodPreventMixin, DeleteView):
    model = models.StudentStatus
    headline = 'Desactivar estudiante %s'
    template_name = 'students/student_deactivate.html'

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(models.Student, sid=self.kwargs['sid'])
        return super(StudentDeactivate, self).dispatch(request, *args, **kwargs)

    def prevent_all(self, request):
        return self.student.status is None

    def get_object(self):
        return self.student.status

    def get_headline(self):
        return self.headline % self.get_object().student

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('student_list'))

    def get_context_data(self, **kwargs):
        context = super(StudentDeactivate, self).get_context_data(**kwargs)
        context['student'] = self.student
        return context


class StudentPromote(StaffRequiredMixin, SetHeadlineMixin, FormView):
    headline = 'Promover estudiantes'
    form_class = forms.StudentPromoteForm
    template_name = 'students/student_promote.html'

    def form_valid(self, form):
        exceptions = form.cleaned_data['exceptions']
         # NOTE: If we change year structures, the following array must be changed accordingly
        advance = [[],[],[],[],[],[],[]]
        for status in models.StudentStatus.objects.exclude(student__in=exceptions).select_related('specialty'):
            next_year = status.year + 1
            if next_year <= status.specialty.max_year:
                advance[next_year].append(status.pk)
            else: # We store in index 0 those to deactivate
                advance[0].append(status.pk)
        for i in range(1, len(advance)):
            models.StudentStatus.objects.filter(pk__in=advance[i]).update(year=i)
        models.StudentStatus.objects.filter(pk__in=advance[0]).delete()
        return redirect('student_list')

    def get_context_data(self, **kwargs):
        context = super(StudentPromote, self).get_context_data(**kwargs)
        return context


class StudentRulesTransform(StaffRequiredMixin, SetHeadlineMixin, FormView):
    headline = 'Transformar reglas de pago'
    form_class = forms.StudentRulesTransformForm
    template_name = 'students/student_rules_transform.html'

    def form_valid(self, form):
        locations = {}
        partitions = {}
        for rule in PaymentRule.objects.select_related('payment_type'):
            partitions.setdefault(rule.payment_type.pk, [])
            partitions[rule.payment_type.pk].append(rule.pk)
            locations[rule.pk] = rule.payment_type.pk
        to_add = []
        to_delete = []
        raw_transformed_rules = [int(x) for x in form.cleaned_data['transformed_rules']]
        for item in raw_transformed_rules:
            if item > 0:
                to_add.append(item)
                to_delete += partitions[locations[item]]
            else:
                to_delete += partitions[-item]
        to_delete = filter(lambda x: x not in to_add, to_delete)
        ####
        query = Q(pk__gte=0)
        if form.cleaned_data['student_type']: query &= Q(student_type=form.cleaned_data['student_type'])
        if form.cleaned_data['specialty']: query &= Q(specialty=form.cleaned_data['specialty'])
        if form.cleaned_data['year']: query &= Q(year=form.cleaned_data['year'])
        if form.cleaned_data['current_rules']: query &= Q(rules__in=form.cleaned_data['current_rules'])
        ###
        status_list = [x.pk for x in models.StudentStatus.objects.filter(query)]
        RuleLink = models.StudentStatus.rules.through
        RuleLink.objects.filter(studentstatus_id__pk__in=status_list, paymentrule_id__pk__in=to_delete).delete()
        to_bulk_create = []
        for status in status_list:
            for rule in to_add:
                to_bulk_create.append(RuleLink(studentstatus_id=status, paymentrule_id=rule))
        RuleLink.objects.bulk_create(to_bulk_create)
        return redirect('student_list')

    def get_context_data(self, **kwargs):
        context = super(StudentRulesTransform, self).get_context_data(**kwargs)
        return context