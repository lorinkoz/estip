# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [

	url(r'^pagos/$', views.PaymentList.as_view(), name='payment_list'),
    url(r'^pagos/ver-actual/$', views.PaymentCurrent.as_view(), name='payment_current'),
    url(r'^pagos/inicializar/$', views.PaymentCreate.as_view(), name='payment_create'),
    url(r'^pagos/(?P<slug>[\w-]+)/$', views.PaymentDetails.as_view(), name='payment_details'),
    url(r'^pagos/(?P<slug>[\w-]+)/editar/$', views.PaymentUpdate.as_view(), name='payment_update'),
    url(r'^pagos/(?P<slug>[\w-]+)/eliminar/$', views.PaymentDelete.as_view(), name='payment_delete'),
    url(r'^pagos/(?P<slug>[\w-]+)/cerrar/$', views.PaymentClose.as_view(), name='payment_close'),
    url(r'^pagos/(?P<slug>[\w-]+)/calcular/$', views.PaymentGenerate.as_view(), name='payment_generate'),
    url(r'^pagos/(?P<slug>[\w-]+)/nomina/$', views.PaymentPrint.as_view(), name='payment_print'),
    url(r'^pagos/(?P<slug>[\w-]+)/(?P<sid>\d+)/$', views.PaymentRecords.as_view(), name='payment_records'),

]
