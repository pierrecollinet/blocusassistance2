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
from coursparticuliers.models import DemandeCP, CoursParticulier, Matiere


class CoursParticuliersModelForm(forms.ModelForm):

    class Meta:
        model = DemandeCP
        exclude = ('date_demande','user','statut', 'cours_particulier',)
        widgets = {
                  'remarque': forms.Textarea(attrs={'rows':4, 'placeholder':"Donnez-nous plus de détails quant à votre demande..."}),
                }
    def __init__(self, *args, **kwargs):
        super(CoursParticuliersModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Field('matiere'),
                                Field('email_contact', placeholder="votre_adresse@domain.com"),
                                Field('tel_contact', placeholder="0499 99 99 99"),
                                Field('remarque'),
                                )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))


class CoursParticuliersUserModelForm(forms.ModelForm):

    class Meta:
        model = DemandeCP
        exclude = ('date_demande','email_contact','tel_contact','user','statut', 'cours_particulier',)
        widgets = {
                  'remarque': forms.Textarea(attrs={'rows':4, 'placeholder':"Donnez-nous plus de détails quant à votre demande..."}),
                }
    def __init__(self, *args, **kwargs):
        super(CoursParticuliersUserModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Field('matiere'),
                                Field('email_contact', placeholder="votre_adresse@domain.com"),
                                Field('tel_contact', placeholder="0499 99 99 99"),
                                Field('remarque'),
                                )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))


