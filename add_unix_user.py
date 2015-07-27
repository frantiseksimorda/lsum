# -*- coding: utf-8 -*-
from __future__ import print_function
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()
from evid.models import Student, User_account_student
from connection import Connection


def is_generated(user):
    """ Parse /etc/passwd file to findout if user exists """
    file = open('/etc/passwd', 'r')
    passwd = file.read()
    # print(user in passwd)
    return (user in passwd)


def generate(username, default_passwdord, name, surname, typ_uzivatele):
    """ Generovani uzvatelu Unixserveru a Sambe """
    if typ_uzivatele == "kantor":
        group_id = "kantori" # nebo ID
        homedir_path = "/user/kantori/"

    else:
        group_id = "studenti"
        homedir_path = "/user/studenti/"

    kod_baka = "Q"
    # Student.object.values_list('surname', 'name').filter(kod_baka=kod_baka)
    os.system('useradd -m /user/studenti/' + username)


is_generated('fanda')