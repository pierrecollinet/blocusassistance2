from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from datetime import datetime, timedelta, date
# Create your models here.
from ba2.models import Universite, Faculte, Etude
from blocus.models import ModuleBlocus, Blocus
from professeurs.models import RapportBlocusModule
annees = (
    ('BA1', 'BA1'),
    ('BA2', 'BA2'),
    ('BA3', 'BA3'),
    ('MA1', 'MA1'),
    ('MA2', 'MA2'),
    ('diplome', 'Diplômé'),
)

class Etudiant(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)

  # required fields
  nom = models.CharField(max_length=200)
  prenom = models.CharField(max_length=200)
  email = models.EmailField(unique=True)
  gsm = models.CharField(max_length=200)
  universite = models.ForeignKey(Universite)
  faculte = models.ForeignKey(Faculte)
  etude = models.ForeignKey(Etude)
  email_parent1 = models.EmailField()
  annee = models.CharField(max_length=200, choices=annees)

  # optional fields
  email_parent2 = models.EmailField(blank=True)
  gsm_parent1 = models.CharField(max_length=200, blank=True)
  gsm_parent2 = models.CharField(max_length=200, blank=True)
  date_de_naissance = models.DateField(blank=True, null=True)
  photo_profil = models.ImageField(upload_to = 'mes_images/', blank=True)
  adresse = models.CharField(max_length=200, blank=True)

  # fields added by superuser
  active = models.BooleanField(default=True)
  vip = models.BooleanField(default=False)

  def __str__(self):
    return self.prenom +' '+ self.nom

  def veut_un_suivi(self):
    current_module = ModuleBlocus.objects.filter(date_debut__lte=date.today(), date_fin__gte=date.today(), blocus=Blocus.objects.filter(is_current=True).first()).first()
    rapportmodule = RapportBlocusModule.objects.filter(module = current_module, etudiant = self)
    if len(rapportmodule)>0:
      return True
    else:
      return False

  def get_suivi_actuel(self,date):
    current_module = ModuleBlocus.objects.filter(date_debut__lte=date, date_fin__gte=date, blocus=Blocus.objects.filter(is_current=True).first()).first()
    if self.veut_un_suivi():
      return RapportBlocusModule.objects.filter(module = current_module, etudiant = self).first()
    else :
      return None

  def calculate_completed_profile_rate(self):
    counter = 0
    if self.nom :
      counter += 1
    if self.prenom :
      counter += 1
    if self.email :
      counter += 1
    if self.gsm :
      counter += 1
    if self.universite :
      counter += 1
    if self.faculte :
      counter += 1
    if self.email_parent1 :
      counter += 1
    if self.annee :
      counter += 1
    if self.email_parent2 :
      counter += 1
    if self.gsm_parent2 :
      counter += 1
    if self.gsm_parent1 :
      counter += 1
    if self.date_de_naissance :
      counter += 1
    if self.photo_profil :
      counter += 1
    if self.adresse :
      counter += 1
    total = 14.0
    return 100*float(counter)/total
