# -*- coding: utf-8 -*-
# from django.shortcuts import render
from .models import Student
from django.shortcuts import render_to_response

def print_papers_students(request):

    data = list(Student.objects.raw("""
                              SELECT * FROM evid_student
                              INNER JOIN evid_user_account_student
                              ON evid_student.kod_baka = evid_user_account_student.kod_baka
                        """))

    while divmod(len(data), 40)[1] != 0:
        data.append("")

    return render_to_response("print_papers_students.html", {"elements": data})


def match_rfids(request):

    return render_to_response("match_rfids.html", {})