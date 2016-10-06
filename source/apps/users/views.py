# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView

from braces.views import SetHeadlineMixin

from apps.audit.models import Trace
from common.mixins import ConsultorRequiredMixin, StaffRequiredMixin


class LoginView(SetHeadlineMixin, FormView):
    form_class = AuthenticationForm
    headline = 'Iniciar sesión'
    template_name = 'users/login.html'
    
    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        Trace.log('{} accedió al sistema'.format(self.user.traceable_name), user=self.user)
        return super(LoginView, self).form_valid(form)
    
    def get_success_url(self):
        redirect_to = ''
        next = self.request.GET.get('volver', reverse(self.user.get_absolute_url()))
        return next


class LogoutView(View):
    
    def get(self, request):
        raise Http404()
    
    def post(self, request):
        if request.user.is_authenticated():
            Trace.log('{} salió del sistema'.format(request.user.traceable_name), user=request.user)
            logout(request)
        return redirect('user_login')


class ProfileView(SetHeadlineMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_headline(self):
        return self.request.user.get_full_name

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['base_template'] = self.base_template
        return context

class ConsultorProfileView(ConsultorRequiredMixin, ProfileView):
    base_template = 'base_frontend.html'


class OperatorProfileView(StaffRequiredMixin, ProfileView):
    base_template = 'base_backend.html'