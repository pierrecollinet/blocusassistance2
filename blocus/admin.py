# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from .models import Blocus, ModuleBlocus, PresenceJourBlocus

class BlocusAdmin(admin.ModelAdmin):
    model = Blocus
    filter_horizontal = ("campus",)

class ModuleBlocusAdmin(admin.ModelAdmin):
    model = ModuleBlocus
    filter_horizontal = ("campus",)

admin.site.register(Blocus, BlocusAdmin)
admin.site.register(ModuleBlocus, ModuleBlocusAdmin)
admin.site.register(PresenceJourBlocus)
