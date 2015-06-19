# coding: utf8

__author__ = "karlosss"

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()
from evid.models import Student, School_class
from connection import Connection

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
            active=True,
        )

        student.save()
