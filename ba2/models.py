# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save, post_save, post_delete

from django.utils.text import slugify

from django.db import transaction

from datetime import timedelta
import datetime

#from blocus.models import Blocus, ModuleBlocus

class Campus(models.Model):
    nom  = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    capacite_maximale = models.SmallIntegerField(default=10)

    def __str__(self):
        return self.nom

    def get_image_url(self):
        img = self.campusimage_set.first()
        if img:
            return img.image.url
        return img #None

    def get_images(self):
        imgs = self.campusimage_set.all()
        return imgs



def image_upload_to(instance, filename):
    title = instance.campus.nom
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
    return "campus/%s/%s" %(slug, new_filename)


class CampusImage(models.Model):
    campus = models.ForeignKey(Campus)
    image = models.ImageField(upload_to=image_upload_to)

    def __unicode__(self):
        return self.campus.nom

class Universite(models.Model):
  nom = models.CharField(max_length=200)
  abreviation = models.CharField(max_length=200, blank=True, null=True)
  logo = models.ImageField(upload_to = 'mes_images/', blank=True, null=True)

  def __str__(self):
    return self.nom

class Faculte(models.Model):
  universite = models.ForeignKey(Universite)
  abreviation = models.CharField(max_length=200, blank=True, null=True)
  nom = models.CharField(max_length=200)
  logo = models.ImageField(upload_to = 'mes_images/', blank=True, null=True)

  def __str__(self):
    return self.nom

class Etude(models.Model):
  faculte = models.ForeignKey(Faculte)
  abreviation = models.CharField(max_length=200, blank=True, null=True)
  nom = models.CharField(max_length=200)
  logo = models.ImageField(upload_to = 'mes_images/', blank=True, null=True)

  def __str__(self):
    return self.nom

annees = (
    ('BA1', 'BA1'),
    ('BA2', 'BA2'),
    ('BA3', 'BA3'),
    ('MA1', 'MA1'),
    ('MA2', 'MA2'),
    ('diplome', 'Diplômé'),
)

CATEGORIES = (('blocus','Blocus Assistés'),('cours','Cours Particuliers'),('suiviintensif','Suivi Intensif'),)
class TemoignageEleve(models.Model):
    prenom = models.CharField(max_length=200)
    photo = models.ImageField(upload_to = 'mes_images/')
    temoignage = models.TextField()
    etude = models.CharField(max_length=200)
    annee = models.CharField(max_length=200, choices=annees)
    active = models.BooleanField(default=False)
    categories = models.CharField(max_length=200, choices = CATEGORIES)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.prenom
