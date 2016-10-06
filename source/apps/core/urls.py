# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [

	url(r'^$', views.SorterView.as_view(), name='sorter'),

    url(r'^panel/$', views.BackendDashboard.as_view(), name='backend_dashboard'),
    url(r'^resumen/$', views.FrontendDashboard.as_view(), name='frontend_dashboard'),

    url(r'^universidad/$', views.SchoolDetails.as_view(), name='school_details'),
    url(r'^universidad/editar/$', views.SchoolUpdate.as_view(), name='school_update'),

    url(r'^facultades/$', views.FacultyList.as_view(), name='faculty_list'),
    url(r'^facultades/agregar/$', views.FacultyCreate.as_view(), name='faculty_create'),
    url(r'^facultades/(?P<slug>[\w-]+)/editar/$', views.FacultyUpdate.as_view(), name='faculty_update'),
    url(r'^facultades/(?P<slug>[\w-]+)/eliminar/$', views.FacultyDelete.as_view(), name='faculty_delete'),

    url(r'^especialidades/$', views.SpecialtyList.as_view(), name='specialty_list'),
    url(r'^especialidades/agregar/$', views.SpecialtyCreate.as_view(), name='specialty_create'),
    url(r'^especialidades/(?P<slug>[\w-]+)/editar/$', views.SpecialtyUpdate.as_view(), name='specialty_update'),
    url(r'^especialidades/(?P<slug>[\w-]+)/eliminar/$', views.SpecialtyDelete.as_view(), name='specialty_delete'),

    url(r'^tipos-estudiante/$', views.StudentTypeList.as_view(), name='student_type_list'),
    url(r'^tipos-estudiante/agregar/$', views.StudentTypeCreate.as_view(), name='student_type_create'),
    url(r'^tipos-estudiante/(?P<slug>[\w-]+)/editar/$', views.StudentTypeUpdate.as_view(), name='student_type_update'),
    url(r'^tipos-estudiante/(?P<slug>[\w-]+)/eliminar/$', views.StudentTypeDelete.as_view(), name='student_type_delete'),

    url(r'^tipos-pago/$', views.PaymentTypeList.as_view(), name='payment_type_list'),
    url(r'^tipos-pago/agregar/$', views.PaymentTypeCreate.as_view(), name='payment_type_create'),
    url(r'^tipos-pago/(?P<slug>[\w-]+)/editar/$', views.PaymentTypeUpdate.as_view(), name='payment_type_update'),
    url(r'^tipos-pago/(?P<slug>[\w-]+)/eliminar/$', views.PaymentTypeDelete.as_view(), name='payment_type_delete'),
    url(r'^tipos-pago/(?P<slug>[\w-]+)/subir/$', views.PaymentTypeSort.as_view(), {'upwards': True}, name='payment_type_up'),
    url(r'^tipos-pago/(?P<slug>[\w-]+)/bajar/$', views.PaymentTypeSort.as_view(), {'upwards': False}, name='payment_type_down'),

    url(r'^reglas-pago/$', views.PaymentRuleList.as_view(), name='payment_rule_list'),
    url(r'^reglas-pago/agregar/$', views.PaymentRuleCreate.as_view(), name='payment_rule_create'),
    url(r'^reglas-pago/(?P<slug>[\w-]+)/editar/$', views.PaymentRuleUpdate.as_view(), name='payment_rule_update'),
    url(r'^reglas-pago/(?P<slug>[\w-]+)/eliminar/$', views.PaymentRuleDelete.as_view(), name='payment_rule_delete'),
]
