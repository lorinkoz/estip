# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^estudiantes/$', views.StudentList.as_view(), name='student_list'),
    url(r'^estudiantes/activos/$', views.ActiveStudentList.as_view(), name='active_student_list'),
    url(r'^estudiantes/inactivos/$', views.InactiveStudentList.as_view(), name='inactive_student_list'),
    url(r'^estudiantes/sin-reglas/$', views.UnruledStudentList.as_view(), name='unruled_student_list'),
    url(r'^estudiantes/agregar/$', views.StudentCreate.as_view(), name='student_create'),
    url(r'^estudiantes/promover/$', views.StudentPromote.as_view(), name='student_promote'),
    url(r'^estudiantes/transformar-reglas/$', views.StudentRulesTransform.as_view(), name='student_rules_transform'),
    url(r'^estudiantes/(?P<sid>\d+)/editar/$', views.StudentUpdate.as_view(), name='student_update'),
    url(r'^estudiantes/(?P<sid>\d+)/eliminar/$', views.StudentDelete.as_view(), name='student_delete'),
    url(r'^estudiantes/(?P<sid>\d+)/activar/$', views.StudentActivate.as_view(), name='student_activate'),
    url(r'^estudiantes/(?P<sid>\d+)/desactivar/$', views.StudentDeactivate.as_view(), name='student_deactivate'),
]
