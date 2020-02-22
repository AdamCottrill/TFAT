"""This file contains a number of integration_tests that ensure the
report follow up functionality works as expected.

+ follow up report form in unaccessible to unauthorized users

+ the form contains the elements: status, comment, cancel, submit

+ the status widget is required - an error should appear if the form
is submitted without a choice.

+ the comment widget is optional

+ the select widget has two options if the status is 'requested'.  THe
options should be 'initiated' and 'completed'

+ the select widget has one option if the status is 'initiated'.  THe
options should 'completed' and is a required field.

+ the cancel and submit buttons return us to the report detail page or the report
list, depending on where we came from.

+ after the form is submitted, the detail page should contain a
message indicting that the follow up was completed, by whom, when, and
optionally the comment.

"""

import pytest
import pytz

# import unittest
from django.test import TestCase
from django.urls import reverse

from tfat.tests.factories import UserFactory, JoePublicFactory, ReportFactory

# from datetime import datetime


class ReportFollowUpTestCase(TestCase):
    def setUp(self):

        self.password = "Abcd1234"
        self.email = "micky@disney.com"
        self.user = UserFactory(email=self.email, password=self.password)
        self.joe = JoePublicFactory()
        self.report = ReportFactory(reported_by=self.joe)

    @pytest.mark.django_db
    def test_followup_form_requires_login(self):
        """The follow up report form in unaccessible to unauthorized users. If
        an unathenticated user tries to access the url, they should be
        rediected to the login page.

        """
        url = reverse(
            "tfat:create_report_followup", kwargs={"report_id": self.report.id}
        )

        response = self.client.get(url)
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_followup_form_elements(self):
        """An authorized user should be able to access the form and it should
        contain the following elements: status select widget, comment text
        area, cancel button, submit submit button, reporter's name and
        report date.

        """

        url = reverse(
            "tfat:create_report_followup", kwargs={"report_id": self.report.id}
        )

        self.client.force_login(self.user)
        response = self.client.get(url)
        assert response.status_code == 200

        content = str(response.content)

        assert self.joe.first_name in content
        assert self.joe.last_name in content
        assert '<select name="status"' in content
        assert '<textarea name="comment"' in content
        assert "Cancel" in content
        assert "Update Status" in content

    def test_followup_form_good_data(self):
        """If we post data with both a status choice and a comment, we should
        be redirected to the report detail page which should include
        the followup details.

        """

        url = reverse(
            "tfat:create_report_followup", kwargs={"report_id": self.report.id}
        )

        data = {"comment": "Something pithy"}

        self.client.force_login(self.user)
        response = self.client.post(url)
        assert response.status_code == 200

        content = str(response.content)
        assert "This field is required" in content

    def test_followup_form_status_required(self):
        """the status widget is required - an error should appear if the form
        is submitted without a choice.
        """

        url = reverse(
            "tfat:create_report_followup", kwargs={"report_id": self.report.id}
        )

        data = {"comment": "Something pithy"}

        self.client.force_login(self.user)
        response = self.client.post(url)
        assert response.status_code == 200

        content = str(response.content)
        assert "This field is required" in content

    # def test_followup_form_comment_optional(client, db_setup):
    #     """the comment widget is optional, the form should still submit if the
    #     comment box is empty.
    #     """
    #     assert 0 == 1

    # def test_followup_form_status_requested(client, db_setup):
    #     """ the select widget has two options if the status is 'requested'.  THe
    #     options should be 'initiated' and 'completed'
    #     """
    #     assert 0 == 1

    # def test_followup_form_status_initiated_complete(client, db_setup):
    #     """the select widget has one option if the status is 'initiated'.  THe
    #     options should 'completed' and is a required field.
    #     """
    #     assert 0 == 1

    # def test_followup_form_duplicate_status(client, db_setup):
    #     """- this might be better as a unit test rather than a integration
    #     test - we might not be able to sumbit a duplicate here ("Not a
    #     valid selection".)

    #     """
    #     assert 0 == 1

    # def test_followup_form_cancel_redirects_to_report_detail(client, db_setup):
    #     """If we access the followup form from the report detail - we should
    #     be redirected back there if we click cancel.  The status of the
    #     report followup should not change and follow up details should NOT
    #     included in the response

    #     """
    #     assert 0 == 1

    # def test_followup_form_cancel_redirects_to_report_list(client, db_setup):
    #     """If we access the followup form from the report list - we should be
    #     redirected back there if we click cancel.  The status of the report
    #     followup should not change.

    #     """
    #     assert 0 == 1

    # def test_followup_form_submit_redirects_to_report_detail(client, db_setup):
    #     """If we access the followup form from the report detail - we should
    #     be redirected back there if we click submit.  The status of the
    #     report followup should have changed and the follow up details should
    #     be included in the response
    #     """
    #     assert 0 == 1

    # def test_followup_form_submit_redirects_to_report_list(client, db_setup):
    #     """If we access the followup form from the report list - we should be
    #     redirected back there if we click submit.  The status of the report
    #     followup should not change.
    #     """
    #     assert 0 == 1
