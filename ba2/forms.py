# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div,Submit, HTML
from crispy_forms.layout import MultiWidgetField


from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import gettext as _
import datetime

sujets = (
          ('Blocus Assisté','blocus'),
          ('Cours Particuliers','coursparticuliers'),
          ('Suivi intensif','suiviintensif'),
          ('Autre','autre'),
          )
class ContactForm(forms.Form):
    nom = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=100)
    sujet = forms.ChoiceField(choices=sujets)
#    message = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                                Field('nom', placeholder='NOM & PRENOM'),
                                Field('phone_number', placeholder='NUMERO DE GSM'),
                                Field('email', placeholder='Adresse email'),
                                Field('sujet', placeholder='Faculté'),
   #                             Field('message', placeholder='Donnez-nous plus de précisions'),
                                )
        self.helper.add_input(Submit('submit', 'Envoyer', css_class='btn btn-default btn-lg btn-main-page text-left'))
