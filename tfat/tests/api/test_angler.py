"""=============================================================
 /tfat/tfat/tests/api/test_angler.py 
 Created: 2021-06-17 18:03:33

 DESCRIPTION:

  integration tests to ensure that the api endpoints for anglers work as
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

from tfat.models import JoePublic
from ..factories import JoePublicFactory, UserFactory


class TestAnglerAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="hsimpson")
        self.user.set_password("Abcd1234")
        self.user.save()

        self.bart = JoePublicFactory(
            first_name="Bart",
            last_name="Simpson",
            address1="742 Evergreen Tarrace",
            address2="Box 123",
            town="Springfield",
            province="Ontario",
            postal_code="N0W2T2",
            email="elbarto@gmail.com",
            phone="555-321-1234",
        )
        JoePublicFactory(
            first_name="Barney",
            last_name="Gumble",
            address1="999 Evergreen Tarrace",
            address2="Box 999",
            town="Springfield",
            province="Ontario",
            postal_code="N0W2T2",
            email="barney@yahoo.com",
            phone="555-987-1234",
        )
        JoePublicFactory(
            first_name="Monty",
            last_name="Burns",
            address1="1597 BooYah Blvd",
            town="Springfield",
            province="Ontario",
            postal_code="N0W2T2",
            email="monty@burns.com",
            phone="555-321-4321",
        )

    def test_angler_api_get_list(self):

        # create a list of dicts that will be used create our objects
        # and tested against the json in the response.

        url = reverse("tfat_api:joepublic-list")

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert len(response.data["results"]) == 3

        observed = {x.get("first_name") for x in response.data["results"]}

        assert observed == {"Barney", "Bart", "Monty"}

    def test_angler_api_get_detail(self):
        """We should be able to get the details of a single angler
        object by passing it's id to the url."""

        angler = self.bart
        url = reverse("tfat_api:joepublic-detail", kwargs={"pk": angler.id})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        observed = response.data
        expected = [
            "id",
            "first_name",
            "last_name",
            "initial",
            "address1",
            "address2",
            "town",
            "province",
            "postal_code",
            "email",
            "phone",
            "affiliation",
        ]
        assert list(observed.keys()) == expected

        assert observed["first_name"] == angler.first_name
        assert observed["last_name"] == angler.last_name
        assert observed["address1"] == angler.address1
        assert observed["address2"] == angler.address2
        assert observed["town"] == angler.town
        assert observed["province"] == angler.province
        assert observed["postal_code"] == angler.postal_code
        assert observed["email"] == angler.email
        assert observed["phone"] == angler.phone

    def test_angler_api_get_detail_404(self):
        """If we pass in a angler code that does not exsits, the response
        should be a 404."""

        # make sure there is a least one angler in our database:

        url = reverse("tfat_api:joepublic-detail", kwargs={"pk": 9999})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_protected_actions(self):
        """the angler route, should not allow post, put, or delete for
        annonymous users."""

        angler = self.bart
        url = reverse("tfat_api:joepublic-detail", kwargs={"pk": angler.id})

        # put
        response = self.client.put(url, data={"prj_nm": "Updated angler Name"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = self.client.patch(url, data={"prj_nm": "Updated angler Name"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # delete
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # new angler:
        url = reverse("tfat_api:joepublic-list")
        response = self.client.post(
            url,
            data={
                "first_name": "Crusty",
                "last_name": "TheClown",
                "address1": "1597 BooYah Blvd",
                "town": "Springfield",
                "province": "Ontario",
                "postal_code": "N0W2T2",
                "email": "crusty@clown.com",
                "phone": "555-321-9999",
            },
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_authenticated_user_can_create_angler(self):
        """An authenticated user should be able to create a new angler by submitting
        a post request."""

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        data = {
            "first_name": "Crusty",
            "last_name": "TheClown",
            "address1": "1597 BooYah Blvd",
            "town": "Springfield",
            "province": "ON",
            "postal_code": "N0W2T2",
            "email": "crusty@clown.com",
            "phone": "555-321-9999",
        }

        # new angler:
        url = reverse("tfat_api:joepublic-list")
        response = self.client.post(
            url,
            data=data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        # make sure that our newly created angler has all of the attributes we think it does:
        angler = JoePublic.objects.get(pk=response.data["id"])

        assert angler.first_name == "Crusty"
        assert angler.last_name == "TheClown"
        assert angler.address1 == "1597 BooYah Blvd"
        assert angler.town == "Springfield"
        assert angler.province == "ON"
        assert angler.postal_code == "N0W2T2"
        assert angler.email == "crusty@clown.com"
        assert angler.phone == "555-321-9999"

    def test_authenticated_user_can_delete_angler(self):
        """An authenticated user should be able to delete an existing angler by
        submitting a delete request to the appropriate endpoint."""

        angler1 = self.bart

        # verify that our angler exists in the database:
        angler = JoePublic.objects.filter(pk=angler1.id).all()
        assert len(angler) == 1

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        url = reverse("tfat_api:joepublic-detail", kwargs={"pk": angler1.id})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        angler = JoePublic.objects.filter(pk=angler1.id).all()
        # verify that our angler is gone:
        assert len(angler) == 0

    def test_authenticated_user_can_update_angler(self):
        """An authenticated user should be able to update the attributes of an
        existing angler by submitting a put/pathc request to the appropriate
        endpoint."""

        angler1 = self.bart

        # verify that our angler exists and has the name we think it does:
        angler = JoePublic.objects.get(pk=angler1.id)

        assert angler.first_name == "Bart"
        assert angler.last_name == "Simpson"
        assert angler.address1 == "742 Evergreen Tarrace"
        assert angler.email == "elbarto@gmail.com"
        assert angler.phone == "555-321-1234"

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        url = reverse("tfat_api:joepublic-detail", kwargs={"pk": angler1.id})

        response = self.client.patch(
            url,
            data={
                "first_name": "Betty",
                "last_name": "Sampson",
                "address1": "742 Evergreen Terrace",
                "email": "betty@gmail.com",
                "phone": "555-321-4321",
            },
        )
        assert response.status_code == status.HTTP_200_OK

        angler = JoePublic.objects.get(pk=angler1.id)
        assert angler.first_name == "Betty"
        assert angler.last_name == "Sampson"
        assert angler.address1 == "742 Evergreen Terrace"
        assert angler.email == "betty@gmail.com"
        assert angler.phone == "555-321-4321"
