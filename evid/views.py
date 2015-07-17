# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .models import Student
from django.shortcuts import render
from .forms import RfidScanForm, RfidAssignToAnotherOwnerForm, RfidSelectStudentForm, RfidRemoveFromStudentForm, RfidAssignSingleScanForm
from misc import stringList
from django import forms
from user_agents import parse


def print_papers_students(request):

    data = list(Student.objects.raw("""
                              SELECT * FROM evid_student
                              INNER JOIN evid_user_account_student
                              ON evid_student.kod_baka = evid_user_account_student.kod_baka
                        """))

    while divmod(len(data), 40)[1] != 0:
        data.append("")

    return render(request, "print_papers_students.html", {"elements": data})


def match_rfids(request):

    count_unmatched = len(Student.objects.filter(rfid=""))

    meta = parse(request.META['HTTP_USER_AGENT'])
    chrome = (meta.browser.family).lower() == "chrome"


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

    active_student = Student.objects.filter(rfid="")[0]

    if form.is_valid():
        chip = form.cleaned_data["Chip"]

        if chip not in stringList(Student.objects.values_list("rfid")):
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

            active_student = Student.objects.filter(rfid="")[0]

            message_color = "#008800"
        else:
            x = Student.objects.filter(rfid=chip)[0]
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

    form2.fields['Chip'].widget = forms.HiddenInput()
    form3.fields['Chip'].widget = forms.HiddenInput()

    if request.method == "POST":

        if "submit1" in request.POST:
            form1 = RfidScanForm(request.POST)
            if form1.is_valid():
                chip = form1.cleaned_data["Chip"]
                owner = Student.objects.filter(rfid=chip)
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
                owner = False
                scanned = True

        elif "submit3" in request.POST:
            form3 = RfidAssignToAnotherOwnerForm(request.POST)
            form3.fields['Chip'].widget = forms.HiddenInput()

            if form3.is_valid():
                chip = form3.cleaned_data["Chip"]
                student_id = form3.cleaned_data["Select"]
                Student.objects.filter(rfid=chip).update(rfid="")
                Student.objects.filter(id=student_id).update(rfid=chip)
                owner = Student.objects.filter(rfid=chip)[0]
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

                if chip not in stringList(Student.objects.values_list("rfid")):
                    Student.objects.filter(id=student_id).update(rfid=chip)
                else:
                    x = Student.objects.filter(rfid=chip)[0]
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