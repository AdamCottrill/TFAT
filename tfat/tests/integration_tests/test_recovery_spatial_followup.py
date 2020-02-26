"""=============================================================
~/tfat/tfat/tests/integration_tests/test_recovery_spatial_followup.py
Created: 02 Jun 2016 15:23:34

DESCRIPTION:

The tests in this module verify that the view that renders the list of
tag recoveries that require spatial follow-up renders as expected.

A. Cottrill
=============================================================

"""

import pytest
import pytz
from django.urls import reverse


from tfat.models import Recovery
from tfat.tests.factories import (
    UserFactory,
    JoePublicFactory,
    SpeciesFactory,
    ReportFactory,
    RecoveryFactory,
)


from datetime import datetime


@pytest.fixture()
def user():
    """
    """
    user = UserFactory(email="mickey@disney.com")
    user.set_password("Abcd1234")
    user.save()

    return user


@pytest.fixture()
def species():
    spc = SpeciesFactory(common_name="Lake Trout")
    return spc


@pytest.fixture()
def angler():
    angler = JoePublicFactory.create(first_name="Homer", last_name="Simpson")
    return angler


@pytest.fixture()
def db_setup(species, angler):
    """

    Arguments:
    - `db`:
    """

    report_date = datetime(2010, 10, 10).replace(tzinfo=pytz.UTC)

    # report filed by Homer
    report = ReportFactory(reported_by=angler, report_date=report_date)
    tagids = ["111111", "222222", "333333"]
    for tag in tagids:
        recovery = RecoveryFactory(
            report=report,
            spc=species,
            tagid=tag,
            general_location="Over There",
            specific_location="Right There",
        )


@pytest.mark.django_db
def test_recovery_spatial_follup_url(client, db_setup):
    """verify that the list of recovereries requiring spatial followup
    renders properly (status code=200), uses the correct template and
    includes the appropriate title.

    """

    response = client.get(reverse("tfat:spatial_followup"))
    assert response.status_code == 200
    content = str(response.content)

    template_name = "tfat/spatial_followup_list.html"
    assert template_name in [x.name for x in response.templates]

    assert "Tag Recoveries Requiring Spatial Follow-up" in content


@pytest.mark.django_db
def test_recovery_spatial_followup_empty(client, db_setup):
    """If there aren't any recoveries that need follow-up, the response
    should include a meaningful message.

    """

    response = client.get(reverse("tfat:spatial_followup"))
    content = str(response.content)

    msg = (
        "There are currently no tags requiring spatial follow-up." + " Congratulations!"
    )
    assert msg in content


@pytest.mark.django_db
def test_recovery_spatial_followup(client, db_setup):
    """If there are some recoveries that need follow-up, the response
    should include a table containing the tag number, species, general
    location and specific location associated with those tags.

    """

    # update one of the records so that spatial follow-up is required.
    recovery = Recovery.objects.get(tagid="111111")
    recovery.spatial_followup = True
    recovery.save()

    response = client.get(reverse("tfat:spatial_followup"))
    content = str(response.content)

    msg = (
        "There are currently no tags requiring spatial follow-up." + " Congratulations!"
    )
    assert msg not in content

    # check fo table headings
    assert "Tag Number" in content
    assert "General Location" in content
    assert "Specific Location" in content
    assert "Species" in content

    # check for tag details
    assert "111111" in content
    assert "Over There" in content
    assert "Right There" in content
    assert "Lake Trout" in content

    # check for recovery detail url:
    url = reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    assert url in content
