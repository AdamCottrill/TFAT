'''
=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_species_model.py
Created: 31 May 2016 14:54:38


DESCRIPTION:



A. Cottrill
=============================================================
'''


from tfat.models import Species
from tfat.tests.factories import SpeciesFactory

import pytest


@pytest.fixture(scope='class')
def db_setup():
    """Create some species objects.  Two species that have primary
    designation, and one that does not.

    """

    lake_trout = SpeciesFactory(common_name="Lake Trout",
                                scientific_name='Salvelinus namaycush',
                                species_code=81,
                                primary=True)

    walleye = SpeciesFactory(common_name="Walleye",
                             scientific_name='Sander vitreum',
                             species_code=334,
                             primary=True)

    round_whitefish = SpeciesFactory(common_name="Round Whitefish",
                                     scientific_name='Prosopium cylindraceum',
                                     species_code=102,
                                     primary=False)



def test_species_str():
    """str() method method of a Species object should return a string
    like so: <Common Name> (Scientific Name)

    """

    attrs = {'common_name':'Lake Trout',
             'scientific_name':'Salvelinus namaycush',
             'species_code':81,
             'primary':True
    }

    species = Species(common_name=attrs.get('common_name'),
                      scientific_name=attrs.get('scientific_name'),
                      species_code=attrs.get('species_code'),
                      primary=attrs.get('primary'))


    should_be = '{common_name} ({scientific_name})'
    assert str(species) == should_be.format(**attrs)



def test_species_no_scientific_name():
    """If there is no scientific name, the string representation of a
    species object is just the common name.
    """
    attrs = {'common_name':'Salvelinus Sp.',
             'species_code':86,
             'primary':True
    }

    species = Species(common_name=attrs.get('common_name'),
                      scientific_name=attrs.get('scientific_name'),
                      species_code=attrs.get('species_code'),
                      primary=attrs.get('primary'))

    should_be = '{common_name}'
    assert str(species) == should_be.format(**attrs)




@pytest.mark.django_db
def test_species_model_manager(db_setup):
    """The default species manager should only return the active
    species.
    """
    species = Species.objects.all()
    spc_codes = [x.species_code for x in species]
    should_be = [81, 334]

    should_be.sort()
    spc_codes.sort()
    assert spc_codes==should_be


@pytest.mark.django_db
def test_species_model_manager_all_species(db_setup):
    """the custom manager allspecies should return all species, regardless
    of their primary designation.

    """

    species = Species.allspecies.all()
    spc_codes = [x.species_code for x in species]
    should_be = [81, 102, 334]

    should_be.sort()
    spc_codes.sort()
    assert spc_codes==should_be
