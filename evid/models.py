# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.contrib import admin
from django.utils import timezone


SEX_CHOICES = (
('M', 'Muž'),
('Z', 'Zena'),
)


class School_class(models.Model):
    """ Trida """
    short_name = models.CharField(max_length=5)
    start_year = models.DateField(auto_now_add=True)
    letter = models.CharField(max_length=2, editable=False)
    length_of_studdy = models.IntegerField(editable=False)

    def __unicode__(self):
        return self.short_name

    def save(self, *args, **kwargs):
        """ Custumize  save process """
        self.letter = self.short_name[:1]
        self.length_of_studdy = 8 if self.short_name[0] == "R" else 4

        super(School_class, self).save(*args, **kwargs)



class Teacher(models.Model):
    """ Kantori """
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    login = models.CharField(null=True,max_length=20)
    default_passwd = models.CharField(max_length=50,null=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    kod_baka = models.CharField(max_length=20) # blank=True ???ANO/NE???
    add_date = models.DateTimeField(auto_now_add=True)
    chip = models.CharField(null=True,max_length=20)
    email = models.EmailField(null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.name



class Student(models.Model):
    """ Studenti """
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    kod_baka = models.CharField(max_length=20)
    school_class = models.ForeignKey(School_class)
    rfid = models.CharField(max_length=20, null=True)

    def save(self, *args, **kwargs):
        """ Custumize  save process """
        super(Student, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class User_account_student(models.Model):
    kod_baka = models.CharField(max_length=20)
    login = models.CharField(max_length=50, null=True, editable=False)
    default_passwd = models.CharField(max_length=50, null=True, editable=False)
    isActive = models.NullBooleanField(null=True, editable=False)
    banTime = models.DateTimeField(null=True, editable=False)
    unbanTime = models.DateTimeField(null=True, editable=False)
    autoDeleteTime = models.DateTimeField(null=True, editable=False)
    email = models.EmailField(null=True)

class Ban_reason(models.Model):
    """Duvody zabanovani uctu"""
    reason = models.CharField(max_length=50)
    duration = models.DurationField(null=True)

    def __unicode__(self):
        return self.reason

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')