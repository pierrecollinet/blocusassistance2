from django.contrib import admin
from .models import Matiere, CoursParticulier, DemandeCP


class DemandeCPAdmin(admin.ModelAdmin):
    model = DemandeCP
    list_display = ['date_demande', 'matiere', 'email_contact','tel_contact', 'statut','cours_particulier','user']
    list_filter = ['statut',]


admin.site.register(Matiere)
admin.site.register(CoursParticulier)
admin.site.register(DemandeCP,DemandeCPAdmin)
