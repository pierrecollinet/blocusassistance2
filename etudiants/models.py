from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
# Create your models here.
from ba2.models import Universite, Faculte, Etude

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

