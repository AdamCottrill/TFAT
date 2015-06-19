'''=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_report_list.py
Created: 19 Jun 2015 10:07:24

DESCRIPTION:

The tests in this module verify that the view that renders the list of
tag reports render as expected.

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

    Arguments:
    - `db`:
    """

    report_date = datetime(2010,10,10)
    spc = SpeciesFactory()

    angler1 = JoePublicFactory.create(first_name='Homer',
                                           last_name='Simpson')

    angler2 = JoePublicFactory.create(first_name='Montgomery',
                                           last_name='Burns')

    angler3 = JoePublicFactory.create(first_name='Barney',
                                           last_name='Gumble')

    #report filed by Homer
    report = ReportFactory(reported_by=angler1, report_date = report_date)
    tagids = ['111111','222222','333333']
    for tag in tagids:
        recovery = RecoveryFactory(report=report,spc=spc,tagid=tag)

    #a report filed by Monty Burns
    report = ReportFactory(reported_by=angler2, follow_up=True,
                                report_date = report_date)
    tagids = ['4444','5555','6666']
    for tag in tagids:
        recovery = RecoveryFactory(report=report,spc=spc,tagid=tag)


@pytest.mark.django_db
def test_tag_report_list(client, db_setup):
    '''verify that the report list renders properly and includes the
    appropriate title.'''
    url = reverse('recovery_report_list')
    response = client.get(reverse('recovery_report_list'))
    assert response.status_code == 200
    content = str(response.content)
    assert 'Tag Recovery Reports' in content

@pytest.mark.django_db
def test_angler_names_in_tag_report_list(client, db_setup):
    '''the name of the anglers who have sumbitted reports should appear in
    the report list, any anglers who have not sumbitted reports should not
    appear in the list.'''

    url = reverse('recovery_report_list')
    response = client.get(reverse('recovery_report_list'))
    content = str(response.content)
    assert 'Homer Simpson' in content
    assert 'Montgomery Burns' in content
    assert 'Barney Gumble' not in content


@pytest.mark.django_db
def test_tagids_in_tag_report_list(client, db_setup):
    '''the tag numbers assocaited with the reports should appear in the
    resonse'''
    url = reverse('recovery_report_list')
    response = client.get(reverse('recovery_report_list'))
    content = str(response.content)

    tagids = ['111111','222222','333333','4444','5555','6666']
    for tagid in tagids:
        assert tagid in content


@pytest.mark.django_db
def test_follow_up_in_tag_report_list(client, db_setup):
    '''If there is a follow required for a report, it should appear in the
    list of reports
    '''
    url = reverse('recovery_report_list')
    response = client.get(reverse('recovery_report_list'))
    content = str(response.content)
    assert 'Follow-up Required' in content
