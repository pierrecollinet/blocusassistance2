from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

# Create your models here.
from ba2.models import Universite, Faculte, Etude, Campus
from blocus.models import ProfesseurBlocus, Presence, ModuleBlocus

annees = (
    ('BA1', 'BA1'),
    ('BA2', 'BA2'),
    ('BA3', 'BA3'),
    ('MA1', 'MA1'),
    ('MA2', 'MA2'),
    ('diplome', 'Diplômé'),
)

class Professeur(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)

  # required fields
  nom = models.CharField(max_length=200)
  prenom = models.CharField(max_length=200)
  email = models.EmailField()
  gsm = models.CharField(max_length=200)
  universite = models.ForeignKey(Universite)
  faculte = models.ForeignKey(Faculte)
  etude = models.ForeignKey(Etude)
  annee = models.CharField(max_length=200, choices=annees)

  # optional fields
  date_de_naissance = models.DateField(blank=True, null=True)
  photo_profil = models.ImageField(upload_to = 'mes_images/', blank=True)
  adresse = models.CharField(max_length=200, blank=True)

  # actif ou non
  active = models.BooleanField(default=False)

  def __str__(self):
    return self.prenom +' '+ self.nom

class JourneeBlocusProf(models.Model):
    date = models.DateField()
    professeur = models.ForeignKey(Professeur)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    campus = models.ForeignKey(Campus, blank=True, null=True )
    is_paid = models.BooleanField(default=False)
    remarque = models.TextField(blank=True, null=True)
    blocus = models.ForeignKey('blocus.Blocus', blank=True)
    total = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.professeur.user.username +' - '+ str(self.date.strftime('%d/%m/%Y'))

    def calcul_salaire(self):
        nombre_minutes =  (self.heure_fin.hour*60+self.heure_fin.minute) - (self.heure_debut.hour*60+self.heure_debut.minute)
        prix = 12.5/60
        return nombre_minutes*prix

def journeeblocus_pre_save(sender, instance, *args, **kwargs):
    nombre_minutes =  (instance.heure_fin.hour*60+instance.heure_fin.minute) - (instance.heure_debut.hour*60+instance.heure_debut.minute)
    prix = 12.5/60
    instance.total = nombre_minutes*prix

def journeeblocus_post_save(sender, instance, *args, **kwargs):
    professeurblocus = ProfesseurBlocus.objects.filter(professeur=instance.professeur, blocus=instance.blocus).first()

    journee_blocus_prof = JourneeBlocusProf.objects.filter(professeur=instance.professeur, blocus=instance.blocus)
    total = 0
    for j in journee_blocus_prof :
      total += float(j.total)
    professeurblocus.total = str(total)
    professeurblocus.save()
pre_save.connect(journeeblocus_pre_save, sender = JourneeBlocusProf)
post_save.connect(journeeblocus_post_save, sender = JourneeBlocusProf)


class RapportBlocusModule(models.Model):
  module     = models.ForeignKey(ModuleBlocus)
  etudiant   = models.ForeignKey('etudiants.Etudiant')
  date_envoi = models.DateField(blank=True, null=True)
  # Automatic fields
  rapport_envoye = models.BooleanField(default = False)
  date_creation  = models.DateTimeField(auto_now_add=True)
  auteur         = models.ForeignKey(Professeur)

  def __str__(self):
    return self.etudiant.prenom + ' ' + self.etudiant.nom +' - '+ str(self.date_creation.strftime('%d/%m/%Y'))

RATING = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),)
STATUTS = (('objectif_fixe','Objectif Fixé'),('bilan_realise','Bilan Réalisé'),('rapport_envoye','Rapport Envoyé'),)
class RapportBlocusJournalier(models.Model):
  objectif         = models.TextField()
  objectif_atteint = models.BooleanField(default=False)
  bilan            = models.TextField(blank=True, null=True)
  date             = models.DateField(blank=True, null=True)
  recommandation   = models.TextField(blank=True, null=True)
  remarque         = models.TextField(blank=True, null=True)
  # Rating fields
  concentration  = models.CharField(max_length=100, choices=RATING, default='1')
  productivite   = models.CharField(max_length=100, choices=RATING, default='1')
  moral          = models.CharField(max_length=100, choices=RATING, default='1')
  # Automatic fields
  presence       = models.OneToOneField(Presence)
  date_creation  = models.DateTimeField(auto_now_add=True)
  rapport_envoye = models.BooleanField(default = False)
  date_envoi     = models.DateField(blank=True, null=True)
  auteur         = models.ForeignKey(Professeur)
  rapportmodule  = models.ForeignKey(RapportBlocusModule)
  statut         = models.CharField(max_length=100, choices=STATUTS, default='objectif_fixe')
