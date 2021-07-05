"""
=============================================================
~/tfat/tests/api/test_report_filters.py
Created: Jul-05-2021 11:19
DESCRIPTION:

    The tests in this file ensure that the filters available for
    tag report endpoint function as expected.

    Filters:

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

from ..factories import LakeFactory, RecoveryFactory, ReportFactory, SpeciesFactory


@pytest.fixture
def reports():

    superior = LakeFactory(abbrev="SU", lake_name="Lake Superior")
    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
    ontario = LakeFactory(abbrev="ON", lake_name="Lake Ontario")

    walleye = SpeciesFactory(spc="334", spc_nmco="walleye")
    lake_trout = SpeciesFactory(spc="081", spc_nmco="lake trout")
    perch = SpeciesFactory(spc="331", spc_nmco="yellow perch")

    report0 = ReportFactory(
        report_date=datetime(2013, 11, 11).replace(tzinfo=pytz.UTC),
    )

    RecoveryFactory(report=report0, lake=ontario, species=perch)

    report1 = ReportFactory(
        report_date=datetime(2015, 11, 11).replace(tzinfo=pytz.UTC),
    )

    RecoveryFactory(report=report1, lake=huron, species=walleye)

    # this one the only one from a dcr:
    report2 = ReportFactory(
        report_date=datetime(2017, 11, 11).replace(tzinfo=pytz.UTC),
        dcr="ABDC123",
    )

    RecoveryFactory(report=report2, lake=superior, species=lake_trout)

    return [report0, report1, report2]


filter_args = [
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
def test_report_filters(client, reports, filter, expected):
    """The readonly api endpoint for tag reports accept filters that are
    attributes of the report (reporting date) and the recovery (lake, and
    species). There are currently no filters for tag reporter attributes (such
    as first or last name).

    This test is parameterized to accept a list of two element tuples, the first
    element is the filter to apply, the second is the list of indices that
    correspond to the angler records that should be returned in the response.
    The indices are used to extract the id from the fixture and compare those to
    the angler id's returned by the response.

    """

    ids = []
    for i, x in enumerate(reports):
        if i in expected:
            ids.append(x.id)

    url = reverse("tfat_api:report-list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the ids from the response:
    payload = response.data["results"]
    observed_ids = {x["id"] for x in payload}

    assert len(payload) == len(expected)
    assert set(ids) == observed_ids
