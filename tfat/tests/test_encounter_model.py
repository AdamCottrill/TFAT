from tfat.models import Encounter
from tfat.constants import (TAG_COLOUR_CHOICES, TAG_ORIGIN_CHOICES,
                            TAG_TYPE_CHOICES, TAG_POSITION_CHOICES)

from tfat.tests.factories import *

import pytest


@pytest.mark.django_db
def test_encounter_tag_type():
    """
    """

    species = SpeciesFactory()
    project = ProjectFactory()

    tagdoc_base = '{}5012'

    should_be = {k:v for k,v in TAG_TYPE_CHOICES}
    for k,tag_type in should_be.items():
        tagdoc = tagdoc_base.format(k)
        encounter = EncounterFactory(project=project, spc=species,
                                     tagdoc=tagdoc)
        assert encounter.tag_type() == tag_type


@pytest.mark.django_db
def test_encounter_tag_origin():
    """
    """

    species = SpeciesFactory()
    project = ProjectFactory()

    tagdoc_base = '25{}2'

    should_be = {k:v for k,v in TAG_ORIGIN_CHOICES}
    for k,origin in should_be.items():
        tagdoc = tagdoc_base.format(k)
        encounter = EncounterFactory(project=project, spc=species,
                                     tagdoc=tagdoc)
        assert encounter.tag_origin() == origin


@pytest.mark.django_db
def test_encounter_tag_position():
    """
    """

    species = SpeciesFactory()
    project = ProjectFactory()

    tagdoc_base = '2{}012'

    should_be = {k:v for k,v in TAG_POSITION_CHOICES}
    for k,position in should_be.items():
        tagdoc = tagdoc_base.format(k)
        encounter = EncounterFactory(project=project, spc=species,
                                     tagdoc=tagdoc)
        assert encounter.tag_position() == position


@pytest.mark.django_db
def test_encounter_tag_colour():
    """
    """

    species = SpeciesFactory()
    project = ProjectFactory()

    tagdoc_base = '2501{}'

    should_be = {k:v for k,v in TAG_COLOUR_CHOICES}
    for k,colour in should_be.items():
        tagdoc = tagdoc_base.format(k)
        encounter = EncounterFactory(project=project, spc=species,
                                     tagdoc=tagdoc)
        assert encounter.tag_colour() == colour



@pytest.mark.django_db
def test_encounter_pop_text():
    """Verify that the pop_text() method returns the elements we think it should
    """


    project = ProjectFactory()

    elements = {'tagid': '1234',
                'tagdoc':'25015',
                'tagstat':'A',
                'obs_date':datetime(2013,10,16),
                'common_name':'Walleye',
                'species_code':'334',}
    species = SpeciesFactory(common_name=elements['common_name'],
                             species_code=elements['species_code'])

    encounter = EncounterFactory(project=project,
                                 spc=species,
                                 tagid=elements['tagid'],
                                 tagdoc=elements['tagdoc'],
                                 observation_date=elements['obs_date'])

    popup_text = encounter.popup_text()

    elements['obs_date'] = elements['obs_date'].strftime('%b-%d-%Y')

    for k,v in elements.items():
        print(k,v)
        assert v in popup_text
