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
