"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_angler_list.py
Created: 26 Jun 2015 11:34:21


DESCRIPTION:

This test script ensurs that that the angler list renderes properly
and that the option to add a new person is provided if a person
matching the filter criteris is not found.

A. Cottrill
=============================================================

"""


import pytest
from django.urls import reverse

from tfat.tests.factories import JoePublicFactory, UserFactory


@pytest.fixture()
def user():
    """Create a user we can login to some views:
    """

    user = UserFactory(email="mickey@disney.com")
    user.set_password("Abcd1234")
    user.save()

    return user


@pytest.fixture()
def anglers():
    """Create some users with easy to remember names.
    """

    angler1 = JoePublicFactory(first_name="Homer", last_name="Simpson")
    angler2 = JoePublicFactory(first_name="Montgomery", last_name="Burns")
    angler3 = JoePublicFactory(first_name="Barney", last_name="Gumble")


@pytest.mark.django_db
def test_angler_list(client, anglers):
    """The default angler list should include a list of all anlgers in the
    database.

    The link to add a new angler should not appear until a filter has
    been applied and we can be reasonably sure that this person is not
    already there.

    """

    url = reverse("tfat:angler_list")
    response = client.get(url)
    content = str(response.content)

    assert "Homer Simpson" in content
    assert "Montgomery Burns" in content
    assert "Barney Gumble" in content
    assert "George Costansa" not in content

    # These should not appear in the response if people are returned
    assert "Sorry no people match that criteria" not in content
    assert "Add New Person" not in content


@pytest.mark.django_db
def test_angler_list_filter_first_name(client, anglers):
    """Verify that the filter works if we provide a partial first name
    """

    url = reverse("tfat:angler_list")
    response = client.get(url + "?first_name=home")
    content = str(response.content)

    assert "Homer Simpson" in content
    assert "Montgomery Burns" not in content
    assert "Barney Gumble" not in content
    assert "George Costansa" not in content

    # These should not appear in the response if people are returned
    assert "Sorry no people match that criteria" not in content
    assert "Add New Person" in content


@pytest.mark.django_db
def test_add_new_person_link(client, anglers):
    """when we apply a filter, the Add New Person should be the content
    and it should point to the create_angler url not the
    report_a_tag_new_angler url.

    """

    url = reverse("tfat:angler_list")
    response = client.get(url + "?first_name=home")
    content = str(response.content)

    assert "Add New Person" in content
    url = reverse("tfat:create_angler")
    assert url in content

    url = reverse("tfat:report_a_tag_new_angler")
    assert url not in content


@pytest.mark.django_db
def test_add_new_person_report_a_tag_link_logged_in(client, user, anglers):
    """when we apply a filter to the report_a_tag link, the string "Add
    New Person" should be the content and it should point to
    report_a_tag_new_angler url not the url for create_angler if the
    user is logged in.

    """

    url = reverse("tfat:report_a_tag_angler_list")
    client.login(username=user.email, password="Abcd1234")
    response = client.get(url + "?first_name=home")
    content = str(response.content)

    assert "Add New Person" in content
    url = reverse("tfat:create_angler")
    assert url not in content

    url = reverse("tfat:report_a_tag_new_angler")
    assert url in content


@pytest.mark.django_db
def test_no_add_new_person_report_a_tag_link(client, anglers):
    """The "Add a New" person button and url shold not be in the view if it
    is accessed by a anonymous user.

    """

    url = reverse("tfat:report_a_tag_angler_list")
    response = client.get(url + "?first_name=home")
    content = str(response.content)

    assert "Add New Person" not in content
    url = reverse("tfat:create_angler")
    assert url not in content

    url = reverse("tfat:report_a_tag_new_angler")
    assert url not in content


@pytest.mark.django_db
def test_report_a_tag_no_match(client, user, anglers):
    """If we apply a filter that that does not match any existing anglers
    and we are accessing the report-a-tag urls, a message explaining what
    do do next should be included in the response
    """

    url = reverse("tfat:report_a_tag_angler_list")
    client.login(username=user.email, password="Abcd1234")
    response = client.get(url + "?first_name=nomatch")
    content = str(response.content)

    msg = (
        "Sorry no people match that criteria. Please add their "
        + "contact information to continue."
    )
    assert msg in content


@pytest.mark.django_db
def test_angler_list_filter_last_name(client, anglers):
    """Verify that the filter works if we provide a partial last name

    """

    url = reverse("tfat:angler_list")
    response = client.get(url + "?last_name=impson")
    content = str(response.content)

    assert "Homer Simpson" in content
    assert "Add New Person" in content

    assert "Montgomery Burns" not in content
    assert "Barney Gumble" not in content
    assert "George Costansa" not in content

    # These should not appear in the response if people are returned
    assert "Sorry no people match that criteria" not in content


@pytest.mark.django_db
def test_angler_not_in_angler_list(client, anglers):
    """If an angler who is not in the data base is queried, the response
    should indicate that no people matching that criteria could be
    found and provide an option to add a new person.

    """

    url = reverse("tfat:angler_list")
    response = client.get(url + "?last_name=costanza")
    content = str(response.content)

    # what should not be there
    assert "Homer Simpson" not in content
    assert "Montgomery Burns" not in content
    assert "Barney Gumble" not in content
    assert "George Costansa" not in content

    # what should be there:
    assert "Sorry no people match that criteria" in content
    assert "Add New Person" in content
