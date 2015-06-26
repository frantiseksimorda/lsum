# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from evid.models import Student, School_class, User_account_student
from connection import Connection
from misc import stringList
from random import randint
from hashlib import sha512
from unicodedata import normalize


def baka_sync(request):
    """ Sync users with Bakalari MSSQL database, add new studenst from new classes"""
    # connection and query to the source database
    conn = Connection("bakalari")
    data = conn.execute("SELECT trida FROM zaci")

    # selecting each class, appending it only once
    classes = []

    for line in data:
        if line[0] not in classes:
            classes.append(line[0])

    # editing the list to look nicer :)
    classes.sort()
    classes.reverse()

    # parsing classes to the correct format for insertion
    existing_classes = School_class.objects.values_list("short_name")
    existing_classes_parsed = []

    for item in existing_classes:
        existing_classes_parsed.append(item[0])

    # inserting to the school_class table of the Django DB
    for item in classes:
        if item not in existing_classes_parsed:
            school_class = School_class(short_name=item)
            school_class.save()

    def get_class_id(class_name):

        return School_class.objects.values_list("id").filter(short_name=class_name)[0][0]


    conn = Connection("bakalari")
    data = conn.execute("SELECT jmeno, prijmeni, pohlavi, intern_kod, trida, isic_cip FROM zaci")


    existing_codes = Student.objects.values_list("kod_baka")
    existing_codes_parsed = []

    for item in existing_codes:
        existing_codes_parsed.append(item[0])


    for line in data:

        if line[3] not in existing_codes_parsed:

            student = Student(
                name=line[0],
                surname=line[1],
                sex=line[2],
                kod_baka=line[3],
                school_class_id=get_class_id(line[4]),
                rfid=line[5],
                # active=True,
            )

            student.save()

    return HttpResponseRedirect("/admin/evid/student")


def maturanti_lock(request):
    """ lock users logins of thoses, who sucessfully end school"""
    return request


def generate_logins(request):
    """ after sync with bakalari (imported new users), generate new usernames and password for new classes """

    baka_codes = stringList(Student.objects.values_list("kod_baka"))
    login_codes = stringList(User_account_student.objects.values_list("kod_baka"))
    existing_logins = stringList(User_account_student.objects.values_list("login"))


    def shorten(x, length):
        # first chars of string x, normalized, lowercase; if shorter than 3, automatically extended by xs from the right
        x = x[:3].rstrip()
        x = normalize('NFKD', x).encode('ascii', 'ignore')
        x = x.lower()

        while len(x) < 3:
            x += "x"

        return x


    def generate_login(name, surname):

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


    # write user accounts into DB
    for code in baka_codes:
        if code not in login_codes:

            # get name and surname of the student and generate username and password
            surname = Student.objects.values_list("surname").filter(kod_baka=code)[0][0]
            name = Student.objects.values_list("name").filter(kod_baka=code)[0][0]

            login = generate_login(name, surname)
            password = generate_password()

            # generate email
            email = login + "@gjk.cz"

            account = User_account_student(
                kod_baka=code,
                login=login,
                default_passwd=password,
                email=email,
            )

            account.save()
            existing_logins.append(login)

    return HttpResponseRedirect("/admin/evid/user_account_student/")