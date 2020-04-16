"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_detail_report.py
Created: 26 Jun 2015 13:25:34

DESCRIPTION:

This script contains an integraion test to verify that the report detail
page renders as expected.

Specifically, the details page must contain:

- the report number
- the name of the reporter and link to their summary page
- the date of the report
- the value of the date flag
- the report format
- a link to edit the report
- a link to associate tags with this report


Additionally, the detail page may (conditionally) contain:

- table of tags if tags are associated with this report including
  links to tag details and a link to edit this tag recapture
  occurence.

- comments if comments are available

- a follow-up reminder if a follow-up is requested

- DCR and effort number (if this is from a commerical fishing report)

- a link to a file if the report has an file associated with it
  (email, or scanned letter)

- warning if no tags are found


A. Cottrill
=============================================================

"""

import pytest
import pytz
from django.core.files import File
from django.urls import reverse

from tfat.models import Report, JoePublic

from tfat.tests.factories import (
    UserFactory,
    JoePublicFactory,
    SpeciesFactory,
    ReportFactory,
    RecoveryFactory,
    ReportFollowUpFactory,
)

from datetime import datetime

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
def species():
    species = SpeciesFactory()
    return species


@pytest.fixture()
def db_setup(user, species):

    report_date = datetime(2010, 10, 10).replace(tzinfo=pytz.timezone("Canada/Eastern"))

    angler1 = JoePublicFactory.create(first_name="Homer", last_name="Simpson")
    angler2 = JoePublicFactory.create(first_name="Montgomery", last_name="Burns")

    mock_file = StringIO("fake file content.")
    mock_file.name = "path/to/some/fake/fake_test_file.txt"

    # report filed by Homer
    report = ReportFactory(
        reported_by=angler1,
        report_date=report_date,
        reporting_format="dcr",
        dcr="dcr123",
        effort="eff001",
        follow_up_status="requested",
        associated_file=File(mock_file),
        comment="A fake comment.",
        follow_up=True,
    )
    tagids = ["111111", "222222", "333333"]
    for tag in tagids:
        recovery = RecoveryFactory(report=report, species=species, tagid=tag)

    followup = ReportFollowUpFactory(report=report, created_by=user, status="requested")

    # a minimal report filed by Monty Burns without any options or
    # associated tags to test conditional elements
    report = ReportFactory(
        reported_by=angler2, follow_up=False, report_date=report_date
    )


@pytest.mark.django_db
def test_reports_detail(client, db_setup):
    """Verify that we can navigate to the report detail page (status
    code=200) and that the template is the one we think it is.
    """

    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )

    assert "tfat/report_detail.html" in [x.name for x in response.templates]
    assert response.status_code == 200


@pytest.mark.django_db
def test_reports_detail_contains_report_id(client, db_setup):
    """verify that the report id number is included in the reponse
    """
    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )

    content = str(response.content)
    should_be = "Tag Report {}".format(report.id)
    assert should_be in content


@pytest.mark.django_db
def test_reports_detail_contains_reported_by(client, db_setup):
    """verify that the name of the reporter and a link to their reports page
    is included in the reponse
    """
    angler = JoePublic.objects.get(first_name="Homer")
    report = Report.objects.get(reported_by=angler)
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )

    content = str(response.content)
    url = reverse("tfat:angler_reports", kwargs={"angler_id": angler.id})
    assert url in content
    assert angler.first_name in content
    assert angler.last_name in content
    assert str(angler) in content


@pytest.mark.django_db
def test_reports_detail_contains_edit_report_authenticated(client, user, db_setup):
    """verify that a link to edit the report is included in the reponse if
    our user is authenticated.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    client.login(username=user.email, password="Abcd1234")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})
    assert url in content


@pytest.mark.django_db
def test_reports_detail_does_not_contain_edit_report(client, db_setup):
    """verify that a link to edit the report is NOT included if our user
    is not logged in.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)
    url = reverse("tfat:edit_report", kwargs={"report_id": report.id})
    assert url not in content


@pytest.mark.django_db
def test_reports_detail_contains_report_date(client, db_setup):
    """verify that the report date and value of the date flag is included
    in the reponse

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)

    assert "Oct 10, 2010" in content


