# lsum
Sprava unix useru a Sync s Bakaláři, SafeQ a Vstupní systém

# Installation
- Install `python2` package
- Install `python2-django` package
- Install `git` package
- Install `pip2` prackage
- Clone the repository (via `git clone https://github.com/frantiseksimorda/lsum`)
- Execute `pip2 install argument`, replacing the `argument` with the following:
  -  `pymssql`
  -  `python2-psycopg2`
  -  `django-import-export`
  -  `django-overextends`
- Replace your `python27/site-packages/overextends/templatetags/overextends_tags.py` with [this file](https://github.com/stephenmcd/django-overextends/blob/master/overextends/templatetags/overextends_tags.py)
- Execute `python2 manage.py runserver`
- Open your browser at `http://localhost:8000/admin`
