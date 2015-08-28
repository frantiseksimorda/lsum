# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.contrib import admin
from django.utils import timezone

from django.contrib.auth.models import User
from oauth2client.django_orm import FlowField, CredentialsField


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
    kod_baka = models.CharField(max_length=20) # blank=True ???ANO/NE???
    rfid = models.CharField(null=True,max_length=20)
    active = models.BooleanField(default=True)

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
    status = models.CharField(max_length=10, null=True)
    to_be_skipped = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """ Custumize  save process """
        super(Student, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class User_account_student(models.Model):
    kod_baka = models.CharField(max_length=20)
    login = models.CharField(max_length=50, null=True, editable=False)
    default_passwd = models.CharField(max_length=50, null=True, default="")
    email = models.EmailField(null=True)
    email_to_create = models.BooleanField(default=True)
    email_created = models.BooleanField(default=False)
    email_to_disable = models.BooleanField(default=False)
    email_disabled = models.BooleanField(default=False)
    delete_time = models.DateTimeField(null=True, blank=True)

class Ban_reason(models.Model):
    """Duvody zabanovani uctu"""
    reason = models.CharField(max_length=50)
    duration = models.DurationField(null=True)

    def __unicode__(self):
        return self.reason

class Email_changes(models.Model):
    """tabulka pro GAPI"""
    user_type = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=20, null=True, blank=True)
    default_passwd = models.CharField(max_length=1000, null=True, blank=True)
    action = models.CharField(max_length=50, null=True, blank=True)
    timestamp_written = models.DateTimeField(null=True, blank=True)
    timestamp_executed = models.DateTimeField(null=True, blank=True)
    result_code = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.email

class Error_log(models.Model):
    """logovani chyb"""
    timestamp = models.DateTimeField(auto_now_add=True)
    command = models.CharField(max_length=1000)
    stderr = models.CharField(max_length=1000)

class Lsum_account(models.Model):
    login = models.CharField(max_length=20)
