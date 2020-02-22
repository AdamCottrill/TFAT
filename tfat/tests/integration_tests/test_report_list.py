"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_report_list.py
Created: 19 Jun 2015 10:07:24

DESCRIPTION:

The tests in this module verify that the view that renders the list of
tag reports render as expected.

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
    """

    Arguments:
    - `db`:
    """

    user = UserFactory()

    report_date = datetime(2010, 10, 10).replace(tzinfo=pytz.UTC)

    spc = SpeciesFactory()

    angler1 = JoePublicFactory.create(first_name="Homer", last_name="Simpson")

    angler2 = JoePublicFactory.create(first_name="Montgomery", last_name="Burns")

    angler3 = JoePublicFactory.create(first_name="Barney", last_name="Gumble")

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
def test_tag_report_list(client, db_setup):
    """verify that the report list renders properly and includes the
    appropriate title."""

    response = client.get(reverse("tfat:recovery_report_list"))
    assert response.status_code == 200
    content = str(response.content)
    assert "Tag Recovery Reports" in content


@pytest.mark.django_db
def test_angler_names_in_tag_report_list(client, db_setup):
    """the name of the anglers who have sumbitted reports should appear in
    the report list, any anglers who have not sumbitted reports should not
    appear in the list."""

    response = client.get(reverse("tfat:recovery_report_list"))
    content = str(response.content)
    assert "Homer Simpson" in content
    assert "Montgomery Burns" in content
    assert "Barney Gumble" not in content


@pytest.mark.django_db
def test_tagids_in_tag_report_list(client, db_setup):
    """the tag numbers assocaited with the reports should appear in the
    resonse"""

    response = client.get(reverse("tfat:recovery_report_list"))
    content = str(response.content)

    tagids = ["111111", "222222", "333333", "4444", "5555", "6666"]
    for tagid in tagids:
        assert tagid in content


@pytest.mark.django_db
def test_follow_up_in_tag_report_list(client, db_setup):
    """If there is a follow required for a report, it should appear in the
    list of reports
    """

    response = client.get(reverse("tfat:recovery_report_list"))
    content = str(response.content)

    assert "Follow-up Required" in content


@pytest.mark.django_db
def test_follow_up_not_in_tag_report_list(client, db_setup):
    """If there there are no more follow-ups required for a report,
    "Follow-up Required" it should not appear in the list of reports
    """

    # get the only report with a follow required and update it
    report = Report.objects.get(reported_by__last_name="Burns")

    user = UserFactory()
    followup = ReportFollowUpFactory(report=report, created_by=user, status="completed")
    followup.save()

    # verify that follow-up required is not in the list now:
    response = client.get(reverse("tfat:recovery_report_list"))
    content = str(response.content)
    assert "Follow-up Required" not in content
