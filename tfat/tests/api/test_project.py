"""=============================================================
 /tfat/tfat/tests/api/test_project.py
 Created: 29 Apr 2021 14:13:57

 DESCRIPTION:

  integration tests to ensure that the api endpoints work as expected:


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

from collections import OrderedDict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tfat.models import Project
from ..factories import LakeFactory, ProjectFactory, UserFactory


class TestProjectAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="hsimpson")
        self.user.set_password("Abcd1234")
        self.user.save()

    def test_project_api_get_list(self):

        # create a list of dicts that will be used create our objects
        # and tested against the json in the response.
        objects = [
            dict(prj_cd="LHA_IA09_001", prj_nm="Huron Project "),
            dict(prj_cd="LSA_IA09_001", prj_nm="Superior Project "),
            dict(prj_cd="LEU_IA09_001", prj_nm="Erie Project "),
        ]

        for obj in objects:
            ProjectFactory(**obj)

        url = reverse("tfat_api:project-list")

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert len(response.data["results"]) == 3

        observed = {x.get("prj_cd") for x in response.data["results"]}
        expected = {x.get("prj_cd") for x in objects}

        assert observed == expected

    def test_project_api_get_detail(self):
        """We should be able to get the details of a single Project
        object by passing it's project code to the url."""

        prj_cd = "LHA_IA20_123"
        prj_nm = "Huron Project"

        ProjectFactory(prj_cd=prj_cd, prj_nm=prj_nm)

        url = reverse("tfat_api:project-detail", kwargs={"prj_cd": prj_cd})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        observed = response.data

        expected = ["id", "year", "prj_cd", "prj_nm", "slug", "lake"]
        assert list(observed.keys()) == expected

        assert observed["prj_cd"] == prj_cd
        assert observed["prj_nm"] == prj_nm

    def test_project_api_get_detail_404(self):
        """If we pass in a project code that does not exsits, the response
        should be a 404."""

        # make sure there is a least one project in our database:
        prj_cd = "LHA_IA20_123"
        prj_nm = "Huron Project"
        ProjectFactory(prj_cd=prj_cd, prj_nm=prj_nm)

        url = reverse("tfat_api:project-detail", kwargs={"prj_cd": "LHA_CF10_999"})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_protected_actions(self):
        """the project route, should not allow post, put, or delete for
        annonymous users."""

        prj_cd = "LHA_IA20_123"
        prj_nm = "Huron Project"
        ProjectFactory(prj_cd=prj_cd, prj_nm=prj_nm)

        # post
        url = reverse("tfat_api:project-detail", kwargs={"prj_cd": "LHA_CF10_999"})
        # put
        response = self.client.put(url, data={"prj_nm": "Updated Project Name"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # delete
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # new project:
        url = reverse("tfat_api:project-list")
        response = self.client.post(
            url,
            data={
                "prj_cd": "LHA_IA18_123",
                "prj_nm": "New Project",
            },
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_authenticated_user_can_create_project(self):
        """An authenticated user should be able to create a new project by submitting
        a post request."""

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        # make sure our lake exists before we try to create a project asscoiated with it
        # lakes cannot be created though the api:
        lake_data = {"abbrev": "HU", "lake_name": "Huron"}
        lake = LakeFactory(**lake_data)

        data = {
            "prj_cd": "LHA_IA18_123",
            "prj_nm": "New Project",
            "year": 2018,
            "slug": "lha_ia18_123",
            "lake": lake.id,
        }

        # new project:
        url = reverse("tfat_api:project-list")
        response = self.client.post(
            url,
            data=data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        # make sure that our newly created project has all of the attributes we think it does:
        project = Project.objects.get(prj_cd=data["prj_cd"])

        assert project.prj_nm == data["prj_nm"]
        assert project.year == data["year"]
        assert project.lake.abbrev == lake_data["abbrev"]

    def test_authenticated_user_can_delete_project(self):
        """An authenticated user should be able to delete an existing project by
        submitting a delete request to the appropriate endpoint."""

        prj_cd = "LHA_IA20_123"
        prj_nm = "Huron Project"
        ProjectFactory(prj_cd=prj_cd, prj_nm=prj_nm)

        # verify that our project exists in the database:
        project = Project.objects.filter(prj_cd=prj_cd).all()
        assert len(project) == 1

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        url = reverse("tfat_api:project-detail", kwargs={"prj_cd": prj_cd})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # verify that our project is gone:
        project = Project.objects.filter(prj_cd=prj_cd).all()
        assert len(project) == 0

    def test_authenticated_user_can_update_project(self):
        """An authenticated user should be able to delete an existing project by
        submitting a delete request to the appropriate endpoint."""

        prj_cd = "LHA_IA20_123"
        prj_nm = "Huron Project"
        new_prj_nm = "New Project Name"

        ProjectFactory(prj_cd=prj_cd, prj_nm=prj_nm)

        # verify that our project exists and has the name we think it does:
        project = Project.objects.get(prj_cd=prj_cd)
        assert project.prj_nm == prj_nm

        login = self.client.login(username=self.user.email, password="Abcd1234")
        assert login is True

        url = reverse("tfat_api:project-detail", kwargs={"prj_cd": prj_cd})

        response = self.client.patch(url, data={"prj_nm": new_prj_nm})
        assert response.status_code == status.HTTP_200_OK

        project = Project.objects.get(prj_cd=prj_cd)
        assert project.prj_nm == new_prj_nm
