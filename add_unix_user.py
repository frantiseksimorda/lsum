# -*- coding: utf-8 -*-
from __future__ import print_function
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()
from evid.models import Student, User_account_student, Script
from connection import Connection
from subprocess import Popen, PIPE
from datetime import datetime

def is_generated(user):
    """ Parse /etc/passwd file to findout if user exists """
    file = open('/etc/passwd', 'r')
    passwd = file.read()
    # print(user in passwd)
    return (user in passwd)


def generate(username=""):
    """ Generovani uzvatelu Unixserveru a Sambe """
    # Script.object.values_list('command')
    users_for_process = Script.objects.values_list()

    process = Popen(["useradd","-m", "-G" ], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    script = Script(
        timestamp_executed = datetime.now(),
        stdout = stdout,
        stderr = stderr,
        result_code = 1 if not stderr else 0
                    )
    script.save()

for user in Script.objects.values_list():
    print (user)

# generate('fanda')