# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()
from subprocess import Popen, PIPE
from connection import Connection
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

connKopirky = Connection("kopirky")
connKnihovna = Connection("knihovna")

def is_generated(user):
    """ Parse /etc/passwd file to findout if user exists """
    file = codecs.open('/etc/passwd', 'r', 'utf-8')
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
    
    name = name.strip()
    surname = surname.strip()

    fullname = name + " " + surname

    # useradd process
    # print ("login="+login,"user_group="+user_group,"user_homedir="+user_homedir,"fullname="+fullname,"password="+password)
    useradd_proc = Popen(["useradd -s /bin/false -m -d " + user_homedir + " -c \"" + fullname + "\" -g " + user_group + " " + login], shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = useradd_proc.communicate()

    # password sett process
    # smbpasswd_proc = Popen(["printf \"%s\n%s\n\"" + password + " " + password + "| /usr/bin/smbpasswd ", "-s", "-a", login,], stdout=PIPE, stderr=PIPE)
    smbpasswd_proc = Popen(["printf \"%s\n%s\n\" \"" + password + "\" \"" + password + "\" | /usr/bin/smbpasswd -a -s " + login], stdout=PIPE, stderr=PIPE, shell=True)
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


def safeq_create_user(login, user_type, name, surname, email, password, rfid):

    if user_type == 1:
        stredisko = 1
    elif user_type == 0:
        stredisko = 2
    else:
        stredisko = 2

    query = "INSERT INTO users (login,pass,name,surname,sign,email,flag,ip,ou_id,ext_id,login_ascii,name_ascii,surname_ascii,replicated,safeq_oid,card_num,homedir,ext_name) VALUES ('%s', '%s', '%s', '%s', NULL, '%s', 1, NULL, %s, NULL, '%s', '%s', '%s', 0, NULL, NULL, NULL, NULL);" % (login, password, name, surname, email, stredisko, login, name, surname)
    connKopirky.execute(query, protected=False)

    user_id = connKopirky.execute("SELECT id FROM users WHERE login = '"+login+"'")[0][0]

    query = "INSERT INTO users_cards (user_id,card,dual_pin,replicated_card,replicated_card_from,replicated_card_flag,pin_expiration_date) VALUES (%s,'%s',NULL,0,NULL,0,NULL);" % (user_id, rfid)
    connKopirky.execute(query, protected=False)

def safeq_delete_user(login):

    user_id = connKopirky.execute("SELECT id FROM users WHERE login = '"+login+"'")[0][0]

    query = "DELETE FROM users WHERE login = '"+login+"'"
    connKopirky.execute(query, protected=False)

    query = "DELETE FROM users_cards WHERE user_id = "+str(user_id)
    connKopirky.execute(query, protected=False)

def safeq_is_generated(login):
    try:
        line = connKopirky.execute("SELECT login FROM users WHERE login = '"+login+"'")[0][0]
        return True
    except:
        return False

def safeq_update_user(login, rfid):

    user_id = connKopirky.execute("SELECT id FROM users WHERE login = '"+login+"'")[0][0]

    query = "UPDATE users_cards SET card = '"+rfid+"' WHERE user_id = "+str(user_id)
    connKopirky.execute(query, protected=False)

def knihovna_update_user(kod_baka, rfid):

    query = "UPDATE ctenari SET bar_cod = '"+rfid+"' WHERE bakalari = '"+kod_baka+"'"
    connKnihovna.execute(query, protected=False)

def get_unix_users():
    file = codecs.open("/etc/passwd", "r", 'utf-8')
    content = file.readlines()

    user_list = []

    for i in content:
        user_list.append(i.split(":")[0])

    return user_list

get_unix_users()

