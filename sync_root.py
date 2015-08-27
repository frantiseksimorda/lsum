import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()

from evid.models import Student, School_class, User_account_student, Email_changes
from misc import stringList
from time import time, asctime
from login_generator import generate_login, generate_password, generate_email
from datetime import timedelta
from django.utils import timezone
from add_unix_user import *

sync_interval = 200

def create_user_accounts():

    data = list(Student.objects.raw("""
        SELECT evid_student.id,
        evid_student.name,
        evid_student.surname,
        evid_user_account_student.login,
        evid_user_account_student.default_passwd
        FROM evid_student
        INNER JOIN evid_user_account_student
        ON evid_student.kod_baka = evid_user_account_student.kod_baka
    """))

    for i in data:
        if not is_generated(i.login):
            create_unix_user(i.login, 0, i.name, i.surname, i.default_passwd)


def update_user_accounts():
    pass

def delete_user_accounts():
    for i in get_unix_users():
        if i not in stringList(User_account_student.objects.values_list("login")):
            remove_unix_account(i)

def run():
    create_user_accounts()
    update_user_accounts()
    delete_user_accounts()


while True:
    print "probiha non root synchronizace, nevypinat skript!"
    timestamp = time()
    run()
    print "synchronizace provedena "+str(asctime())

    while timestamp + sync_interval > time():
        pass


