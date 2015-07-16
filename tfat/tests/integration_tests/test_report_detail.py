'''=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_report_detail.py
Created: 26 Jun 2015 13:25:34


DESCRIPTION:

This script contains an integraion test to verify that the report
detail page renders as expected.

A. Cottrill
=============================================================

'''



import pytest
from django.core.urlresolvers import reverse

from tfat.tests.factories import *

from datetime import datetime


@pytest.fixture(scope='class')
def db_setup():

    report_date = datetime(2010,10,10)
    spc = SpeciesFactory()

    angler1 = JoePublicFactory.create(first_name='Homer',
                                      last_name='Simpson',
                                      address1 = '742 Evergreen Tarrace',
                                      address2 = 'Box 123',
                                      town = 'Springfield',
                                      province = 'Ontario',
                                      postal_code = 'N0W2T2',
                                      email = 'hsimpson@hotmail.com',
                                      phone = '555-321-1234',)

    angler2 = JoePublicFactory.create(first_name='Montgomery',
                                           last_name='Burns')

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
def test_report_detail(client, db_setup):
    """Verify that we can navigate to the report detail page (status
    code=200) and that the template is the one we think it is.
    """

    angler = JoePublic.objects.get(first_name='Homer')
    response = client.get(reverse('angler_reports',
                                  kwargs={'angler_id':angler.id}))

    assert 'tfat/angler_reports.html' in [x.name for x in response.templates]
    assert response.status_code == 200


@pytest.mark.django_db
def test_report_detail_has_crud_links(client, db_setup):
    """The report list for a partuclar angler should have links to allow
    us to create and update reports.
    """

    angler = JoePublic.objects.get(first_name='Homer')
    response = client.get(reverse('angler_reports',
                                  kwargs={'angler_id':angler.id}))
    content = str(response.content)

    assert 'Edit Details' in content #angler details
    assert 'Create New Report' in content
    assert 'Edit Report' in content


@pytest.mark.django_db
def test_tagids_in_report_detail(client, db_setup):
    """The tags reported by a particular individual should appear in the
    report details pages but tags reported by other anlgers should
    not.
    """

    angler = JoePublic.objects.get(first_name='Homer')
    response = client.get(reverse('angler_reports',
                                  kwargs={'angler_id':angler.id}))
    content = str(response.content)

    tagids = ['111111','222222','333333']
    for tag in tagids:
        assert tag in content

    tagids = ['4444','5555','6666']
    for tag in tagids:
        assert tag not in content


@pytest.mark.django_db
def test_report_date_in_report_detail(client, db_setup):
    """The data each report was filed on should appear on the report details
    page."""

    report_date = datetime(2010,10,10)

    angler = JoePublic.objects.get(first_name='Homer')
    response = client.get(reverse('angler_reports',
                                  kwargs={'angler_id':angler.id}))
    content = str(response.content)

    #format the date and replace any leading zeros
    date = report_date.strftime('%b %d, %Y').replace(' 0',' ')
    assert date in content


@pytest.mark.django_db
def test_angler_info_in_report_detail(client, db_setup):
    """The basic angler information should be included in the report list
    - who filled all of these reports and how do we get in touch with
    them.
    """

    angler = JoePublic.objects.get(first_name='Homer')
    response = client.get(reverse('angler_reports',
                                  kwargs={'angler_id':angler.id}))
    content = str(response.content)

    assert '742 Evergreen Tarrace' in content
    assert 'Box 123' in content
    assert 'Springfield' in content
    assert 'Ontario' in content
    assert 'N0W2T2' in content
    assert 'hsimpson@hotmail.com' in content
    assert '555-321-1234' in content


@pytest.mark.django_db
def test_report_follow_up_not_in_response(client, db_setup):
    """If a follow is requested for this report, it should be included in
    the reponse.
    """

    angler = JoePublic.objects.get(first_name='Homer')
    #verify that follow-up required is not in the list now:
    response = client.get(reverse('angler_reports',
                                  kwargs={'angler_id':angler.id}))
    content = str(response.content)
    assert 'Follow-up Required' not in content


@pytest.mark.django_db
def test_report_follow_up_in_response(client, db_setup):
    """If not follow-up is currently required for this report, 'Follow-up
    Required' should not appear in the response.
    """

    angler = JoePublic.objects.get(first_name='Montgomery')
    response = client.get(reverse('angler_reports',
                                  kwargs={'angler_id':angler.id}))
    content = str(response.content)
    assert 'Follow-up Required' in content
