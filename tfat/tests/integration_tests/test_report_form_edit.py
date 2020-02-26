"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_report_form.py
Created: 22 Jul 2015 11:41:41

DESCRIPTION:

These currently FAIL.

A series of tests to verify that the report form works as expected
when used to create or edit reports.



required data elements:
- tag reporter's name

optional data elements:
- report date
- date flage


calculated/derived/default quantities:

- if report date is null when submitted, it should be set to current
  date and the date flag set to 'derived'

- if report format is dcr, we need effort and dcr number

- if report format is not dcr, effort and dcr number should be empty

- after succesfully creating a new report, or editing and existing
  one, we should be redirected to the report detail page.

A. Cottrill
=============================================================

"""

import pytest
import pytz

from django.urls import reverse
from django.core.files import File

from tfat.models import JoePublic, Report
from tfat.tests.factories import *

from datetime import datetime, timedelta


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


@pytest.fixture()
def user():

    user = UserFactory(email="mickey@disney.com")
    user.set_password("Abcd1234")
    user.save()

    return user


@pytest.fixture()
def db_setup():
    """Create some users with easy to remember names.
    """

    report_date = datetime(2010, 10, 10).replace(tzinfo=pytz.timezone("Canada/Eastern"))

    angler1 = JoePublicFactory.create(first_name="Homer", last_name="Simpson")
    angler2 = JoePublicFactory.create(first_name="Montgomery", last_name="Burns")

    # complete report filed by Homer
    report = ReportFactory(
        reported_by=angler1,
        report_date=report_date,
        reporting_format="dcr",
        dcr="dcr123",
        effort="eff001",
        comment="A fake comment.",
        follow_up=True,
    )

    # a minimal report filed by Monty Burns without any options or
    # associated tags to test conditional elements
    report = ReportFactory(
        reported_by=angler2, follow_up=False, report_date=report_date
    )


@pytest.mark.django_db
def test_report_edit_requires_login(client, db_setup):
    """If an unauthorized user tries to access the edit report url, he or
    she should be redirected to the login page.

    Arguments:
    - `client`:
    - `dbsetup`:

"""

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_report_url(client, user, db_setup):
    """Verify that the form and its correct elements are rendered when we
    call the edit_report form and all of the appropriate elements are there"""

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    client.login(username=user.email, password="Abcd1234")

    response = client.get(url)
    assert response.status_code == 200
    assert "tfat/report_form.html" in [x.name for x in response.templates]

    content = str(response.content)
    assert "Report Date:" in content
    assert "Date Flag:" in content
    assert "Report Format:" in content
    assert "DCR:" in content
    assert "Effort Number:" in content
    assert "Comment:" in content
    assert "Follow-up Required or Requested" in content


@pytest.mark.django_db
def test_edit_report_url_404(client, user, db_setup):
    """If we try to edit a report that does not exist, we
    should get a 404 error."""

    url = reverse("tfat:edit_report", kwargs={"report_id": 9999999})

    client.login(username=user.email, password="Abcd1234")
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_edit_report_post_url(client, user, db_setup):
    """verifty that we can post data some valid data it should be
    processed and we will be redirected to the report detail page."""

    # angler = JoePublic.objects.get(first_name='Homer')
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data, follow=True)

    # verify that the form was successfully submitted and we are
    # re-directed to report details page.
    assert response.status_code == 200
    assert "tfat/report_detail.html" in [x.name for x in response.templates]


# REPORT EDITING:
@pytest.mark.django_db
def test_edit_report_change_date(client, user, db_setup):
    """verifty that we can post data with a different date and change the
    report in the database."""

    last_week = datetime.today() - timedelta(days=7)
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"report_date": last_week}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data, follow=True)

    report = Report.objects.get(reported_by__first_name="Homer")
    assert report.report_date.date() == last_week.date()


@pytest.mark.django_db
def test_edit_report_change_invalid_date(client, user, db_setup):
    """verifty that we can post data with a different date and change the
    report in the database."""

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"report_date": "not a date"}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data)

    content = str(response.content)
    assert "Enter a valid date/time." in content


@pytest.mark.django_db
def test_edit_report_change_future_date(client, user, db_setup):
    """verifty that we can post data with a different date and change the
    report in the database."""

    next_week = datetime.today() + timedelta(days=7)
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"report_date": next_week}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data, follow=True)

    content = str(response.content)
    assert "Dates in the future are not allowed." in content


@pytest.mark.xfail
@pytest.mark.django_db
def test_edit_report_change_date_flag(client, user, db_setup):
    """verifty that we can post data with a different date flag and change the
    report in the database.

    This test is currently failing - it is not clear why. Several
    other tests associated with choice fields (latlon_flag) are also
    failing.  - may be related to warning message from collections library??
    """

    should_be = "reported"
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"date_flag": should_be}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data, follow=True)

    # check the report in the database:
    report = Report.objects.get(reported_by__first_name="Homer")
    assert report.date_flag == 1  # reported


@pytest.mark.django_db
def test_edit_report_change_format_to_dcr_without_dcr_number(client, user, db_setup):
    """if we post data to change reporting format to dcr without providing
    a dcr number, an error will be thrown"""

    report = Report.objects.get(reported_by__first_name="Montgomery")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"reporting_format": "dcr"}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data)

    content = str(response.content)
    assert "DCR number is required if reported by &quot;DCR&quot;." in content


@pytest.mark.django_db
def test_edit_report_change_format_to_dcr_without_eff_number(client, user, db_setup):
    """if we post data to change reporting format to dcr without providing
    an effort number, an error will be thrown"""

    report = Report.objects.get(reported_by__first_name="Montgomery")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"reporting_format": "dcr", "dcr": "DCR1234"}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data)

    content = str(response.content)
    msg = "Effort number is required if reported by &quot;DCR&quot;."
    assert msg in content


@pytest.mark.django_db
def test_edit_report_change_format_to_dcr_with_dcr_eff(client, user, db_setup):
    """if we post data to change reporting format to dcr and provide
    dcr and effort numbers, the report should be updated"""

    dcr = "DCR1234"
    effort = "001"

    report = Report.objects.get(reported_by__first_name="Montgomery")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"reporting_format": "dcr", "dcr": dcr, "effort": effort}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data, follow=True)

    # check the report in the database:
    report = Report.objects.get(reported_by__first_name="Montgomery")
    assert report.reporting_format == "dcr"
    assert report.dcr == dcr
    assert report.effort == effort


@pytest.mark.django_db
def test_edit_report_change_format_from_dcr_with_eff(client, user, db_setup):
    """if we post data to change reporting format from dcr to something
    else but forget to clear the effort, an error should be thrown by
    the form and included in the response
    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"reporting_format": "verbal", "dcr": "", "effort": "001"}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data)

    content = str(response.content)
    print("content={}".format(content))
    msg = "Effort should be empty if Report Format is not &quot;DCR&quot;."
    assert msg in content


