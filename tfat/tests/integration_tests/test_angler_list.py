'''=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_angler_list.py
Created: 26 Jun 2015 11:34:21


DESCRIPTION:

This test script ensurs that that the angler list renderes properly
and that the option to add a new person is provided if a person
matching the filter criteris is not found.

A. Cottrill
=============================================================

'''


import pytest
from django.core.urlresolvers import reverse

from tfat.tests.factories import *

from datetime import datetime


@pytest.fixture(scope='class')
def db_setup():
    """Create some users with easy to remember names.
    """

    angler1 = JoePublicFactory.create(first_name='Homer',
                                      last_name='Simpson')

    angler2 = JoePublicFactory.create(first_name='Montgomery',
                                      last_name='Burns')

    angler3 = JoePublicFactory.create(first_name='Barney',
                                      last_name='Gumble')


@pytest.mark.django_db
def test_angler_list(client, db_setup):
    """The default angler list should include a list of all anlgers in the
    database.

    """

    url = reverse('angler_list')
    response = client.get(url)
    content = str(response.content)

    assert 'Homer Simpson' in content
    assert 'Montgomery Burns' in content
    assert 'Barney Gumble' in content
    assert 'George Costansa' not in content

    #These should not appear in the response if people are returned
    assert 'Sorry no people match that criteria' not in content
    assert 'Add New Person' not in content


@pytest.mark.django_db
def test_angler_list_filter_first_name(client, db_setup):
    """Verify that the filter works if we provide a partial first name
    """

    url = reverse('angler_list')
    response = client.get(url + '?first_name=home')
    content = str(response.content)

    assert 'Homer Simpson' in content
    assert 'Montgomery Burns' not in content
    assert 'Barney Gumble' not in content
    assert 'George Costansa' not in content

    #These should not appear in the response if people are returned
    assert 'Sorry no people match that criteria' not in content
    assert 'Add New Person' in content


@pytest.mark.django_db
def test_angler_list_filter_last_name(client, db_setup):
    """Verify that the filter works if we provide a partial last name

    """

    url = reverse('angler_list')
    response = client.get(url + '?last_name=impson')
    content = str(response.content)

    assert 'Homer Simpson' in content
    assert 'Montgomery Burns' not in content
    assert 'Barney Gumble' not in content
    assert 'George Costansa' not in content

    #These should not appear in the response if people are returned
    assert 'Sorry no people match that criteria' not in content
    assert 'Add New Person' in content


@pytest.mark.django_db
def test_angler_not_in_angler_list(client, db_setup):
    """If an angler who is not in the data base is queried, the response
    should indicate that no people matching that criteria could be
    found and provide an option to add a new person.

    """

    url = reverse('angler_list')
    response = client.get(url + '?last_name=costanza')
    content = str(response.content)

    #what should not be there
    assert 'Homer Simpson' not in content
    assert 'Montgomery Burns' not in content
    assert 'Barney Gumble' not in content
    assert 'George Costansa' not in content

    #what should be there:
    assert 'Sorry no people match that criteria' in content
    assert 'Add New Person' in content
