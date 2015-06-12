# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.contrib import admin


POHLAVI_MOZNOSTI = (
('M', 'Muž'),
('Z', 'Zena.'),
)


class Trida(models.Model):
    """ Trida """
    zkratka = models.CharField(max_length=5)
    rok = models.DateField('')
    pismenko = models.CharField(max_length=2)
    delka_studia = models.IntegerField()
    rok_zalozeni = models.DateField()

    def __unicode__(self):
        return self.zkratka

    class Meta:
        verbose_name = 'trida'
        verbose_name_plural = 'tridy'


class Kantor(models.Model):
    """ Kantori """
    jmeno = models.CharField(max_length=50)
    prijmeni = models.CharField(max_length=50)
    login = models.CharField(blank=True,max_length=20)
    pohlavi = models.CharField(max_length=10, choices=POHLAVI_MOZNOSTI)
    kod_baka = models.CharField(max_length=20) # blank=True ???ANO/NE???
    datum_pridani = models.DateTimeField(default=datetime.now, blank=True)
    cip = models.CharField(blank=True,max_length=20)
    email = models.EmailField(blank=True)
    aktivni = models.BooleanField()

    def __unicode__(self):
        return self.jmeno

    class Meta:
        verbose_name = 'kantor'
        verbose_name_plural = 'kantori'


class Student(models.Model):
    """ Studenti """
    jmeno = models.CharField(max_length=50)
    prijmeni = models.CharField(max_length=50)
    login = models.CharField(max_length=20,blank=True)
    pohlavi = models.CharField(max_length=10, choices=POHLAVI_MOZNOSTI)
    kod_baka = models.CharField(max_length=20)
    trida = models.ForeignKey(Trida)
    datum_pridani = models.DateTimeField(default=datetime.now, blank=True)
    cip = models.CharField(max_length=20,blank=True)
    email = models.EmailField(blank=True)
    aktivni = models.BooleanField()


    def __unicode__(self):
        return self.jmeno


    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'studenti'

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')