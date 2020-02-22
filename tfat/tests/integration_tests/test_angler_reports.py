"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_anlger_reports.py
Created: 26 Jun 2015 13:25:34

DESCRIPTION:

This script contains an integraion test to verify that the angler reports
page renders as expected.

A. Cottrill
=============================================================

"""

import pytest
import pytz
from django.urls import reverse

from tfat.tests.factories import *

from datetime import datetime


@pytest.fixture()
def db_setup():

    user = UserFactory()

    report_date = datetime(2010, 10, 10).replace(tzinfo=pytz.timezone("Canada/Eastern"))

    spc = SpeciesFactory()

    angler1 = JoePublicFactory.create(
        first_name="Homer",
        last_name="Simpson",
        address1="742 Evergreen Tarrace",
        address2="Box 123",
        town="Springfield",
        province="Ontario",
        postal_code="N0W2T2",
        email="hsimpson@hotmail.com",
        phone="555-321-1234",
    )

    angler2 = JoePublicFactory.create(first_name="Montgomery", last_name="Burns")

    # report filed by Homer
    report = ReportFactory(reported_by=angler1, report_date=report_date)
    tagids = ["111111", "222222", "333333"]
    for tag in tagids:
        recovery = RecoveryFactory(report=report, spc=spc, tagid=tag)

    # a report filed by Monty Burns
    report = ReportFactory(reported_by=angler2, follow_up=True, report_date=report_date)

    followup = ReportFollowUpFactory(report=report, created_by=user, status="requested")

    tagids = ["4444", "5555", "6666"]
    for tag in tagids:
        recovery = RecoveryFactory(report=report, spc=spc, tagid=tag)


@pytest.mark.django_db
def test_anlger_reports(client, db_setup):
    """Verify that we can navigate to the angler reports page (status
    code=200) and that the template is the one we think it is.
    """

    angler = JoePublic.objects.get(first_name="Homer")
    response = client.get(
        reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    )

    assert "tfat/angler_reports.html" in [x.name for x in response.templates]
    assert response.status_code == 200


@pytest.mark.django_db
def test_anlger_report_has_crud_links(client, db_setup):
    """The report list for a partuclar angler should have links to allow
    us to create and update reports.
    """

    angler = JoePublic.objects.get(first_name="Homer")
    response = client.get(
        reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    )
    content = str(response.content)

    assert "Edit Details" in content  # angler details
    assert "Create New Report" in content
    assert "Report Details" in content


@pytest.mark.django_db
def test_tagids_in_anlger_reports(client, db_setup):
    """The tags reported by a particular individual should appear in the
    angler reports pages but tags reported by other anlgers should
    not.
    """

    angler = JoePublic.objects.get(first_name="Homer")
    response = client.get(
        reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    )
    content = str(response.content)

    tagids = ["111111", "222222", "333333"]
    for tag in tagids:
        assert tag in content

    tagids = ["4444", "5555", "6666"]
    for tag in tagids:
        assert tag not in content


@pytest.mark.django_db
def test_report_date_in_anlger_reports(client, db_setup):
    """The data each report was filed on should appear on the angler reports
    page."""

    report_date = datetime(2010, 10, 10).replace(tzinfo=pytz.timezone("Canada/Eastern"))

    angler = JoePublic.objects.get(first_name="Homer")
    response = client.get(
        reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    )
    content = str(response.content)

    # format the date and replace any leading zeros
    date = report_date.strftime("%b %d, %Y").replace(" 0", " ")
    assert date in content


@pytest.mark.django_db
def test_angler_info_in_anlger_reports(client, db_setup):
    """The basic angler information should be included in the report list
    - who filled all of these reports and how do we get in touch with
    them.
    """

    angler = JoePublic.objects.get(first_name="Homer")
    response = client.get(
        reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    )
    content = str(response.content)

    assert "742 Evergreen Tarrace" in content
    assert "Box 123" in content
    assert "Springfield" in content
    assert "Ontario" in content
    assert "N0W2T2" in content
    assert "hsimpson@hotmail.com" in content
    assert "555-321-1234" in content


@pytest.mark.django_db
def test_report_follow_up_not_in_response(client, db_setup):
    """If a follow is requested for this report, it should be included in
    the reponse.
    """

    angler = JoePublic.objects.get(first_name="Homer")
    # verify that follow-up required is not in the list now:
    response = client.get(
        reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    )
    content = str(response.content)
    assert "Follow-up Required" not in content


@pytest.mark.django_db
def test_report_follow_up_in_response(client, db_setup):
    """If not follow-up is currently required for this report, 'Follow-up
    Required' should not appear in the response.
    """

    angler = JoePublic.objects.get(first_name="Montgomery")
    response = client.get(
        reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    )
    content = str(response.content)

    assert "Follow-up Required" in content


@pytest.mark.django_db
def test_step2_not_in_anlger_reports(client, db_setup):
    """Verify that Step 2 instructions are not in the normal angler report view.
    """

    angler = JoePublic.objects.get(first_name="Homer")
    response = client.get(
        reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    )
    content = str(response.content)
    assert "Step 2" not in content


@pytest.mark.django_db
def test_step2_in_anlger_report_a_tag_url(client, db_setup):
    """Verify that the report_at_tag_angler url works as expected (status
    code=200).
    """

    angler = JoePublic.objects.get(first_name="Homer")
    response = client.get(
        reverse("tfat:report_a_tag_angler_reports", kwargs={"angler_id": angler.id})
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_step2_in_anlger_report_a_tag(client, db_setup):
    """When the angler reports is accessed through the
    report_a_tag_angler_reports url, it should contain a message
    describing the next step in the process. (i.e. - click the new
    report button)

    """

    angler = JoePublic.objects.get(first_name="Homer")
    response = client.get(
        reverse("tfat:report_a_tag_angler_reports", kwargs={"angler_id": angler.id})
    )
    content = str(response.content)

    msg = "Step 2 - To create a new report click on the" + ' "Create New Report" button'
    assert msg in content


@pytest.mark.django_db
def test_report_a_tag_anlger_report_create_report_link(client, db_setup):
    """When we view the angler reports through the report-a-tag url, the
    link to create reports shoudl also be report-a-tag url, not the
    standard create report url.

    """

    angler = JoePublic.objects.get(first_name="Homer")
    response = client.get(
        reverse("tfat:report_a_tag_angler_reports", kwargs={"angler_id": angler.id})
    )
    content = str(response.content)

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    assert url not in content

    url = reverse("tfat:report_a_tag_create_report", kwargs={"angler_id": angler.id})
    assert url in content
