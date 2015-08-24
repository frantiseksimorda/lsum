# -*- coding: utf-8 -*-
from __future__ import print_function
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()
from subprocess import Popen, PIPE

def is_generated(user):
    """ Parse /etc/passwd file to findout if user exists """
    file = open('/etc/passwd', 'r')
    passwd = file.read()
    return user in passwd


def create_unix_user(login, user_type, name, surname, password):
    """ Generate samba users, homedirs and WWW folder  """
    # 0 = student
    # 1 = kantor
    # (psat tam string je fuj a hnuj)
    if user_type == 0:
        user_group = "505"
        user_homedir = "/user/studenti/" + login
    elif user_type == 1:
        user_group = "555"
        user_homedir = "/user/kantori/" + login
    else:
        raise Exception("ses vul")
    # ty taky, když raisuješ string a ne exception :)
    fullname = name + " " + surname

    # useradd process
    # print ("login="+login,"user_group="+user_group,"user_homedir="+user_homedir,"fullname="+fullname,"password="+password)
    useradd_proc = Popen(["useradd -s /bin/false -m -d " + user_homedir + " -c \"" + fullname + "\" -g " + user_group + " " + login], shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = useradd_proc.communicate()

    # password sett process
    # smbpasswd_proc = Popen(["printf \"%s\n%s\n\"" + password + " " + password + "| /usr/bin/smbpasswd ", "-s", "-a", login,], stdout=PIPE, stderr=PIPE)
    smbpasswd_proc = Popen(["printf \"%s\n%s\n\" \"" + password + "\" \"" + password + "\" | /usr/bin/smbpasswd -a " + login], stdout=PIPE, stderr=PIPE, shell=True)
    stdout1, stderr1 = smbpasswd_proc.communicate()

    # create WWW dir and correct rights
    create_www_proc = Popen(["mkdir", user_homedir + "/WWW"], stdout=PIPE, stderr=PIPE)
    stdout2, stderr2 = create_www_proc.communicate()

    # fix owner and group of WWW dir
    chown_www_proc = Popen(["chown", login + ":nobody", user_homedir + "/WWW"], stdout=PIPE, stderr=PIPE)
    stdout3, stderr3 = chown_www_proc.communicate()

    # chmod on homedir
    chmod_homedir_proc = Popen(["chmod", "711", "-R", user_homedir], stdout=PIPE, stderr=PIPE)
    stdout4, stderr4 = chmod_homedir_proc.communicate()

    # fix owner and group of WWW dir
    chmod_www_proc = Popen(["chmod", "750", user_homedir + "/WWW"], stdout=PIPE, stderr=PIPE)
    stdout5, stderr5 = chmod_www_proc.communicate()

    return (stdout, stderr, stdout1, stderr1, stdout2, stderr2, stdout3, stderr3, stdout4, stderr4, stdout5, stderr5)


def disable_unix_account(login):
    """ smbpasswd -d user - disable Windows login to domain """
    lockUser = Popen(["smbpasswd",  "-d", login], stdout=PIPE, stderr=PIPE)
    stdout, stderr = lockUser.communicate()
    return (stdout, stderr)


def enable_unix_account(login):
    """ smbpasswd -e user - enable Windows login to domain """
    unlockUser = Popen(["smbpasswd",  "-e", login], stdout=PIPE, stderr=PIPE)
    stdout, stderr = unlockUser.communicate()
    return (stdout, stderr)

def remove_unix_account(login):
    """ remove user from system and homedir """
    smbRemoveUser = Popen(["smbpasswd", "-x", login], stdout=PIPE, stderr=PIPE)
    stdouts, stderrs = smbRemoveUser.communicate()
    removeUser = Popen(["userdel",  "-r", login], stdout=PIPE, stderr=PIPE)
    stdout, stderr = removeUser.communicate()
    return (stdout,stderr,stdouts,stderrs)

def cahange_unxi_password():
    """ smbpasswd -a user - change password """
    pass

