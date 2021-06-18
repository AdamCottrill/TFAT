"""=============================================================
 /tfat/tfat/tests/api/test_recovery.py 
 Created: 2021-06-17 15:33:27

 DESCRIPTION:

  integration tests to ensure that the api endpoints for tag recoverys work as
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

from tfat.models import Recovery
from ..factories import (
    LakeFactory,
    ReportFactory,
    SpeciesFactory,
    UserFactory,
    RecoveryFactory,
)


class TestRecoveryAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="hsimpson")
        self.user.set_password("Abcd1234")
        self.user.save()

        huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
        walleye = SpeciesFactory(spc="334", spc_nmco="walleye")
        lake_trout = SpeciesFactory(spc="081", spc_nmco="lake trout")
        report = ReportFactory()

        self.recovery = RecoveryFactory(
            species=walleye,
            lake=huron,
            report=report,
            recovery_date=datetime(2013, 10, 10).replace(tzinfo=pytz.UTC),
            general_location="Off my dock",
            specific_location="The very end.",
            dd_lat=45.00,
            dd_lon=-81.00,
            tlen=500,
            flen=484,
            tagid="123456",
            tagdoc="25012",
            fate="K",
        )

        RecoveryFactory(
            species=lake_trout,
            lake=huron,
            report=report,
            recovery_date=datetime(2013, 10, 10).replace(tzinfo=pytz.UTC),
            general_location="Georgian Bay",
            specific_location="The middle.",
            dd_lat=45.00,
            dd_lon=-81.00,
            tlen=500,
            flen=484,
            tagid="888888",
            tagdoc="25019",
            fate="K",
        )

        RecoveryFactory(
            species=walleye,
            lake=huron,
            report=report,
            recovery_date=datetime(2013, 10, 10).replace(tzinfo=pytz.UTC),
            general_location="Severn Sound",
            specific_location="Midland Harbour.",
            dd_lat=45.00,
            dd_lon=-81.00,
            tlen=500,
            flen=484,
            tagid="555555",
            tagdoc="25020",
            fate="R",
        )

    def test_recovery_api_get_list(self):

        # create a list of dicts that will be used create our objects
        # and tested against the json in the response.

        url = reverse("tfat_api:recovery-list")

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert len(response.data["results"]) == 3

        observed = {x.get("tagid") for x in response.data["results"]}
        assert observed == {"123456", "555555", "888888"}

        observed = {x.get("general_location") for x in response.data["results"]}
        assert observed == {"Off my dock", "Severn Sound", "Georgian Bay"}

    def test_recovery_api_get_detail(self):
        """We should be able to get the details of a single recovery
        object by passing it's recovery code to the url."""

        recovery = self.recovery
        url = reverse("tfat_api:recovery-detail", kwargs={"pk": recovery.id})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        observed = response.data

        expected = [
            "id",
            "report",
            "species",
            "lake",
            "recovery_date",
            "date_flag",
            "general_location",
            "specific_location",
            "dd_lat",
            "dd_lon",
            "latlon_flag",
            "spatial_followup",
            "flen",
            "tlen",
            "rwt",
            "girth",
            "sex",
            "clipc",
            "tagid",
            "_tag_origin",
            "_tag_position",
            "_tag_type",
            "_tag_colour",
            "tagdoc",
            "fate",
            "comment",
        ]

        assert list(observed.keys()) == expected

        # verify that some of the attributes:
        assert observed["general_location"] == recovery.general_location
        assert observed["specific_location"] == recovery.specific_location
        assert observed["dd_lat"] == recovery.dd_lat
        assert observed["dd_lon"] == recovery.dd_lon
        assert observed["tlen"] == recovery.tlen
        assert observed["flen"] == recovery.flen
        assert observed["tagid"] == recovery.tagid
        assert observed["tagdoc"] == recovery.tagdoc

    def test_recovery_api_get_detail_404(self):
        """If we pass in a recovery code that does not exsits, the response
        should be a 404."""

        # make sure there is a least one recovery in our database:

        url = reverse("tfat_api:recovery-detail", kwargs={"pk": 99999999})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_protected_actions(self):
        """the recovery route, should not allow post, put, or delete for
        annonymous users."""

        recovery = self.recovery
        url = reverse("tfat_api:recovery-detail", kwargs={"pk": recovery.id})

        # put
        response = self.client.put(url, data={"prj_nm": "Updated recovery Name"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = self.client.patch(url, data={"prj_nm": "Updated recovery Name"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # delete
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # new recovery:
        url = reverse("tfat_api:recovery-list")
        response = self.client.post(
            url,
            data={
                "report": 123,
                "species": 4,
                "lake": 1,
                "recovery_date": datetime(2018, 10, 10).replace(tzinfo=pytz.UTC),
                "general_location": "Off my dock",
                "specific_location": "The very end.",
                "dd_lat": 45.00,
                "dd_lon": -81.00,
                "spatial_followup": False,
                "tlen": 500,
                "flen": 484,
                "clipc": 5,
                "tagid": "123456",
                "tagdoc": "25012",
                "tag_type": "2",
                "tag_position": "5",
                "tag_origin": "01",
                "tag_colour": "2",
                "fate": "K",
                "tag_removed": False,
            },
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_authenticated_user_can_create_recovery(self):
        """An authenticated user should be able to create a new recovery by submitting
        a post request."""

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        superior = LakeFactory(abbrev="SU", lake_name="Lake Superior")
        rainbow = SpeciesFactory(spc="076", spc_nmco="rainbow trout")
        report = ReportFactory()

        data = {
            "lake": superior.id,
            "species": rainbow.id,
            "report": report.id,
            "recovery_date": "2018-10-10",
            "general_location": "Off my dock",
            "specific_location": "The very end.",
            "dd_lat": 45.00,
            "dd_lon": -81.00,
            "spatial_followup": False,
            "tlen": 500,
            "flen": 484,
            "clipc": 5,
            "tagid": "123456",
            "tagdoc": "25012",
            "tag_type": "2",
            "tag_position": "5",
            "tag_origin": "01",
            "tag_colour": "2",
            "fate": "K",
            "tag_removed": False,
        }

        # new recovery:
        url = reverse("tfat_api:recovery-list")
        response = self.client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED

        # make sure that our newly created recovery has all of the attributes we think it does:
        recovery = Recovery.objects.get(pk=response.data["id"])

        assert recovery.lake_id == superior.id
        assert recovery.species_id == rainbow.id
        assert recovery.report_id == report.id
        assert recovery.general_location == data["general_location"]
        assert recovery.specific_location == data["specific_location"]
        assert recovery.dd_lat == data["dd_lat"]
        assert recovery.dd_lon == data["dd_lon"]
        assert recovery.tlen == data["tlen"]
        assert recovery.flen == data["flen"]
        assert recovery.tagid == data["tagid"]
        assert recovery.fate == data["fate"]

    def test_authenticated_user_can_delete_recovery(self):
        """An authenticated user should be able to delete an existing recovery by
        submitting a delete request to the appropriate endpoint."""

        recovery1 = self.recovery

        # verify that our recovery exists in the database:
        recovery = Recovery.objects.filter(pk=recovery1.id).all()
        assert len(recovery) == 1

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        url = reverse("tfat_api:recovery-detail", kwargs={"pk": recovery1.id})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # verify that our recovery is gone:
        recovery = Recovery.objects.filter(pk=recovery1.id).all()
        assert len(recovery) == 0

    def test_authenticated_user_can_update_recovery(self):
        """An authenticated user should be able to delete an existing recovery by
        submitting a delete request to the appropriate endpoint."""

        # verify that our recovery exists and the attributes we think it does:
        recovery = Recovery.objects.get(pk=self.recovery.id)

        assert recovery.general_location == "Off my dock"
        assert recovery.specific_location == "The very end."
        assert recovery.dd_lat == 45.00
        assert recovery.dd_lon == -81.00
        assert recovery.tlen == 500
        assert recovery.flen == 484
        assert recovery.tagid == "123456"
        assert recovery.fate == "K"

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        url = reverse("tfat_api:recovery-detail", kwargs={"pk": self.recovery.id})

        updates = {
            "general_location": "Town Harbour",
            "specific_location": "The boat launch.",
            "dd_lat": 45.5,
            "dd_lon": -81.5,
            "tlen": 550,
            "flen": 525,
            "tagid": "111111",
            "fate": "R",
        }
        response = self.client.patch(url, data=updates)
        assert response.status_code == status.HTTP_200_OK

        recovery = Recovery.objects.get(pk=self.recovery.id)
        assert recovery.general_location == updates["general_location"]
        assert recovery.specific_location == updates["specific_location"]
        assert recovery.dd_lat == updates["dd_lat"]
        assert recovery.dd_lon == updates["dd_lon"]
        assert recovery.tlen == updates["tlen"]
        assert recovery.flen == updates["flen"]
        assert recovery.tagid == updates["tagid"]
        assert recovery.fate == updates["fate"]
