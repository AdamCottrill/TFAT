'''=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_tagid_detail_view.py
Created: 19 Jun 2015 10:07:24

DESCRIPTION:

The tests in this module verify that the view that renders the
the details associated with a particular tag render correctly.

A. Cottrill
=============================================================

'''

import pytest
from django.core.urlresolvers import reverse

from tfat.tests.factories import *

from datetime import datetime


def test_multiple_species_warning(client):
    """If there is more than one species associated with a tag, a warning
    should be included in the repsonse.
    """

    assert 1==0



def test_multiple_species_warning_ok(client):
    """As long as all of the species associated with a tag are the same,
    the warning should not appear in the reponse.

    """

    assert 1==0



def test_multiple_tagdoc_warning(client):
    """If there is more than one tagdoc associated with a tag, a warning
    should be included in the repsonse.
    """
    assert 1==0



def test_multiple_tagdoc_warning_ok(client):
    """As long as all of the tagdocs associated with a tag are the same,
    the warning should not appear in the reponse.

    """
    assert 1==0
