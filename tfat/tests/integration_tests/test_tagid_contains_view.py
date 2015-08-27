'''=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_tagid_contains_view.py
Created: 27 Aug 2015 09:06:04

DESCRIPTION:

The tests in this module verify that the view that renders the
the details associated with a partial tagid render correctly.

This file was modified directly from the tests of tagid_detail_view

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

    project = ProjectFactory(prj_cd='LHA_IA11_111', prj_nm='Fake Project')

    #same species, same tagdoc - everything is A-Ok.
    encounter1 = EncounterFactory(spc=spc1, tagid='11111', project=project,
                                  tagdoc='25012')
    encounter2 = EncounterFactory(spc=spc1, tagid='11111', project=project,
                                  tagdoc='25012')

    encounter2 = EncounterFactory(spc=spc1, tagid='11111', project=project,
                                  tagdoc='25012')

    #different species
    encounter3 = EncounterFactory(spc=spc1, tagid='22222', project=project,
                                  tagdoc='25012')
    encounter4 = EncounterFactory(spc=spc2, tagid='22222', project=project,
                                  tagdoc='25012')

    #same species, different tagdoc
    encounter3 = EncounterFactory(spc=spc1, tagid='33333', project=project,
                                  tagdoc='25012')
    encounter4 = EncounterFactory(spc=spc1, tagid='33333', project=project,
                                  tagdoc='15012')


    angler1 = JoePublicFactory.create(first_name='Homer',
                                           last_name='Simpson')
    #angler report filed by Homer
    report = ReportFactory(reported_by=angler1)
    recovery = RecoveryFactory(report=report,spc=spc1,tagid='11111')


#@pytest.mark.django_db
#def test_tagid_does_not_exist(client, db_setup):
#    '''if we try to access the detail page for a tagid that does no exist
#    the age should render but contain appropriate messages indicating
#    that the tag has not been obseved by UGMLU or reported by the
#    general public.
#
#    '''
#
#    tagid = 9999
#    url = reverse('tagid_detail_view', kwargs={'tagid':tagid})
#    response = client.get(url)
#
#    content = str(response.content)
#
#    #No UGMLU observations
#    msg = "{} has not been observed in any UGLMU project."
#    assert msg.format(tagid) in content
#
#    #No Angler reports
#    msg = ("There are no reports of tag {} from the general"
#           " public or other agencies")
#    assert msg.format(tagid) in content
#

#
#@pytest.mark.django_db
#def test_multiple_species_warning(client, db_setup):
#    """If there is more than one species associated with a tag, a warning
#    should be included in the repsonse.
#    """
#
#    url = reverse('tagid_detail_view', kwargs={'tagid':'33333'})
#    response = client.get(url)
#    content = str(response.content)
#
#    msg = ("There appears to be more than one tagdoc code associated "
#           "with the records on this page. Interpret with caution.")
#
#    assert msg in content
#
#
#@pytest.mark.django_db
#def test_multiple_species_warning_ok(client, db_setup):
#    """As long as all of the species associated with a tag are the same,
#    the warning should not appear in the reponse.
#
#    """
#
#    url = reverse('tagid_detail_view', kwargs={'tagid':'11111'})
#    response = client.get(url)
#    content = str(response.content)
#
#    msg = ("There appears to be more than one tagdoc code associated "
#           "with the records on this page. Interpret with caution.")
#
#    assert msg not in content
#
#
#
#@pytest.mark.django_db
#def test_multiple_tagdoc_warning(client, db_setup):
#    """If there is more than one tagdoc associated with a tag, a warning
#    should be included in the repsonse.
#    """
#
#    url = reverse('tagid_detail_view', kwargs={'tagid':'22222'})
#    response = client.get(url)
#    content = str(response.content)
#
#    msg = ("There appears to be more than one species associated "
#           "with the records on this page. Interpret with caution.")
#
#    assert msg in content
#
##
#@pytest.mark.django_db
#def test_multiple_tagdoc_warning_ok(client, db_setup):
#    """As long as all of the tagdocs associated with a tag are the same,
#    the warning should not appear in the reponse.
#
#    """
#
#    url = reverse('tagid_detail_view', kwargs={'tagid':'11111'})
#    response = client.get(url)
#    content = str(response.content)
#
#    msg = ("There appears to be more than one species associated "
#           "with the records on this page. Interpret with caution.")
#
#    assert msg not in content
#
#
#@pytest.mark.django_db
#def test_tagid_details_includes_encounters_and_angler_recaps(client, db_setup):
#    """The tagid details page should include encounter events from both
#    the MNR and any angler returns.
#
#    Arguments:
#    - `client`:
#    - `db_setup`:
#
#    """
#    url = reverse('tagid_detail_view', kwargs={'tagid':'11111'})
#
#    response = client.get(url)
#    content = str(response.content)
#
#    assert 'Homer Simpson' in content  #angler return record
#    assert 'LHA_IA11_111' in content   #omnr project code
#    assert 'Fake Project' in content   #omnr project name


@pytest.mark.django_db
def test_tagid_contains_includes_encounters_and_angler_recaps(client, db_setup):
    """The tagid contains page should include encounter events from both
    the MNR and any angler returns.

    Arguments:
    - `client`:
    - `db_setup`:

    """
    url = reverse('tagid_contains', kwargs={'partial':'111'})

    response = client.get(url)
    content = str(response.content)

    assert 'Homer Simpson' in content  #angler return record
    assert 'LHA_IA11_111' in content   #omnr project code
    assert 'Fake Project' in content   #omnr project name


@pytest.mark.django_db
def test_tagid_contains_includes_nobs_with_angler_recaps(client, db_setup):

    """The tagid contains page should include the string N = {nobs} that
    correctly indicates the number of times this tags matching <partial>
    have been observed including both OMNR encounters and angler
    recaptures.

    Arguments:
    - `client`:
    - `db_setup`:

    """
    url = reverse('tagid_contains', kwargs={'partial':'111'})

    response = client.get(url)
    content = str(response.content)

    assert 'N = 4' in content

#@pytest.mark.django_db
#def test_tagid_details_includes_nobs_with_anlger_recaps(client, db_setup):
#    """The tagid details page should include the string 'N = {nobs}' that
#    correctly indicates the number of times this tag number has been
#    observed including both OMNR encounters and angler recaptures.
#
#    Arguments:
#    - `client`:
#    - `db_setup`:
#
#    """
#    url = reverse('tagid_detail_view', kwargs={'tagid':'11111'})
#
#    response = client.get(url)
#    content = str(response.content)
#
#    assert 'N = 4' in content
#

@pytest.mark.django_db
def test_tagid_detail_includes_nobs_without_angler_recaps(client, db_setup):
    """The tagid details page should include the string 'N = {nobs}' that
    correctly indicates the number of times this tag number has been
    observed - even if it has not been reported by any anglers.

    Arguments:
    - `client`:
    - `db_setup`:

    """
    url = reverse('tagid_contains', kwargs={'partial':'222'})

    response = client.get(url)
    content = str(response.content)

    assert 'N = 2' in content

#@pytest.mark.django_db
#def test_tagid_detail_includes_nobs_without_anlger_recaps(client, db_setup):
#    """The tagid detail page should include the string 'N = {nobs}' that
#    correctly indicates the number of times this tag number has been
#    observed even without any angler recaps.
#
#    Arguments:
#    - `client`:
#    - `db_setup`:
#
#    """
#    url = reverse('tagid_detail_view', kwargs={'tagid':'22222'})
#
#    response = client.get(url)
#    content = str(response.content)
#
#    assert 'N = 2' in content
