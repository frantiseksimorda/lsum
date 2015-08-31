# coding: utf8

from __future__ import unicode_literals

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()

from evid.models import Student, School_class, User_account_student, Email_changes, Teacher
from misc import stringList
from time import time, asctime
from login_generator import generate_login, generate_password, generate_email, generate_teacher_login
from datetime import timedelta
from django.utils import timezone
from add_unix_user import *


sync_interval = 200
connBaka = Connection("bakalari")
connKopirky = Connection("kopirky")

def convert_date(x):
    x = x.split(".")

    x[0] = x[0].strip()
    x[1] = x[1].strip()
    x[2] = x[2].strip()

    if len(x[0]) < 2: x[0]="0"+x[0]
    if len(x[1]) < 2: x[1]="0"+x[1]

    return x[2]+"-"+x[1]+"-"+x[0]



def get_class_id(class_name):
    return School_class.objects.values_list("id").filter(short_name=class_name)[0][0]

def fetch_data():

    priznaky = connBaka.execute("SELECT intern_kod, druh, datum FROM histzaku ORDER BY datum DESC ")
    studenti = connBaka.execute("SELECT intern_kod, jmeno, prijmeni, pohlavi, trida, datum_nar FROM zaci ORDER BY intern_kod")
    school_classes = connBaka.execute("SELECT trida FROM zaci GROUP BY trida")

    school_classes_parsed = stringList(school_classes)

    priznaky_parsed = []

    for i in priznaky:

        if i[0] not in stringList(priznaky_parsed):
            priznaky_parsed.append((i[0], i[1]))

    studenti_parsed = []

    for i in range(0,len(studenti),1):

        date = convert_date(studenti[i][5])


        if studenti[i][0] not in stringList(priznaky_parsed):
            studenti_parsed.append((studenti[i][0], studenti[i][1], studenti[i][2], studenti[i][3], studenti[i][4], "", date))
        else:
            for j in priznaky_parsed:
                if j[0] == studenti[i][0]:
                    studenti_parsed.append((studenti[i][0], studenti[i][1], studenti[i][2], studenti[i][3], studenti[i][4], j[1], date))

    return (studenti_parsed, school_classes_parsed)

def fetch_data_teachers():
    ucitele = connBaka.execute("SELECT intern_kod, jmeno, prijmeni, deleted_rc FROM ucitele ORDER BY intern_kod")
    return ucitele

def create_user_accounts():

    for i in Student.objects.all():

        if i.kod_baka not in stringList(User_account_student.objects.values_list("kod_baka")):
            username = generate_login(i.name, i.surname)
            password = generate_password()
            email = generate_email(username)

            user_account = User_account_student(
                kod_baka=i.kod_baka,
                login=username,
                default_passwd=password,
                email=email,
                email_to_create=True,
            )
            user_account.save()

        else:
            if User_account_student.objects.filter(kod_baka=i.kod_baka).values_list("default_passwd")[0][0] == "":
                User_account_student.objects.filter(kod_baka=i.kod_baka).update(
                    default_passwd=generate_password()
                )

    for i in Teacher.objects.all():

        if i.kod_baka not in stringList(User_account_student.objects.values_list("kod_baka")):
            username = generate_teacher_login(i.surname)
            password = generate_password()
            email = generate_email(username)

            user_account = User_account_student(
                kod_baka=i.kod_baka,
                login=username,
                default_passwd=password,
                email=email,
                email_to_create=True,
            )
            user_account.save()

        else:
            if User_account_student.objects.filter(kod_baka=i.kod_baka).values_list("default_passwd")[0][0] == "":
                User_account_student.objects.filter(kod_baka=i.kod_baka).update(
                    default_passwd=generate_password()
                )

    data = list(Student.objects.raw("""
        SELECT evid_student.id,
        evid_student.name,
        evid_student.surname,
        evid_student.rfid,
        evid_user_account_student.login,
        evid_user_account_student.default_passwd,
        evid_user_account_student.email
        FROM evid_student
        INNER JOIN evid_user_account_student
        ON evid_student.kod_baka = evid_user_account_student.kod_baka
    """))

    for i in data:
        if not safeq_is_generated(i.login):
            safeq_create_user(i.login, 0, i.name, i.surname, i.email, i.default_passwd, i.rfid)

    data = list(Teacher.objects.raw("""
        SELECT evid_teacher.id,
        evid_teacher.name,
        evid_teacher.surname,
        evid_teacher.rfid,
        evid_user_account_student.login,
        evid_user_account_student.default_passwd,
        evid_user_account_student.email
        FROM evid_teacher
        INNER JOIN evid_user_account_student
        ON evid_teacher.kod_baka = evid_user_account_student.kod_baka
    """))

    for i in data:
        if not safeq_is_generated(i.login):
            safeq_create_user(i.login, 1, i.name, i.surname, i.email, i.default_passwd, i.rfid)


