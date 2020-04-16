"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_recovery_detail_view.py
Created: 25 Aug 2015 12:05:44

DESCRIPTION:

This script contains an integraion test to verify that the recovery detail
page renders as expected.

Specifically, the recovery details page must contain:

- the recapture date
- the name of the reporter and link to their summary page
- link to the report details
- a link to edit the recovery data
- tag details:
  + tagid
  + tagdoc
  + tag colour
  + tag position
  + tag type
- recovery location
- fish attributes including flen, tlen, rwt, and girth
- additional comments

- the date of the report
- the date of the recovery
- the value of the date flag



Additionally, the recovery detail page may (conditionally) contain:

- latitude and longitude
- fork length (mm and inches)
- total length (mm and inches)
- round weight (g and pounds)

A. Cottrill
=============================================================

"""

import pytest
import pytz
from django.core.files import File
from django.urls import reverse

from tfat.tests.factories import (
    SpeciesFactory,
    UserFactory,
    JoePublicFactory,
    ReportFactory,
    RecoveryFactory,
)

from datetime import datetime


@pytest.fixture()
def user():
    """Create some users with easy to remember names."""

    user = UserFactory(email="mickey@disney.com")
    user.set_password("Abcd1234")
    user.save()

    return user


@pytest.fixture()
def angler():
    return JoePublicFactory(first_name="Homer", last_name="Simpson")


@pytest.fixture()
def report_date():
    return datetime(2010, 10, 10).replace(tzinfo=pytz.timezone("Canada/Eastern"))


@pytest.fixture()
def report(angler, report_date):
    return ReportFactory(report_date=report_date, reported_by=angler)


@pytest.fixture()
def species():
    return SpeciesFactory()


@pytest.mark.django_db
def test_recovery_detail(client, report, species):
    """Verify that we can navigate to the recovery detail page (status
    code=200) and that the template is the one we think it is.
    """
    recovery = RecoveryFactory(report=report, species=species)

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    assert "tfat/recovery_detail.html" in [x.name for x in response.templates]
    assert response.status_code == 200


@pytest.mark.django_db
def test_recovery_panel_headings(client, report, species):
    """The recovery details page is orgainized into several panels that
    display different attributes of the recovery.  The panel heading
    are 'Recovery Details', 'Tag Attributes', 'Recapture Location',
    'Fish Attributes', 'Additional Comments'.
    """

    recovery = RecoveryFactory(
        report=report, species=species, tlen=None, flen=None, rwt=2200
    )

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)

    headings = [
        "Recovery Details",
        "Tag Attributes",
        "Recapture Location",
        "Fish Attributes",
        "Additional Comments",
    ]

    for heading in headings:
        assert heading in content


@pytest.mark.django_db
def test_recovery_detail_links(client, angler, report, species):
    """Verify that we have links to the report's page, the report details
    page, and the form to edit the recovery information."""

    recovery = RecoveryFactory(report=report, species=species)

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)

    assert "Homer Simpson" in content  # this should be a link to tag-details

    url = reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    assert url in content

    url = reverse("tfat:report_detail", kwargs={"report_id": report.id})
    assert url in content


@pytest.mark.django_db
def test_recovery_detail_links(client, angler, report, species):
    """Verify that we have links to the report's page, the report details
    page, and the form to edit the recovery information."""

    recovery = RecoveryFactory(report=report, species=species)

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)

    assert "Homer Simpson" in content  # this should be a link to tag-details

    url = reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    assert url in content

    url = reverse("tfat:report_detail", kwargs={"report_id": report.id})
    assert url in content


@pytest.mark.django_db
def test_no_edit_recovery_link(client, angler, report, species):
    """if the page is accessed by a user who is not logged in, the link to
    the edit_recovery view should *NOT* be provided."""

    recovery = RecoveryFactory(report=report, species=species)

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )
    content = str(response.content)
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})
    assert url not in content
    assert "Edit Recovery Details" not in content


@pytest.mark.django_db
def test_edit_recovery_link_authorized(client, user, angler, report, species):
    """if the page is accessed by a user who is logged in, a link to
    the edit_recovery view should be provided."""

    recovery = RecoveryFactory(report=report, species=species)

    client.login(username="mickey@disney.com", password="Abcd1234")
    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )
    content = str(response.content)
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})
    assert url in content
    assert "Edit Recovery Details" in content


@pytest.mark.django_db
def test_recovery_detail_dates(client, report, species, report_date):
    """Verify that we have links to the report's page, the report details
    page, and the form to edit the recovery information."""

    recovery_date = datetime(2010, 9, 9).replace(tzinfo=pytz.timezone("Canada/Eastern"))

    recovery = RecoveryFactory(
        report=report, species=species, recovery_date=recovery_date, date_flag=0
    )

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)

    assert "Sep 09, 2010" in content
    assert "Oct 10, 2010" in content
    assert "Reported" in content


@pytest.mark.django_db
def test_detail_tag_details(client, report, species):
    """The response should contain all of the basic tag attributes
    including a link to the tag details page."""

    tagid = "54321"
    recovery = RecoveryFactory(
        report=report, species=species, tagid=tagid, tagdoc="25012"
    )

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
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
def test_recovery_details_with_locations(client, report, species):
    """If location descriptions are provided, they should be included in
    the details page.

    """

    general_location = "North Channel"
    specific_location = "Off my dock."

    recovery = RecoveryFactory(
        report=report,
        species=species,
        general_location=general_location,
        specific_location=specific_location,
    )

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)
    assert general_location in content
    assert specific_location in content


@pytest.mark.django_db
def test_recovery_details_with_latlon(client, report, species):
    """If lat-lon are available for this recovery event, the strings
    Latitude: and Longitude: should appear in rendered page.
    """

    recovery = RecoveryFactory(
        report=report, species=species, dd_lat=45.5, dd_lon=-81.3
    )

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)
    assert "Latitude:" in content
    assert "Longitude:" in content


@pytest.mark.django_db
def test_recovery_details_no_latlon(client, report, species):
    """If lat-lon are not available for this recovery event, the
    strings Latitude: and Longitude: should not appear in rendered
    page."""

    recovery = RecoveryFactory(report=report, species=species, dd_lat=None, dd_lon=None)

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)
    assert "Latitude:" not in content
    assert "Longitude:" not in content


@pytest.mark.django_db
def test_recovery_details_no_lat(client, report, species):
    """If a valid lat-lon are is available for this recovery event (ie. -
    latitude is missing), the strings Latitude: and Longitude: should
    not appear in rendered page.
    """

    recovery = RecoveryFactory(
        report=report, species=species, dd_lat=None, dd_lon=-81.3
    )

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)
    assert "Latitude:" not in content
    assert "Longitude:" not in content


@pytest.mark.django_db
def test_recovery_details_no_lon(client, report, species):
    """If a valid lat-lon are is available for this recovery event (ie. -
    longitude is missing), the strings Latitude: and Longitude: should
    not appear in rendered page.
    """

    recovery = RecoveryFactory(report=report, species=species, dd_lat=45.5, dd_lon=None)

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)
    assert "Latitude:" not in content
    assert "Longitude:" not in content


@pytest.mark.django_db
def test_recovery_details_flen(client, report, species):
    """If this recovery has a fork lenght, (but no total length or round
    weight), the response should contain the strings "Fork Length:", the
    fork length in mm, the fork length in inches.  The response should not
    contain "Total Length:" or "Weight:"

    """

    recovery = RecoveryFactory(
        report=report, species=species, flen=450, tlen=None, rwt=None
    )

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)

    assert "Total Length:" not in content
    assert "Weight:" not in content

    assert "Fork Length:" in content
    assert "450 mm" in content
    assert "( 17.7 inches)" in content


@pytest.mark.django_db
def test_recovery_details_tlen(client, report, species):
    """If this recovery has a total length, (but no fork length or round
    weight), the response should contain the strings "Tolal Length:", the
    total length in mm, the total length in inches.  The response should not
    contain the strings "Fork Length:" or "Weight:"
    """

    recovery = RecoveryFactory(
        report=report, species=species, tlen=450, flen=None, rwt=None
    )

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)

    assert "Fork Length:" not in content
    assert "Weight:" not in content

    assert "Total Length:" in content
    assert "450 mm" in content
    assert "( 17.7 inches)" in content


@pytest.mark.django_db
def test_recovery_details_rwt(client, report, species):
    """If this recovery has a round weight (but no fork or total lengths)
    the response should contain the strings "Weight:", the
    weight in g, and the weight in pounds.  The response should not
    contain the strings "Fork Length:" or "Total Length:"
    """

    recovery = RecoveryFactory(
        report=report, species=species, tlen=None, flen=None, rwt=2200
    )

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)

    assert "Fork Length:" not in content
    assert "Total Length:" not in content

    assert "Weight:" in content
    assert "2,200 g" in content
    assert "( 4.9 lbs)" in content


@pytest.mark.django_db
def test_recovery_details_girth(client, report, species):
    """If this recovery has a girth (but no fork or total lengths, or
    round weight) the response should contain the strings "Girth:",
    the girth in mm, and the girth in inches.  The response should
    not contain the strings "Fork Length:", "Total Length:" or "Girth:"
    """

    recovery = RecoveryFactory(
        report=report, species=species, tlen=None, flen=None, girth=450
    )

    response = client.get(
        reverse("tfat:recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    content = str(response.content)

    assert "Fork Length:" not in content
    assert "Total Length:" not in content
    assert "Weight:" not in content

    assert "Girth:" in content
    assert "450 mm" in content
    assert "( 17.7 inches)" in content
