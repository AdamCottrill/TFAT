"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_utils.py
Created: 19 Jun 2015 15:14:46


DESCRIPTION:

The tests in this script verify that the utility functions work as
expected.  Many of htem utilize mocks to emulate queryset objects.

A. Cottrill
=============================================================

"""


from tfat.models import *
from tfat.tests.factories import *

from tfat.utils import tagdoc_warning, spc_warning, qs_to_tagdict, sort_tagdict

from datetime import datetime, date
from unittest.mock import MagicMock

import pytest


def test_warn_species_true():
    """spc_warning should return true if the querysets/lists we pass in
    have more than one species assocaited with them.
    """

    species = ["091", "334"]

    species1 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.species.spc = species[0]
        species1.append(tmp)

    species2 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.species.spc = species[1]
        species2.append(tmp)

    assert spc_warning([species1, species2]) == True


def test_warn_species_false():
    """spc_warning should return false if the querysets/lists we pass in
    have only one species assocaited with them.
    """

    species = "334"

    species1 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.species.spc = species
        species1.append(tmp)

    species2 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.species.spc = species
        species2.append(tmp)

    assert spc_warning([species1, species2]) == False


def test_warn_tagdoc_true():
    """tagdoc_warning should return true if the querysets/lists we pass in
    have more than one tagdoc assocaited with them.
    """

    tagdoc = "25012"

    tags1 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.tagdoc = tagdoc
        tags1.append(tmp)

    tags2 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.tagdoc = tagdoc
        tags2.append(tmp)

    assert tagdoc_warning([tags1, tags2]) == False


def test_warn_tagdoc_false():
    """tagdoc_warning should return false if the querysets/lists we pass in
    has one, and only one tagdoc assocaited with them.
    """

    tagdocs = ["25012", "15012"]

    tags1 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.tagdoc = tagdocs[0]
        tags1.append(tmp)

    tags2 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.tagdoc = tagdocs[1]
        tags2.append(tmp)

    assert tagdoc_warning([tags1, tags2]) == True


# ======================================


@pytest.fixture()
def tag_querysets():

    # OMNR observations
    species = SpeciesFactory()

    EncounterFactory(
        tagid="123",
        observation_date=datetime(2001, 6, 15),
        dd_lat=45.000,
        dd_lon=-81.000,
        species=species,
    )

    EncounterFactory(
        tagid="123",
        observation_date=datetime(2002, 6, 15),
        dd_lat=46.000,
        dd_lon=-81.000,
        species=species,
    )

    EncounterFactory(
        tagid="123",
        observation_date=datetime(2003, 6, 15),
        dd_lat=47.000,
        dd_lon=-81.000,
        species=species,
    )

    EncounterFactory(
        tagid="123",
        observation_date=datetime(2000, 6, 15),
        dd_lat=44.000,
        dd_lon=-81.000,
        species=species,
    )

    EncounterFactory(
        tagid="123",
        observation_date=datetime(1999, 6, 15),
        dd_lat=43.000,
        dd_lon=-81.000,
        species=species,
    )

    # a second tag =
    EncounterFactory(
        tagid="678",
        observation_date=datetime(2000, 11, 15),
        dd_lat=44.000,
        dd_lon=-81.000,
        species=species,
    )

    EncounterFactory(
        tagid="678",
        observation_date=datetime(1999, 11, 15),
        dd_lat=43.000,
        dd_lon=-81.000,
        species=species,
    )

    report = ReportFactory()

    # angler returns

    RecoveryFactory(
        tagid="123",
        recovery_date=datetime(2001, 7, 15),
        dd_lat=45.000,
        dd_lon=-81.000,
        species=species,
        report=report,
    )

    RecoveryFactory(
        tagid="123",
        recovery_date=datetime(2002, 7, 15),
        dd_lat=46.000,
        dd_lon=-81.000,
        species=species,
        report=report,
    )

    RecoveryFactory(
        tagid="999",
        recovery_date=datetime(2001, 7, 15),
        dd_lat=45.000,
        dd_lon=-81.000,
        species=species,
        report=report,
    )


@pytest.mark.django_db
def test_qs_to_tagdict_missing_latlong():
    """records with missing lat or long should not appear in resultant
    dictionary - the dict is used for plotting and lat or lon of None
    can't be plotted'

    Create 4 tag recoveries, only one has both lat and lon populated.

    """

    species = SpeciesFactory()
    RecoveryFactory(
        tagid="good",
        recovery_date=datetime(1999, 11, 15),
        dd_lat=43.000,
        dd_lon=-81.000,
        species=species,
    )

    RecoveryFactory(
        tagid="no_lat",
        recovery_date=datetime(1999, 11, 15),
        dd_lat=None,
        dd_lon=-81.000,
        species=species,
    )

    RecoveryFactory(
        tagid="no_long",
        recovery_date=datetime(1999, 11, 15),
        dd_lat=46.00,
        dd_lon=None,
        species=species,
    )

    RecoveryFactory(
        tagid="no_latlong",
        recovery_date=datetime(1999, 11, 15),
        dd_lat=None,
        dd_lon=None,
        species=species,
    )

    qs = Recovery.objects.all()
    tag_dict = qs_to_tagdict(qs)
    keys = list(tag_dict.keys())
    keys.sort()
    assert keys == ["good"]
    assert len(keys) == 1
    assert "no_lat" not in keys
    assert "no_long" not in keys
    assert "no_latlong" not in keys


@pytest.mark.django_db
def test_qs_to_tagdict_new_keys(tag_querysets):
    """If we pass a queryset like object to qs_to_tagdict() we should get
    back a dictionary.  The keys of the dictionary should be the
    tagids we passed in.

    """

    qs = Encounter.objects.all()
    tag_dict = qs_to_tagdict(qs)
    keys = list(tag_dict.keys())
    keys.sort()
    assert keys == ["123", "678"]
    assert "999" not in keys


@pytest.mark.django_db
def test_qs_to_tagdict_keys_existing_dict(tag_querysets):
    """If we pass a queryset like object to an existing tag_dict to
    qs_to_tagdict() we should get back a dictionary.  The keys of the
    dictionary should be the tagids of both querysets.

    """

    qs1 = Encounter.objects.all()
    qs2 = Recovery.objects.all()

    tag_dict = qs_to_tagdict(qs1)
    tag_dict = qs_to_tagdict(qs2, tag_dict)

    keys = list(tag_dict.keys())
    keys.sort()
    assert keys == ["123", "678", "999"]


@pytest.mark.django_db
def test_qs_to_tagdict_new_value_attributes(tag_querysets):
    """If we pass a queryset like object to qs_to_tagdict() we should get
    back a dictionary.  The values of the dictionary should be the
    lists of two element tuples.  The first element of each tuple
    should be a date, the second should be another two element tuple
    representing the coordinates of a point.

    """
    qs = Recovery.objects.all()
    tag_dict = qs_to_tagdict(qs)
    # convert the values to a list and get the first one
    vals = list(tag_dict["123"])

    for val in vals:
        assert len(val) == 2
        assert isinstance(val[0], date)
        assert len(val[1]) == 2


@pytest.mark.django_db
def test_qs_to_tagdict_new_value_values(tag_querysets):
    """If we pass a queryset like object to qs_to_tagdict() we should get
    back a dictionary.  The values of the dictionary should be
    contains the dates and points in the orginal queryset.

    """

    qs = Recovery.objects.all()
    tag_dict = qs_to_tagdict(qs)

    assert "123" in tag_dict.keys()
    values = tag_dict["123"]

    dates = [x[0] for x in values]
    pts = [x[1] for x in values]

    assert date(2002, 7, 15) in dates
    assert date(2001, 7, 15) in dates

    assert (-81, 46) in pts
    assert (-81, 45) in pts


@pytest.mark.django_db
def test_qs_to_tagdict_existing_value_attributes(tag_querysets):
    """If we pass a queryset like object to qs_to_tagdict() we should get
    back a dictionary.  The values of the dictionary should be the
    lists of two element tuples.  The first element of each tuple
    should be a date, the second should be another two element tuple
    representing the coordinates of a point.  This is exactly the same
    attributes as passing a single queryset.

    """
    # process the first queryset
    qs1 = Encounter.objects.all()
    tag_dict = qs_to_tagdict(qs1)

    # now add the second
    qs2 = Recovery.objects.all()
    tag_dict = qs_to_tagdict(qs2, tag_dict)
    # convert the values to a list and get the first one
    vals = list(tag_dict.values())[0]

    for val in vals:
        assert len(val) == 2
        assert isinstance(val[0], date)
        assert len(val[1]) == 2


@pytest.mark.django_db
def test_qs_to_tagdict_existing_value_values(tag_querysets):
    """If we pass a queryset-like object and an exsisting tag_dict to
    qs_to_tagdict() we should get back a dictionary The values of the
    dictionary should be contains the dates and points in BOTH
    querysets.

    """

    # process the first queryset
    qs1 = Encounter.objects.all()
    tag_dict = qs_to_tagdict(qs1)

    # now add the second
    qs2 = Recovery.objects.all()
    tag_dict = qs_to_tagdict(qs2, tag_dict)

    # convert the values to a list
    values = list(tag_dict.values())

    # lists to hold our data:
    dates = []
    pts = []

    for obs in values:
        dates.extend([x[0] for x in obs])
        pts.extend([x[1] for x in obs])

    # anlger returns (qs2)
    assert date(2002, 7, 15) in dates
    assert date(2001, 7, 15) in dates

    # omnr tags (qs1)
    assert date(1999, 6, 15) in dates
    assert date(2000, 11, 15) in dates
    assert date(1999, 11, 15) in dates

    # Angler returns (qs0)
    assert (-81, 46) in pts
    assert (-81, 45) in pts
    # omnr tags (qs1)
    assert (-81, 43) in pts
    assert (-81, 44) in pts


@pytest.mark.django_db
def test_sort_tagdict_existing_single_qs(tag_querysets):
    """sort_tagdict takes a tagdict from qs_to_tagdict and sorts the list
    of observations for each tagid.  If we create a tag dict from our
    queryset objects, the returned dates should be chronological
    order.

    """

    should_be_123 = [
        date(1999, 6, 15),
        date(2000, 6, 15),
        date(2001, 6, 15),
        date(2002, 6, 15),
        date(2003, 6, 15),
    ]

    should_be_678 = [date(1999, 11, 15), date(2000, 11, 15)]

    # process the queryset and return a tagdict
    qs1 = Encounter.objects.all()
    tag_dict = qs_to_tagdict(qs1)

    tag_dict = sort_tagdict(tag_dict)

    actual_123 = [x[0] for x in tag_dict.get("123")]
    actual_678 = [x[0] for x in tag_dict.get("678")]

    assert actual_123 == should_be_123
    assert actual_678 == should_be_678
