'''=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_report_form.py
Created: 22 Jul 2015 11:41:41

DESCRIPTION:

These currently FAIL.

A series of tests to verify that the report form works as expected
when used to create or edit reports.



required data elements:
- tag reporter's name

optional data elements:
- report date
- date flage


calculated/derived/default quantities:
- if report date is null when submitted, it should be set to current date and the date flag set to 'derived'
- if report format is dcr, we need effort and dcr number
- if report format is not dcr, effort and dcr number should be empty

- after succesfully creating a new report, or editing and existing
  one, we should be redirected to the report detail page.

A. Cottrill
=============================================================

'''

import pytest
from django.core.urlresolvers import reverse
from django.core.files import File

from tfat.models import JoePublic, Report
from tfat.tests.factories import *

from datetime import datetime, timedelta

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def setup_module(module):
    print ("setup_module      module:%s" % module.__name__)

def teardown_module(module):
    print ("teardown_module   module:%s" % module.__name__)


@pytest.fixture(scope='class')
def db_setup():
    """Create some users with easy to remember names.
    """

    report_date = datetime(2010,10,10)
    spc = SpeciesFactory()

    angler1 = JoePublicFactory.create(first_name='Homer',
                                      last_name='Simpson')
    angler2 = JoePublicFactory.create(first_name='Montgomery',
                                           last_name='Burns')
    angler3 = JoePublicFactory.create(first_name='Barney',
                                      last_name='Gumble')

    mock_file = StringIO('fake file content.')
    mock_file.name = "path/to/some/fake/fake_test_file.txt"

    #complete report filed by Homer
    report = ReportFactory(reported_by=angler1,
                           report_date = report_date,
                           reporting_format = 'dcr',
                           dcr = 'dcr123', effort='eff001',
                           associated_file = File(mock_file),
                           comment='A fake comment.',
                           follow_up=True
    )

    #a minimal report filed by Monty Burns without any options or
    #associated tags to test conditional elements
    report = ReportFactory(reported_by=angler2, follow_up=False,
                                report_date = report_date)


