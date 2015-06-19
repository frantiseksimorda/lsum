# coding: utf8

__author__ = "karlosss"

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()
from evid.models import Student
from connection import Connection

# Script to import data and insert them to the Django database


# connection and queries to the source database
conn = Connection("bakalari")
data = conn.execute("SELECT jmeno, prijmeni, pohlavi, intern_kod, trida, isic_cip FROM zaci")

for line in data:
    print line





def get_class_id(class_name):
    pass

for line in data:
    student = Student(name=line[0], surname=line[1], sex=line[2], kod_baka=line[3], school_class_id=1, rfid=line[5], active=True)
    student.save()




# username: xPrijmeniJmeno01 (prijmeni+jmeno 5 znaku)
# password: nějakej bordel -> sha -> náhodných 8 znaků
#