@pytest.mark.django_db
def test_edit_report_change_format_from_dcr_with_dcr(client, user, db_setup):
    """if we post data to change reporting format from dcr to something
    else but forget to clear the dcr number, an error should be thrown by
    the form and included in the response
    """
    report = Report.objects.get(reported_by__first_name="Homer")

    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"reporting_format": "verbal", "dcr": "DCR1234", "effort": ""}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data)

    content = str(response.content)
    msg = "DCR should be empty if Report Format is not &quot;DCR&quot;."
    assert msg in content


@pytest.mark.django_db
def test_edit_report_change_format_from_dcr(client, user, db_setup):
    """if we post data to change reporting format from dcr to something
    else and we remember to clear the dcr and effort boxes, the report
    should be updated and the associated effort and dcr values should
    be none.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"reporting_format": "verbal", "dcr": "", "effort": ""}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data)

    # check the report in the database:
    report = Report.objects.get(reported_by__first_name="Homer")
    assert report.reporting_format == "verbal"
    assert report.dcr is None
    assert report.effort is None


@pytest.mark.django_db
def test_edit_report_change_comment(client, user, db_setup):
    """if we post data to change reporting format to dcr and provide
    dcr and effort numbers, the report should be updated"""

    report = Report.objects.get(reported_by__first_name="Homer")
    before = report.comment
    after = "This a our new comment"
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"comment": after}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data)

    report = Report.objects.get(reported_by__first_name="Homer")
    assert report.comment != before
    assert report.comment == after


@pytest.mark.django_db
def test_edit_report_change_follow_up(client, user, db_setup):
    """if we post data to change reporting format to dcr and provide
    dcr and effort numbers, the report should be updated"""

    report = Report.objects.get(reported_by__first_name="Montgomery")
    before = report.follow_up
    assert before is False

    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})

    data = {"follow_up": True}

    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data)

    report = Report.objects.get(reported_by__first_name="Homer")
    assert report.follow_up != before
    assert report.follow_up is True


@pytest.mark.django_db
def test_edit_report_add_file(client, user, db_setup):
    """if we post data to add a file to a report, the file should be
    available and associated with our report.
    """

    mock_file = StringIO("fake file content.")
    mock_file.name = "path/to/some/fake/fake_test_file.txt"
    data = {"associated_file": mock_file}

    report = Report.objects.get(reported_by__first_name="Montgomery")
    assert report.associated_file.name == ""

    client.login(username=user.email, password="Abcd1234")

    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})
    response = client.post(url, data, follow=True)

    content = str(response.content)
    assert "Associated File:" in content
    assert "reports/fake_test_file" in content
    assert "serve_file" in content

    report = Report.objects.get(reported_by__first_name="Montgomery")
    assert "reports/fake_test_file" in report.associated_file.name
