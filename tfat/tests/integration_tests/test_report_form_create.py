"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_report_form.py
Created: 22 Jul 2015 11:41:41

DESCRIPTION:

A series of tests to verify that the report form works as expected
when used to create reports.

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
from django.urls import reverse
from django.core.files import File

from tfat.models import JoePublic, Report
from tfat.tests.factories import JoePublicFactory, UserFactory

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
def angler():
    """Create an angler"""
    angler = JoePublicFactory.create(first_name="Barney", last_name="Gumble")
    return angler


@pytest.mark.django_db
def test_report_create_requires_login(client, angler):
    """If an unauthorized user tries to access the edit report url, he or
    she should be redirected to the login page.

    Arguments:
    - `client`:
    - `dbsetup`:
    """

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_report_url(client, user, angler):
    """Verify that the form rendered with status code 200 and uses teh
    correct template.
    """
    client.login(username=user.email, password="Abcd1234")
    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "tfat/report_form.html" in [x.name for x in response.templates]


@pytest.mark.django_db
def test_create_report_elements(client, user, angler):
    """Verify that the form has the correct elements. WHen the form is
    accessed throught the basic approach, it will not have an
    instructional message.
    """

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    client.login(username=user.email, password="Abcd1234")
    response = client.get(url)

    content = str(response.content)
    assert "Report Date:" in content
    assert "Date Flag:" in content
    assert "Report Format:" in content
    assert "DCR:" in content
    assert "Effort Number:" in content
    assert "Comment:" in content
    assert "Follow-up Required or Requested" in content

    assert "Step 2b - Fill in Report Details:" not in content


@pytest.mark.django_db
def test_create_report_url_404(client, user, angler):
    """If we try to create a report for an angler who does not exist, we
    should get a 404 error."""

    url = reverse("tfat:create_report", kwargs={"angler_id": 9999999})
    client.login(username=user.email, password="Abcd1234")
    response = client.get(url)
    assert response.status_code == 404


# REPORT CREATION
@pytest.mark.django_db
def test_create_report_minimal_data(client, user, angler):
    """if we post minimal data, a report should be created for this
    angler.  Date should be today, date flag should be 'unknown', and
    the other fields should all be empty, and we should be re-directed
    to the report's detail page
    """

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    data = {"reported_by": angler.id}
    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data, follow=True)

    assert response.status_code == 200
    templates = [x.name for x in response.templates]
    assert "tfat/report_detail.html" in templates

    # query the database and make sure the data is how we expect it.
    today = datetime.today()
    report = Report.objects.get(reported_by__first_name="Barney")
    assert report.report_date.date() == today.date()
    assert report.date_flag == 0
    assert report.associated_file.name == ""
    assert report.dcr is None
    assert report.effort is None
    assert report.comment is None
    assert report.follow_up is False


@pytest.mark.django_db
def test_create_report_invalid_date(client, user, angler):
    """if we post data with a date that does not make sense, an error
    should be thrown"""

    data = {"reported_by": angler.id, "report_date": "not a date"}
    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data, follow=True)

    content = str(response.content)
    assert "Enter a valid date/time." in content


@pytest.mark.django_db
def test_create_report_future_date(client, user, angler):
    """if we post data with a date in the future, an error
    should be thrown"""

    next_week = datetime.today() + timedelta(days=7)

    data = {"reported_by": angler.id, "report_date": next_week}
    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data, follow=True)

    content = str(response.content)
    assert "Dates in the future are not allowed." in content


@pytest.mark.django_db
def test_create_report_dcr_complete(client, user, angler):
    """If we post data with format=dcr, and provide a dcr number and
    effort number, the report should be created."""

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})

    data = {
        "reported_by": angler.id,
        "reporting_format": "dcr",
        "dcr": "DCR1234",
        "effort": "001",
    }
    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data, follow=True)

    report = Report.objects.get(reported_by__first_name="Barney")
    assert report.reporting_format == "dcr"
    assert report.dcr == "DCR1234"
    assert report.effort == "001"


@pytest.mark.django_db
def test_create_report_dcr_missing_dcr_number(client, user, angler):
    """If we post data with format=dcr, but omit the dcr number, an error
    should be thrown.
    """

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    data = {"reported_by": angler.id, "reporting_format": "dcr", "effort": "001"}
    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data, follow=True)
    content = str(response.content)
    assert "DCR number is required if reported by &quot;DCR&quot;." in content


