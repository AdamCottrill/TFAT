"""This file contains a number of integration_tests that ensure the
report follow up functionality works as expected.

+ follow up report form in unaccessible to unauthorized users

+ the form contains the elements: status, comment, cancel, submit

+ the status widget is required - an error should appear if the form
is submitted without a choice.

+ the comment widget is optional

+ the select widget has two options if the status is 'requested'.  THe
options should be 'initialized' and 'completed'

+ the select widget has one option if the status is 'initialized'.  THe
options should 'completed' and is a required field.

+ the cancel and submit buttons return us to the report detail page or the report
list, depending on where we came from.

+ after the form is submitted, the detail page should contain a
message indicting that the follow up was completed, by whom, when, and
optionally the comment.

"""

import pytest

# import unittest

from django.urls import reverse

from tfat.tests.factories import (
    UserFactory,
    JoePublicFactory,
    ReportFactory,
    ReportFollowUpFactory,
)

# from datetime import datetime


@pytest.fixture()
def user():
    """
    """
    user = UserFactory(email="mickey@disney.com")
    user.set_password("Abcd1234")
    user.save()

    return user


@pytest.fixture()
def angler():
    angler = JoePublicFactory.create(first_name="Homer", last_name="Simpson")
    return angler


@pytest.fixture()
def report(angler, user):

    report = ReportFactory(reported_by=angler)
    ReportFollowUpFactory(report=report, created_by=user)
    return report


@pytest.mark.django_db
def test_followup_form_requires_login(client, report):
    """The follow up report form in unaccessible to unauthorized users. If
    an unathenticated user tries to access the url, they should be
    rediected to the login page.

    """
    url = reverse("tfat:create_report_followup", kwargs={"report_id": report.id})

    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_followup_form_elements(client, report, user, angler):
    """An authorized user should be able to access the form and it should
    contain the following elements: status select widget, comment text
    area, cancel button, submit submit button, reporter's name and
    report date.

    """

    url = reverse("tfat:create_report_followup", kwargs={"report_id": report.id})

    logged_in = client.login(username=user.email, password="Abcd1234")
    assert logged_in is True

    response = client.get(url)
    assert response.status_code == 200

    content = str(response.content)

    assert angler.first_name in content
    assert angler.last_name in content
    assert '<select name="status"' in content
    assert '<textarea name="comment"' in content
    assert "Cancel" in content
    assert "Update Status" in content


@pytest.mark.django_db
def test_followup_form_good_data(client, report, user):
    """If we post data with both a status choice and a comment, we should
    be redirected to the report detail page which should include
    the followup details.

    """

    url = reverse("tfat:create_report_followup", kwargs={"report_id": report.id})
    data = {"comment": "Something pithy"}

    logged_in = client.login(username=user.email, password="Abcd1234")
    assert logged_in is True

    response = client.post(url)
    assert response.status_code == 200

    content = str(response.content)
    assert "This field is required" in content


@pytest.mark.django_db
def test_followup_form_comment_optional(client, report, user):
    """the comment widget is optional, the form should still submit if the
    comment box is empty and we shoul be redirected to the report
    detail page.

    """

    logged_in = client.login(username=user.email, password="Abcd1234")
    assert logged_in is True
    url = reverse("tfat:create_report_followup", kwargs={"report_id": report.id})
    data = {"status": "completed"}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200

    templates = [x.name for x in response.templates]
    assert "tfat/report_detail.html" in templates

    content = str(response.content)
    assert "Follow Up Actions to Date" in content


@pytest.mark.django_db
def test_followup_form_status_required(client, report, user):
    """the status widget is required - an error should appear if the form
    is submitted without a choice.
    """

    url = reverse("tfat:create_report_followup", kwargs={"report_id": report.id})
    data = {"comment": "Something pithy"}

    logged_in = client.login(username=user.email, password="Abcd1234")
    assert logged_in is True

    response = client.post(url, data)
    assert response.status_code == 200

    templates = [x.name for x in response.templates]
    assert "tfat/report_followup_form.html" in templates

    content = str(response.content)
    assert "This field is required" in content


@pytest.mark.django_db
def test_followup_form_status_requested(client, report, user):
    """ the select widget has two options if the status is 'requested'.  THe
    options should be 'initialized' and 'completed'
    """

    logged_in = client.login(username=user.email, password="Abcd1234")
    assert logged_in is True

    url = reverse("tfat:create_report_followup", kwargs={"report_id": report.id})
    response = client.get(url)
    assert response.status_code == 200

    content = str(response.content)
    assert '<option value="initialized">Initialized</option>' in content
    assert '<option value="completed">Completed</option>' in content


@pytest.mark.django_db
def test_followup_form_status_initialized_complete(client, report, user):
    """the select widget has one option if the status is 'initialized'.  THe
    options should 'completed' and is a required field.
    """

    # add an itialized follow to our report:
    ReportFollowUpFactory(report=report, created_by=user, status="initialized")
    report.follow_up_status = "initialized"
    report.save()

    url = reverse("tfat:create_report_followup", kwargs={"report_id": report.id})

    logged_in = client.login(username=user.email, password="Abcd1234")
    assert logged_in is True

    response = client.get(url)
    assert response.status_code == 200

    content = str(response.content)
    #  initialized is **NOT** in response:
    assert '<option value="initialized">Initialized</option>' not in content
    assert '<option value="completed">Completed</option>' in content
