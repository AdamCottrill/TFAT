"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_tagid_detail_view.py
Created: 19 Jun 2015 10:07:24

DESCRIPTION:

The tests in this module verify that the view that renders the
the details associated with a particular tag render correctly.

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

    species1 = SpeciesFactory(spc="334", spc_nmco="Walleye")
    species2 = SpeciesFactory(spc="091", spc_nmco="Whitefish")

    project = ProjectFactory(prj_cd="LHA_IA11_111", prj_nm="Fake Project")

    encounters = [
        (species1, "11111", project, "25012"),
        (species1, "11111", project, "25012"),
        (species1, "11111", project, "25012"),
        (species1, "22222", project, "25012"),
        (species2, "22222", project, "25012"),
        (species1, "33333", project, "25012"),
        (species1, "33333", project, "15012"),
    ]

    for item in encounters:
        EncounterFactory(
            species=item[0], tagid=item[1], project=item[2], tagdoc=item[3]
        )

    angler1 = JoePublicFactory.create(first_name="Homer", last_name="Simpson")
    # angler report filed by Homer
    report = ReportFactory(reported_by=angler1)
    RecoveryFactory(report=report, species=species1, tagid="11111")
    # a recovered tag that has not been observed by the omnr
    RecoveryFactory(report=report, species=species1, tagid="654321")


@pytest.mark.django_db
def test_tagid_details_includes_encounters_and_angler_recaps(client, db_setup):
    """The tagid details page should include encounter events from both
    the MNR and any angler returns.

    Arguments:
    - `client`:
    - `db_setup`:

    """
    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": "11111"})

    response = client.get(url)
    content = str(response.content)

    assert "Homer Simpson" in content  # angler return record
    assert "LHA_IA11_111" in content  # omnr project code
    assert "Fake Project" in content  # omnr project name


@pytest.mark.django_db
def test_tagid_details_includes_nobs_with_anlger_recaps(client, db_setup):
    """The tagid details page should include the string 'N = {nobs}' that
    correctly indicates the number of times this tag number has been
    observed including both OMNR encounters and angler recaptures.

    Arguments:
    - `client`:
    - `db_setup`:

    """
    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": "11111"})

    response = client.get(url)
    content = str(response.content)

    assert "N = 4" in content


@pytest.mark.django_db
def test_tagid_detail_includes_nobs_without_anlger_recaps(client, db_setup):
    """The tagid detail page should include the string 'N = {nobs}' that
    correctly indicates the number of times this tag number has been
    observed even without any angler recaps.

    Arguments:
    - `client`:
    - `db_setup`:

    """
    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": "22222"})

    response = client.get(url)
    content = str(response.content)

    assert "N = 2" in content


@pytest.mark.django_db
def test_tagid_reported_but_not_observed(client, db_setup):
    """The details page for a tag that has been reported by the general
    public should contain information about the angler recovery but
    will also contain a message indicating the OMNR has not
    observed that tagid.
    """

    tagid = 654321
    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": tagid})
    response = client.get(url)

    content = str(response.content)

    # No UGMLU observations
    msg = "{} has not been observed in any UGLMU project."
    assert msg.format(tagid) in content
    assert "UGLMU Encounters (N = 0)" in content

    # Reported By:
    assert "Homer Simpson" in content
    assert "Non-MNR Recoveries (N = 1)" in content


@pytest.mark.django_db
def test_tagid_observed_but_not_reported(client, db_setup):
    """The details page for a tag that has been observed by the OMNR but
    not reported by the general public should contain information
    about the OMNR tag encounter but will also contain a message
    indicating the tag has not been reported by the general public.

    """

    tagid = 22222
    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": tagid})
    response = client.get(url)

    content = str(response.content)

    # Two UGMLU observations - including project name and project code
    assert "LHA_IA11_111" in content  # omnr project code
    assert "Fake Project" in content  # omnr project name
    assert "UGLMU Encounters (N = 2)" in content

    # No Angler reports
    msg = "There are no reports of tag {} from the general" " public or other agencies"
    assert msg.format(tagid) in content
    assert "Non-MNR Recoveries (N = 0)" in content


@pytest.mark.django_db
def test_tagid_does_not_exist(client, db_setup):
    """if we try to access the detail page for a tagid that has not been
    observed by the UGLMU or the general public, the page should render
    but contain appropriate messages.
    """

    tagid = 9999
    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": tagid})
    response = client.get(url)

    content = str(response.content)

    # No UGMLU observations
    msg = "{} has not been observed in any UGLMU project."
    assert msg.format(tagid) in content
    assert "UGLMU Encounters (N = 0)" in content

    # No Angler reports
    msg = "There are no reports of tag {} from the general" " public or other agencies"
    assert msg.format(tagid) in content
    assert "Non-MNR Recoveries (N = 0)" in content


# ====================
#  WARNING MESSAGES
# ====================


@pytest.mark.django_db
def test_multiple_species_warning(client, db_setup):
    """If there is more than one species associated with a tag, a warning
    should be included in the repsonse.
    """

    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": "33333"})
    response = client.get(url)
    content = str(response.content)

    msg = (
        "There appears to be more than one tagdoc code associated "
        "with the records on this page. Interpret with caution."
    )

    assert msg in content


@pytest.mark.django_db
def test_multiple_species_warning_ok(client, db_setup):
    """As long as all of the species associated with a tag are the same,
    the warning should not appear in the reponse.

    """

    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": "11111"})
    response = client.get(url)
    content = str(response.content)

    msg = (
        "There appears to be more than one tagdoc code associated "
        "with the records on this page. Interpret with caution."
    )

    assert msg not in content


@pytest.mark.django_db
def test_multiple_tagdoc_warning(client, db_setup):
    """If there is more than one tagdoc associated with a tag, a warning
    should be included in the repsonse.
    """

    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": "22222"})
    response = client.get(url)
    content = str(response.content)

    msg = (
        "There appears to be more than one species associated "
        "with the records on this page. Interpret with caution."
    )

    assert msg in content


@pytest.mark.django_db
def test_multiple_tagdoc_warning_ok(client, db_setup):
    """As long as all of the tagdocs associated with a tag are the same,
    the warning should not appear in the reponse.

    """

    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": "11111"})
    response = client.get(url)
    content = str(response.content)

    msg = (
        "There appears to be more than one species associated "
        "with the records on this page. Interpret with caution."
    )

    assert msg not in content
