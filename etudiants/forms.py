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

statuts = (('etudiant','Etudiant'),('parent','Parent'),('professeur', 'Professeur'),)
class SignupForm(forms.Form):
    statut = forms.ChoiceField(choices = statuts)

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
      self.helper.layout = Layout(
                                Field('statut'),
                                Field('username',placeholder="Nom d'utilisateur"),
                                Field('password1'),
                                Field('password2'),
                                )

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
                                Field('gsm'),
                                Field('annee'),
                                Field('universite'),
                                Field('faculte'),
                                Field('etude'),
                                Field('email_parent1'),
                                )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))
