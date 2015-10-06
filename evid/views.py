# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .models import Email_changes, User_account_student, Error_log, Student, School_class
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import *
from misc import stringList, activeBrowser, UnicodeWriter
from django import forms
import subprocess
import csv

def get_class_name(idx):
    return School_class.objects.values_list("short_name").filter(id=idx)[0][0]

def print_papers_students(request):

    data = list(Student.objects.raw("""
                              SELECT * FROM evid_student
                              INNER JOIN evid_user_account_student
                              ON evid_student.kod_baka = evid_user_account_student.kod_baka
                              WHERE evid_student.school_class_id =
                              (SELECT id FROM evid_school_class WHERE short_name = 'R1.A')
                              OR evid_student.school_class_id =
                              (SELECT id FROM evid_school_class WHERE short_name = '1.A')
                              OR evid_student.school_class_id =
                              (SELECT id FROM evid_school_class WHERE short_name = '1.B')
                              OR evid_student.school_class_id =
                              (SELECT id FROM evid_school_class WHERE short_name = '1.C')
                              """))

    while divmod(len(data), 40)[1] != 0:
        data.append("")

    chrome = activeBrowser(request) == "chrome"

    return render(request, "print_papers_students.html", {"elements": data, "chrome": chrome})


def print_paper_one_student(request):

    form = SelectPositionOnPaperForm()

    if request.method == "POST":

        selected = True

        if "submit1" in request.POST:
            form = SelectPositionOnPaperForm(request.POST)

            if form.is_valid():
                student_id = form.cleaned_data["Select"]
                pos = int(form.cleaned_data["Select2"])

                data = []
                for i in range(40):
                    data.append("")

                data[pos-1] = list(Student.objects.raw("""
                              SELECT * FROM evid_student
                              INNER JOIN evid_user_account_student
                              ON evid_student.kod_baka = evid_user_account_student.kod_baka
                              WHERE evid_student.id = '"""+str(student_id)+"""'
                              """))[0]

                chrome = activeBrowser(request) == "chrome"

                return render(request, "print_papers_students.html", {"elements": data, "chrome": chrome})

    else:
        form = SelectPositionOnPaperForm()
        selected = False

    return render(request, 'print_paper_one_student.html',
                  {'form': form,
                   'selected': selected,
                   })


def match_rfids(request):

    count_unmatched = len(Student.objects.filter(rfid=""))
    chrome = activeBrowser(request) == "chrome"

    return render(request, 'match_rfids.html',
                  {'count_unmatched': count_unmatched,
                   'chrome': chrome
                   })


def match_rfids_all(request):

    if request.method == "POST":
        form = RfidScanForm(request.POST)

    else:
        form = RfidScanForm()

    count_unmatched = len(Student.objects.filter(rfid=""))

    if count_unmatched == 0:
                message_color = "#008800"
                message = "Všichni studenti již mají čip přiřazen."

                return render(request, 'match_rfids_all.html',
                  {'form': form,
                   'message': message,
                   'message_color': message_color,
                   })

    active_student = Student.objects.filter(rfid="", to_be_skipped=False)[0]

    if form.is_valid():
        chip = form.cleaned_data["Chip"]

        if chip not in stringList(Student.objects.values_list("rfid")) and chip not in stringList(Teacher.objects.values_list("rfid")):
            Student.objects.filter(kod_baka=active_student.kod_baka).update(rfid=chip)
            message = "Čip úspěšně uložen: "+active_student.name+" "+active_student.surname+" ("+str(active_student.school_class)+")."
            count_unmatched = len(Student.objects.filter(rfid=""))

            if count_unmatched == 0:
                message_color = "#008800"
                message = "Všichni studenti již mají čip přiřazen."

                return render(request, 'match_rfids_all.html',
                  {'form': form,
                   'message': message,
                   'message_color': message_color,
                   })

            active_student = Student.objects.filter(rfid="", to_be_skipped=False)[0]

            message_color = "#008800"
        else:
            try:
                x = Student.objects.filter(rfid=chip)[0]
            except:
                x = Teacher.objects.filter(rfid=chip)[0]
                x.school_class = "ucitel"
            message = "Čip je již zaevidován: "+x.name+" "+x.surname+" ("+str(x.school_class)+"), "+x.kod_baka+". Vyberte jiný."
            message_color = "#FF0000"

        form = RfidScanForm()

    else:
        message = False
        message_color = False

    return render(request, 'match_rfids_all.html',
                  {'form': form,
                   'active_student': active_student,
                   'message': message,
                   'message_color': message_color,
                   'count_unmatched': count_unmatched,
                   })


