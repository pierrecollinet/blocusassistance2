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
from professeurs.models import Professeur

class ProfesseurModelForm(forms.ModelForm):
    class Meta:
        model = Professeur
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(ProfesseurModelForm, self).__init__(*args, **kwargs)
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

                                # optional fields
                                Field('date_de_naissance'),
                                Field('photo_profil'),
                                Field('adresse'),
                                )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))
