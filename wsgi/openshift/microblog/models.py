# -*- coding: utf-8 -*-
__author__ = 'Joanna667'
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Article(models.Model):
    tytul = models.CharField(max_length=50)
    tresc = models.CharField(max_length=500)
    pub_date = models.DateTimeField()
    mod_date = models.DateTimeField(blank=True, null=True)
    pub_user = models.ForeignKey(User, related_name='pub_users')
    mod_user = models.ForeignKey(User, related_name='mod_users', blank=True, null=True)

    def __unicode__(self):
        return self.tytul

class UserActivation(models.Model):
    user = models.ForeignKey(User)
    activation_key = models.CharField(max_length=6, null=True, blank=True)

    def __unicode__(self):
        return self.activation_key

class Tag(models.Model):
    name = models.CharField(max_length=25)
    articles = models.ManyToManyField(Article)

    def __unicode__(self):
        return self.name