@pytest.mark.django_db
def test_reports_detail_contains_report_format(client, db_setup):
    """verify that the report format is included in the reponse

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)

    assert "Format:" in content
    assert "dcr" in content


@pytest.mark.django_db
def test_reports_detail_contains_add_tag_link_authorized(client, user, db_setup):
    """verify that the reponse to an authorized user contains a link to
    add tags to this report.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    client.login(username=user.email, password="Abcd1234")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})
    assert url in content


@pytest.mark.django_db
def test_reports_detail_contains_no_add_tag_link(client, db_setup):
    """verify that the reponsce to unauthorized users does not contains a
    link to add tags to this report

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})
    assert url not in content


# CONTDITIONAL ELEMENTS BELOW THIS POINT
@pytest.mark.django_db
def test_reports_detail_does_not_contain(client, db_setup):
    """before we test that conditional elements are reported when
    appropriate, we need to verify that a very basic report does not
    contain them by default.
    - DCR and effort
    - follow-up
    - comments
    - tag list
    - edit tag link

    """
    report = Report.objects.get(reported_by__first_name="Montgomery")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)

    assert "DCR:" not in content
    assert "Effort:" not in content
    assert "Associated File:" not in content
    assert "Comments:" not in content
    assert "A fake comment." not in content
    assert "Follow-up Required" not in content


@pytest.mark.django_db
def test_report_detail_without_tags_has_warning(client, db_setup):
    """the report detail for a report without tags should include the
    warning about no associated tags.
    """
    report = Report.objects.get(reported_by__first_name="Montgomery")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)

    assert "<h3>Oops!</h3>" in content
    msg = "seem to be any tags associated with this report."
    assert msg in content


@pytest.mark.django_db
def test_report_detail_with_tags_has_no_warning(client, db_setup):
    """the report detail for a report with tags should not include the
    warning about no associated tags.
    """
    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)

    assert "<h3>Oops!</h3>" not in content
    msg = "seem to be any tags associated with this report."
    assert msg not in content


@pytest.mark.django_db
def test_report_detail_with_follow_up(client, db_setup):
    """if there is a follow required or requested for a report, that
    should appear on the detail page for the report.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)

    assert "Follow-up Required" in content


@pytest.mark.django_db
def test_report_detail_with_dcr(client, db_setup):
    """if the report has a dcr and effort number, they should be included
    on the detail page for the report.

    """
    report = Report.objects.get(reported_by__first_name="Homer")

    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)

    assert "DCR:" in content
    assert "dcr123" in content
    assert "Effort:" in content
    assert "eff001" in content


@pytest.mark.django_db
def test_report_detail_with_associated_file(client, db_setup):
    """if the report has an associated file, a link to download the
    associated file should be included in the response.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)

    assert "Associated File:" in content
    assert "reports/path/to/some/fake/fake_test_file" in content


@pytest.mark.django_db
def test_report_detail_with_comment(client, db_setup):
    """if the report has comments assocaited with it, they should be included
    on the detail page for the report.

    """
    report = Report.objects.get(reported_by__first_name="Homer")

    url = reverse("tfat:report_detail", kwargs={"report_id": report.id})
    response = client.get(url)
    content = str(response.content)

    assert "Comments:" in content
    assert "A fake comment." in content


@pytest.mark.django_db
def test_report_detail_no_step3_message(client, db_setup):
    """When we access the report detail page through the normal url,
    it should NOT include an instructive message.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)
    msg = "Step 3 - Add tags as necessary to complete report"
    assert msg not in content


@pytest.mark.django_db
def test_report_a_tag_report_detail_url(client, db_setup):
    """Verify that we can navigate to the report detail page (status
    code=200) and that the template is the one we think it is when we
    access it through the report-a-tag url.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_a_tag_report_detail", kwargs={"report_id": report.id})
    )

    assert "tfat/report_detail.html" in [x.name for x in response.templates]
    assert response.status_code == 200


@pytest.mark.django_db
def test_report_a_tag_report_detail_message(client, db_setup):
    """When we access the report detail page through the report-a-tag url,
    it should include an instructive message.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    response = client.get(
        reverse("tfat:report_a_tag_report_detail", kwargs={"report_id": report.id})
    )
    content = str(response.content)
    msg = "Step 3 - Add tags as necessary to complete report"
    assert msg in content
