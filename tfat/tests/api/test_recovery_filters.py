"""
=============================================================
~/tfat/tests/api/test_recovery_filters.py
Created: Jul-05-2021 11:27
DESCRIPTION:

    The tests in this file ensure that the filters available for
    tag recovery endpoint function as expected.

    Filters:

      + recovery_year
      + recovery_year__gte
      + recovery_year__lte
      + recovery_year__gt
      + recovery_year__lt
      + from_dcr
      + lake
      + lake__not
      + spc
      + spc__not
      + tagid
      + tagid__like
      + tagdoc
      + tagdoc__not
      + tagdoc__like
      + tag_origin
      + tag_origin__not
      + tag_position
      + tag_position__not
      + tag_type
      + tag_type__not
      + tag_colour
      + tag_colour__not
      + tlen
      + tlen__gte
      + tlen__lte
      + tlen__gt
      + tlen__lt
      + flen
      + flen__gte
      + flen__lte
      + flen__gt
      + flen__lt
      + rwt
      + rwt__null
      + rwt__gte
      + rwt__lte
      + rwt__gt
      + rwt__lt
      + sex
      + sex__not
      + sex__null
      + clipc
      + clipc__not
      + clipc__null
      + clipc__like
      + clipc__not_like
      + fate
      + fate__not



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
def recoveries():

    superior = LakeFactory(abbrev="SU", lake_name="Lake Superior")
    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")
    ontario = LakeFactory(abbrev="ON", lake_name="Lake Ontario")

    walleye = SpeciesFactory(spc="334", spc_nmco="walleye")
    lake_trout = SpeciesFactory(spc="081", spc_nmco="lake trout")
    perch = SpeciesFactory(spc="331", spc_nmco="yellow perch")

    report0 = ReportFactory(
        report_date=datetime(2013, 11, 11).replace(tzinfo=pytz.UTC),
    )

    report1 = ReportFactory(
        report_date=datetime(2015, 11, 11).replace(tzinfo=pytz.UTC),
    )

    report2 = ReportFactory(
        report_date=datetime(2017, 11, 11).replace(tzinfo=pytz.UTC), dcr="ABDC123"
    )

    fish0 = RecoveryFactory(
        lake=huron,
        species=walleye,
        report=report0,
        recovery_date=datetime(2013, 11, 11).replace(tzinfo=pytz.UTC),
        flen=225,
        tlen=250,
        rwt=None,
        clipc="0",
        sex=9,
        fate="K",
        tagid="1111",
        tagdoc="25012",
        tag_type="2",
        tag_position="5",
        tag_origin="01",
        tag_colour="2",
    )
    fish1 = RecoveryFactory(
        lake=huron,
        species=perch,
        report=report0,
        recovery_date=datetime(2013, 11, 11).replace(tzinfo=pytz.UTC),
        flen=275,
        tlen=300,
        rwt=500,
        clipc="2",
        sex=1,
        fate="K",
        tagid="2222",
        tagdoc="45042",
        tag_type="4",
        tag_position="5",
        tag_origin="04",
        tag_colour="2",
    )
    fish2 = RecoveryFactory(
        lake=superior,
        species=walleye,
        report=report2,
        recovery_date=datetime(2017, 11, 11).replace(tzinfo=pytz.UTC),
        flen=375,
        tlen=400,
        rwt=1000,
        clipc="5",
        sex=1,
        fate="K",
        tagid="3333",
        tagdoc="34013",
        tag_type="3",
        tag_position="4",
        tag_origin="01",
        tag_colour="3",
    )
    fish3 = RecoveryFactory(
        lake=superior,
        species=lake_trout,
        report=report1,
        recovery_date=datetime(2015, 11, 11).replace(tzinfo=pytz.UTC),
        flen=375,
        tlen=400,
        rwt=1100,
        clipc="0",
        sex=2,
        fate="R",
        tagid="4444",
        tagdoc="43043",
        tag_type="4",
        tag_position="3",
        tag_origin="04",
        tag_colour="3",
    )
    fish4 = RecoveryFactory(
        lake=ontario,
        species=lake_trout,
        report=report2,
        recovery_date=datetime(2017, 11, 11).replace(tzinfo=pytz.UTC),
        flen=325,
        tlen=350,
        rwt=800,
        clipc="23",
        sex=None,
        fate="R",
        tagid="4444",
        tagdoc="43994",
        tag_type="4",
        tag_position="3",
        tag_origin="99",
        tag_colour="4",
    )
    fish5 = RecoveryFactory(
        lake=ontario,
        species=perch,
        report=report1,
        recovery_date=datetime(2015, 11, 11).replace(tzinfo=pytz.UTC),
        flen=225,
        tlen=250,
        rwt=500,
        clipc=None,
        sex=None,
        fate="R",
        tagid="5511",
        tagdoc="25044",
        tag_type="2",
        tag_position="5",
        tag_origin="04",
        tag_colour="4",
    )

    return [fish0, fish1, fish2, fish3, fish4, fish5]


filter_args = [
    # where, when, what and how:
    ({"lake": "ON"}, [4, 5]),
    ({"lake__not": "ON"}, [0, 1, 2, 3]),
    ({"lake": "ON,HU"}, [0, 1, 4, 5]),
    ({"lake__not": "ON,HU"}, [2, 3]),
    ({"year": "2015"}, [3, 5]),
    ({"year__gte": "2015"}, [2, 3, 4, 5]),
    ({"year__lte": "2015"}, [0, 1, 3, 5]),
    ({"year__gt": "2015"}, [2, 4]),
    ({"year__lt": "2015"}, [0, 1]),
    ({"spc": "081"}, [3, 4]),
    ({"spc_not": "081"}, [0, 1, 2, 5]),
    ({"spc": "081,334"}, [0, 2, 3, 4]),
    ({"spc_not": "081,334"}, [1, 5]),
    ({"from_dcr": True}, [2, 4]),
    # fish attributes
    ({"tlen": 350}, [4]),
    ({"tlen__gte": 350}, [2, 3, 4]),
    ({"tlen__lte": 350}, [0, 1, 4, 5]),
    ({"tlen__gt": 350}, [2, 3]),
    ({"tlen__lt": 350}, [0, 1, 5]),
    ({"flen": 325}, [4]),
    ({"flen__gte": 325}, [2, 3, 4]),
    ({"flen__lte": 325}, [0, 1, 4, 5]),
    ({"flen__gt": 325}, [2, 3]),
    ({"flen__lt": 325}, [0, 1, 5]),
    ({"rwt": 800}, [4]),
    ({"rwt__null": True}, [0]),
    ({"rwt__null": False}, [1, 2, 3, 4, 5]),
    ({"rwt__gte": 800}, [2, 3, 4]),
    ({"rwt__lte": 800}, [1, 4, 5]),
    ({"rwt__gt": 800}, [2, 3]),
    ({"rwt__lt": 800}, [1, 5]),
    ({"sex": 1}, [1, 2]),
    ({"sex": "1,9"}, [0, 1, 2]),
    ({"sex__not": 1}, [0, 3, 4, 5]),
    ({"sex__not": "1,9"}, [3, 4, 5]),
    ({"sex__null": True}, [4, 5]),
    ({"sex__null": False}, [0, 1, 2, 3]),
    ({"clipc": 0}, [0, 3]),
    ({"clipc": "2,5"}, [1, 2]),
    ({"clipc__not": 0}, [1, 2, 4, 5]),
    ({"clipc__not": "2,5"}, [0, 3, 4, 5]),
    ({"clipc__null": True}, [5]),
    ({"clipc__null": False}, [0, 1, 2, 3, 4]),
    ({"clipc__like": 2}, [1, 4]),
    ({"clipc__not_like": 2}, [0, 2, 3, 5]),
    ({"fate": "K"}, [0, 1, 2]),
    ({"fate__not": "K"}, [3, 4, 5]),
    # tag attributes:
    ({"tagid": "1111"}, [0]),
    ({"tagid__like": "11"}, [0, 5]),
    ({"tagdoc": "25012"}, [0]),
    ({"tagdoc__not": "25012"}, [1, 2, 3, 4, 5]),
    ({"tagdoc__like": "250"}, [0, 5]),
    ({"tag_origin": "01"}, [0, 2]),
    ({"tag_origin__not": "01"}, [1, 3, 4, 5]),
    ({"tag_origin": "01,99"}, [0, 2, 4]),
    ({"tag_origin__not": "01,99"}, [1, 3, 5]),
    ({"tag_position": "3"}, [3, 4]),
    ({"tag_position": "3,4"}, [2, 3, 4]),
    ({"tag_position__not": "3"}, [0, 1, 2, 5]),
    ({"tag_position__not": "3,4"}, [0, 1, 5]),
    ({"tag_type": "4"}, [1, 3, 4]),
    ({"tag_type__not": "4"}, [0, 2, 5]),
    ({"tag_type": "3,4"}, [1, 2, 3, 4]),
    ({"tag_type__not": "3,4"}, [0, 5]),
    ({"tag_colour": "2"}, [0, 1]),
    ({"tag_colour__not": "2"}, [2, 3, 4, 5]),
    ({"tag_colour": "2,3"}, [0, 1, 2, 3]),
    ({"tag_colour__not": "2,3"}, [4, 5]),
]


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_recovery_filters(client, recoveries, filter, expected):
    """The readonly api endpoint for tag recoveries accepts filters that are
    attributes of the report (reporting date) and the recovered fish (species,
    size, sex, ect) as well as the tag attributes. There are currently no
    filters for tag reporter attributes (such as first or last name).

    This test is parameterized to accept a list of two element tuples, the first
    element is the filter to apply, the second is the list of indices that
    correspond to the angler records that should be returned in the response.
    The indices are used to extract the id from the fixture and compare those to
    the angler id's returned by the response.

    """

    ids = []
    for i, x in enumerate(recoveries):
        if i in expected:
            ids.append(x.id)

    url = reverse("tfat_api:recovery-list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the ids from the response:
    payload = response.data["results"]
    observed_ids = {x["id"] for x in payload}

    assert len(payload) == len(expected)
    assert set(ids) == observed_ids
