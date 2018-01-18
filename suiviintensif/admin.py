from django.contrib import admin
from .models import DemandeInfo


class DemandeInfoAdmin(admin.ModelAdmin):
    model = DemandeInfo
    list_display = ['date_demande', 'sujet', 'email','gsm', 'statut',]
    list_filter = ['statut',]


admin.site.register(DemandeInfo, DemandeInfoAdmin)
