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
from blocus.models import InscriptionBlocus

choices_origine=(('facebook','Facebook'),('mail', 'Mail'),('ancien étudiant', 'Je suis un ancien étudiant'), ('radio', 'A la radio'),('google','Google'),('presse','Dans la presse'),('autre','Autre'))
class InscriptionBlocusModelForm(forms.ModelForm):
    origine = forms.ChoiceField(label="Comment avez-vous entendu parler de Blocus Assistance?",choices=choices_origine,error_messages={'required': "Indiquez-nous comment vous avez découvert Blocus Assistance SVP"})

    class Meta:
        model = InscriptionBlocus
        exclude = ('etudiant','blocus','montant', 'is_paid', 'date_inscription', 'suivi_inscription')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(InscriptionBlocusModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Field('campus'),
                                HTML("""
                                        <div id="checkbox_module_id"></div>
                                    """
                                    ),
                                Field('origine'),
                                Field('code_promo'),
                                )
        self.helper.add_input(Submit('submit', 'Confirmer', css_class='btn btn-default btn-lg'))

    def clean(self):
        print(self)
        cleaned_data=super(InscriptionBlocusModelForm, self).clean()
        modules = cleaned_data.get('module')
        if not modules:
          raise forms.ValidationError("Il faut sélectionner au moins un module")

        else :
          for mod in modules :
            if len(InscriptionBlocus.objects.filter(etudiant=self.request.user.etudiant, module__id__in=modules)) > 0:
              raise forms.ValidationError("Tu es déjà inscrit à l'un de ces modules")
        return cleaned_data















