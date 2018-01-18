# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div,Submit, HTML
from crispy_forms.layout import MultiWidgetField


from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import gettext as _
import datetime

from suiviintensif.models import DemandeInfo


class SuiviIntensifContactModelForm(forms.ModelForm):
    class Meta:
        model = DemandeInfo
        fields = ('nom','email','gsm', 'faculte','etudes', 'sujet', 'message')
        widgets = {
                  'message': forms.Textarea(attrs={'rows':4, 'placeholder':"Donnez-nous plus de détails quant à votre demande..."}),
                }

    def __init__(self, *args, **kwargs):
        super(SuiviIntensifContactModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Field('nom', placeholder='NOM & PRENOM'),
                                Field('email', placeholder='Adresse email'),
                                Field('gsm', placeholder='NUMERO DE GSM'),
                                Field('faculte', placeholder='Faculté'),
                                Field('etudes', placeholder='Etudes'),
                                Field('sujet', placeholder='Faculté'),
                                Field('message', placeholder='Donnez-nous plus de précisions'),
                                )
        self.helper.add_input(Submit('submit', 'Envoyer', css_class='btn btn-default btn-lg btn-main-page text-left'))