def match_rfids_one(request):

    owner = False
    scanned = False
    chip = False

    form1 = RfidScanForm()
    form2 = RfidScanForm(request.POST)
    form3 = RfidAssignToAnotherOwnerForm(request.POST)
    form4 = RfidAssignToAnotherTeacherForm(request.POST)

    form2.fields['Chip'].widget = forms.HiddenInput()
    form3.fields['Chip'].widget = forms.HiddenInput()
    form4.fields['Chip'].widget = forms.HiddenInput()

    if request.method == "POST":

        if "submit1" in request.POST:
            form1 = RfidScanForm(request.POST)
            if form1.is_valid():
                chip = form1.cleaned_data["Chip"]
                owner = Student.objects.filter(rfid=chip)
                if len(owner) > 0:
                    owner = owner[0]
                else:
                    owner = Teacher.objects.filter(rfid=chip)
                    if len(owner) > 0:
                        owner = owner[0]
                    else:
                        owner = False

                form1 = RfidScanForm()
                scanned = True

        elif "submit2" in request.POST:
            form2 = RfidScanForm(request.POST)
            form2.fields['Chip'].widget = forms.HiddenInput()

            if form2.is_valid():
                chip = form2.cleaned_data["Chip"]
                Student.objects.filter(rfid=chip).update(rfid="")
                Teacher.objects.filter(rfid=chip).update(rfid="")
                owner = False
                scanned = True

        elif "submit3" in request.POST:
            form3 = RfidAssignToAnotherOwnerForm(request.POST)
            form3.fields['Chip'].widget = forms.HiddenInput()

            if form3.is_valid():
                chip = form3.cleaned_data["Chip"]
                student_id = form3.cleaned_data["Select"]
                Student.objects.filter(rfid=chip).update(rfid="")
                Teacher.objects.filter(rfid=chip).update(rfid="")
                Student.objects.filter(id=student_id).update(rfid=chip)
                owner = Student.objects.filter(rfid=chip)[0]
                scanned = True
            else:
                owner = False
                scanned = False

        elif "submit4" in request.POST:
            form4 = RfidAssignToAnotherTeacherForm(request.POST)
            form4.fields['Chip'].widget = forms.HiddenInput()

            if form4.is_valid():
                chip = form4.cleaned_data["Chip"]
                student_id = form4.cleaned_data["Select"]
                Student.objects.filter(rfid=chip).update(rfid="")
                Teacher.objects.filter(rfid=chip).update(rfid="")
                Teacher.objects.filter(id=student_id).update(rfid=chip)
                owner = Teacher.objects.filter(rfid=chip)[0]
                scanned = True
            else:
                owner = False
                scanned = False

        else:
            owner = False
            scanned = False

    else:
        form1 = RfidScanForm()
        owner = False
        scanned = False

    return render(request, 'match_rfids_one.html',
                  {'form1': form1,
                   'form2': form2,
                   'form3': form3,
                   'form4': form4,
                   'owner': owner,
                   'scanned': scanned,
                   'chip': chip})


def match_rfids_student(request):

    item = False
    message = False

    form1 = RfidSelectStudentForm()
    form2 = RfidRemoveFromStudentForm()
    form3 = RfidAssignSingleScanForm()

    form2.fields['Student_id'].widget = forms.HiddenInput()
    form3.fields['Student_id'].widget = forms.HiddenInput()

    if request.method == "POST":

        scanned = True

        if "submit1" in request.POST:
            form1 = RfidSelectStudentForm(request.POST)

            if form1.is_valid():
                student_id = form1.cleaned_data["Select"]
                item = Student.objects.filter(id=student_id)[0]
                form2.fields["Student_id"].initial = str(student_id)
                form3.fields["Student_id"].initial = str(student_id)

        elif "submit2" in request.POST:
            form2 = RfidRemoveFromStudentForm(request.POST)
            form2.fields['Student_id'].widget = forms.HiddenInput()

            if form2.is_valid():
                student_id = form2.cleaned_data["Student_id"]
                Student.objects.filter(id=student_id).update(rfid="")
                form1.fields["Select"].initial = student_id
                form3.fields["Student_id"].initial = student_id
                item = Student.objects.filter(id=student_id)[0]

        elif "submit3" in request.POST:
            form3 = RfidAssignSingleScanForm(request.POST)
            form3.fields['Student_id'].widget = forms.HiddenInput()

            if form3.is_valid():
                chip = form3.cleaned_data["Chip"]
                student_id = form3.cleaned_data["Student_id"]

                if chip not in stringList(Student.objects.values_list("rfid")) and chip not in stringList(Teacher.objects.values_list("rfid")):
                    Student.objects.filter(id=student_id).update(rfid=chip)
                else:
                    try:
                        x = Student.objects.filter(rfid=chip)[0]
                    except:
                        x = Teacher.objects.filter(rfid=chip)[0]
                        x.school_class = "ucitel"
                    message = "Čip je již zaevidován: "+x.name+" "+x.surname+" ("+str(x.school_class)+"), "+x.kod_baka+". Vyberte jiný."
                    form3 = RfidAssignSingleScanForm()
                    form3.fields["Student_id"].initial = student_id
                    form3.fields['Student_id'].widget = forms.HiddenInput()

                form1.fields["Select"].initial = student_id
                form2.fields["Student_id"].initial = str(student_id)
                item = Student.objects.filter(id=student_id)[0]

    else:
        form1 = RfidSelectStudentForm()
        scanned = False

    return render(request, 'match_rfids_student.html',
                  {'form1': form1,
                   'form2': form2,
                   'form3': form3,
                   'item': item,
                   'scanned': scanned,
                   'message': message,
                   })

