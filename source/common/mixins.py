# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect

from braces.views import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    redirect_field_name = 'volver'

    def test_func(self, user):
        return user.is_superuser

    def get_login_url(self):
        if self.request.user.is_authenticated(): 
            return reverse('sorter')
        return super(AdminRequiredMixin, self).get_login_url()


class StaffRequiredMixin(UserPassesTestMixin):
    redirect_field_name = 'volver'

    def test_func(self, user):
        return user.is_staff

    def get_login_url(self):
        if self.request.user.is_authenticated(): 
            return reverse('sorter')
        return super(StaffRequiredMixin, self).get_login_url()


class ConsultorRequiredMixin(UserPassesTestMixin):
    redirect_field_name = 'volver'

    def test_func(self, user):
        return user.is_consultor

    def get_login_url(self):
        if self.request.user.is_authenticated(): 
            return reverse('sorter')
        return super(ConsultorRequiredMixin, self).get_login_url()


class MethodPreventMixin(object):

    def prevent_all(self, request):
        return False

    def prevent_get(self, request):
        return False

    def prevent_post(self, request):
        return False

    def dispatch(self, request, *args, **kwargs):
        if self.prevent_all(request):
            return redirect('sorter')
        return super(MethodPreventMixin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.prevent_get(request):
            return redirect('sorter')
        return super(MethodPreventMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.prevent_post(request):
            return redirect('sorter')
        return super(MethodPreventMixin, self).post(request, *args, **kwargs)