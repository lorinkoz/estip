# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-11 15:50
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.PositiveIntegerField(unique=True, verbose_name='c\xf3digo')),
                ('cid', models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator('\\d{11}')], verbose_name='carn\xe9 de identidad')),
                ('name', models.CharField(max_length=512, verbose_name='nombres')),
                ('surname', models.CharField(max_length=512, verbose_name='apellidos')),
                ('gender', models.CharField(choices=[('m', 'Masculino'), ('f', 'Femenino')], max_length=1, verbose_name='sexo')),
                ('linked_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student', to=settings.AUTH_USER_MODEL, verbose_name='usuario asociado')),
            ],
            options={
                'ordering': ('surname', 'name', 'sid'),
                'verbose_name': 'estudiante',
                'verbose_name_plural': 'estudiantes',
            },
        ),
        migrations.CreateModel(
            name='StudentStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(choices=[(0, 'Preparatoria'), (1, '1ro'), (2, '2do'), (3, '3ro'), (4, '4to'), (5, '5to'), (6, '6to')], default=1, verbose_name='a\xf1o que cursa')),
                ('rules', models.ManyToManyField(blank=True, related_name='students_status', to='core.PaymentRule', verbose_name='reglas de pago')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='core.Specialty', verbose_name='especialidad')),
                ('student_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='core.StudentType', verbose_name='tipo de estudiante')),
            ],
            options={
                'verbose_name': 'estado de estudiante',
                'verbose_name_plural': 'estados de estudiante',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='status',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student', to='students.StudentStatus', verbose_name='estado'),
        ),
    ]