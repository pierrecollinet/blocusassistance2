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

class Matiere(models.Model):
    nom_complet = models.CharField(max_length=200)
    abreviation = models.CharField(max_length=200)

    def __str__(self):
        return self.nom_complet

class CoursParticulier(models.Model):
    date_cours = models.DateTimeField(blank=True, null=True)
    professeur = models.ForeignKey(Professeur, blank=True, null=True)
    eleves = models.ManyToManyField(Etudiant, blank=True, null=True)
    heure_debut = models.TimeField(blank=True, null=True)
    heure_fin = models.TimeField(blank=True, null=True)
    eleve_a_paye = models.BooleanField(default=False)
    prof_paye = models.BooleanField(default=False)
    tarif_horaire_eleve = models.CharField(max_length=200, default=30)
    tarif_horaire_prof =  models.CharField(max_length=200, default=20)
    remarque = models.TextField(blank=True, null=True)
    matiere = models.ForeignKey(Matiere)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
      if self.professeur:
        return self.professeur.prenom +' - '+ str(self.date_demande.strftime('%d/%m/%Y'))
      else :
        return "Pas de prof attribué - " + str(self.date_demande.strftime('%d/%m/%Y'))

statuts = (('attente','En attente'),('regle','Cours créé'),('decline','Demande déclinéé'),)
class DemandeCP(models.Model):
    date_demande = models.DateTimeField(auto_now_add=True)
    matiere = models.ForeignKey(Matiere)
    email_contact = models.EmailField()
    tel_contact = models.CharField(max_length=20)
    user = models.ForeignKey(User, blank=True, null=True)
    statut = models.CharField(max_length=40, choices=statuts, default="attente")
    cours_particulier = models.ForeignKey(CoursParticulier, blank=True, null=True)
    remarque = models.TextField(blank=True, null=True)

    def __str__(self):
      counter = len(DemandeCP.objects.all())
      return "Demande en " + self.matiere.nom_complet