@pytest.mark.django_db
def test_create_report_dcr_missing_effort_number(client, user, angler):
    """If we post data with format=dcr, but omit the effort number, an error
    should be thrown.
    """

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})

    data = {"reported_by": angler.id, "reporting_format": "dcr", "dcr": "DCR1234"}
    client.login(username=user.email, password="Abcd1234")

    response = client.post(url, data, follow=True)

    content = str(response.content)
    msg = "Effort number is required if reported by &quot;DCR&quot;."
    assert msg in content


@pytest.mark.django_db
def test_create_report_not_dcr_with_effort_number(client, user, angler):
    """If we post data with format other than dcr, and include an effort
    number, an error should be thrown - effort is not meaningful
    unless reporting format is dcr

    """

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})

    data = {"reported_by": angler.id, "reporting_format": "verbal", "effort": "001"}
    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data, follow=True)

    content = str(response.content)
    msg = "Effort should be empty if Report Format is not &quot;DCR&quot;."
    assert msg in content


@pytest.mark.django_db
def test_create_report_not_dcr_with_dcr_number(client, user, angler):
    """If we post data with format other than dcr, and include an dcr
    number, an error should be thrown - a dcr number is not meaningful
    unless reporting format is dcr

    """

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})

    data = {"reported_by": angler.id, "reporting_format": "verbal", "dcr": "DCR1234"}
    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data, follow=True)

    content = str(response.content)
    msg = "DCR should be empty if Report Format is not &quot;DCR&quot;."

    print(content)
    assert msg in content


@pytest.mark.django_db
def test_create_report_with_file(client, user, angler):
    """if we post data with an associated file object, the report should
    be created and have an associated file object."""

    mock_file = StringIO("fake file content.")
    mock_file.name = "path/to/some/fake/fake_test_file.txt"

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    data = {"reported_by": angler.id, "associated_file": mock_file}
    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data, follow=True)

    content = str(response.content)
    assert "Associated File:" in content
    assert "reports/fake_test_file" in content
    assert "serve_file" in content

    report = Report.objects.get(reported_by__first_name="Barney")
    assert "reports/fake_test_file" in report.associated_file.name


@pytest.mark.django_db
def test_create_report_with_comment(client, user, angler):
    """if we post data with a comment, the report should
    be created and have that comment associated with it."""

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    data = {"reported_by": angler.id, "comment": "My Fake Comment"}
    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data, follow=True)

    # query the database and make sure the data is how we expect it.
    report = Report.objects.get(reported_by__first_name="Barney")
    assert report.comment == "My Fake Comment"


@pytest.mark.django_db
def test_create_report_with_follow_up(client, user, angler):
    """if we post data with follow_up=True, the report should
    be created and its follow_up value should be TRUE."""

    url = reverse("tfat:create_report", kwargs={"angler_id": angler.id})
    data = {"reported_by": angler.id, "follow_up": True}
    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, data, follow=True)

    # query the database and make sure the data is how we expect it.
    report = Report.objects.get(reported_by__first_name="Barney")
    assert report.follow_up is True
    assert report.follow_up_status == "requested"


# ======================================
#         REPORT-A-TAG


@pytest.mark.django_db
def test_report_at_tag_create_report_url(client, user, angler):
    """Verify that the report-a-tag create report url renders properly"""

    url = reverse("tfat:report_a_tag_create_report", kwargs={"angler_id": angler.id})
    client.login(username=user.email, password="Abcd1234")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_report_at_tag_create_report_url(client, user, angler):
    """When rendered through the report-a-tag create report url, the    response should include an instructional message."""

    url = reverse("tfat:report_a_tag_create_report", kwargs={"angler_id": angler.id})
    client.login(username=user.email, password="Abcd1234")
    response = client.get(url)
    content = str(response.content)

    assert "Step 2b - Fill in Report Details:" in content


@pytest.mark.django_db
def test_report_a_tag_create_report_url_404(client, user, angler):
    """If we try to create a report for an angler who does not exist, we
    should get a 404 error."""

    url = reverse("tfat:report_a_tag_create_report", kwargs={"angler_id": 9999999})
    client.login(username=user.email, password="Abcd1234")
    response = client.get(url)
    assert response.status_code == 404
