import pytz
from tfat.models import Encounter
from tfat.constants import (
    TAG_COLOUR_CHOICES,
    TAG_ORIGIN_CHOICES,
    TAG_TYPE_CHOICES,
    TAG_POSITION_CHOICES,
)

from tfat.tests.factories import *

import pytest


@pytest.mark.django_db
def test_encounter_tag_type():
    """
    """

    species = SpeciesFactory()
    project = ProjectFactory()

    tagdoc_base = "{}5012"

    should_be = {k: v for k, v in TAG_TYPE_CHOICES}
    for k, tag_type in should_be.items():
        tagdoc = tagdoc_base.format(k)
        encounter = EncounterFactory(project=project, spc=species, tagdoc=tagdoc)
        assert encounter.tag_type() == tag_type


@pytest.mark.django_db
def test_encounter_tag_origin():
    """
    """

    species = SpeciesFactory()
    project = ProjectFactory()

    tagdoc_base = "25{}2"

    should_be = {k: v for k, v in TAG_ORIGIN_CHOICES}
    for k, origin in should_be.items():
        tagdoc = tagdoc_base.format(k)
        encounter = EncounterFactory(project=project, spc=species, tagdoc=tagdoc)
        assert encounter.tag_origin() == origin


@pytest.mark.django_db
def test_encounter_tag_position():
    """
    """

    species = SpeciesFactory()
    project = ProjectFactory()

    tagdoc_base = "2{}012"

    should_be = {k: v for k, v in TAG_POSITION_CHOICES}
    for k, position in should_be.items():
        tagdoc = tagdoc_base.format(k)
        encounter = EncounterFactory(project=project, spc=species, tagdoc=tagdoc)
        assert encounter.tag_position() == position


@pytest.mark.django_db
def test_encounter_tag_colour():
    """
    """

    species = SpeciesFactory()
    project = ProjectFactory()

    tagdoc_base = "2501{}"

    should_be = {k: v for k, v in TAG_COLOUR_CHOICES}
    for k, colour in should_be.items():
        tagdoc = tagdoc_base.format(k)
        encounter = EncounterFactory(project=project, spc=species, tagdoc=tagdoc)
        assert encounter.tag_colour() == colour


@pytest.mark.django_db
def test_encounter_pop_text():
    """Verify that the pop_text() method returns the elements we think it should
    """

    project = ProjectFactory()

    elements = {
        "tagid": "1234",
        "tagdoc": "25015",
        "tagstat": "A",
        "obs_date": datetime(2013, 10, 16).replace(tzinfo=pytz.UTC),
        "common_name": "Walleye",
        "species_code": "334",
    }
    species = SpeciesFactory(
        common_name=elements["common_name"], species_code=elements["species_code"]
    )

    encounter = EncounterFactory(
        project=project,
        spc=species,
        tagid=elements["tagid"],
        tagdoc=elements["tagdoc"],
        observation_date=elements["obs_date"],
    )

    popup_text = encounter.popup_text()

    elements["obs_date"] = elements["obs_date"].strftime("%b-%d-%Y")

    for k, v in elements.items():
        print(k, v)
        assert v in popup_text


@pytest.mark.django_db
def test_encounter_has_latlon_true():
    """
    """
    species = SpeciesFactory()
    project = ProjectFactory()
    encounter = EncounterFactory(
        project=project, spc=species, dd_lat=45.5, dd_lon=-81.3
    )
    assert encounter.has_latlon() is True


@pytest.mark.django_db
def test_encounter_flen_inches():
    """
    """
    species = SpeciesFactory()
    project = ProjectFactory()
    encounter = EncounterFactory(project=project, spc=species, flen=450)
    assert encounter.flen_inches() == 17.7


@pytest.mark.django_db
def test_encounter_flen_inches_none():
    """
    """
    species = SpeciesFactory()
    project = ProjectFactory()
    encounter = EncounterFactory(project=project, spc=species, flen=None)
    assert encounter.flen_inches() is None


@pytest.mark.django_db
def test_encounter_tlen_inches():
    """
    """
    species = SpeciesFactory()
    project = ProjectFactory()
    encounter = EncounterFactory(project=project, spc=species, tlen=450)
    assert encounter.tlen_inches() == 17.7


@pytest.mark.django_db
def test_encounter_tlen_inches_none():
    """
    """
    species = SpeciesFactory()
    project = ProjectFactory()
    encounter = EncounterFactory(project=project, spc=species, tlen=None)
    assert encounter.tlen_inches() is None


@pytest.mark.django_db
def test_encounter_rwt_pounds():
    """
    """
    species = SpeciesFactory()
    project = ProjectFactory()
    encounter = EncounterFactory(project=project, spc=species, rwt=2000)
    assert encounter.pounds() == 4.4


@pytest.mark.django_db
def test_encounter_rwt_pounds_none():
    """
    """
    species = SpeciesFactory()
    project = ProjectFactory()
    encounter = EncounterFactory(project=project, spc=species, rwt=None)
    assert encounter.pounds() is None
