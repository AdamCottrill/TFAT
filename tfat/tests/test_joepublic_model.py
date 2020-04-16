"""
=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_joepublic_model.py
Created: 18 Jun 2015 12:05:51


DESCRIPTION:

Tests of the methods associated with the tag report model.

A. Cottrill
=============================================================
"""

import pytz
from tfat.models import Recovery

from tfat.tests.factories import *

import pytest


@pytest.fixture()
def db_setup():

    report_date = datetime(2010, 10, 10).replace(tzinfo=pytz.UTC)
    species = SpeciesFactory()

    angler1 = JoePublicFactory.create(
        first_name="Homer",
        last_name="Simpson",
        address1="742 Evergreen Tarrace",
        address2="Box 123",
        town="Springfield",
        province="Ontario",
        postal_code="N0W2T2",
        email="hsimpson@hotmail.com",
        phone="555-321-1234",
    )

    angler2 = JoePublicFactory.create(first_name="Montgomery", last_name="Burns")

    # report filed by Homer
    report = ReportFactory(reported_by=angler1, report_date=report_date)
    tagids = ["111111", "222222", "333333"]
    for tag in tagids:
        recovery = RecoveryFactory(report=report, species=species, tagid=tag)

    # a report filed by Monty Burns
    report = ReportFactory(reported_by=angler1, follow_up=True, report_date=report_date)

    tagids = ["4444", "5555"]
    for tag in tagids:
        recovery = RecoveryFactory(report=report, species=species, tagid=tag)


@pytest.mark.django_db
def test_str_complete():
    """if an angler (joe public) has both first name and an initial, the
    __str__ should return {first_name} {initial}. {last_name}"""

    names = {"first_name": "Homer", "initial": "J", "last_name": "Simpson"}

    angler = JoePublicFactory(
        first_name=names.get("first_name"),
        initial=names.get("initial"),
        last_name=names.get("last_name"),
    )

    should_be = "{first_name} {initial}. {last_name}"
    assert str(angler) == should_be.format(**names)


@pytest.mark.django_db
def test_str_no_initial():
    """if an angler (joe public) has both first name and an initial, the
    __str__ should return {first_name} {last_name}"""

    names = {"first_name": "Homer", "last_name": "Simpson"}

    angler = JoePublicFactory(
        first_name=names.get("first_name"),
        initial=None,
        last_name=names.get("last_name"),
    )
    should_be = "{first_name} {last_name}"

    assert str(angler) == should_be.format(**names)


# @pytest.mark.django_db
# def test_str_last_name_only():
#    '''if an angler (joe public) only has a last_name, the
#    __str__ method should return just the last_name'''
#
#    names = {'last_name':'Simpson'}
#
#    angler = JoePublicFactory(first_name=None,
#                              initial=None,
#                              last_name=names.get('last_name'))
#    assert str(angler) == names['last_name']


@pytest.mark.django_db
def test_joepublic_report_count(db_setup):
    """the report count() method of a JoePublic object should be the number
    of tag reports they have filed.
    """
    # homer has 2 reports, monty has 0

    homer = JoePublic.objects.get(first_name="Homer")
    assert homer.report_count() == 2

    monty = JoePublic.objects.get(first_name="Montgomery")
    assert monty.report_count() == 0


@pytest.mark.django_db
def test_joepublic_tag_count(db_setup):
    """the tag_count() method of a JoePublic object should be the number
    of tags tehy have reported (summed across all reports)
    """
    # homer has 5 tags, monty has 0

    homer = JoePublic.objects.get(first_name="Homer")
    assert homer.tag_count() == 5

    monty = JoePublic.objects.get(first_name="Montgomery")
    assert monty.tag_count() == 0
