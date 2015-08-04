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
    return (user in passwd)


def generate(login, user_type, name, surname):
    """ Generate samba users, homedirs and WWW folder  """
    # for user in Script.objects.all():
    #     if not user.timestamp_executed:
    #         if user.action == "add":

    if user_type == "student":
        user_group = "505"
        user_homedir = "/user/studenti/" + login
    elif user_type == "kantor":
        user_group = "555"
        user_homedir = "/user/kantori/" + login
    fullname = name + " " + surname

    # useradd process
    useradd_proc = Popen(["useradd", "-s /bin/false", "-m", "-d", user_homedir, "-c", fullname, "-g", user_group, login], stdout=PIPE, stderr=PIPE)
    stdout, stderr = useradd_proc.communicate()

    # password sett process
    smbpasswd_proc = Popen(["smbpasswd", "-a", login, ], stdout=PIPE, stderr=PIPE)
    stdout1, stderr1 = smbpasswd_proc.communicate()

    # create WWW dir and correct rights
    create_www_proc = Popen(["mkdir", user_homedir + "WWW"], stdout=PIPE, stderr=PIPE)
    stdout2, stderr2 = create_www_proc.communicate()

    # fix owner and group of WWW dir
    chown_www_proc = Popen(["chown", login + ":nobody", user_homedir + "WWW"], stdout=PIPE, stderr=PIPE)
    stdout3, stderr3 = chown_www_proc.communicate()

    # fix owner and group of WWW dir
    chmod_www_proc = Popen(["chmod", "750"], stdout=PIPE, stderr=PIPE)
    stdout4, stderr4 = chmod_www_proc.communicate()

    # Script.objects.filter(login=login).update(
    #     timestamp_executed = datetime.now(),
    #     stdout = stdout,
    #     stderr = stderr,
    #     result_code = 1 if not stderr else 0
    #         )
    return (stdout, stderr, stdout1, stderr1, stdout2, stderr2, stdout3, stderr3, stdout4, stderr4)

def disable_account(login):
    """ smbpasswd -d user - disable Windows login to domain """
    lockUser = Popen(["smbpasswd",  "-d", login], stdout=PIPE, stderr=PIPE)
    stdout, stderr = lockUser.communicate()
    return (stdout, stderr)


def enable_account(login):
    """ smbpasswd -e user - enable Windows login to domain """
    unlockUser = Popen(["smbpasswd",  "-e", login], stdout=PIPE, stderr=PIPE)
    stdout, stderr = unlockUser.communicate()
    return (stdout, stderr)

def remove_account(login):
    """ remove user from system and homedir """
    smbRemoveUser = Popen(["smbpasswd", "-x", login], stdout=PIPE, stderr=PIPE)
    stdouts, stderrs = smbRemoveUser.communicate()
    removeUser = Popen(["userdell",  "-r", login], stdout=PIPE, stderr=PIPE)
    stdout, stderr = removeUser.communicate()
    return (stdout,stderr,stdouts,stderrs)

def cahange_password():
    """ smbpasswd -a user - change password """
    pass

generate('fanda')