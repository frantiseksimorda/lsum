# coding: utf8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lsum.settings")
import django
django.setup()
from evid.models import Student, School_class, User_account_student
from connection import Connection
from misc import stringList
from time import time, asctime
from login_generator import generate_login, generate_password, generate_email



sync_interval = 20
connBaka = Connection("bakalari")



def get_class_id(class_name):
    return School_class.objects.values_list("id").filter(short_name=class_name)[0][0]

def fetch_data():
    priznaky = connBaka.execute("SELECT intern_kod, druh, datum FROM histzaku ORDER BY datum DESC ")
    studenti = connBaka.execute("SELECT intern_kod, jmeno, prijmeni, pohlavi, trida FROM zaci ORDER BY intern_kod")
    school_classes = connBaka.execute("SELECT trida FROM zaci GROUP BY trida")

    school_classes_parsed = stringList(school_classes)

    priznaky_parsed = []

    for i in priznaky:

        if i[0] not in stringList(priznaky_parsed):
            priznaky_parsed.append((i[0], i[1]))

    studenti_parsed = []

    for i in range(0,len(studenti),1):

        if studenti[i][0] not in stringList(priznaky_parsed):
            studenti_parsed.append((studenti[i][0], studenti[i][1], studenti[i][2], studenti[i][3], studenti[i][4], ""))
        else:
            for j in priznaky_parsed:
                if j[0] == studenti[i][0]:
                    studenti_parsed.append((studenti[i][0], studenti[i][1], studenti[i][2], studenti[i][3], studenti[i][4], j[1]))

    return (studenti_parsed, school_classes_parsed)

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
        evid_user_account_student.login,
        evid_user_account_student.default_passwd
        FROM evid_student
        INNER JOIN evid_user_account_student
        ON evid_student.kod_baka = evid_user_account_student.kod_baka
    """))

    for i in data:
        print i.name, i.surname, i.login, i.default_passwd

    #for i in studenti:
    #
    #    if not user_factory.isUnixUser(i.login):
    #        # TODO vytvor uzivatele - funkce od Fandy
    #
    #    if not user_factory.isGoogleUser(i.email):
    #        # TODO vytvor uzivatele na Google

def update_user_accounts():
    pass





def sync_all():

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
            kod_baka=i[0],
            school_class_id=get_class_id(i[4]),
            status=i[5],
        )

    create_user_accounts()
    update_user_accounts()


while True:
    print "probiha synchronizace, nevypinat skript!"
    timestamp = time()
    sync_all()
    print "synchronizace provedena "+str(asctime())

    while timestamp + sync_interval > time():
        pass




