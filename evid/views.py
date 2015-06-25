# -*- coding: utf-8 -*-
# from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Document
from .forms import DocumentForm


def baka_sync(request):
    """ Sync users with Bakalari MSSQL database, add new studenst from new classes"""
    from evid.models import Student, School_class
    from connection import Connection

    # connection and query to the source database
    conn = Connection("bakalari")
    data = conn.execute("SELECT trida FROM zaci")

    # selecting each class, appending it only once
    classes = []

    for line in data:
        if line[0] not in classes:
            classes.append(line[0])

    # editing the list to look nicer :)
    classes.sort()
    classes.reverse()

    # parsing classes to the correct format for insertion
    existing_classes = School_class.objects.values_list("short_name")
    existing_classes_parsed = []

    for item in existing_classes:
        existing_classes_parsed.append(item[0])

    # inserting to the school_class table of the Django DB
    for item in classes:
        if item not in existing_classes_parsed:
            school_class = School_class(short_name=item)
            school_class.save()

    def get_class_id(class_name):

        return School_class.objects.values_list("id").filter(short_name=class_name)[0][0]


    conn = Connection("bakalari")
    data = conn.execute("SELECT jmeno, prijmeni, pohlavi, intern_kod, trida, isic_cip FROM zaci")


    existing_codes = Student.objects.values_list("kod_baka")
    existing_codes_parsed = []

    for item in existing_codes:
        existing_codes_parsed.append(item[0])


    for line in data:

        if line[3] not in existing_codes_parsed:

            student = Student(
                name=line[0],
                surname=line[1],
                sex=line[2],
                kod_baka=line[3],
                school_class_id=get_class_id(line[4]),
                rfid=line[5],
                # active=True,
            )

            student.save()

    return HttpResponseRedirect("/admin/evid/student")


def maturanti_lock(request):
    """ lock users logins of thoses, who sucessfully end school"""
    return request


def generate_logins(request):
    """ after sync with bakalari (imported new users), generate new usernames and password for new classes """
    return request