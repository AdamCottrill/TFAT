"""=============================================================
 /tfat/tfat/tests/api/test_report.py 
 Created: 2021-06-17 15:33:27

 DESCRIPTION:

  integration tests to ensure that the api endpoints for tag reports work as
  expected:

  - detail
  - list
  - filters

  - authtenciated routes:
      + create
      + update
      + delete



 A. Cottrill
=============================================================

"""


import pytest
import pytz
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tfat.models import Report
from ..factories import JoePublicFactory, ReportFactory, UserFactory


class TestReportAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="hsimpson")
        self.user.set_password("Abcd1234")
        self.user.save()

        self.bart = JoePublicFactory(first_name="Bart", last_name="Simpson")
        barney = JoePublicFactory(first_name="Barney", last_name="Gumble")

        self.report1 = ReportFactory(
            reported_by=self.bart,
            report_date=datetime(2013, 11, 11).replace(tzinfo=pytz.UTC),
            reporting_format="e-mail",
        )

        ReportFactory(
            reported_by=self.bart,
            report_date=datetime(2018, 11, 11).replace(tzinfo=pytz.UTC),
            reporting_format="letter",
        )

        ReportFactory(
            reported_by=barney,
            report_date=datetime(2015, 11, 11).replace(tzinfo=pytz.UTC),
            reporting_format="verbal",
        )

    def test_report_api_get_list(self):

        # create a list of dicts that will be used create our objects
        # and tested against the json in the response.

        url = reverse("tfat_api:report-list")

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert len(response.data["results"]) == 3

        observed = {x.get("reporting_format") for x in response.data["results"]}

        assert observed == {"e-mail", "letter", "verbal"}

    def test_report_api_get_detail(self):
        """We should be able to get the details of a single report
        object by passing it's report code to the url."""

        report = self.report1
        url = reverse("tfat_api:report-detail", kwargs={"pk": report.id})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        observed = response.data
        expected = [
            "id",
            "reported_by",
            "report_date",
            "date_flag",
            "reporting_format",
            "dcr",
            "effort",
            "associated_file",
            "comment",
            "follow_up",
            "follow_up_status",
        ]
        assert list(observed.keys()) == expected

        assert observed["reporting_format"] == report.reporting_format

    def test_report_api_get_detail_404(self):
        """If we pass in a report code that does not exsits, the response
        should be a 404."""

        # make sure there is a least one report in our database:

        url = reverse("tfat_api:report-detail", kwargs={"pk": 99999999})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_protected_actions(self):
        """the report route, should not allow post, put, or delete for
        annonymous users."""

        report = self.report1
        url = reverse("tfat_api:report-detail", kwargs={"pk": report.id})

        # put
        response = self.client.put(url, data={"prj_nm": "Updated report Name"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = self.client.patch(url, data={"prj_nm": "Updated report Name"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # delete
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # new report:
        url = reverse("tfat_api:report-list")
        response = self.client.post(
            url,
            data={
                "reported_by": 1737,
                "report_date": "2020-04-22T00:00:00-04:00",
                "date_flag": 0,
                "reporting_format": "verbal",
                "comment": "a fake comment",
                "follow_up": False,
            },
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_authenticated_user_can_create_report(self):
        """An authenticated user should be able to create a new report by submitting
        a post request."""

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        data = {
            "reported_by": self.bart.id,
            "report_date": "2020-04-22T00:00:00-04:00",
            "date_flag": 0,
            "reporting_format": "verbal",
            "comment": "a fake comment",
            "follow_up": False,
        }

        # new report:
        url = reverse("tfat_api:report-list")
        response = self.client.post(
            url,
            data=data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        # make sure that our newly created report has all of the attributes we think it does:
        report = Report.objects.get(pk=response.data["id"])

        assert report.reported_by_id == self.bart.id
        assert report.reporting_format == "verbal"
        assert report.follow_up == False

    def test_authenticated_user_can_delete_report(self):
        """An authenticated user should be able to delete an existing report by
        submitting a delete request to the appropriate endpoint."""

        report1 = self.report1

        # verify that our report exists in the database:
        report = Report.objects.filter(pk=report1.id).all()
        assert len(report) == 1

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        url = reverse("tfat_api:report-detail", kwargs={"pk": report1.id})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # verify that our report is gone:
        report = Report.objects.filter(pk=report1.id).all()
        assert len(report) == 0

    def test_authenticated_user_can_update_report(self):
        """An authenticated user should be able to delete an existing report by
        submitting a delete request to the appropriate endpoint."""

        report1 = self.report1

        # verify that our report exists and has the name we think it does:
        report = Report.objects.get(pk=report1.id)
        assert report.reporting_format == "e-mail"
        assert report.follow_up == False

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        url = reverse("tfat_api:report-detail", kwargs={"pk": report1.id})

        response = self.client.patch(
            url, data={"reporting_format": "verbal", "follow_up": True}
        )
        assert response.status_code == status.HTTP_200_OK

        report = Report.objects.get(pk=report1.id)
        assert report.reporting_format == "verbal"
        assert report.follow_up == True
