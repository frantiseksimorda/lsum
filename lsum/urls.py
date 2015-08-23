# -*- coding: utf-8 -*-
"""lsum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/print_papers_students/$', 'evid.views.print_papers_students'),
    url(r'^admin/print_paper_one_student/$', 'evid.views.print_paper_one_student'),
    url(r'^admin/match_rfids/$', 'evid.views.match_rfids'),
    url(r'^admin/match_rfids_all/$', 'evid.views.match_rfids_all'),
    url(r'^admin/match_rfids_one/$', 'evid.views.match_rfids_one'),
    url(r'^admin/match_rfids_student/$', 'evid.views.match_rfids_student'),
    url(r'^sync_emails/$', 'evid.views.sync_emails', name="sync_emails"),
]
