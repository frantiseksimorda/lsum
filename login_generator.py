# coding: utf8

__author__ = 'karlosss'

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()
from evid.models import Student, User_account_student
from misc import stringList
from random import randint
from hashlib import sha512
from unicodedata import normalize

def shorten(x, length):
    # first chars of string x, normalized, lowercase; if shorter than 3, automatically extended by xs from the right
    x = x[:length].rstrip()
    x = normalize('NFKD', x).encode('ascii', 'ignore')
    x = x.lower()

    while len(x) < length:
        x += "x"

    return x


def generate_login(name, surname):

    existing_logins = stringList(User_account_student.objects.values_list("login"))

    surname = shorten(surname, 3)
    name = shorten(name, 2)
    username = "x" + surname + name

    counter = 1

    for existing_login in existing_logins:
        if username in existing_login:
            counter += 1

    number = "0" + str(counter) if counter < 10 else str(counter)

    username += number

    return username

def generate_password():
    # takes a random seq. of a SHA512 hash of a random integer in range from 0 to 2bil.
    random_hash = ""

    while len(random_hash) < 8:
        random_hash = sha512(str(randint(0, 2000000000))).hexdigest()

    random_offset = randint(0, len(random_hash)-8)

    def_pwd = random_hash[random_offset:random_offset+8]

    return def_pwd

def generate_email(login):
    return login + "@gjk.cz"

def generate_teacher_login(surname):

    existing_logins = stringList(User_account_student.objects.values_list("login"))

    username = shorten(surname, len(surname))

    counter = 0
    for existing_login in existing_logins:
        if username in existing_login:
            counter += 1

    if counter > 0:
        username += str(counter)

    return username




