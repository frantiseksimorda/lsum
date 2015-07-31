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
    users_for_process = Script.objects.values_list()
    for user in Script.objects.all():
        # print (user)
        if not user.timestamp_executed:
            if user.action == "add":

                if user.user_type == "student":
                    user_group = "505"
                    user_homedir = "/user/studenti/" + user.login
                elif user.user_type == "kantor":
                    user_group = "555"
                    user_homedir = "/user/kantori/" + user.login
                fullname = user.name + " " + user.surname

                # useradd process
                useradd_proc = Popen(["useradd", "-s /bin/false", "-m", "-d", user_homedir, "-c", fullname, "-g", user_group, user.login], stdout=PIPE, stderr=PIPE)
                stdout, stderr = useradd_proc.communicate()

                # password sett process
                smbpasswd_proc = Popen(["smbpasswd", "-a", user.login, ], stdout=PIPE, stderr=PIPE)
                stdout1, stderr1 = smbpasswd_proc.communicate()

                # create WWW dir and correct rights
                create_www_proc = Popen(["mkdir", user_homedir + "WWW"], stdout=PIPE, stderr=PIPE)
                stdout2, stderr2 = create_www_proc.communicate()

                # fix owner and group of WWW dir
                chown_www_proc = Popen(["chown", user.login + ":nobody", user_homedir + "WWW"], stdout=PIPE, stderr=PIPE)
                stdout3, stderr3 = chown_www_proc.communicate()

                # fix owner and group of WWW dir
                chmod_www_proc = Popen(["chmod", "750"], stdout=PIPE, stderr=PIPE)
                stdout4, stderr4 = chmod_www_proc.communicate()

                Script.objects.filter(login=user.login).update(
                    timestamp_executed = datetime.now(),
                    stdout = stdout,
                    stderr = stderr,
                    result_code = 1 if not stderr else 0
                        )


generate('fanda')