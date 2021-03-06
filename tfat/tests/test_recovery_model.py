"""
=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_recovery_model.py
Created: 18 Jun 2015 12:05:51

DESCRIPTION:

Tests of the methods associated with the tag recovery model object.

A. Cottrill
=============================================================
"""

import pytz

from tfat.models import Recovery
from tfat.constants import (
    TAG_COLOUR_CHOICES,
    TAG_ORIGIN_CHOICES,
    TAG_TYPE_CHOICES,
    TAG_POSITION_CHOICES,
)

from tfat.tests.factories import *

import pytest


@pytest.mark.django_db
def test_recovery_pop_text():
    """Verify that the pop_text() method returns the elements we think it should
    """

    elements = {
        "first_name": "Homer",
        "last_name": "Simpson",
        "tagid": "1234",
        "tagdoc": "25015",
        "obs_date": datetime(2013, 10, 16).replace(tzinfo=pytz.UTC),
        "common_name": "Walleye",
        "species_code": "334",
        "general_loc": "out there",
        "specific_loc": "in Georgian Bay",
        "comment": "It had three eyes.",
    }

    angler = JoePublicFactory(
        first_name=elements["first_name"], last_name=elements["last_name"]
    )

    report = ReportFactory(reported_by=angler)

    species = SpeciesFactory(
        spc_nmco=elements["common_name"], spc=elements["species_code"]
    )

    encounter = Recovery(
        report=report,
        species=species,
        tagid=elements["tagid"],
        tagdoc=elements["tagdoc"],
        recovery_date=elements["obs_date"],
        general_location=elements["general_loc"],
        specific_location=elements["specific_loc"],
        comment=elements["comment"],
    )

    popup_text = encounter.popup_text()

    # convert out date the expected string format
    elements["obs_date"] = elements["obs_date"].strftime("%b-%d-%Y")

    # loop over all of the elements we used to build our models and
    # expect to see in the popup text and assert they are there:
    for k, v in elements.items():
        assert v in popup_text


@pytest.mark.django_db
def test_recovery_get_comments():
    """get comments is a little helper function that converts the comments
    in the general, specific and comments field to a single formatted
    string.

    """

    elements = {
        "general_loc": "out there",
        "specific_loc": "in Georgian Bay",
        "comment": "It had three eyes.",
    }

    report = ReportFactory()
    species = SpeciesFactory()
    encounter = RecoveryFactory(
        report=report,
        species=species,
        general_location=elements["general_loc"],
        specific_location=elements["specific_loc"],
        comment=elements["comment"],
    )

    comments = encounter.get_comments()
    should_be = "{general_loc}({specific_loc})<br />{comment}"
    assert comments == should_be.format(**elements)


@pytest.mark.django_db
def test_recovery_get_comments_without_comment():
    """get comments is a little helper function that converts the comments
    in the general, specific and comments field to a single formatted
    string. - if the comment is missing, it should just ignored.

    """

    elements = {
        "general_loc": "out there",
        "specific_loc": "in Georgian Bay",
        "comment": "It had three eyes.",
    }

    report = ReportFactory()
    species = SpeciesFactory()
    encounter = RecoveryFactory(
        report=report,
        species=species,
        general_location=elements["general_loc"],
        specific_location=elements["specific_loc"],
        comment=None,
    )

    comments = encounter.get_comments()
    should_be = "{general_loc}({specific_loc})"
    assert comments == should_be.format(**elements)


@pytest.mark.django_db
def test_recovery_get_comments_without_specific():
    """get comments is a little helper function that converts the comments
    in the general, specific and comments field to a single formatted
    string. - if the comment is missing, it should just ignored.

    """

    elements = {
        "general_loc": "out there",
        "specific_loc": "in Georgian Bay",
        "comment": "It had three eyes.",
    }

    report = ReportFactory()
    species = SpeciesFactory()
    encounter = RecoveryFactory(
        report=report,
        species=species,
        general_location=elements["general_loc"],
        specific_location=None,
        comment=None,
    )

    comments = encounter.get_comments()
    should_be = "{general_loc}"
    assert comments == should_be.format(**elements)


@pytest.mark.django_db
def test_recovery_get_comments_when_all_are_none():
    """get comments is a little helper function that converts the comments
    in the general, specific and comments field to a single formatted
    string. - if the general location, specific lcoation, and comment
    field are all empty, we should return an empty string.

    """

    elements = {
        "general_loc": "out there",
        "specific_loc": "in Georgian Bay",
        "comment": "It had three eyes.",
    }

    report = ReportFactory()
    species = SpeciesFactory()
    encounter = RecoveryFactory(
        report=report,
        species=species,
        general_location=None,
        specific_location=None,
        comment=None,
    )

    comments = encounter.get_comments()
    assert comments == ""


@pytest.mark.django_db
def test_recovery_observation_date():
    """If a recovery has a recovery date, recovery.observation_date()
    should return the recovery date.
    """
    obs_date = datetime(2013, 6, 15)

    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species, recovery_date=obs_date)

    assert recovery.observation_date == obs_date


