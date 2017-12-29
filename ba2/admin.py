# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from .models import Campus, CampusImage, Universite, Faculte, Etude

class CampusImageInline(admin.TabularInline):
    model = CampusImage
    extra = 0
    max_num = 10

class CampusAdmin(admin.ModelAdmin):
    inlines = [
        CampusImageInline,
    ]
    class Meta:
        model = Campus

class FaculteInline(admin.TabularInline):
    model = Faculte
    extra = 0
    max_num = 100

class UniversiteAdmin(admin.ModelAdmin):
    inlines = [
        FaculteInline,
    ]
    class Meta:
        model = Universite

class EtudeInline(admin.TabularInline):
    model = Etude
    extra = 0
    max_num = 100

class FaculteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'universite',]
    list_filter = ['universite',]
    inlines = [
        EtudeInline,
    ]
    class Meta:
        model = Faculte


admin.site.register(Campus, CampusAdmin)
admin.site.register(Universite, UniversiteAdmin)
admin.site.register(Faculte, FaculteAdmin)
admin.site.register(Etude)


