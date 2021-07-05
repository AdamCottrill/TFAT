"""
=============================================================
~\tfat\tests\api\test_project_filters.py
Created: Jul-05-2021 14:52
DESCRIPTION:

    The tests in this file ensure that the filters available for
    tagging project endpoint function as expected.

    Filters:


    + year
    + year__gte
    + year__lte
    + year__gt
    + year__lt
    + prj_cd
    + prj_cd__not
    + prj_cd__like
    + prj_cd__not_like
    + prj_cd__endswith
    + prj_cd__not_endswith
    + prj_nm__like
    + prj_nm__not_like
    + spc
    + spc__not
    + tagstat



A. Cottrill
=============================================================
"""

from datetime import datetime

import pytest
import pytz
from django.urls import reverse
from rest_framework import status

from ..factories import EncounterFactory, LakeFactory, ProjectFactory, SpeciesFactory


@pytest.fixture
def projects():

    superior = LakeFactory(abbrev="SU", lake_name="Lake Superior")
    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
    ontario = LakeFactory(abbrev="ON", lake_name="Lake Ontario")

    walleye = SpeciesFactory(spc="334", spc_nmco="walleye")
    lake_trout = SpeciesFactory(spc="081", spc_nmco="lake trout")
    perch = SpeciesFactory(spc="331", spc_nmco="yellow perch")

    project0 = ProjectFactory(
        year="2012", prj_cd="LSA_IS12_123", prj_nm="Superior Index", lake=superior
    )

    EncounterFactory(project=project0, species=perch, tagstat="A")

    project1 = ProjectFactory(
        year="2015",
        prj_cd="LHA_IA15_ABC",
        prj_nm="Huron Community Index Netting",
        lake=huron,
    )

    EncounterFactory(project=project1, species=walleye, tagstat="A")

    project2 = ProjectFactory(
        year="2017",
        prj_cd="LOA_SC17_XYZ",
        prj_nm="Lake Ontario Sport Creel",
        lake=ontario,
    )

    EncounterFactory(project=project2, species=lake_trout, tagstat="C")

    return [project0, project1, project2]


filter_args = [
    ({"lake": "ON"}, [2]),
    ({"lake": "HU,SU"}, [0, 1]),
    ({"lake__not": "HU,SU"}, [2]),
    ({"lake__not": "HU"}, [0, 2]),
    ({"year": "2015"}, [1]),
    ({"year__gte": "2015"}, [1, 2]),
    ({"year__lte": "2015"}, [0, 1]),
    ({"year__gt": "2015"}, [2]),
    ({"year__lt": "2015"}, [0]),
    ({"prj_cd": "LHA_IA15_ABC"}, [1]),
    ({"prj_cd__not": "LHA_IA15_ABC"}, [0, 2]),
    ({"prj_cd__like": "Ia15"}, [1]),
    ({"prj_cd__not_like": "Ia15"}, [0, 2]),
    ({"prj_cd__endswith": "xyZ"}, [2]),
    ({"prj_nm__like": "creel"}, [2]),
    ({"prj_nm__not_like": "creel"}, [0, 1]),
    ({"spc": "081"}, [2]),
    ({"spc": "081,334"}, [1, 2]),
    ({"spc__not": "081"}, [0, 1]),
    ({"spc__not": "081,334"}, [0]),
    ({"tagstat": "A"}, [0, 1]),
    ({"tagstat": "C"}, [2]),
    ({"tagstat": "A,C"}, [0, 1, 2]),
]


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_project_filters(client, projects, filter, expected):
    """The readonly api endpoint for tagging projocts accept filters that are
    attributes of the project (year, lake, project code, project name) and the
    tagging/recovery events (tag stat and species encountered).

    This test is parameterized to accept a list of two element tuples, the first
    element is the filter to apply, the second is the list of indices that
    correspond to the angler records that should be returned in the response.
    The indices are used to extract the id from the fixture and compare those to
    the angler id's returned by the response.

    """

    ids = []
    for i, x in enumerate(projects):
        if i in expected:
            ids.append(x.id)

    url = reverse("tfat_api:project-list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the ids from the response:
    payload = response.data["results"]
    observed_ids = {x["id"] for x in payload}

    assert len(payload) == len(expected)
    assert set(ids) == observed_ids
