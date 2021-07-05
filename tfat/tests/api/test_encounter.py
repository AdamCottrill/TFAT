"""=============================================================
 /tfat/tfat/tests/api/test_encounter.py
 Created: 2021-06-17 15:33:27

 DESCRIPTION:

  integration tests to ensure that the api endpoints for tag encounters work as
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


from datetime import datetime

import pytest
import pytz
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tfat.models import Encounter

from ..factories import (
    EncounterFactory,
    LakeFactory,
    ProjectFactory,
    SpeciesFactory,
    UserFactory,
)


class TestencounterAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="hsimpson")
        self.user.set_password("Abcd1234")
        self.user.save()

        huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
        walleye = SpeciesFactory(spc="334", spc_nmco="walleye")
        lake_trout = SpeciesFactory(spc="081", spc_nmco="lake trout")
        project = ProjectFactory(lake=huron)

        self.encounter = EncounterFactory(
            project=project,
            species=walleye,
            sam="1001",
            eff="001",
            grp="55",
            fish="123698",
            # observation_date = '2013-11-11'
            observation_date=datetime(2013, 11, 11).replace(tzinfo=pytz.UTC),
            grid="1940",
            dd_lat=45.550,
            dd_lon=-80.125,
            flen=525,
            tlen=535,
            rwt=2500,
            age=12,
            sex="2",
            clipc=0,
            tagid="1234",
            tagdoc="25012",
        )

        EncounterFactory(
            project=project,
            species=walleye,
            sam="1002",
            eff="001",
            # observation_date = '2013-11-11'
            observation_date=datetime(2013, 11, 12).replace(tzinfo=pytz.UTC),
            grid="1940",
            dd_lat=45.50,
            dd_lon=-80.25,
            flen=425,
            tlen=435,
            rwt=1500,
            age=7,
            sex="2",
            clipc=0,
            tagid="12345",
            tagdoc="25012",
        )

        EncounterFactory(
            project=project,
            species=lake_trout,
            sam="1003",
            eff="001",
            # observation_date = '2013-11-11'
            observation_date=datetime(2013, 11, 12).replace(tzinfo=pytz.UTC),
            grid="1940",
            dd_lat=45.40,
            dd_lon=-80.15,
            flen=625,
            tlen=635,
            rwt=3500,
            age=9,
            sex="1",
            clipc=5,
            tagid="54321",
            tagdoc="25019",
        )

    def test_encounter_api_get_list(self):

        # create a list of dicts that will be used create our objects
        # and tested against the json in the response.

        url = reverse("tfat_api:encounter-list")

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert len(response.data["results"]) == 3

        observed = {x.get("tagid") for x in response.data["results"]}
        assert observed == {"1234", "12345", "54321"}

    def test_encounter_api_get_detail(self):
        """We should be able to get the details of a single encounter
        object by passing it's encounter code to the url."""

        encounter = self.encounter
        url = reverse("tfat_api:encounter-detail", kwargs={"pk": encounter.id})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        observed = response.data

        expected = [
            "id",
            "fish_label",
            "project",
            "species",
            "sam",
            "eff",
            "grp",
            "fish",
            "observation_date",
            "grid",
            "dd_lat",
            "dd_lon",
            "flen",
            "tlen",
            "rwt",
            "age",
            "sex",
            "clipc",
            "tagid",
            "tagdoc",
            "tagstat",
            "fate",
            "comment",
        ]

        assert list(observed.keys()) == expected

        # verify that some of the attributes:
        assert observed["sam"] == encounter.sam
        assert observed["eff"] == encounter.eff
        assert observed["grp"] == encounter.grp
        assert observed["fish"] == encounter.fish
        # assert observed["observation_date"] == encounter.observation_date
        assert observed["grid"] == encounter.grid
        assert observed["dd_lat"] == encounter.dd_lat
        assert observed["dd_lon"] == encounter.dd_lon
        assert observed["flen"] == encounter.flen
        assert observed["tlen"] == encounter.tlen
        assert observed["rwt"] == encounter.rwt
        assert observed["age"] == encounter.age
        assert observed["sex"] == encounter.sex
        assert observed["clipc"] == str(encounter.clipc)
        assert observed["tagid"] == encounter.tagid
        assert observed["tagdoc"] == encounter.tagdoc
        assert observed["tagstat"] == encounter.tagstat
        assert observed["fate"] == encounter.fate
        assert observed["comment"] == encounter.comment

    def test_encounter_api_get_detail_404(self):
        """If we pass in a encounter code that does not exsits, the response
        should be a 404."""

        # make sure there is a least one encounter in our database:

        url = reverse("tfat_api:encounter-detail", kwargs={"pk": 99999999})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_protected_actions(self):
        """the encounter route, should not allow post, put, or delete for
        annonymous users."""

        encounter = self.encounter
        url = reverse("tfat_api:encounter-detail", kwargs={"pk": encounter.id})

        # patch
        response = self.client.patch(
            url,
            data={
                "sam": "03096",
                "eff": "1",
                "grp": "00",
                "fish": "00008",
            },
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # delete
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        project = ProjectFactory()
        species = SpeciesFactory()

        data = {
            "project": project.id,
            "species": species.id,
            "sam": "03096",
            "eff": "1",
            "grp": "00",
            "fish": "00008",
            "observation_date": "2004-09-27",
            "grid": "3228",
            "dd_lat": 43.6986,
            "dd_lon": -81.8848,
            "flen": 588,
            "tlen": 618,
            "rwt": 2075,
            "age": 9,
            "sex": "",
            "clipc": "0",
            "tagid": "170873",
            "tagdoc": "03",
            "tagstat": "C",
            "fate": "K",
            "comment": "Tag doc - MDNR",
        }

        response = self.client.patch(url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # new encounter:
        url = reverse("tfat_api:encounter-list")
        response = self.client.post(url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_authenticated_user_can_create_encounter(self):
        """An authenticated user should be able to create a new encounter by submitting
        a post request."""

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        project = ProjectFactory()
        species = SpeciesFactory()

        data = {
            "project": project.id,
            "species": species.id,
            "sam": "03096",
            "eff": "1",
            "grp": "00",
            "fish": "00008",
            "observation_date": "2004-09-27",
            "grid": "3228",
            "dd_lat": 43.6986,
            "dd_lon": -81.8848,
            "flen": 588,
            "tlen": 618,
            "rwt": 2075,
            "age": 9,
            "sex": "",
            "clipc": "0",
            "tagid": "170873",
            "tagdoc": "03",
            "tagstat": "C",
            "fate": "K",
            "comment": "Tag doc - MDNR",
        }

        # new encounter:
        url = reverse("tfat_api:encounter-list")
        response = self.client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED

        # make sure that our newly created encounter has all of the attributes we think it does:
        encounter = Encounter.objects.get(pk=response.data["id"])

        assert encounter.species_id == species.id
        assert encounter.project_id == project.id
        assert encounter.sam == data["sam"]
        assert encounter.eff == data["eff"]
        assert encounter.grp == data["grp"]
        assert encounter.fish == data["fish"]
        assert encounter.dd_lat == data["dd_lat"]
        assert encounter.dd_lon == data["dd_lon"]
        assert encounter.tlen == data["tlen"]
        assert encounter.flen == data["flen"]
        assert encounter.tagid == data["tagid"]
        assert encounter.fate == data["fate"]

    def test_authenticated_user_can_delete_encounter(self):
        """An authenticated user should be able to delete an existing encounter by
        submitting a delete request to the appropriate endpoint."""

        encounter1 = self.encounter

        # verify that our encounter exists in the database:
        encounter = Encounter.objects.filter(pk=encounter1.id).all()
        assert len(encounter) == 1

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        url = reverse("tfat_api:encounter-detail", kwargs={"pk": encounter1.id})
        response = self.client.delete(url)

        # verify that our encounter is gone:
        encounter = Encounter.objects.filter(pk=encounter1.id).all()
        assert len(encounter) == 0

    def test_authenticated_user_can_update_encounter(self):
        """An authenticated user should be able to delete an existing encounter by
        submitting a delete request to the appropriate endpoint."""

        # verify that our encounter exists and the attributes we think it does:
        encounter = Encounter.objects.get(pk=self.encounter.id)

        assert encounter.sam == "1001"
        assert encounter.eff == "001"
        assert encounter.grp == "55"
        assert encounter.fish == "123698"
        assert encounter.dd_lat == 45.55
        assert encounter.dd_lon == -80.125
        assert encounter.tlen == 535
        assert encounter.flen == 525
        assert encounter.tagid == "1234"
        assert encounter.fate == "K"

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        url = reverse("tfat_api:encounter-detail", kwargs={"pk": self.encounter.id})

        updates = {
            "sam": "03096",
            "eff": "1",
            "grp": "00",
            "fish": "00008",
            "dd_lat": 45.5,
            "dd_lon": -81.5,
            "tlen": 550,
            "flen": 525,
            "tagid": "111111",
            "fate": "R",
        }
        response = self.client.patch(url, data=updates)
        assert response.status_code == status.HTTP_200_OK

        encounter = Encounter.objects.get(pk=self.encounter.id)

        assert encounter.sam == updates["sam"]
        assert encounter.eff == updates["eff"]
        assert encounter.grp == updates["grp"]
        assert encounter.fish == updates["fish"]
        assert encounter.dd_lat == updates["dd_lat"]
        assert encounter.dd_lon == updates["dd_lon"]
        assert encounter.tlen == updates["tlen"]
        assert encounter.flen == updates["flen"]
        assert encounter.tagid == updates["tagid"]
        assert encounter.fate == updates["fate"]
