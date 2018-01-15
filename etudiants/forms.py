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
from etudiants.models import Etudiant

statuts = (('none', 'none'),('etudiants','Etudiant'),('parents','Parent'),('professeurs', 'Professeur'),)
class SignupForm(forms.Form):
    statut = forms.ChoiceField(choices = statuts, required=True)

    def signup(self, request, user):
      # user.first_name = self.cleaned_data['first_name']
      # user.last_name = self.cleaned_data['last_name']
      # user.save()
      print('rien de special...')

    def __init__(self, *args, **kwargs):
      super(SignupForm, self).__init__(*args, **kwargs)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.empty_permitted = False
      self.helper.form_class = 'form-horizontal'
      self.fields['statut'].label = False
      self.helper.layout = Layout(
                                Field('statut', css_class="hidden-radio-field"),
                                Field('username',placeholder="Nom d'utilisateur"),
                                Field('password1'),
                                Field('password2'),
                                )

    def clean(self):
      cleaned_data = super(SignupForm, self).clean()
      statut = cleaned_data.get('statut')
      if statut == "none":
        raise forms.ValidationError("Veuillez sélectionner un statut")

class EtudiantModelForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        exclude = ('user','vip','active')

    def __init__(self, *args, **kwargs):
        super(EtudiantModelForm, self).__init__(*args, **kwargs)
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
                                Field('email_parent1'),
                                )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))

class EtudiantFullModelForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        exclude = ('user','vip','active')

    def __init__(self, *args, **kwargs):
        super(EtudiantFullModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Field('nom'),
                                Field('prenom'),
                                Field('gsm'),
                                Field('annee'),
                                Field('universite'),
                                Field('faculte'),
                                Field('etude'),
                                Field('email_parent1'),

                                # optional fields
                                Field('email_parent2'),
                                Field('gsm_parent1'),
                                Field('gsm_parent2'),
                                Field('date_de_naissance'),
                                Field('photo_profil'),
                                Field('adresse'),
                                )


        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))
