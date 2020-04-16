=====
TFAT
=====

TFAT is a Django application that provides an interface and API for
tags and tag recovery information. It is built as an installable
application.

Detailed documentation is in the "docs" directory.

Quick start
-----------

0. > pip install tfat.zip

1. Add tfat, django restframework, django_filter, and common and
   to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'myusers'
        'common',
        "leaflet",
        'tfat',
    ]

2. Include the tfat URLconf in your project urls.py like this::

     path("tfat/", include(tfat_urls, namespace="tfat")),

3. Run `python manage.py migrate` to create the tfat models.

4. Visit http://127.0.0.1:8000/tfat 


Updating the Application
------------------------


Rebuilding the App.
------------------------

TFAT was built as a standard applicaiton can be rebuild for
distrubition following the instructions found here:

https://docs.djangoproject.com/en/2.2/intro/reusable-apps/

With the tfat virtualenv active, and from within the
~/django_tfat directory, simply run:

> python setup.py sdist

The package will be placed in the ~/dist folder.  To install the
application run the command:

> pip install tfat.zip

To update an existing application issue the command:

> pip install --upgrade tfat.zip


Running the tests
------------------------

TFAT contains a number of unit tests that verify that the
application works as expected and that any regregressions are caught
early. The package uses pytest to run all of the tests, which can be
run by issuing the command:

> pytest

After the tests have completed, coverage reports can be found here:

~/htmlcov
