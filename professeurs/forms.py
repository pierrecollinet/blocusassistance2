# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import gettext as _

from django.http import HttpResponseRedirect

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div,Submit, HTML
from crispy_forms.layout import MultiWidgetField
from crispy_forms.bootstrap import InlineRadios, InlineCheckboxes

import datetime

# import models
from professeurs.models import Professeur, JourneeBlocusProf, RapportBlocusJournalier

class ProfesseurModelForm(forms.ModelForm):
    date_de_naissance = forms.DateField(initial=datetime.date.today(), required=True, widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}),  input_formats=('%d/%m/%Y',))

    class Meta:
        model = Professeur
        exclude = ('user','active')

    def __init__(self, *args, **kwargs):
        super(ProfesseurModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Field('nom'),
                                Field('prenom'),
                                Field('email'),
                                Field('gsm'),
                                Field('annee'),
                                Field('universite'),
                                Field('faculte'),
                                Field('etude'),

                                # optional fields
                                Field('date_de_naissance'),
                                Field('photo_profil'),
                                Field('adresse'),
                                )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))

class BlocusJourneeForm(forms.ModelForm):
    date        = forms.DateField(initial=datetime.date.today(), required=True, widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}),  input_formats=('%d/%m/%Y',))
    heure_debut = forms.TimeField(initial='09:00', required=True, widget=forms.TimeInput(format='%H:%M', attrs={'class': 'timepicker','placeholder': "Début du cours"}), input_formats=('%H:%M',))
    heure_fin   = forms.TimeField(initial='18:00', required=True, widget=forms.TimeInput(format='%H:%M', attrs={'class': 'timepicker','placeholder': "Fin du cours"}), input_formats=('%H:%M',))

    class Meta:
        model = JourneeBlocusProf
        exclude = ('professeur','is_paid','blocus')
        widgets = {
              'remarque': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        fields = ('date','heure_debut','heure_fin','remarque', 'campus')


    def clean(self):
        cleaned_data = super(BlocusJourneeForm, self).clean()
        heure_debut  = cleaned_data.get("heure_debut")
        heure_fin    = cleaned_data.get("heure_fin")
        campus       = cleaned_data.get("campus")
        date         = cleaned_data.get("date")

        # Vérifie que les 2 champs sont validés
        if heure_debut > heure_fin :
          raise forms.ValidationError("Tu ne peux pas terminer avant d'avoir commencé. Vérifie les heures encodées...")
        if date > datetime.date.today():
          raise forms.ValidationError("Tu ne peux pas encoder tes jours à l'avance")
        if len(JourneeBlocusProf.objects.filter(date=date, professeur=self.request.user.professeur))>0 :
          raise forms.ValidationError("Tu as déjà encodé une journée de blocus à cette date")
        if campus is None :
          raise forms.ValidationError("Il faut encoder le campus sur lequel tu as travaillé")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BlocusJourneeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Field('campus'),
                                Field('date'),
                                Field('heure_debut'),
                                Field('heure_fin'),
                                Field('remarque', placeholder="N'hésite pas à laisser un commentaire ou une remarque si nécessaire (FACULTATIF)"),
                                )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))

class ModifyBlocusJourneeForm(BlocusJourneeForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        heure_debut  = cleaned_data.get("heure_debut")
        heure_fin    = cleaned_data.get("heure_fin")
        campus       = cleaned_data.get("campus")
        date         = cleaned_data.get("date")

        # Vérifie que les 2 champs sont validés
        if heure_debut > heure_fin :
          raise forms.ValidationError("Tu ne peux pas terminer avant d'avoir commencé. Vérifie les heures encodées...")
        if date > datetime.date.today():
          raise forms.ValidationError("Tu ne peux pas encoder tes jours à l'avance")
        if campus is None :
          raise forms.ValidationError("Il faut encoder le campus sur lequel tu as travaillé")
        return cleaned_data

class RapportBlocusJournalierModelForm(forms.ModelForm):
    class Meta:
        model = RapportBlocusJournalier
        widgets = {
              'objectif':forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        fields = ('objectif',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RapportBlocusJournalierModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Field('objectif'),
                                )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))

class ModifierRapportBlocusJournalierModelForm(forms.ModelForm):
    class Meta:
        model = RapportBlocusJournalier
        widgets = {
              'remarque': forms.Textarea(attrs={'rows':4, 'cols':15}),
              'objectif':forms.Textarea(attrs={'rows':4, 'cols':15}),
              'bilan':forms.Textarea(attrs={'rows':4, 'cols':15}),
              'recommandation':forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        fields = ('objectif','objectif_atteint','bilan', 'recommandation','remarque','proactivite','productivite','moral')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ModifierRapportBlocusJournalierModelForm, self).__init__(*args, **kwargs)
        self.fields['objectif'].required = True
        self.fields['bilan'].required = True
        self.fields['recommandation'].required = True
        self.fields['remarque'].required = True
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Field('objectif'),
                                Field('objectif_atteint'),
                                Field('bilan'),
                                Field('recommandation'),
                                Field('remarque'),
                                Field('proactivite'),
                                Field('productivite'),
                                Field('moral'),
                                )
        self.helper.add_input(Submit('enregistrer', 'Enregistrer', css_class='btn btn-default btn-lg m-3'))
        self.helper.add_input(Submit('enregistrer_and_email', 'Enregistrer & Envoyer', css_class='btn btn-default btn-lg m-3'))
