'''=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_utils.py
Created: 19 Jun 2015 15:14:46


DESCRIPTION:

The tests in this script verify that the utility functions work as
expected.  Many of htem utilize mocks to emulate queryset objects.

A. Cottrill
=============================================================

'''


from tfat.models import *
from tfat.tests.factories import *

from tfat.utils import tagdoc_warning, spc_warning, qs_to_tagdict, sort_tagdict

from datetime import datetime, date
from unittest.mock import MagicMock

import pytest


def test_warn_spc_true():
    """spc_warning should return true if the querysets/lists we pass in
    have more than one species assocaited with them.
    """

    species = ['091', '334']

    spc1 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.spc.species_code = species[0]
        spc1.append(tmp)

    spc2 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.spc.species_code = species[1]
        spc2.append(tmp)

    assert spc_warning([spc1, spc2]) == True



def test_warn_spc_false():
    """spc_warning should return false if the querysets/lists we pass in
    have only one species assocaited with them.
    """

    species = '334'

    spc1 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.spc.species_code = species
        spc1.append(tmp)

    spc2 = []
    for x in range(4):
        tmp = MagicMock()
        tmp.spc.species_code = species
        spc2.append(tmp)


    assert spc_warning([spc1, spc2]) == False


def test_warn_tagdoc_true():
    """tagdoc_warning should return true if the querysets/lists we pass in
    have more than one tagdoc assocaited with them.
    """

    tagdoc = '25012'

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

    tagdocs = ['25012','15012']

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



#======================================

@pytest.fixture(scope='class')
def tag_querysets():

    #OMNR observations
    spc = SpeciesFactory()

    EncounterFactory(tagid = '123',
                     observation_date = datetime(2001,6,15),
                     dd_lat = 45.000,
                     dd_lon = -81.000,
                     spc = spc
    )

    EncounterFactory(tagid = '123',
                     observation_date = datetime(2002,6,15),
                     dd_lat = 46.000,
                     dd_lon = -81.000,
                     spc = spc
    )

    EncounterFactory(tagid = '123',
                     observation_date = datetime(2003,6,15),
                     dd_lat = 47.000,
                     dd_lon = -81.000,
                     spc = spc
    )

    EncounterFactory(tagid = '123',
                     observation_date = datetime(2000,6,15),
                     dd_lat = 44.000,
                     dd_lon = -81.000,
                     spc = spc
    )

    EncounterFactory(tagid = '123',
                     observation_date = datetime(1999,6,15),
                     dd_lat = 43.000,
                     dd_lon = -81.000,
                     spc = spc
    )


    #a second tag =
    EncounterFactory(tagid = '678',
                     observation_date = datetime(2000,11,15),
                     dd_lat = 44.000,
                     dd_lon = -81.000,
                     spc = spc
    )

    EncounterFactory(tagid = '678',
                     observation_date = datetime(1999,11,15),
                     dd_lat = 43.000,
                     dd_lon = -81.000,
                     spc = spc
    )


    report = ReportFactory()


    #angler returns

    RecoveryFactory(tagid = '123',
                    recovery_date = datetime(2001,7,15),
                    dd_lat = 45.000,
                    dd_lon = -81.000,
                    spc = spc, report=report
    )

    RecoveryFactory(tagid = '123',
                    recovery_date = datetime(2002,7,15),
                    dd_lat = 46.000,
                    dd_lon = -81.000,
                    spc = spc, report=report
    )

    RecoveryFactory(tagid = '999',
                    recovery_date = datetime(2001,7,15),
                    dd_lat = 45.000,
                    dd_lon = -81.000,
                    spc = spc, report=report
    )


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
    assert keys == ['123','678']
    assert '999' not in keys


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
    assert keys == ['123','678', '999']


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
    #convert the values to a list and get the first one
    vals = list(tag_dict['123'])

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

    assert '123' in tag_dict.keys()
    values = tag_dict['123']

    dates = [x[0] for x in values]
    pts = [x[1] for x in values]

    assert date(2002,7,15) in dates
    assert date(2001,7,15) in dates

    assert (-81,46) in pts
    assert (-81,45) in pts


@pytest.mark.django_db
def test_qs_to_tagdict_existing_value_attributes(tag_querysets):
    """If we pass a queryset like object to qs_to_tagdict() we should get
    back a dictionary.  The values of the dictionary should be the
    lists of two element tuples.  The first element of each tuple
    should be a date, the second should be another two element tuple
    representing the coordinates of a point.  This is exactly the same
    attributes as passing a single queryset.

    """
    #process the first queryset
    qs1 = Encounter.objects.all()
    tag_dict = qs_to_tagdict(qs1)

    #now add the second
    qs2 = Recovery.objects.all()
    tag_dict = qs_to_tagdict(qs2, tag_dict)
    #convert the values to a list and get the first one
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

    #process the first queryset
    qs1 = Encounter.objects.all()
    tag_dict = qs_to_tagdict(qs1)

    #now add the second
    qs2 = Recovery.objects.all()
    tag_dict = qs_to_tagdict(qs2, tag_dict)

    #convert the values to a list
    values = list(tag_dict.values())

    #lists to hold our data:
    dates = []
    pts = []

    for obs in values:
        dates.extend([x[0] for x in obs])
        pts.extend([x[1] for x in obs])

    #anlger returns (qs2)
    assert date(2002,7,15) in dates
    assert date(2001,7,15) in dates

    #omnr tags (qs1)
    assert date(1999,6,15) in dates
    assert date(2000,11,15) in dates
    assert date(1999,11,15) in dates

    #Angler returns (qs0)
    assert (-81,46) in pts
    assert (-81,45) in pts
    #omnr tags (qs1)
    assert (-81,43) in pts
    assert (-81,44) in pts


@pytest.mark.django_db
def test_sort_tagdict_existing_single_qs(tag_querysets):
    """sort_tagdict takes a tagdict from qs_to_tagdict and sorts the list
    of observations for each tagid.  If we create a tag dict from our
    queryset objects, the returned dates should be chronological
    order.

    """

    should_be_123 = [date(1999,6,15),
                     date(2000,6,15),
                     date(2001,6,15),
                     date(2002,6,15),
                     date(2003,6,15), ]

    should_be_678 = [date(1999,11,15), date(2000,11,15),]

    #process the queryset and return a tagdict
    qs1 = Encounter.objects.all()
    tag_dict = qs_to_tagdict(qs1)

    tag_dict = sort_tagdict(tag_dict)

    actual_123 = [x[0] for x in tag_dict.get('123')]
    actual_678 = [x[0] for x in tag_dict.get('678')]

    assert actual_123 == should_be_123
    assert actual_678 == should_be_678
