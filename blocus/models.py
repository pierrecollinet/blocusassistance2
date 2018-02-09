# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save, post_save, post_delete

from django.utils.text import slugify

from django.db import transaction

from datetime import timedelta, date
import datetime

# Models from intern apps
from ba2.models import Campus
from etudiants.models import Etudiant
from professeurs.models import Professeur


periodes = (('noel','Noël'),('paques','Pâques'),('mai','Mai'),('juillet','Juillet/Août'),)
class Blocus(models.Model):
    nom = models.CharField(max_length=200)
    campus = models.ManyToManyField('ba2.Campus', blank=False)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    periode = models.CharField(max_length=200, choices=periodes, blank=True)
    is_current = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

    def calcul_ca(self):
        all_inscriptions = self.inscriptionblocus_set.all()
        total=0
        for inscription in all_inscriptions:
            total += float(inscription.montant)
        return total

STATUTS = (('professeur','Professeur'),('responsable','Responsable'),('nouveau_prof','Nouveau Prof'))
class ProfesseurBlocus(models.Model):
  professeur = models.ForeignKey(Professeur)
  blocus = models.ForeignKey(Blocus)
  statut = models.CharField(max_length=50, choices = STATUTS, default="professeur")

  def __str__(self):
    return self.professeur.prenom + ' ' + self.professeur.nom
# post save MODULE and PRESENCEJOURBLOCUS
def post_save_blocus_model_receiver(sender, instance, created, *args, **kwargs):
    campus = instance.campus.all()
    date_debut = instance.date_debut
    date_fin = instance.date_fin

    # 1°. On sauve les modules correspondant au blocus
    # Initialisation des variables
    continuer = True
    count_semaine = 0
    count_weekend = 0
    debut_module = date_debut
    while continuer:
      # Rappel for weekday : monday = 0 & sunday = 6
      if debut_module.weekday() >= 0 and debut_module.weekday() <= 4 : #--> entre lundi et vendredi
        nom = "Semaine " + str(count_semaine)
        count_semaine += 1
        prix = "250"
        fin_module = debut_module + datetime.timedelta( (4-debut_module.weekday()) % 7 )
        sem_or_we = "sem"
      else : #--> weekend
        nom = "Weekend " + str(count_weekend)
        count_weekend += 1
        prix = "120"
        fin_module =  debut_module + datetime.timedelta( (6-debut_module.weekday()) % 7 )
        sem_or_we = "we"
      if fin_module >= date_fin :
        continuer = False
        fin_module = date_fin
      delta = fin_module - debut_module
      if delta.days != 4 and delta.days != 1 :
        prix = str((delta.days + 1) * 60)
      module, created = ModuleBlocus.objects.get_or_create(
                                                nom = nom,
                                                date_debut = debut_module,
                                                date_fin = fin_module,
                                                prix = prix,
                                                blocus = instance,
                                                sem_or_we = sem_or_we
                                                )
      list_campus = list(campus)
      module.campus.add(*list_campus)  # on ajoute le many 2 many field
      debut_module = fin_module + timedelta(days = 1)

    # 2°. On sauve les presences
    delta = date_fin - date_debut
    for i in range(delta.days + 1):
        date = date_debut + timedelta(days=i)
        for c in campus:
            presencejourblocus, created = PresenceJourBlocus.objects.get_or_create(
                                                      campus=c,
                                                      date=date,
                                                      blocus=instance
                                                      )
post_save.connect(post_save_blocus_model_receiver, sender=Blocus)



class ModuleBlocusQuerySet(models.query.QuerySet):
    def active(self):
      try:
        blocus = Blocus.objects.filter(is_current=True)[0]
        return self.filter(blocus=blocus)
      except :
        pass

class ModuleBlocusManager(models.Manager):
    def get_queryset(self):
        return ModuleBlocusQuerySet(self.model, using=self._db)

    def all(self,*args,**kwargs):
        return self.get_queryset().active()

sem_or_we = (('sem','Semaine'),('we','Weekend'),('jour','Jour'),)
class ModuleBlocus(models.Model):
  nom = models.CharField(max_length=200)
  date_debut = models.DateField()
  date_fin = models.DateField()
  prix = models.CharField(max_length=200)
  blocus = models.ForeignKey(Blocus)
  campus = models.ManyToManyField(Campus)
  sem_or_we = models.CharField(max_length=200, choices=sem_or_we, default='sem')

  objects = ModuleBlocusManager()

  def __str__(self):
    if str(self.date_debut.strftime('%d/%m/%Y')) == str(self.date_fin.strftime('%d/%m/%Y')):
      name = self.nom +' - '+ str(self.date_debut.strftime('%d/%m/%Y'))
    else :
      name = self.nom +' - du '+ str(self.date_debut.strftime('%d/%m/%Y'))+ ' au '+str(self.date_fin.strftime('%d/%m/%Y'))
    return name

  def get_name(self):
    if str(self.date_debut.strftime('%d/%m/%Y')) == str(self.date_fin.strftime('%d/%m/%Y')):
        name = self.nom +' - '+ str(self.date_debut.strftime('%d/%m/%Y'))
    else :
        name = self.nom +' - du '+ str(self.date_debut.strftime('%d/%m/%Y'))+ ' au '+str(self.date_fin.strftime('%d/%m/%Y'))
    return str(name)

  def get_date_debut(self):
    return datetime.date(self.date_debut.year,self.date_debut.month,self.date_debut.day)
  def get_date_fin(self):
    return datetime.date(self.date_fin.year,self.date_fin.month,self.date_fin.day)


