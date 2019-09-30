"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_report_a_tag.py
Created: 30 May 2016 11:21:17

DESCRIPTION:

This test script ensures that the angler list renders properly
with instructions when the report_a_tag is True.

When report_a_tag is true the heading should say:

'Find or Create Person or Organization'

and the filter box should be visible (this is a java script function
that we can't test here.)





A. Cottrill
=============================================================

"""


import pytest
from django.core.urlresolvers import reverse

from tfat.tests.factories import *

# from datetime import datetime


@pytest.fixture()
def db_setup():
    """Create some users with easy to remember names.
    """

    angler1 = JoePublicFactory.create(first_name="Homer", last_name="Simpson")

    angler2 = JoePublicFactory.create(first_name="Montgomery", last_name="Burns")

    angler3 = JoePublicFactory.create(first_name="Barney", last_name="Gumble")


@pytest.mark.django_db
def test_report_a_tag(client, db_setup):
    """When we follow report_a_tag url the response should contain the string:
    'Step 1 - Find or Create the Person or Organization'

    """

    url = reverse("tfat:report_a_tag_angler_list")
    response = client.get(url)
    content = str(response.content)

    assert "Step 1 - Find or Create the Person or Organization" in content

    assert "Homer Simpson" in content
    assert "Montgomery Burns" in content
    assert "Barney Gumble" in content
    assert "George Costansa" not in content

    # These should not appear in the response if people are returned
    assert "Sorry no people match that criteria" not in content
    assert "Add New Person" not in content
