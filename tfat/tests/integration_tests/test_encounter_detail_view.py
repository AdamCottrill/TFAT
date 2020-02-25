"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_encounter_detail_view.py
Created: 04 Sep 2015 11:15:55

DESCRIPTION:

This script contains an integraion test to verify that the encounter detail
page renders as expected.

Specifically, an encounter is essentiall a view of a 125 record in one
of our master databases. The encounter details page must contain:

- the project name and project code
- the fishnet key for the fish associated with the recovery
- tag details:
  + tagid
  + tagdoc
  + tag colour
  + tag position
  + tag type
- encounter location - ddlat, ddlon, and grid
- fish attributes
- additional comments

Additionally, the encounter detail page may (conditionally) contain:

- fork length (mm and inches)
- total length (mm and inches)
- round weight (g and pounds)
- clipcode
- sex

A. Cottrill
=============================================================

"""

import pytest
from django.core.files import File
from django.urls import reverse

from tfat.tests.factories import *

from datetime import datetime


@pytest.fixture()
def project():
    return ProjectFactory(prj_cd="LHA_IA15_999", prj_nm="Fake Project")


@pytest.fixture()
def report_date():
    return datetime(2010, 10, 10)


@pytest.fixture()
def species():
    return SpeciesFactory()


@pytest.mark.django_db
def test_encounter_detail(client, project, species):
    """Verify that we can navigate to the encounter detail page (status
    code=200) and that the template is the one we think it is.
    """
    encounter = EncounterFactory(project=project, spc=species)

    response = client.get(
        reverse("tfat:encounter_detail", kwargs={"encounter_id": encounter.id})
    )

    assert "tfat/encounter_detail.html" in [x.name for x in response.templates]
    assert response.status_code == 200


@pytest.mark.django_db
def test_encounter_panel_headings(client, project, species):
    """The encounter details page is orgainized into several panels that
    display different attributes of the encounter.  The panel heading
    are 'Encounter Details', 'Tag Attributes', 'Encounter Location',
    'Fish Attributes', 'Additional Comments'.
    """

    encounter = EncounterFactory(
        project=project, spc=species, tlen=None, flen=None, rwt=2200
    )

    response = client.get(
        reverse("tfat:encounter_detail", kwargs={"encounter_id": encounter.id})
    )

    content = str(response.content)

    headings = [
        "Encounter Details",
        "Tag Attributes",
        "Encounter Location",
        "Fish Attributes",
        "Additional Comments",
    ]

    for heading in headings:
        assert heading in content


@pytest.mark.django_db
def test_encounter_detail_dates(client, project, species):
    """Verify that we the date of the observation appears on the detail
    page."""

    encounter_date = datetime(2010, 9, 9)

    encounter = EncounterFactory(
        project=project, spc=species, observation_date=encounter_date
    )

    response = client.get(
        reverse("tfat:encounter_detail", kwargs={"encounter_id": encounter.id})
    )

    content = str(response.content)

    assert "Sep 09, 2010" in content


@pytest.mark.django_db
def test_detail_tag_details(client, project, species):
    """The response should contain all of the basic tag attributes
    including a link to the tag details page."""

    tagid = "54321"
    encounter = EncounterFactory(
        project=project, spc=species, tagid=tagid, tagdoc="25012"
    )

    response = client.get(
        reverse("tfat:encounter_detail", kwargs={"encounter_id": encounter.id})
    )

    content = str(response.content)

    assert tagid in content  # this should be a link to tag-details

    url = reverse("tfat:tagid_detail_view", kwargs={"tagid": tagid})
    assert url in content

    assert "25012" in content

    assert "Yellow" in content
    assert "Flesh of Back" in content
    assert "Tubular Vinyl" in content
    assert "MNRF" in content


@pytest.mark.django_db
def test_encounter_details_with_location_info(client, project, species):
    """If location descriptions are provided, they should be included in
    the details page.

    """

    grid = "0909"
    dd_lat = 45.5
    dd_lon = -81.25

    encounter = EncounterFactory(
        project=project, spc=species, grid=grid, dd_lat=dd_lat, dd_lon=dd_lon
    )

    response = client.get(
        reverse("tfat:encounter_detail", kwargs={"encounter_id": encounter.id})
    )

    content = str(response.content)
    assert grid in content
    assert "45&#186; 30.000&#39;" in content
    assert "-81&#186; 15.000&#39;" in content


@pytest.mark.django_db
def test_encounter_details_flen(client, project, species):
    """If this encounter has a fork lenght, (but no total length or round
    weight), the response should contain the strings "Fork Length:", the
    fork length in mm, the fork length in inches.  The response should not
    contain "Total Length:" or "Weight:"

    """

    encounter = EncounterFactory(
        project=project, spc=species, flen=450, tlen=None, rwt=None
    )

    response = client.get(
        reverse("tfat:encounter_detail", kwargs={"encounter_id": encounter.id})
    )

    content = str(response.content)

    assert "Total Length:" not in content
    assert "Weight:" not in content

    assert "Fork Length:" in content
    assert "450 mm" in content
    assert "( 17.7 inches)" in content


@pytest.mark.django_db
def test_encounter_details_tlen(client, project, species):
    """If this encounter has a total length, (but no fork length or round
    weight), the response should contain the strings "Tolal Length:", the
    total length in mm, the total length in inches.  The response should not
    contain the strings "Fork Length:" or "Weight:"
    """

    encounter = EncounterFactory(
        project=project, spc=species, tlen=450, flen=None, rwt=None
    )

    response = client.get(
        reverse("tfat:encounter_detail", kwargs={"encounter_id": encounter.id})
    )

    content = str(response.content)

    assert "Fork Length:" not in content
    assert "Weight:" not in content

    assert "Total Length:" in content
    assert "450 mm" in content
    assert "( 17.7 inches)" in content


@pytest.mark.django_db
def test_encounter_details_rwt(client, project, species):
    """If this encounter has a round weight (but no fork or total lengths)
    the response should contain the strings "Weight:", the
    weight in g, and the weight in pounds.  The response should not
    contain the strings "Fork Length:" or "Total Length:"
    """

    encounter = EncounterFactory(
        project=project, spc=species, tlen=None, flen=None, rwt=2200
    )

    response = client.get(
        reverse("tfat:encounter_detail", kwargs={"encounter_id": encounter.id})
    )

    content = str(response.content)

    assert "Fork Length:" not in content
    assert "Total Length:" not in content

    assert "Weight:" in content
    assert "2,200 g" in content
    assert "( 4.9 lbs)" in content
