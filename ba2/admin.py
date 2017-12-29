# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from .models import Campus, CampusImage

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



admin.site.register(Campus, CampusAdmin)
