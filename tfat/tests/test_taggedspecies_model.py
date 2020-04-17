"""=============================================================
~/tfat/tests/test_taggedspecies_model.py
Created: 16 Apr 2020 13:13:39

DESCRIPTION:

TFAT now uses a model inherted from the UGMLU Common application to
limit the number of species available in the application.  The tests
in this file ensure that the inherted models work as expected, and
that the model manager only returned tagged species by default,
although all speceis are available through a special model manager.

A. Cottrill
=============================================================

"""


from tfat.models import TaggedSpecies as Species
from tfat.tests.factories import SpeciesFactory

import pytest


@pytest.fixture()
def db_setup():
    """Create some species objects.  Two species that have tagged
    designation, and one that does not.

    """

    lake_trout = SpeciesFactory(
        spc_nmco="Lake Trout", spc_nmsc="Salvelinus namaycush", spc="081", tagged=True
    )

    walleye = SpeciesFactory(
        spc_nmco="Walleye", spc_nmsc="Sander vitreum", spc="334", tagged=True
    )

    round_whitefish = SpeciesFactory(
        spc_nmco="Round Whitefish",
        spc_nmsc="Prosopium cylindraceum",
        spc="102",
        tagged=False,
    )


@pytest.mark.django_db
def test_species_str():
    """str() method method of a Species object should return a string
    like so: <Common Name> (Scientific Name)

    """

    attrs = {
        "spc_nmco": "Lake Trout",
        "spc_nmsc": "Salvelinus namaycush",
        "spc": 81,
        "tagged": True,
    }

    species = Species(
        spc_nmco=attrs.get("spc_nmco"),
        spc_nmsc=attrs.get("spc_nmsc"),
        spc=attrs.get("spc"),
        tagged=attrs.get("tagged"),
    )

    should_be = "{spc_nmco} ({spc_nmsc})"
    assert str(species) == should_be.format(**attrs)


@pytest.mark.django_db
def test_species_str_no_common_name():
    """str() method method of a Species object that does not have a common
    name should return a string like so:(Scientific Name)

    """

    attrs = {"spc_nmsc": "Salvelinus namaycush", "spc": "081", "tagged": True}

    species = Species(
        spc_nmsc=attrs.get("spc_nmsc"), spc=attrs.get("spc"), tagged=attrs.get("tagged")
    )

    should_be = "({spc_nmsc})"
    assert str(species) == should_be.format(**attrs)


def test_species_no_spc_nmsc():
    """If there is no scientific name, the string representation of a
    species object is just the common name.
    """
    attrs = {"spc_nmco": "Salvelinus Sp.", "spc": "086", "tagged": True}

    species = Species(
        spc_nmco=attrs.get("spc_nmco"),
        spc_nmsc=attrs.get("spc_nmsc"),
        spc=attrs.get("spc"),
        tagged=attrs.get("tagged"),
    )

    should_be = "{spc_nmco}"
    assert str(species) == should_be.format(**attrs)


@pytest.mark.django_db
def test_species_model_manager(db_setup):
    """The default species manager should only return the active
    species.
    """
    species = Species.objects.all()
    spc_codes = [x.spc for x in species]
    should_be = ["081", "334"]

    should_be.sort()
    spc_codes.sort()
    assert spc_codes == should_be


@pytest.mark.django_db
def test_species_model_manager_all_species(db_setup):
    """the custom manager allspecies should return all species, regardless
    of their tagged designation.

    """

    species = Species.all_objects.all()
    spc_codes = [x.spc for x in species]
    should_be = ["081", "102", "334"]

    should_be.sort()
    spc_codes.sort()
    assert spc_codes == should_be
