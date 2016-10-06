# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^iniciar-sesion/$', views.LoginView.as_view(), name='user_login'),
    url(r'^cerrar-sesion/$', views.LogoutView.as_view(), name='user_logout'),

    url(r'^consultor/$', views.ConsultorProfileView.as_view(), name='consultor_profile'),
    url(r'^perfil/$', views.OperatorProfileView.as_view(), name='operator_profile'),
]
