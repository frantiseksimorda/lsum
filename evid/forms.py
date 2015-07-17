# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from .models import Student

STUDENTS = tuple((item.id, item.surname+" "+item.name+" ("+str(item.school_class)+"), "+item.kod_baka)
                 for item in Student.objects.all().order_by("surname"))

class RfidScanForm(forms.Form):
    Chip = forms.CharField(max_length=8,
                           min_length=8,
                           label="",
                           widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),
                           validators=[RegexValidator(r'^[0-9A-Fa-f]+$', 'Enter a valid RFID code.')],
                           )


class RfidAssignToAnotherOwnerForm(forms.Form):
    Chip = forms.CharField(label="")

    Select = forms.CharField(widget=forms.Select(choices=STUDENTS),
                             label="",
                             required=False,
                             )


class RfidSelectStudentForm(forms.Form):
    Select = forms.CharField(widget=forms.Select(choices=STUDENTS),
                             label="",
                             required=False,
                             )

class RfidRemoveFromStudentForm(forms.Form):
    Student_id = forms.CharField(label="")


class RfidAssignSingleScanForm(forms.Form):
    Student_id = forms.CharField(label="")

    Chip = forms.CharField(max_length=8,
                           min_length=8,
                           label="",
                           widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),
                           validators=[RegexValidator(r'^[0-9A-Fa-f]+$', 'Enter a valid RFID code.')],
                           )
