'''
=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_recovery_model.py
Created: 18 Jun 2015 12:05:51

DESCRIPTION:

Tests of the methods associated with the tag recovery model object.

A. Cottrill
=============================================================
'''


from tfat.models import Recovery

from tfat.tests.factories import *

import pytest


@pytest.mark.django_db
def test_recovery_pop_text():
    """Verify that the pop_text() method returns the elements we think it should
    """


    elements = {'first_name':'Homer',
                'last_name':'Simpson',
                'tagid': '1234',
                'tagdoc':'25015',
                'obs_date':datetime(2013,10,16),
                'common_name':'Walleye',
                'species_code':'334',
                'general_loc':'out there',
                'specific_loc':'in Georgian Bay',
                'comment':'It had three eyes.'
    }


    angler = JoePublicFactory(first_name=elements['first_name'],
                       last_name=elements['last_name'],
    )

    report = ReportFactory(reported_by=angler)

    species = SpeciesFactory(common_name=elements['common_name'],
                             species_code=elements['species_code'])

    encounter = Recovery(report=report,
                                spc=species,
                                tagid=elements['tagid'],
                                tagdoc=elements['tagdoc'],
                                recovery_date=elements['obs_date'],
                                general_name =elements['general_loc'],
                                specific_name =elements['specific_loc'],
                                comment =elements['comment'],
)

    popup_text = encounter.popup_text()

    #convert out date the expected string format
    elements['obs_date'] = elements['obs_date'].strftime('%b-%d-%Y')

    #loop over all of the elements we used to build our models and
    #expect to see in the popup text and assert they are there:
    for k,v in elements.items():
        assert v in popup_text
