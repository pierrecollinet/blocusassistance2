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


class InscriptionBlocusModelForm(forms.ModelForm):
    class Meta:
        model = InscriptionBlocus
        exclude = ('etudiant','blocus','montant', 'is_paid', 'date_inscription', 'suivi_inscription')

    def __init__(self, *args, **kwargs):
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
