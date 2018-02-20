# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from .models import Blocus, ModuleBlocus, PresenceJourBlocus, InscriptionBlocus, ProfesseurBlocus, Presence, Feedback
from etudiants.models import Etudiant
class BlocusAdmin(admin.ModelAdmin):
    model = Blocus
    list_display = ['nom', 'is_current', ]
    filter_horizontal = ("campus",)

class ProfesseurBlocusAdmin(admin.ModelAdmin):
    model = ProfesseurBlocus
    list_display = ['professeur', 'blocus', 'statut','total']
    list_filter = ['statut',]
    filter_horizontal = ("campus",)

class ModuleBlocusAdmin(admin.ModelAdmin):
    model = ModuleBlocus
    list_display = ['nom', 'date_debut', 'date_fin', 'blocus',]
    filter_horizontal = ("campus",)

class InscriptionBlocusAdmin(admin.ModelAdmin):
    class Meta:
        Etudiant
    filter_horizontal = ("module",)
    list_display = ['etudiant',  'is_paid', 'code_promo','campus', 'origine','suivi_inscription', 'date_inscription', 'get_email']
    list_filter = ['is_paid','campus','origine','blocus',]
    ordering = ['etudiant']
 #   actions = [make_paid]
    search_fields = ['blocus__nom','etudiant__nom','etudiant__prenom']
    def get_email(self, obj):
        return obj.etudiant.email

class PresenceAdmin(admin.ModelAdmin):
    model = Presence
    list_display = ['etudiant', 'date', 'heure_arrivee','statut','jourblocus']
    list_filter = ['statut',]
    ordering = ['etudiant']
    search_fields = ['etudiant__nom','etudiant__prenom']

admin.site.register(Blocus, BlocusAdmin)
admin.site.register(ModuleBlocus, ModuleBlocusAdmin)
admin.site.register(PresenceJourBlocus)
admin.site.register(InscriptionBlocus, InscriptionBlocusAdmin)
admin.site.register(ProfesseurBlocus, ProfesseurBlocusAdmin)
admin.site.register(Presence, PresenceAdmin)
admin.site.register(Feedback)