@pytest.mark.django_db
def test_recovery_observation_date_report_date():
    """If a recovery has does not have recovery date, but there is a
    report date, recovery.observation_date should use it.
    """

    obs_date = datetime(2013, 6, 15).replace(tzinfo=pytz.UTC)

    species = SpeciesFactory()
    report = ReportFactory(report_date=obs_date)
    recovery = RecoveryFactory(report=report, species=species, recovery_date=None)

    assert recovery.observation_date == obs_date


@pytest.mark.django_db
def test_recovery_observation_date_none():
    """If a recovery has doe not have recovery_date or a report date,
    recovery.observation_date should return None.
    """

    species = SpeciesFactory()
    report = ReportFactory(report_date=None)
    recovery = RecoveryFactory(report=report, species=species, recovery_date=None)

    assert recovery.observation_date is None


@pytest.mark.django_db
def test_recovery_has_latlon_true():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(
        report=report, species=species, dd_lat=45.5, dd_lon=-81.3
    )
    assert recovery.has_latlon() is True


@pytest.mark.django_db
def test_recovery_has_latlon_false():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species, dd_lat=None, dd_lon=None)
    assert recovery.has_latlon() is False


@pytest.mark.django_db
def test_recovery_has_latlon_no_lat_is_false():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(
        report=report, species=species, dd_lat=None, dd_lon=-81.3
    )
    assert recovery.has_latlon() is False


@pytest.mark.django_db
def test_recovery_has_latlon_no_lon_is_false():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species, dd_lat=45.5, dd_lon=None)
    assert recovery.has_latlon() is False


@pytest.mark.django_db
def test_recovery_flen_inches():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species, flen=450)
    assert recovery.flen_inches() == 17.7


@pytest.mark.django_db
def test_recovery_girth_inches():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species, girth=450)
    assert recovery.girth_inches() == 17.7


@pytest.mark.django_db
def test_recovery_flen_inches_none():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species, flen=None)
    assert recovery.flen_inches() is None


@pytest.mark.django_db
def test_recovery_tlen_inches():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species, tlen=450)
    assert recovery.tlen_inches() == 17.7


@pytest.mark.django_db
def test_recovery_tlen_inches_none():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species, tlen=None)
    assert recovery.tlen_inches() is None


@pytest.mark.django_db
def test_recovery_rwt_pounds():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species, rwt=2000)
    assert recovery.pounds() == 4.4


@pytest.mark.django_db
def test_recovery_rwt_pounds_none():
    """
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species, rwt=None)
    assert recovery.pounds() is None


@pytest.mark.django_db
def test_recovery_tagstat():
    """ By definintion, all of the recoveries from other agencies/the
        general public will have the tag on capture.  This method will ensure
        that the appropriate code is returned for rending in templates.
    """
    species = SpeciesFactory()
    report = ReportFactory()
    recovery = RecoveryFactory(report=report, species=species)
    assert recovery.tagstat() == "C"


# ======================
#   TAG ATTRIBUTES


@pytest.mark.django_db
def test_recovery_tag_type():
    """
    """

    species = SpeciesFactory()
    report = ReportFactory()

    tagdoc_base = "{}5012"

    should_be = {k: v for k, v in TAG_TYPE_CHOICES}
    for k, tag_type in should_be.items():
        tagdoc = tagdoc_base.format(k)
        recovery = RecoveryFactory(report=report, species=species, tagdoc=tagdoc)
        assert recovery.tag_type == tag_type


@pytest.mark.django_db
def test_recovery_tag_origin():
    """
    """

    species = SpeciesFactory()
    report = ReportFactory()

    tagdoc_base = "25{}2"

    should_be = {k: v for k, v in TAG_ORIGIN_CHOICES}
    for k, origin in should_be.items():
        tagdoc = tagdoc_base.format(k)
        recovery = RecoveryFactory(report=report, species=species, tagdoc=tagdoc)
        assert recovery.tag_origin == origin


@pytest.mark.django_db
def test_recovery_tag_position():
    """
    """

    species = SpeciesFactory()
    report = ReportFactory()

    tagdoc_base = "2{}012"

    should_be = {k: v for k, v in TAG_POSITION_CHOICES}
    for k, position in should_be.items():
        tagdoc = tagdoc_base.format(k)
        recovery = RecoveryFactory(report=report, species=species, tagdoc=tagdoc)
        assert recovery.tag_position == position


@pytest.mark.django_db
def test_recovery_tag_colour():
    """
    """

    species = SpeciesFactory()
    report = ReportFactory()

    tagdoc_base = "2501{}"

    should_be = {k: v for k, v in TAG_COLOUR_CHOICES}
    for k, colour in should_be.items():
        tagdoc = tagdoc_base.format(k)
        recovery = RecoveryFactory(report=report, species=species, tagdoc=tagdoc)
        assert recovery.tag_colour == colour
