from django.contrib import admin
from .models import Professeur, JourneeBlocusProf, RapportBlocusModule,RapportBlocusJournalier


class JourneeBlocusAdmin(admin.ModelAdmin):
    model = JourneeBlocusProf
    list_display = ['professeur', 'date', 'heure_debut','heure_fin', 'total', 'is_paid', 'remarque', 'campus' ]

class RapportBlocusJournalierAdmin(admin.ModelAdmin):
    model = RapportBlocusJournalier
    list_display = ['presence', 'date','objectif_atteint', 'auteur']


admin.site.register(Professeur)
admin.site.register(JourneeBlocusProf, JourneeBlocusAdmin)
admin.site.register(RapportBlocusModule)
admin.site.register(RapportBlocusJournalier, RapportBlocusJournalierAdmin)
