"""
=============================================================
~/tfat/tests/api/test_angler_filters.py
Created: Jul-05-2021 09:33
DESCRIPTION:

    The tests in this file ensure that the filters available for
    anglers function as expected.

    Filters:

      + first_name ("exact", "icontains")
      + last_name ("exact", "icontains")
      + phone ("exact", "icontains")
      + email ("icontains")
      + report_year
      + report_year__gte
      + report_year__lte
      + report_year__gt
      + report_year__lt
      + from_dcr
      + lake
      + lake__not
      + spc
      + spc__not


A. Cottrill
=============================================================
"""

from datetime import datetime

import pytest
import pytz
from django.urls import reverse
from rest_framework import status

from ..factories import (
    JoePublicFactory,
    LakeFactory,
    RecoveryFactory,
    ReportFactory,
    SpeciesFactory,
    UserFactory,
)


@pytest.fixture
def user():
    user = UserFactory(username="bgumble")
    user.set_password("Abcd1234")
    user.save()
    return user


# three anglers
@pytest.fixture
def anglers():

    superior = LakeFactory(abbrev="SU", lake_name="Lake Superior")
    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
    ontario = LakeFactory(abbrev="ON", lake_name="Lake Ontario")

    walleye = SpeciesFactory(spc="334", spc_nmco="walleye")
    lake_trout = SpeciesFactory(spc="081", spc_nmco="lake trout")
    perch = SpeciesFactory(spc="331", spc_nmco="yellow perch")

    homer = JoePublicFactory(
        first_name="homer",
        last_name="Simpson",
        address1="742 Evergreen Tarrace",
        address2="Box 123",
        town="Springfield",
        province="Ontario",
        postal_code="N0W2T2",
        email="homer@simpsons.com",
        phone="555-321-1234",
    )

    bart = JoePublicFactory(
        first_name="Bart",
        last_name="Simpson",
        address1="742 Evergreen Tarrace",
        address2="Box 123",
        town="Springfield",
        province="Ontario",
        postal_code="N0W2T2",
        email="bart@simpsons.com",
        phone="555-321-1234",
    )
    barney = JoePublicFactory(
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

    report0 = ReportFactory(
        reported_by=homer,
        report_date=datetime(2013, 11, 11).replace(tzinfo=pytz.UTC),
    )

    RecoveryFactory(report=report0, lake=ontario, species=perch)

    report1 = ReportFactory(
        reported_by=bart,
        report_date=datetime(2015, 11, 11).replace(tzinfo=pytz.UTC),
    )

    RecoveryFactory(report=report1, lake=huron, species=walleye)

    # this one the only one from a dcr:
    report2 = ReportFactory(
        reported_by=barney,
        report_date=datetime(2017, 11, 11).replace(tzinfo=pytz.UTC),
        dcr="ABDC123",
    )

    RecoveryFactory(report=report2, lake=superior, species=lake_trout)

    return [homer, bart, barney]


filter_args = [
    # angler attributes
    ({"first_name": "homer"}, [0]),
    ({"first_name__like": "bar"}, [1, 2]),
    ({"last_name": "simpson"}, [0, 1]),
    ({"last_name__like": "simp"}, [0, 1]),
    ({"phone": "555-321-1234"}, [0, 1]),
    ({"phone__like": "1234"}, [0, 1, 2]),
    ({"email": "homer@simpsons.com"}, [0]),
    ({"email__like": "simpsons.com"}, [0, 1]),
    # report attributes
    ({"report_year": "2015"}, [1]),
    ({"report_year__gte": "2015"}, [1, 2]),
    ({"report_year__gt": "2015"}, [2]),
    ({"report_year__lte": "2015"}, [0, 1]),
    ({"report_year__lt": "2015"}, [0]),
    ({"from_dcr": True}, [2]),
    # recovery attributes
    ({"lake": "ON"}, [0]),
    ({"lake": "HU,SU"}, [1, 2]),
    ({"lake__not": "HU"}, [0, 2]),
    ({"spc": "081"}, [2]),
    ({"spc": "081,334"}, [1, 2]),
    ({"spc__not": "334"}, [0, 2]),
]


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_angler_filters(client, user, anglers, filter, expected):
    """The readonly api endpoint for anglers objects accepts filters that are
    associated with attributes of the reporting angler (first name, last name,
    phone number and email), attributes of the report (reporting date) and the
    recovery (lake, and species).

    This test is parameterized to accept a list of two element tuples, the first
    element is the filter to apply, the second is the list of indices that
    correspond to the angler records that should be returned in the response.
    The indices are used to extract the id from the fixture and compare those
    to the angler id's returned by the response.

    """

    ids = []
    for i, x in enumerate(anglers):
        if i in expected:
            ids.append(x.id)

    login = client.login(username=user.email, password="Abcd1234")
    assert login is True
    url = reverse("tfat_api:joepublic-list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the ids from the response:
    payload = response.data["results"]
    observed_ids = {x["id"] for x in payload}

    assert len(payload) == len(expected)
    assert set(ids) == observed_ids
