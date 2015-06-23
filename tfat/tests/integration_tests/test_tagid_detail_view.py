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


@pytest.fixture(scope='class')
def db_setup():
    """
    """
    spc1 = SpeciesFactory(species_code='334', common_name='Walleye')
    spc2 = SpeciesFactory(species_code='091', common_name='Whitefish')

    #same species, same tagdoc - everything is A-Ok.
    encounter1 = EncounterFactory(spc=spc1, tagid='11111',
                                  tagdoc='25012')
    encounter2 = EncounterFactory(spc=spc1, tagid='11111',
                                  tagdoc='25012')

    #different species
    encounter3 = EncounterFactory(spc=spc1, tagid='22222',
                                  tagdoc='25012')
    encounter4 = EncounterFactory(spc=spc2, tagid='22222',
                                  tagdoc='25012')

    #same species, different tagdoc
    encounter3 = EncounterFactory(spc=spc1, tagid='33333',
                                  tagdoc='25012')
    encounter4 = EncounterFactory(spc=spc1, tagid='33333',
                                  tagdoc='15012')


@pytest.mark.django_db
def test_multiple_species_warning(client, db_setup):
    """If there is more than one species associated with a tag, a warning
    should be included in the repsonse.
    """

    url = reverse('tagid_detail_view', kwargs={'tagid':'33333'})
    response = client.get(url)
    content = str(response.content)

    msg = ("There appears to be more than one tagdoc code associated "
           "with the records on this page. Interpret with caution.")

    assert msg in content


@pytest.mark.django_db
def test_multiple_species_warning_ok(client, db_setup):
    """As long as all of the species associated with a tag are the same,
    the warning should not appear in the reponse.

    """

    url = reverse('tagid_detail_view', kwargs={'tagid':'11111'})
    response = client.get(url)
    content = str(response.content)

    msg = ("There appears to be more than one tagdoc code associated "
           "with the records on this page. Interpret with caution.")

    assert msg not in content



@pytest.mark.django_db
def test_multiple_tagdoc_warning(client, db_setup):
    """If there is more than one tagdoc associated with a tag, a warning
    should be included in the repsonse.
    """

    url = reverse('tagid_detail_view', kwargs={'tagid':'22222'})
    response = client.get(url)
    content = str(response.content)

    msg = ("There appears to be more than one species associated "
           "with the records on this page. Interpret with caution.")

    assert msg in content


@pytest.mark.django_db
def test_multiple_tagdoc_warning_ok(client, db_setup):
    """As long as all of the tagdocs associated with a tag are the same,
    the warning should not appear in the reponse.

    """

    url = reverse('tagid_detail_view', kwargs={'tagid':'11111'})
    response = client.get(url)
    content = str(response.content)

    msg = ("There appears to be more than one species associated "
           "with the records on this page. Interpret with caution.")

    assert msg not in content
