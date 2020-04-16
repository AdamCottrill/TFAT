"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_tags_applied_project.py
Created: 23 Jun 2015 11:40:37


DESCRIPTION:

This script tests the helper functions that execute raw sql queries
associated with tags applied in a project and subsequently recovered
by the OMNR or the general public.

A. Cottrill
=============================================================

"""

from tfat.tests.factories import *
from tfat.utils import get_omnr_tag_recoveries, get_angler_tag_recoveries

import pytest


@pytest.fixture()
def db_setup():
    """for all of these tests we will need
    a tagging project
    a recovery project
    and some tags reported by the general public

    some of the tags recovered by the onmr and general public will
    match those applied in the tagging project.  Only those tags with
    the same species and with lat-long will be returned by the helper
    functions.

    """

    species = SpeciesFactory(spc="334", spc_nmco="Walleye")
    species2 = SpeciesFactory(spc="091", spc_nmco="Whitefish")

    report = ReportFactory()

    tagging_prj = ProjectFactory(
        prj_cd="LHA_IA10_111", prj_nm="Tagging", slug="lha_is10_111"
    )

    recovery_prj = ProjectFactory(
        prj_cd="LHA_IA11_999", prj_nm="Recovery", slug="lha_is11_999"
    )

    tagids = ["1", "2", "3", "4", "5", "6", "7", "8"]
    # make the tags and associate them with the tagging project
    for tagid in tagids:
        EncounterFactory(project=tagging_prj, species=species, tagid=tagid, tagstat="A")

    # the first four tags were recaptured by the omnr
    for tagid in tagids[:2]:
        EncounterFactory(
            project=recovery_prj, species=species, tagid=tagid, tagstat="C"
        )

    # encunterd by mnr but a different species
    EncounterFactory(
        project=recovery_prj,
        species=species,
        tagdoc="15012",
        tagid=tagids[2],
        tagstat="C",
    )
    EncounterFactory(
        project=recovery_prj, species=species2, tagid=tagids[3], tagstat="C"
    )

    # the remaining 4 tags were reported by the general public
    for tagid in tagids[4:6]:
        RecoveryFactory(report=report, species=species, tagid=tagid)
    # this one has no lat-lon
    RecoveryFactory(
        report=report, species=species, dd_lat=None, dd_lon=None, tagid=tagids[6]
    )
    # this one is a different species
    RecoveryFactory(report=report, species=species2, tagid=tagids[7])


@pytest.mark.django_db
def test_get_get_omnr_tags_recoveries(db_setup):
    """The function get_get_omnr_tags_recoveries() should return the two
    encounters in omnr projects with the same species as well as the
    one with the different tagdoc.  The record with the different
    species should not be included in the queryset.

    """

    recoveries = get_omnr_tag_recoveries("lha_is10_111")
    nobs = recoveries.get("nobs")
    assert nobs == 3

    tagids = [x.tagid for x in recoveries.get("queryset")]
    tagids.sort()

    should_be = ["1", "2", "3"]

    assert tagids == should_be

    assert "4" not in tagids  # no lat-long


@pytest.mark.django_db
def test_get_angler_tags_recoveries(db_setup):
    """The function get_get_angler_tags_recoveries() should return the
    three tag recovery events.  Two are complete and match perfectly,
    one is missing lat-long, but is still returned.  The record with
    the different species should not be included in the queryset.
    """

    recoveries = get_angler_tag_recoveries("lha_is10_111", tagstat="A")

    nobs = recoveries.get("nobs")
    assert nobs == 3
    tagids = [x.tagid for x in recoveries.get("queryset")]
    tagids.sort()
    should_be = ["5", "6", "7"]
    assert tagids == should_be

    assert "8" not in tagids  # different species


@pytest.mark.django_db
def test_get_angler_tags_recoveries_without_tagstat(db_setup):
    """The function get_get_angler_tags_recoveries() has an option
    argument to specify the tag status of OMNR encounter events to
    include.  By default it is 'A' and as a consequence, this test is
    identical to the previous one.
    """

    recoveries = get_angler_tag_recoveries("lha_is10_111")

    nobs = recoveries.get("nobs")
    assert nobs == 3
    tagids = [x.tagid for x in recoveries.get("queryset")]
    tagids.sort()
    should_be = ["5", "6", "7"]
    assert tagids == should_be

    assert "8" not in tagids  # different species