@pytest.mark.django_db
def test_create_report_url(client, db_setup):
    """Verify that the form and its correct elements are rendered when we
    call create_report and all of the appropriate elements are there"""

    angler = JoePublic.objects.get(first_name='Homer')

    url = reverse('create_report', kwargs={'angler_id':angler.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'tfat/report_form.html' in [x.name for x in response.templates]

    content = str(response.content)
    assert "Report Date:" in content
    assert "Date Flag:" in content
    assert "Report Format:" in content
    assert "DCR:" in content
    assert "Effort Number:" in content
    assert "Comment:" in content
    assert "Follow-up Required or Requested" in content

@pytest.mark.django_db
def test_create_report_url_404(client, db_setup):
    """If we try to create a report for an angler who does not exist, we
    should get a 404 error."""

    url = reverse('create_report', kwargs={'angler_id':9999999})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_edit_report_url(client, db_setup):
    """Verify that the form and its correct elements are rendered when we
    call the edit_report form and all of the appropriate elements are there"""

    report = Report.objects.get(reported_by__first_name='Homer')
    url = reverse('edit_report', kwargs={'report_id':report.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'tfat/report_form.html' in [x.name for x in response.templates]

    content = str(response.content)
    assert "Report Date:" in content
    assert "Date Flag:" in content
    assert "Report Format:" in content
    assert "DCR:" in content
    assert "Effort Number:" in content
    assert "Comment:" in content
    assert "Follow-up Required or Requested" in content


@pytest.mark.django_db
def test_edit_report_url_404(client, db_setup):
    """If we try to edit a report that does not exist, we
    should get a 404 error."""

    url = reverse('edit_report', kwargs={'report_id':9999999})
    response = client.get(url)
    assert response.status_code == 404


# REPORT CREATION
@pytest.mark.django_db
def test_create_report_minimal_data(client, db_setup):
    '''if we post minimal data, a report should be created for this
    angler.  Date should be today, date flag should be 'unknown', and
    the other fields should all be empty, and we should be re-directed
    to the report's detail page
    '''


    angler = JoePublic.objects.get(first_name='Barney')
    url = reverse('create_report', kwargs={'angler_id':angler.id})
    data = {'reported_by':angler.id,}
    response = client.post(url, data, follow=True)

    assert response.status_code == 200
    templates = [x.name for x in response.templates]
    assert 'tfat/report_detail.html' in templates

    #query the database and make sure the data is how we expect it.
    today = datetime.today()
    report = Report.objects.get(reported_by__first_name='Barney')
    assert report.report_date.date() == today.date()
    assert report.date_flag == 0
    assert report.associated_file.name is ''
    assert report.dcr is ''
    assert report.effort is ''
    assert report.comment is ''
    assert report.follow_up is False


@pytest.mark.django_db
def test_create_report_invalid_date(client, db_setup):
    '''if we post data with a date that does not make sense, an error
    should be thrown'''

    angler = JoePublic.objects.get(first_name='Barney')

    data = {'reported_by':angler.id,
            'report_date':'not a date'}

    url = reverse('create_report', kwargs={'angler_id':angler.id})
    response = client.post(url, data, follow=True)

    content = str(response.content)
    assert 'Enter a valid date/time.' in content


@pytest.mark.django_db
def test_create_report_future_date(client, db_setup):
    '''if we post data with a date in the future, an error
    should be thrown'''

    next_week = datetime.today() + timedelta(days=7)

    angler = JoePublic.objects.get(first_name='Barney')

    data = {'reported_by':angler.id,
            'report_date':next_week}

    url = reverse('create_report', kwargs={'angler_id':angler.id})
    response = client.post(url, data, follow=True)

    content = str(response.content)
    assert 'Dates in the future are not allowed.' in content


@pytest.mark.django_db
def test_create_report_dcr_complete(client, db_setup):
    '''If we post data with format=dcr, and provide a dcr number and
    effort number, the report should be created.'''

    angler = JoePublic.objects.get(first_name='Barney')
    url = reverse('create_report', kwargs={'angler_id':angler.id})

    data = {'reported_by':angler.id,
            'reporting_format':'dcr',
            'dcr':'DCR1234',
            'effort':'001'}

    response = client.post(url, data, follow=True)

    report = Report.objects.get(reported_by__first_name='Barney')
    assert report.reporting_format == 'dcr'
    assert report.dcr == 'DCR1234'
    assert report.effort == '001'

@pytest.mark.django_db
def test_create_report_dcr_missing_dcr_number(client, db_setup):
    '''If we post data with format=dcr, but omit the dcr number, an error
    should be thrown.
    '''

    angler = JoePublic.objects.get(first_name='Barney')
    url = reverse('create_report', kwargs={'angler_id':angler.id})

    data = {'reported_by':angler.id,
            'reporting_format':'dcr',
            'effort':'001'}

    response = client.post(url, data, follow=True)

    content = str(response.content)
    assert 'DCR number is required if reported by &quot;DCR&quot;.' in content


@pytest.mark.django_db
def test_create_report_dcr_missing_effort_number(client, db_setup):
    '''If we post data with format=dcr, but omit the effort number, an error
    should be thrown.
    '''

    angler = JoePublic.objects.get(first_name='Barney')
    url = reverse('create_report', kwargs={'angler_id':angler.id})

    data = {'reported_by':angler.id,
            'reporting_format':'dcr',
            'dcr':'DCR1234',}

    response = client.post(url, data, follow=True)

    content = str(response.content)
    assert 'Effort number is required if reported by &quot;DCR&quot;.' in content


@pytest.mark.django_db
def test_create_report_not_dcr_with_effort_number(client, db_setup):
    '''If we post data with format other than dcr, and include an effort
    number, an error should be thrown - effort is not meaningful
    unless reporting format is dcr

    '''

    angler = JoePublic.objects.get(first_name='Barney')
    url = reverse('create_report', kwargs={'angler_id':angler.id})

    data = {'reported_by':angler.id,
            'reporting_format':'verbal',
            'effort':'001'}

    response = client.post(url, data, follow=True)

    content = str(response.content)
    msg = 'Effort should be empty if Report Format is not &quot;DCR&quot;.'
    assert msg in content


@pytest.mark.django_db
def test_create_report_not_dcr_with_dcr_number(client, db_setup):
    '''If we post data with format other than dcr, and include an dcr
    number, an error should be thrown - a dcr number is not meaningful
    unless reporting format is dcr

    '''

    angler = JoePublic.objects.get(first_name='Barney')
    url = reverse('create_report', kwargs={'angler_id':angler.id})

    data = {'reported_by':angler.id,
            'reporting_format':'verbal',
            'dcr':'DCR1234'}

    response = client.post(url, data, follow=True)

    content = str(response.content)
    msg = 'DCR should be empty if Report Format is not &quot;DCR&quot;.'

    print(content)
    assert msg in content


@pytest.mark.django_db
def test_create_report_with_file(client, db_setup):
    '''if we post data with an associated file object, the report should
    be created and have an associated file object.'''
    assert 0==1


@pytest.mark.django_db
def test_create_report_with_comment(client, db_setup):
    '''if we post data with a comment, the report should
    be created and have that comment associated with it.'''

    angler = JoePublic.objects.get(first_name='Barney')
    url = reverse('create_report', kwargs={'angler_id':angler.id})
    data = {'reported_by':angler.id,
            'comment':'My Fake Comment'}
    response = client.post(url, data, follow=True)

    #query the database and make sure the data is how we expect it.
    report = Report.objects.get(reported_by__first_name='Barney')
    assert report.comment == 'My Fake Comment'


@pytest.mark.django_db
def test_create_report_with_follow_up(client, db_setup):
    '''if we post data with follow_up=True, the report should
    be created and its follow_up value should be TRUE.'''

    angler = JoePublic.objects.get(first_name='Barney')
    url = reverse('create_report', kwargs={'angler_id':angler.id})
    data = {'reported_by':angler.id,
            'follow_up':True}
    response = client.post(url, data, follow=True)

    #query the database and make sure the data is how we expect it.
    report = Report.objects.get(reported_by__first_name='Barney')
    assert report.follow_up is True


# REPORT EDITING:
@pytest.mark.django_db
def test_edit_report_change_date(client, db_setup):
    """verifty that we can post data with a different date and change the
    report in the database."""
    pass


@pytest.mark.django_db
def test_edit_report_change_date_flag(client, db_setup):
    """verifty that we can post data with a different date flag and change the
    report in the database."""
    pass


@pytest.mark.django_db
def test_edit_report_change_format_to_dcr_without_dcr_number(client, db_setup):
    """if we post data to change reporting format to dcr without providing
    a dcr number, an error will be thrown"""
    pass


@pytest.mark.django_db
def test_edit_report_change_format_to_dcr_without_eff_number(client, db_setup):
    """if we post data to change reporting format to dcr without providing
    an effort number, an error will be thrown"""
    pass


@pytest.mark.django_db
def test_edit_report_change_format_to_dcr_with_dcr_eff(client, db_setup):
    """if we post data to change reporting format to dcr and provide
    dcr and effort numbers, the report should be updated"""
    pass


@pytest.mark.django_db
def test_edit_report_change_format_to_dcr_with_dcr_eff(client, db_setup):
    """if we post data to change reporting format from dcr to something
    else the report should be updated and the associated effort and
    dcr values should be none.

    """
    pass


@pytest.mark.django_db
def test_edit_report_change_comment(client, db_setup):
    """if we post data to change reporting format to dcr and provide
    dcr and effort numbers, the report should be updated"""
    pass



@pytest.mark.django_db
def test_edit_report_change_follow_up(client, db_setup):
    """if we post data to change reporting format to dcr and provide
    dcr and effort numbers, the report should be updated"""
    pass
