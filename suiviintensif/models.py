# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save, post_save, post_delete

from django.utils.text import slugify

from django.db import transaction

from datetime import timedelta, date
import datetime

from professeurs.models import Professeur
from etudiants.models import Etudiant


statuts = (('non_contacte','Pas encore contacté'),('en_cours','En cours/En contact'),('converti','Converti'),('rate','Raté'))
class DemandeInfo(models.Model):
    date_demande = models.DateTimeField(auto_now_add=True)
    nom =  models.CharField(max_length=100)
    email = models.EmailField()
    gsm = models.CharField(max_length=100)
    faculte = models.CharField(max_length=100)
    etudes = models.CharField(max_length=100)
    sujet = models.CharField(max_length=100)
    message = models.TextField()

    suivi_prospect = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=40, choices=statuts, default="non_contacte")
