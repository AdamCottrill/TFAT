"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_tags_recovered_rawsql.py
Created: 24 Jun 2015 11:00:11


DESCRIPTION:

This script tests the helper functions that execute raw sql queries
associated with tags recovered in a project.  THe functions need to
get the tag application events, other recovery events by the OMNR and
recovery events by the general public.


A. Cottrill
=============================================================

"""


from tfat.tests.factories import *
from tfat.utils import (
    get_omnr_tag_application,
    get_angler_tag_recoveries,
    get_other_omnr_recoveries,
)

import pytest


@pytest.fixture()
def db_setup():
    """for all of these tests we will need
    a tagging project
    two recovery projects
    and some tags reported by the general public

    some of the tags recovered by the onmr and general public will
    match those applied in the tagging project.  Only those tags with
    the same spc and with lat-long will be returned by the helper
    functions.

    The follow table attempt to illustrate database setup:


    | TagId | Applied | Recap1  | Recap2 | Angler |
    |-------+---------+---------+--------+--------|
    |     0 | Y       | Y       |        |        |
    |     1 | Y       | Y       |        |        |
    |     2 | Y       | Y       | Y      |        |
    |     3 | Y       | Y       | Y      |        |
    |     4 | Y       |         | Y      | Y      |
    |     5 | Y       |         | Y      | Y      |
    |     6 | Y       |         |        | Y      |
    |     7 | Y       |         |        | Y      |
    |     8 | N       | spc2    |        |        |
    |     9 |         | spc2    | N      |        |
    |    10 |         | spc2    |        | N      |
    |    11 | Y       | tagdoc2 |        |        |
    |    12 |         | tagdoc2 | Y      |        |
    |    13 |         |         |tagdoc2 | Y      |


    tags 8-9 should not ever be returned - they are a different species
    tags 11-13 should still be returned despite having a different tagdoc.

    """

    spc = SpeciesFactory(species_code="334", common_name="Walleye")
    spc2 = SpeciesFactory(species_code="091", common_name="Whitefish")

    report = ReportFactory()

    tagging_prj = ProjectFactory(
        prj_cd="LHA_IA10_111", prj_nm="Tagging", slug="lha_is10_111"
    )

    recovery_prj1 = ProjectFactory(
        prj_cd="LHA_IA11_999", prj_nm="Recovery1", slug="lha_ia11_999"
    )

    recovery_prj2 = ProjectFactory(
        prj_cd="LHA_IA11_888", prj_nm="Recovery2", slug="lha_ia11_888"
    )

    tagids = ["0", "1", "2", "3", "4", "5", "6", "7"]
    # make the tags and associate them with the tagging project
    for tagid in tagids:
        EncounterFactory(project=tagging_prj, spc=spc, tagid=tagid, tagstat="A")

    # the first four tags were recaptured by the omnr in the Recovery1
    for tagid in tagids[:4]:
        EncounterFactory(project=recovery_prj1, spc=spc, tagid=tagid, tagstat="C")

    # the tags 3-6 were recaptured by the omnr in the Recovery2
    for tagid in tagids[2:6]:
        EncounterFactory(project=recovery_prj2, spc=spc, tagid=tagid, tagstat="C")

    # the tags 4: were reported by the general public
    for tagid in tagids[4:]:
        RecoveryFactory(report=report, spc=spc, tagid=tagid)

    # two encounters by mnr (one applied, one recovered) but a different species
    EncounterFactory(project=tagging_prj, spc=spc, tagid="8", tagstat="A")
    EncounterFactory(project=recovery_prj1, spc=spc2, tagid="8", tagstat="C")

    # two encounters by mnr (two recoveries) but a different species
    EncounterFactory(project=recovery_prj1, spc=spc2, tagid="9", tagstat="C")
    EncounterFactory(project=recovery_prj2, spc=spc, tagid="9", tagstat="C")

    # one omnr recap, one anlger recap, different species
    EncounterFactory(project=recovery_prj1, spc=spc2, tagid="10", tagstat="C")
    RecoveryFactory(report=report, spc=spc, tagid="10")

    # two encounters by mnr (one applied, one recovered) but a different species
    EncounterFactory(
        project=tagging_prj, spc=spc, tagdoc="15012", tagid="11", tagstat="A"
    )
    EncounterFactory(project=recovery_prj1, spc=spc, tagid="11", tagstat="C")

    # two encounters by mnr (two recoveries) but a different species
    EncounterFactory(
        project=recovery_prj1, spc=spc, tagdoc="15012", tagid="12", tagstat="C"
    )
    EncounterFactory(project=recovery_prj2, spc=spc, tagid="12", tagstat="C")

    # one omnr recap, one anlger recap, different species
    # NOTE use of prj2 - shares early tag recaptures
    EncounterFactory(
        project=recovery_prj2, spc=spc, tagdoc="15012", tagid="13", tagstat="C"
    )
    RecoveryFactory(report=report, spc=spc, tagid="13")


@pytest.mark.django_db
def test_get_omnr_tag_application(db_setup):
    """The function get_get_omnr_tags_recoveries() should return the two
    encounters in omnr projects with the same species as well as the
    one with the different tagdoc.  The record with the different
    species should not be included in the queryset.

    """

    recovery_slug = "lha_ia11_999"
    recoveries = get_omnr_tag_application(recovery_slug)
    nobs = recoveries.get("nobs")
    assert nobs == 5

    tagids = [x.tagid for x in recoveries.get("queryset")]
    tagids.sort()
    should_be = ["0", "1", "11", "2", "3"]

    assert tagids == should_be
    assert len(tagids) == nobs


@pytest.mark.django_db
def test_get_other_omnr_recoveries(db_setup):
    """The function get_other_omnr_recoveries() should return two records
    - tags 3 and 4 where recovered in two different mnr projects

    """

    recovery_slug = "lha_ia11_999"
    recoveries = get_other_omnr_recoveries(recovery_slug)
    nobs = recoveries.get("nobs")

    print("nobs={}".format(nobs))
    assert nobs == 3

    tagids = [x.tagid for x in recoveries.get("queryset")]
    tagids.sort()
    should_be = ["12", "2", "3"]

    assert tagids == should_be
    assert len(tagids) == nobs


@pytest.mark.django_db
def test_get_angler_recaps_tagstat_c(db_setup):
    """The function get_angler_recaps returns all of the angler recap
    events for the tags either applied or recaptured in a project.  the
    optional argument 'tagstat' determines if the OMNR tag events should
    be application or recovery events.  In this case we want tagstat='C'.
    Given a project that recovered some fish with tags, find any angler
    recaps associated with those fish.
    """

    recovery_slug = "lha_ia11_888"
    recoveries = get_angler_tag_recoveries(recovery_slug, tagstat="C")
    nobs = recoveries.get("nobs")
    assert nobs == 3

    tagids = [x.tagid for x in recoveries.get("queryset")]
    tagids.sort()
    should_be = ["13", "4", "5"]

    assert tagids == should_be
    assert len(tagids) == nobs
