# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone

from braces.views import SetHeadlineMixin

from . import models
from common.mixins import ConsultorRequiredMixin, StaffRequiredMixin, AdminRequiredMixin


class SorterView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        user = self.request.user
        if user.is_anonymous():
            return reverse(settings.LOGIN_URL)
        else:
            return reverse(user.get_absolute_url())


class BackendDashboard(StaffRequiredMixin, SetHeadlineMixin, TemplateView):
    headline = 'Panel de control'
    template_name = 'core/dashboard_backend.html'

    def get_context_data(self, **kwargs):
        from django.db.models import Count
        from apps.students.models import Student
        context = super(BackendDashboard, self).get_context_data(**kwargs)
        context['unruled_students'] = Student.objects.exclude(status=None).annotate(rules=Count('status__rules__pk')).filter(rules=0).count()
        return context


class FrontendDashboard(ConsultorRequiredMixin, SetHeadlineMixin, TemplateView):
    headline = 'Resumen'
    template_name = 'core/dashboard_frontend.html'

    def get_context_data(self, **kwargs):
        from apps.payments.models import PaymentRow
        from apps.payments.utils import tabulate_rows
        context = super(FrontendDashboard, self).get_context_data(**kwargs)
        if hasattr(self.request.user, 'student'):
            limit = timezone.now() - timedelta(days=180)
            rows = PaymentRow.objects.filter(student=self.request.user.student)
            headers, data = tabulate_rows(rows)
            context['headers'] = headers
            context['data'] = data
        return context


class SchoolDetails(AdminRequiredMixin, SetHeadlineMixin, DetailView):
    model = models.School
    headline = 'Datos de la universidad'
    template_name = 'core/school_details.html'

    def get_object(self):
        return self.model.objects.get()


class SchoolUpdate(AdminRequiredMixin, SetHeadlineMixin, UpdateView):
    model = models.School
    fields = '__all__'
    headline = 'Editar datos de la universidad'
    template_name = 'core/school_form.html'

    def get_object(self):
        return self.model.objects.get()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('school_details'))


class FacultyList(StaffRequiredMixin, SetHeadlineMixin, ListView):
    model = models.Faculty
    paginate_by = 25
    page_kwarg = 'p'
    headline = 'Facultades'
    template_name = 'core/faculty_list.html'

    def get_queryset(self):
        queryset = super(FacultyList, self).get_queryset()
        query = self.request.GET.get('q','').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class FacultyCreate(StaffRequiredMixin, SetHeadlineMixin, CreateView):
    model = models.Faculty
    fields = ('name',)
    headline = 'Nueva facultad'
    template_name = 'core/faculty_form.html'

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('faculty_list'))


class FacultyUpdate(StaffRequiredMixin, SetHeadlineMixin, UpdateView):
    model = models.Faculty
    fields = ('name',)
    headline = 'Editar facultad %s'
    template_name = 'core/faculty_form.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('faculty_list'))


class FacultyDelete(StaffRequiredMixin, SetHeadlineMixin, DeleteView):
    model = models.Faculty
    headline = 'Eliminar facultad %s'
    template_name = 'core/faculty_delete.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('faculty_list'))


class SpecialtyList(StaffRequiredMixin, SetHeadlineMixin, ListView):
    model = models.Specialty
    paginate_by = 25
    page_kwarg = 'p'
    headline = 'Especialidades'
    template_name = 'core/specialty_list.html'

    def get_queryset(self):
        queryset = super(SpecialtyList, self).get_queryset().select_related('faculty')
        query = self.request.GET.get('q','').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class SpecialtyCreate(StaffRequiredMixin, SetHeadlineMixin, CreateView):
    model = models.Specialty
    fields = ('name', 'faculty', 'structure')
    headline = 'Nueva especialidad'
    template_name = 'core/specialty_form.html'

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('specialty_list'))


class SpecialtyUpdate(StaffRequiredMixin, SetHeadlineMixin, UpdateView):
    model = models.Specialty
    fields = ('name', 'faculty', 'structure')
    headline = 'Editar especialidad %s'
    template_name = 'core/specialty_form.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('specialty_list'))


class SpecialtyDelete(StaffRequiredMixin, SetHeadlineMixin, DeleteView):
    model = models.Specialty
    headline = 'Eliminar especialidad %s'
    template_name = 'core/specialty_delete.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('specialty_list'))


