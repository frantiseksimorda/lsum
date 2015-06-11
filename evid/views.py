# -*- coding: utf-8 -*-
# from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Document
from .forms import DocumentForm

def importcsv(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('importcsv'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'import_template.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

def baka_sync(request):
    """ Sync users with Bakalari MSSQL database, add new studenst from new classes"""
    return request


def maturanti_lock(request):
    """ lock users logins of thoses, who sucessfully end school"""
    return request


def generate_logins(request):
    """ after sync with bakalari (imported new users), generate new usernames and password for new classes """
    return request