# coding: utf8

__author__ = "karlosss"

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()
from evid.models import School_class
from connection import Connection

# Script to import data and insert them to the Django database


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