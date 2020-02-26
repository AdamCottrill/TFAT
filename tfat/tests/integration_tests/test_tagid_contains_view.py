"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_tagid_contains_view.py
Created: 27 Aug 2015 09:06:04

DESCRIPTION:

The tests in this module verify that the view that renders the
the details associated with a partial tagid render correctly.

This file was modified directly from the tests of tagid_detail_view

A. Cottrill
=============================================================

"""

import pytest
from django.urls import reverse

from tfat.tests.factories import (
    SpeciesFactory,
    ProjectFactory,
    EncounterFactory,
    JoePublicFactory,
    ReportFactory,
    RecoveryFactory,
)


@pytest.fixture()
def db_setup():
    """
    """

    spc1 = SpeciesFactory(species_code="334", common_name="Walleye")
    spc2 = SpeciesFactory(species_code="091", common_name="Whitefish")

    project = ProjectFactory(prj_cd="LHA_IA11_111", prj_nm="Fake Project")

    # same species, same tagdoc - everything is A-Ok.

    encounters = [
        (spc1, "11111", project, "25012"),
        (spc1, "11111", project, "25012"),
        (spc1, "11111", project, "25012"),
        (spc1, "22222", project, "25012"),
        (spc2, "22222", project, "25012"),
        (spc1, "33333", project, "25012"),
        (spc1, "33333", project, "15012"),
    ]

    for item in encounters:
        EncounterFactory(spc=item[0], tagid=item[1], project=item[2], tagdoc=item[3])

    angler1 = JoePublicFactory.create(first_name="Homer", last_name="Simpson")
    # angler report filed by Homer
    report = ReportFactory(reported_by=angler1)
    RecoveryFactory(report=report, spc=spc1, tagid="11111")
    # a recovered tag that has not been observed by the omnr
    RecoveryFactory(report=report, spc=spc1, tagid="654321", tagdoc="25012")


@pytest.mark.django_db
def test_tagid_reported_but_not_observed(client, db_setup):
    """The details page for a tag that has been reported by the general
    public should contain information about the angler recovery but
    will also contain a message indicating the OMNR has not
    observed that tagid.
    """

    tagid = 6543
    url = reverse("tfat:tagid_contains", kwargs={"partial": tagid})
    response = client.get(url)

    content = str(response.content)

    # No UGMLU observations
    msg = "Tags containing \\'{}\\' have not been observed " "in any UGLMU project."
    msg = msg.format(tagid)
    assert msg in content
    assert "UGLMU Encounters (N = 0)" in content

    with open("C:/1work/scrapbook/wtf2.html", "wb") as f:
        f.write(response.content)

    # Reported By:
    assert "Non-MNR Recoveries (N = 1)" in content
    assert "Homer Simpson" in content


@pytest.mark.django_db
def test_tagid_observed_but_not_reported(client, db_setup):
    """The details page for a tag that has been observed by the OMNR but
    not reported by the general public should contain information
    about the OMNR tag encounter but will also contain a message
    indicating the tag has not been reported by the general public.

    """

    tagid = 222
    url = reverse("tfat:tagid_contains", kwargs={"partial": tagid})
    response = client.get(url)

    content = str(response.content)

    # Two UGMLU observations - including project name and project code
    assert "LHA_IA11_111" in content  # omnr project code
    assert "Fake Project" in content  # omnr project name
    assert "UGLMU Encounters (N = 2)" in content

    # No Angler reports
    msg = (
        "There are no reports of tags containing \\'{}\\' from "
        "the general public or other agencies."
    )
    msg = msg.format(tagid)
    assert msg in content
    assert "Non-MNR Recoveries (N = 0)" in content


@pytest.mark.django_db
def test_tagid_not_reported_or_observed(client, db_setup):
    """if we try to access the detail page for a tagid that has not been
    observed by the UGLMU or reported by the general public, the page
    should render but contain appropriate messages.

    """

    tagid = 999
    url = reverse("tfat:tagid_contains", kwargs={"partial": tagid})
    response = client.get(url)

    content = str(response.content)

    assert "'quotes'" in "String with 'quotes'"

    # No UGMLU observations
    msg = "Tags containing \\'{}\\' have not been observed " "in any UGLMU project."
    msg = msg.format(tagid)

    assert msg in content
    assert "UGLMU Encounters (N = 0)" in content

    # No Angler reports
    msg = (
        "There are no reports of tags containing \\'{}\\' from "
        "the general public or other agencies."
    )
    msg = msg.format(tagid)
    assert msg in content
    assert "Non-MNR Recoveries (N = 0)" in content


@pytest.mark.django_db
def test_tagid_contains_includes_encounters_and_angler_recaps(client, db_setup):
    """The tagid contains page should include encounter events from both
    the MNR and any angler returns.

    Arguments:
    - `client`:
    - `db_setup`:

    """
    url = reverse("tfat:tagid_contains", kwargs={"partial": "111"})

    response = client.get(url)
    content = str(response.content)

    assert "Homer Simpson" in content  # angler return record
    assert "LHA_IA11_111" in content  # omnr project code
    assert "Fake Project" in content  # omnr project name


@pytest.mark.django_db
def test_tagid_contains_includes_nobs_with_angler_recaps(client, db_setup):

    """The tagid contains page should include the string N = {nobs} that
    correctly indicates the number of times this tags matching <partial>
    have been observed including both OMNR encounters and angler
    recaptures.

    Arguments:
    - `client`:
    - `db_setup`:

    """
    url = reverse("tfat:tagid_contains", kwargs={"partial": "111"})

    response = client.get(url)
    content = str(response.content)

    assert "N = 4" in content


@pytest.mark.django_db
def test_tagid_detail_includes_nobs_without_angler_recaps(client, db_setup):
    """The tagid details page should include the string 'N = {nobs}' that
    correctly indicates the number of times this tag number has been
    observed - even if it has not been reported by any anglers.

    Arguments:
    - `client`:
    - `db_setup`:

    """
    url = reverse("tfat:tagid_contains", kwargs={"partial": "222"})

    response = client.get(url)
    content = str(response.content)

    assert "N = 2" in content