def sync_emails(request):
    data = Email_changes.objects.all()

    for i in data:
        name = unicode(i.name).strip()
        surname = unicode(i.surname).strip()
        email = unicode(i.email)
        password = unicode(i.default_passwd)

        if i.action == "create" and email[0] == "x":
            command = "python2 GAM/gam.py create user \""+email+"\" firstname \""+name+"\" lastname \""+surname+"\" password \""+password+"\" changepassword 1 org studenti"
        elif i.action == "create" and email[0] != "x":
            command = "python2 GAM/gam.py create user \""+email+"\" firstname \""+name+"\" lastname \""+surname+"\" password \""+password+"\" changepassword 1 org Kantori"
        elif i.action == "delete":
            command = "python2 GAM/gam.py delete user \""+email+"\""
        elif i.action == "disable":
            command = "python2 GAM/gam.py update user \""+email+"\" suspended on"
        elif i.action == "enable":
            command = "python2 GAM/gam.py update user \""+email+"\" suspended off"

        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if stderr == "":
            if i.action == "create":
                User_account_student.objects.filter(email=i.email).update(email_created=True)
            elif i.action == "delete":
                User_account_student.objects.filter(email=i.email).update(email_created=False)
            elif i.action == "disable":
                User_account_student.objects.filter(email=i.email).update(email_disabled=True)
            elif i.action == "enable":
                User_account_student.objects.filter(email=i.email).update(email_disabled=False)
        else:
            e = Error_log(command=command, stderr=stderr)
            e.save()

        Email_changes.objects.filter(id=i.id).delete()

    return HttpResponseRedirect("/admin/")

def skip_student(request):
    try:
        active_student = Student.objects.filter(rfid="", to_be_skipped=False)[0]
    except:
        Student.objects.filter(rfid="").update(to_be_skipped=False)
        return HttpResponseRedirect("/admin/match_rfids_all/")

    Student.objects.filter(id=active_student.id).update(to_be_skipped=True)

    if False not in stringList(Student.objects.filter(rfid="", to_be_skipped=False).values_list("to_be_skipped")):
        Student.objects.filter(rfid="").update(to_be_skipped=False)

    return HttpResponseRedirect("/admin/match_rfids_all/")

def create_csv(request):
    data = list(Student.objects.raw("""
            SELECT evid_student.id,
            evid_student.name,
            evid_student.surname,
            evid_student.school_class_id,
            evid_student.date_of_birth,
            evid_student.rfid,
            evid_student.status,
            evid_user_account_student.default_passwd,
            evid_user_account_student.login,
            evid_user_account_student.email
            FROM evid_student
            INNER JOIN evid_user_account_student
            ON evid_student.kod_baka = evid_user_account_student.kod_baka
    """))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="temp.csv"'

    spamwriter = UnicodeWriter(response, delimiter=str(","),
                            quotechar=str('|'), quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["jmeno","prijmeni","trida","datum narozeni","cip","status","login","email","heslo"])
    for i in data:
        spamwriter.writerow([i.name.strip(), i.surname.strip(),  unicode(get_class_name(i.school_class_id)), unicode(i.date_of_birth)[:10], i.rfid, i.status, i.login, i.email, i.default_passwd])


    return response

