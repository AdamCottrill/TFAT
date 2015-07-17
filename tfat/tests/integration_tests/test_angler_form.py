'''=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_angler_form.py
Created: 17 Jul 2015 13:28:23

DESCRIPTION:

This script contain the integration tests that verify the angler form
works as expected for creating new and editing existing
anglers/tag-returnees.

- first_name and last_name are the only two required fields
- adding a new, unique angler is straight forward
- editing an existing angler is straight forward
- if a new angler is created with same first and last names as an
  existing angler, a warning should be produced.
- new users with the same first and last name can only be created if
  the 'same_name' check box is true when the form is re-submitted.


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


def test_can_create_angler_url(client):
    """Verify that the form and its correct elements are rendered when we
    call the create_angler form"""

    url = reverse('create_angler')
    response = client.get(url)
    assert response.status_code == 200
    content = str(response.content)

    assert 'Create New Tag Reporter' in content
    assert 'First name:' in content
    assert 'Last name:' in content
    assert 'Town:' in content
    assert 'Submit' in content

    assert 'Use Duplicate Name Anyway' not in content
    assert 'Existing Anglers:' not in content
    assert 'Edit Details' not in content


@pytest.mark.django_db
def test_can_create_angler(client, db_setup):
    """if we pass in a dictionary with valid angler information, a new angler
    should be created.
    """
    angler = {'first_name':'Barney', 'last_name':'Gumble', 'same_name':False}

    url = reverse('create_angler')
    response = client.post(url, angler, follow=True)
    content = str(response.content)

    assert 'Tag Reports Filed By Barney Gumble' in content
    assert 'Angler Details' in content


@pytest.mark.django_db
def test_create_angler_same_name_warning(client, db_setup):
    """If we try to create a angler who has the same first and last name
    as an existing angler, we should get a warning about it and the
    check box to force a duplicate should be visible and a list of
    anglers with the same name should be included in the response.

    """

    angler = {'first_name':'Homer', 'last_name':'Simpson', 'same_name':False}

    url = reverse('create_angler')
    response = client.post(url, angler)
    content = str(response.content)

    assert 'Homer Simpson already exists.' in content
    assert 'Existing Anglers:' in content
    assert 'Use Duplicate Name Anyway' in content
    assert 'Create New Angler' in content


@pytest.mark.django_db
def test_create_angler_same_name_without_checkbox(client, db_setup):
    """if we try to post a new angler with the same name as an existing
    angler, but do not have 'same_name' checked, the form should not be
    saved and a meaningful error message generated.

    """
    angler = {'first_name':'Homer', 'last_name':'Simpson', 'same_name':False}

    url = reverse('create_angler')
    response = client.post(url, angler, follow=True)
    content = str(response.content)

    assert 'Homer Simpson already exists.' in content
    assert 'Existing Anglers:' in content
    assert 'Use Duplicate Name Anyway' in content
    assert 'Create New Angler' in content


@pytest.mark.django_db
def test_create_angler_same_name_with_checkbox(client, db_setup):
    """if we try to post a new angler with the same name as an existing
    angler and have 'same_name' checked, the form should be saved and
    the we should be re-directed to the summary page for that angler.
    """
    angler = {'first_name':'Homer', 'last_name':'Simpson', 'same_name':True}

    url = reverse('create_angler')
    response = client.post(url, angler, follow=True)
    content = str(response.content)

    assert 'Tag Reports Filed By Homer Simpson' in content
    assert 'Angler Details' in content



@pytest.mark.django_db
def test_can_edit_angler_url(client, db_setup):
    """Verify that the form and its correct elements are rendered when we
    call the update_angler form and that the response includes the
    expected data for this angler.

    """
    angler = JoePublic.objects.get(first_name='Homer')
    url = reverse('update_angler', kwargs={'angler_id':angler.id})
    response = client.get(url)
    assert response.status_code == 200
    content = str(response.content)

    assert 'Edit Tag Reporter' in content
    assert 'First name:' in content
    assert 'Last name:' in content
    assert 'Town:' in content
    assert 'Submit' in content
    #and the data element
    assert 'Homer' in content
    assert 'Simpson' in content
    assert 'Springfield' in content

    #some things in the template that should not be in this response:
    assert 'Use Duplicate Name Anyway' not in content
    assert 'Existing Anglers:' not in content
    assert 'Edit Details' not in content


@pytest.mark.django_db
def test_can_edit_angler(client, db_setup):
    """verify that we can edit the information associated with a angler
    using the form
    """
    new_data = {'first_name':'Homer', 'last_name':'Simpson', 'same_name':False,
                'town':'Vancouver', 'initial':'X', 'address1':'123 Newplace' }

    angler = JoePublic.objects.get(first_name='Homer')
    url = reverse('update_angler', kwargs={'angler_id':angler.id})
    response = client.post(url, new_data, follow=True)
    content = str(response.content)

    assert 'Tag Reports Filed By Homer X. Simpson' in content
    assert 'Angler Details' in content
    assert 'Vancouver' in content
    assert '123 Newplace' in content

    #check the angler attributes from the database
    angler = JoePublic.objects.get(first_name='Homer')
    assert angler.address1 == '123 Newplace'
    assert angler.town == 'Vancouver'
    assert angler.initial == 'X'



@pytest.mark.django_db
def test_create_angler_first_name_required(client, db_setup):
    """first_name is a required field for the create_angler form.  If we
    try to sumbit an angler without a user, the form should throw a
    meaningful error message.

    """
    angler = {'last_name':'Gumble', 'same_name':False}

    url = reverse('create_angler')
    response = client.post(url, angler, follow=True)
    content = str(response.content)

    assert 'This field is required' in content



@pytest.mark.django_db
def test_create_angler_last_name_required(client, db_setup):
    """last_name is a required field for the create_angler form.  If we
    try to sumbit an angler without a user, the form should throw a
    meaningful error message.

    """
    angler = {'first_name':'Barney', 'same_name':False}

    url = reverse('create_angler')
    response = client.post(url, angler, follow=True)
    content = str(response.content)

    assert 'This field is required' in content


@pytest.mark.django_db
def test_edit_angler_first_name_required(client, db_setup):
    """first_name is a required field for the create_angler form.  If we
    try to sumbit an angler without a user, the form should throw a
    meaningful error message.

    """
    new_data = {'first_name':'', 'last_name':'Simpson', 'same_name':False}

    angler = JoePublic.objects.get(first_name='Homer')
    url = reverse('update_angler', kwargs={'angler_id':angler.id})
    response = client.post(url, new_data, follow=True)
    content = str(response.content)

    assert 'This field is required' in content


@pytest.mark.django_db
def test_edit_angler_last_name_required(client, db_setup):
    """last_name is a required field for the create_angler form.  If we
    try to sumbit an angler without a user, the form should throw a
    meaningful error message.

    """
    new_data = {'first_name':'Homer', 'last_name':'', 'same_name':False}

    angler = JoePublic.objects.get(first_name='Homer')
    url = reverse('update_angler', kwargs={'angler_id':angler.id})
    response = client.post(url, new_data, follow=True)
    content = str(response.content)

    assert 'This field is required' in content

@pytest.mark.django_db
def test_nonexistant_angler_get_request(client, db_setup):
    """If we try to edit/view the form for angler who does not exists we
    should get a 404.

    """

    url = reverse('update_angler', kwargs={'angler_id':999999})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_nonexistant_angler_post_request(client, db_setup):
    """If we try to submit the form for angler who does not exists we
    should get a 404.

    """
    new_data = {'first_name':'Montey', 'last_name':'Burns', 'same_name':False}

    url = reverse('update_angler', kwargs={'angler_id':999999})
    response = client.post(url, new_data, follow=True)

    assert response.status_code == 404