class PresenceJourBlocus(models.Model):
    campus = models.ForeignKey(Campus)
    blocus = models.ForeignKey(Blocus)
    date = models.DateField()

    def __str__(self):
        return self.get_name()

    def get_name(self):
        day = self.date.weekday()
        days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        return days[day]+ ' - '+str(self.date.strftime('%d/%m/%Y'))


class InscriptionBlocus(models.Model):
    etudiant = models.ForeignKey(Etudiant)
    blocus = models.ForeignKey(Blocus)
    module = models.ManyToManyField(ModuleBlocus)
    campus = models.ForeignKey(Campus)
    montant = models.CharField(max_length=200)
    is_paid = models.BooleanField(default=False)
    origine = models.CharField(verbose_name="Comment avez-vous entendu parler de Blocus Assistance?", max_length=200)
    date_inscription = models.DateField(auto_now_add=True)
    suivi_inscription = models.TextField(blank=True)
    code_promo = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ["etudiant"]

    def __str__(self):
        return self.etudiant.prenom +'-'+ self.etudiant.nom

    def calculate_total_price(self):
      total = 0
      for mod in self.module.all():
        total += float(mod.prix)
      return total
def post_save_inscription_model_receiver(sender, instance, created, *args, **kwargs):
    modules = instance.module.all()
    etudiant = instance.etudiant
    for module in modules :
        date_debut = datetime.date(module.date_debut.year,module.date_debut.month,module.date_debut.day)
        date_fin = datetime.date(module.date_fin.year,module.date_fin.month,module.date_fin.day)
        delta = date_fin - date_debut

        for i in range(delta.days + 1):
            date = date_debut + timedelta(days=i)
            try:
                jourblocus = PresenceJourBlocus.objects.get(
                                                           campus=instance.campus,
                                                           blocus=instance.blocus,
                                                           date=date
                                                           )
                presence, created = Presence.objects.get_or_create(
                                                          etudiant=etudiant,
                                                          date=date,
                                                          inscription=instance,
                                                          jourblocus = jourblocus
                                                          )
                presence.jourblocus = jourblocus
                presence.save()
            except:
                pass
post_save.connect(post_save_inscription_model_receiver, sender=InscriptionBlocus)


# STATUTS = (('present','Présent'), ('absent','Absent'), ('retard','En retard'), ('absent_justifie','Absence justifiée'), )
# class Presence(models.Model):
#     etudiant = models.ForeignKey(Etudiant)
#     date = models.DateField()
#     heure_arrivee = models.TimeField(default="08:30")
#     statut = models.CharField(max_length=30, default="absent", choices=STATUTS)
#     inscription = models.ForeignKey(InscriptionBlocus)
#     jourblocus = models.ForeignKey(PresenceJourBlocus)
#     commentaire = models.TextField(blank=True)

#     def __str__(self):
#         return self.etudiant.prenom + ' ' + self.etudiant.nom + '(' + self.statut + ')'

#     def is_late(self):
#       heure_arrivee = self.heure_arrivee
#       start_time    = datetime.time(8, 30, 0)
#       if heure_arrivee > start_time :
#         bool = True
#       else :
#         bool = False
#       return bool


STATUTS = (('present','Présent'), ('absent','Absent'), ('retard','En retard'), ('absent_justifie','Absence justifiée'), )
class Presence(models.Model):
    etudiant = models.ForeignKey(Etudiant)
    date = models.DateField()
    heure_arrivee = models.TimeField(default="08:30")
    statut = models.CharField(max_length=30, default="absent", choices=STATUTS)
    inscription = models.ForeignKey(InscriptionBlocus)
    jourblocus = models.ForeignKey(PresenceJourBlocus)
    commentaire = models.TextField(blank=True)

    def __str__(self):
        return self.etudiant.prenom + ' ' + self.etudiant.nom + '(' + self.statut + ')'

    def is_late(self):
      heure_arrivee = self.heure_arrivee
      start_time    = datetime.time(8, 30, 0)
      if heure_arrivee > start_time :
        bool = True
      else :
        bool = False
      return bool