def update_user_accounts():
    data = list(Student.objects.raw("""
        SELECT evid_student.id,
        evid_student.rfid,
        evid_user_account_student.login
        FROM evid_student
        INNER JOIN evid_user_account_student
        ON evid_student.kod_baka = evid_user_account_student.kod_baka
    """))

    for i in data:
        if i.rfid != "":
            safeq_update_user(i.login, i.rfid)
            knihovna_update_user(i.kod_baka, i.rfid)

    data = list(Teacher.objects.raw("""
        SELECT evid_teacher.id,
        evid_teacher.rfid,
        evid_user_account_student.login
        FROM evid_teacher
        INNER JOIN evid_user_account_student
        ON evid_teacher.kod_baka = evid_user_account_student.kod_baka
    """))

    for i in data:
        if i.rfid != "":
            safeq_update_user(i.login, i.rfid)
            knihovna_update_user(i.kod_baka, i.rfid)

def disable_enable_emails():

    data = Student.objects.all()

    for i in data:
        if i.status != "" and i.status[0] == "-" and i.status != "-PS":
            User_account_student.objects.filter(kod_baka=i.kod_baka).update(email_to_disable=True)
        else:
            User_account_student.objects.filter(kod_baka=i.kod_baka).update(email_to_disable=False)

def schedule_deletion_of_graduated():
    data = User_account_student.objects.all()

    for i in data:
        if i.kod_baka not in stringList(Student.objects.values_list("kod_baka")) and i.delete_time is None:
            if i.login[0] != "x":
                continue
            User_account_student.objects.filter(kod_baka=i.kod_baka).update(delete_time=timezone.now() + timedelta(days=365))
            User_account_student.objects.filter(kod_baka=i.kod_baka).update(email_to_disable=True)


def delete_graduated():
    data = User_account_student.objects.all()

    for i in data:
        if i.delete_time is None:
            continue

        if i.delete_time < timezone.now():
            User_account_student.objects.filter(kod_baka=i.kod_baka).update(email_to_create=False)
            safeq_delete_user(i.login)
            if not i.email_created:
                User_account_student.objects.filter(kod_baka=i.kod_baka).delete()


def write_email_changes():

    data2 = User_account_student.objects.all()

    for i in data2:
        if i.email_to_create and not i.email_created:
            cond = i.email in stringList(Email_changes.objects.values_list("email")) and "create" in stringList(Email_changes.objects.values_list("action").filter(email=i.email))
            if not cond:
                data = Student.objects.values_list("name", "surname").filter(kod_baka=i.kod_baka)

                e = Email_changes(user_type=0,
                                  name=data[0][0],
                                  surname=data[0][1],
                                  email=i.email,
                                  default_passwd=i.default_passwd,
                                  action="create",
                                  )

                e.save()

        if i.email_to_disable and not i.email_disabled:

            cond = i.email in stringList(Email_changes.objects.values_list("email")) and "disable" in stringList(Email_changes.objects.values_list("action").filter(email=i.email))
            if not cond:
                e = Email_changes(user_type=0,
                                  email=i.email,
                                  default_passwd=i.default_passwd,
                                  action="disable",
                                  )
                e.save()

        if not i.email_to_disable and i.email_disabled:
            cond = i.email in stringList(Email_changes.objects.values_list("email")) and "enable" in stringList(Email_changes.objects.values_list("action").filter(email=i.email))
            if not cond:
                e = Email_changes(user_type=0,
                                  email=i.email,
                                  default_passwd=i.default_passwd,
                                  action="enable",
                                  )
                e.save()

        if not i.email_to_create and i.email_created:
            cond = i.email in stringList(Email_changes.objects.values_list("email")) and "delete" in stringList(Email_changes.objects.values_list("action").filter(email=i.email))
            if not cond:
                e = Email_changes(user_type=0,
                                  email=i.email,
                                  default_passwd=i.default_passwd,
                                  action="delete",
                                  )
                e.save()



