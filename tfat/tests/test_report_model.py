'''
=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_report_model.py
Created: 18 Jun 2015 12:05:51


DESCRIPTION:

Tests of the methods associated with the tag report model.

A. Cottrill
=============================================================
'''


from tfat.models import Recovery

from tfat.tests.factories import *

import pytest


@pytest.mark.django_db
def test_report_str_complete():
    """The default string representation for a tag report is the anglers
    fist and last name plus the date the report was filed.
    """

    elements = {'first_name':'Homer',
                'last_name':'Simpson',
                'obs_date':datetime(2013,10,16),
    }


    angler = JoePublicFactory(first_name=elements['first_name'],
                       last_name=elements['last_name'],
    )

    report = Report(reported_by=angler, report_date=elements['obs_date'])

    #convert our date the expected string format
    elements['obs_date'] = elements['obs_date'].strftime('%b-%d-%Y')

    should_be = "{first_name} {last_name} on {obs_date}"

    assert str(report) == should_be.format(**elements)


@pytest.mark.django_db
def test_report_str_no_date():
    """the string representation of a report without a date is the anglers
    first and last name plus the report id.

    """

    elements = {'first_name':'Homer',
                'last_name':'Simpson',
    }


    angler = JoePublicFactory(first_name=elements['first_name'],
                       last_name=elements['last_name'],
    )

    report = Report(reported_by=angler, report_date=None)

    elements['id'] = report.id

    should_be = "{first_name} {last_name} <Report id={id}>"

    assert str(report) == should_be.format(**elements)

@pytest.mark.django_db
def test_report_str_no_date_or_angler():
    """The string representation of a report without an angler or date is
    just the report id

    """

    report = Report(reported_by=None, report_date=None)
    assert str(report) == "<Report id={}>".format(report.id)



@pytest.mark.django_db
def test_get_tags():
    """the get_tags() method of the report object should return a list of
    tag numbers associated with the report.

    """
    report = ReportFactory()
    species = SpeciesFactory()
    tag1 = RecoveryFactory(report=report, spc=species)
    tag2 = RecoveryFactory(report=report, spc=species)
    tag3 = RecoveryFactory(report=report, spc=species)

    tags = report.get_tags()

    assert tag1 in tags
    assert tag2 in tags
    assert tag3 in tags

@pytest.mark.django_db
def test_get_tags_no_tags():
    """the get_tags() method of the report object should gracefully return
    None if no tags where associated with this report.  (I'm not sure why
    there is a report if there are not tags')

    """
    report = ReportFactory()
    tags = report.get_tags()
    assert len(tags) == len([])