class StudentTypeList(StaffRequiredMixin, SetHeadlineMixin, ListView):
    model = models.StudentType
    paginate_by = 25
    page_kwarg = 'p'
    headline = 'Tipos de estudiante'
    template_name = 'core/student_type_list.html'

    def get_queryset(self):
        queryset = super(StudentTypeList, self).get_queryset()
        query = self.request.GET.get('q','').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class StudentTypeCreate(StaffRequiredMixin, SetHeadlineMixin, CreateView):
    model = models.StudentType
    fields = ('name',)
    headline = 'Nuevo tipo de estudiante'
    template_name = 'core/student_type_form.html'

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('student_type_list'))


class StudentTypeUpdate(StaffRequiredMixin, SetHeadlineMixin, UpdateView):
    model = models.StudentType
    fields = ('name',)
    headline = 'Editar tipo de estudiante %s'
    template_name = 'core/student_type_form.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('student_type_list'))


class StudentTypeDelete(StaffRequiredMixin, SetHeadlineMixin, DeleteView):
    model = models.StudentType
    headline = 'Eliminar tipo de estudiante %s'
    template_name = 'core/student_type_delete.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('student_type_list'))


class PaymentTypeList(StaffRequiredMixin, SetHeadlineMixin, ListView):
    model = models.PaymentType
    paginate_by = 25
    page_kwarg = 'p'
    headline = 'Tipos de pago'
    template_name = 'core/payment_type_list.html'

    def get_queryset(self):
        queryset = super(PaymentTypeList, self).get_queryset()
        query = self.request.GET.get('q','').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class PaymentTypeCreate(StaffRequiredMixin, SetHeadlineMixin, CreateView):
    model = models.PaymentType
    fields = ('name', 'alias', 'regularity', 'allow_rules')
    headline = 'Nuevo tipo de pago'
    template_name = 'core/payment_type_form.html'

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('payment_type_list'))


class PaymentTypeUpdate(StaffRequiredMixin, SetHeadlineMixin, UpdateView):
    model = models.PaymentType
    fields = ('name', 'alias', 'regularity', 'allow_rules')
    headline = 'Editar tipo de pago %s'
    template_name = 'core/payment_type_form.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('payment_type_list'))


class PaymentTypeSort(StaffRequiredMixin, View):

    def get(self, request, slug, upwards=True):
        from django.shortcuts import redirect, get_object_or_404
        target = get_object_or_404(models.PaymentType, slug=slug)
        dir = -3 if upwards else 3
        for i, payment_type in enumerate(models.PaymentType.objects.all()):
            payment_type.ordering = (i + 1) * 2
            if payment_type == target:
                payment_type.ordering = max(0, payment_type.ordering + dir)
            payment_type.save()
        return redirect('payment_type_list')


class PaymentTypeDelete(StaffRequiredMixin, SetHeadlineMixin, DeleteView):
    model = models.PaymentType
    headline = 'Eliminar tipo de pago %s'
    template_name = 'core/payment_type_delete.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('payment_type_list'))


class PaymentRuleList(StaffRequiredMixin, SetHeadlineMixin, ListView):
    model = models.PaymentRule
    paginate_by = 25
    page_kwarg = 'p'
    headline = 'Reglas de pago'
    template_name = 'core/payment_rule_list.html'

    def get_queryset(self):
        queryset = super(PaymentRuleList, self).get_queryset().select_related('payment_type')
        query = self.request.GET.get('q','').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class PaymentRuleCreate(StaffRequiredMixin, SetHeadlineMixin, CreateView):
    model = models.PaymentRule
    fields = ('name', 'payment_type', 'amount', 'description')
    headline = 'Nueva regla de pago'
    template_name = 'core/payment_rule_form.html'

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('payment_rule_list'))


class PaymentRuleUpdate(StaffRequiredMixin, SetHeadlineMixin, UpdateView):
    model = models.PaymentRule
    fields = ('name', 'payment_type', 'amount', 'description')
    headline = 'Editar regla de pago %s'
    template_name = 'core/payment_rule_form.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('payment_rule_list'))


class PaymentRuleDelete(StaffRequiredMixin, SetHeadlineMixin, DeleteView):
    model = models.PaymentRule
    headline = 'Eliminar regla de pago %s'
    template_name = 'core/payment_rule_delete.html'

    def get_headline(self):
        return self.headline % self.get_object()

    def get_success_url(self):
        return self.request.GET.get('volver', reverse('payment_rule_list'))
