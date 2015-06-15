# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.contrib import admin


SEX_CHOICES = (
('M', 'Muž'),
('Z', 'Zena.'),
)


class School_class(models.Model):
    """ Trida """
    short_name = models.CharField(max_length=5)
    start_year = models.DateField('')
    letter = models.CharField(max_length=2)
    length_of_studdy = models.IntegerField()
    # start_year = models.DateField()

    def __unicode__(self):
        return self.short_name

    # class Meta:
    #     verbose_name = 'Class'
    #     verbose_name_plural = 'Classes'


class Teacher(models.Model):
    """ Kantori """
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    login = models.CharField(blank=True,max_length=20)
    default_passwd = models.CharField(max_length=50,blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    kod_baka = models.CharField(max_length=20) # blank=True ???ANO/NE???
    add_date = models.DateTimeField(default=datetime.now, blank=True)
    chip = models.CharField(blank=True,max_length=20)
    email = models.EmailField(blank=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.name

    # class Meta:
    #     verbose_name = 'teacher'
    #     verbose_name_plural = 'teachers'


class Student(models.Model):
    """ Studenti """
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    login = models.CharField(max_length=20,blank=True)
    default_passwd = models.CharField(max_length=50,blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    kod_baka = models.CharField(max_length=20)
    school_class = models.ForeignKey(School_class)
    add_date = models.DateTimeField(default=datetime.now, blank=True)
    rfid = models.CharField(max_length=20,blank=True)
    email = models.EmailField(blank=True)
    active = models.BooleanField()

    def save(self, *args, **kwargs):
        """ Custumize  """
        self.name = self.name + "blabla"
        super(Student, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


    # class Meta:
    #     verbose_name = 'student'
    #     verbose_name_plural = 'students'

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')