def sync_lsum_db():
    data = fetch_data()

    actual_students = data[0]
    actual_classes = data[1]
    written_students = stringList(Student.objects.values_list("kod_baka"))
    written_classes = stringList(School_class.objects.values_list("short_name"))

    classes_to_delete = []
    classes_to_write = []
    students_to_delete = []
    students_to_write = []
    students_to_update = []

    # finds objects to change

    for i in written_classes:
        if i not in actual_classes:
            classes_to_delete.append(i)

    for i in actual_classes:
        if i not in written_classes:
            classes_to_write.append(i)

    for i in written_students:
        if i not in stringList(actual_students):
            students_to_delete.append(i)

    for i in actual_students:
        if i[0] not in written_students:
            students_to_write.append(i)
        else:
            students_to_update.append(i)

    # executes the changes - important to maintain the order:
    # - delete students
    # - delete classes
    # - add classes
    # - create students
    # - update students

    # old students
    for i in students_to_delete:
        Student.objects.filter(kod_baka=i).delete()

    # old classes
    for i in classes_to_delete:
        School_class.objects.filter(short_name=i).delete()

    # new classes
    for i in classes_to_write:
        school_class = School_class(short_name=i)
        school_class.save()

    # new students
    for i in students_to_write:
        student = Student(
            name=i[1],
            surname=i[2],
            sex=i[3],
            date_of_birth=i[6],
            kod_baka=i[0],
            school_class_id=get_class_id(i[4]),
            status=i[5],
            rfid="",
        )
        student.save()

    # existing students
    for i in students_to_update:
        Student.objects.filter(kod_baka=i[0]).update(
            name=i[1],
            surname=i[2],
            sex=i[3],
            date_of_birth=i[6],
            kod_baka=i[0],
            school_class_id=get_class_id(i[4]),
            status=i[5],
        )

    teachers_to_delete = []
    teachers_to_write = []
    teachers_to_update = []

    actual_teachers = fetch_data_teachers()
    written_teachers = stringList(Teacher.objects.values_list("kod_baka"))

    for i in written_teachers:
        if i not in stringList(actual_teachers):
            teachers_to_delete.append(i)

    for i in actual_teachers:
        if i[0] not in written_teachers:
            teachers_to_write.append(i)
        else:
            teachers_to_update.append(i)

    for i in teachers_to_delete:
        Teacher.objects.filter(kod_baka=i).delete()

    for i in teachers_to_write:
        t = Teacher(
            name=i[1],
            surname=i[2],
            kod_baka=i[0],
            active=not(i[3]),
            rfid="",
        )
        t.save()

    # existing students
    for i in teachers_to_update:
        Teacher.objects.filter(kod_baka=i[0]).update(
            name=i[1],
            surname=i[2],
            active=not(i[3]),
            rfid="",
        )

def safeq_delete_teachers():
    data = list(Student.objects.raw("""
        SELECT evid_teacher.id,
        evid_teacher.rfid,
        evid_user_account_student.login
        FROM evid_teacher
        INNER JOIN evid_user_account_student
        ON evid_teacher.kod_baka = evid_user_account_student.kod_baka
        WHERE evid_teacher.active = 0
    """))

    for i in data:
        if not i.active:
            connKopirky.execute("DELETE FROM users WHERE login "+i.login)













def run():
    sync_lsum_db()
    create_user_accounts()
    update_user_accounts()
    disable_enable_emails()
    schedule_deletion_of_graduated()
    delete_graduated()
    write_email_changes()


while True:
    print("probiha non root synchronizace, nevypinat skript!")
    timestamp = time()
    run()
    print("synchronizace provedena "+str(asctime()))

    while timestamp + sync_interval > time():
        pass




