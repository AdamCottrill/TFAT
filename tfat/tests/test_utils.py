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

from tfat.utils import tagdoc_warning, spc_warning

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
