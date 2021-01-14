"""These tests verify that the api endpoints developed to replicate
the database connections work as expected. THese api endpoints should
be considered temporary work arounds until a real api can be implemented for TFAT.

"""

import pytest
import pytz

from django.urls import reverse

from tfat.models import Encounter
from tfat.tests.factories import (
    LakeFactory,
    SpeciesFactory,
    JoePublicFactory,
    ProjectFactory,
    EncounterFactory,
    ReportFactory,
    RecoveryFactory,
)

from datetime import datetime


@pytest.fixture()
def angler():
    return JoePublicFactory(first_name="Homer", last_name="Simpson")


@pytest.fixture()
def report_date():
    return datetime(2010, 10, 10).replace(tzinfo=pytz.timezone("Canada/Eastern"))


@pytest.fixture()
def species():
    return SpeciesFactory(spc="334", spc_nmco="Walleye")


@pytest.fixture()
def report(angler, report_date):
    return ReportFactory(report_date=report_date, reported_by=angler)


@pytest.fixture()
def recovery(report, species):
    recovery = RecoveryFactory(report=report, species=species, tagid="123456")
    return recovery


@pytest.fixture()
def recoveries(report, species):

    walleye = SpeciesFactory(spc="334", spc_nmco="Walleye")
    lake_trout = SpeciesFactory(spc="081", spc_nmco="Lake Trout")

    superior = LakeFactory(abbrev="SU", lake_name="Lake Superior")
    huron = LakeFactory(abbrev="HU", lake_name="Lake Huron")

    # recovery 1 and 2 will be seelcted by our endpoint, the other
    # three should not (different lake and/or spc)
    recovery1 = RecoveryFactory(
        report=report, lake=superior, species=walleye, tagid="1234"
    )
    recovery2 = RecoveryFactory(
        report=report, lake=superior, species=walleye, tagid="0123"
    )
    recovery3 = RecoveryFactory(
        report=report, lake=superior, species=lake_trout, tagid="3456"
    )
    recovery4 = RecoveryFactory(
        report=report, lake=huron, species=walleye, tagid="4567"
    )
    recovery5 = RecoveryFactory(
        report=report, lake=huron, species=lake_trout, tagid="45678"
    )

    return [recovery1, recovery2, recovery3, recovery4, recovery5]


@pytest.fixture()
def project():
    return ProjectFactory(prj_cd="LHA_IA15_999", prj_nm="Fake Project")


@pytest.fixture()
def encounters(project, species):
    """create some encounters: 2 different tags applied to walleye, one
    tag applied to a lake trout, and one recaptured walleye."""

    encounter1 = EncounterFactory(
        project=project,
        species=species,
        tagid="123456",
        tagstat="A",
        observation_date=datetime(2015, 4, 1),
    )
    # different tagid
    encounter2 = EncounterFactory(
        project=project, species=species, tagid="123457", tagstat="A"
    )

    # same tag number but a different species:
    spc2 = SpeciesFactory(spc="081", spc_nmco="Lake Trout")
    encounter3 = EncounterFactory(project=project, species=spc2, tagid="123456")

    # recapture our our first tag at the end of the month
    encounter4 = EncounterFactory(
        project=project,
        species=species,
        tagid="123456",
        tagstat="C",
        observation_date=datetime(2015, 4, 30),
    )

    return [encounter1, encounter2, encounter3, encounter4]


@pytest.mark.django_db
def test_letter_recovery_detail(client, recovery):
    """the lettter recovery detail accepts a recovery event id and returns
    a json response that contains all of the information about the tag
    recovery report required to populate the Rmarkdown letter

    keys include: general_location, specific_location, tagid, dd_lat,
    dd_lon, tlen, flen, rwt, first_name, last_name, spc, spc_nmco,
    recovery_date_iso

    """

    # recovery = RecoveryFactory(report=report, species=species)

    response = client.get(
        reverse("tfat:letter_recovery_detail", kwargs={"recovery_id": recovery.id})
    )

    payload = response.json()
    observed_keys = payload.keys()
    expected_keys = [
        "general_location",
        "specific_location",
        "tagid",
        "dd_lat",
        "dd_lon",
        "tlen",
        "flen",
        "rwt",
        "first_name",
        "last_name",
        "spc",
        "spc_nmco",
        "recovery_date_iso",
    ]

    assert set(expected_keys) == set(observed_keys)

    # verify that some of the values are correct too:
    assert payload["spc"] == recovery.species.spc
    assert payload["spc_nmco"] == recovery.species.spc_nmco
    assert payload["first_name"] == "Homer"
    assert payload["last_name"] == "Simpson"


@pytest.mark.django_db
def test_letter_recovery_detail_invalid_id(client):
    """If an id that does not match a tagging event is submitted, the view
    should return nohting.

    """

    response = client.get(
        reverse("tfat:letter_recovery_detail", kwargs={"recovery_id": 9999999})
    )
    payload = response.json()

    assert payload is None


@pytest.mark.django_db
def test_letter_tagging_event_detail(client, recovery, encounters):
    """the lettter recovery detail accepts a tagid and lake and returns
    a json response that contains all of the information about the tag
    event required to populate the Rmarkdown letter

    keys include: dd_lat, dd_lon, tlen, flen, sex, rwt, tagdoc, lake_abbrev,
    prj_cd, prj_nm, year, spc, and isodate

    """

    response = client.get(
        reverse(
            "tfat:letter_tagging_event",
            kwargs={
                "tagid": "123456",
                "lake": recovery.lake.abbrev,
                "spc": recovery.species.spc,
            },
        )
    )

    payload = response.json()
    assert len(payload) == 1
    observed_keys = payload[0].keys()
    expected_keys = [
        "dd_lat",
        "dd_lon",
        "tlen",
        "flen",
        "sex",
        "rwt",
        "tagid",
        "tagdoc",
        "lake_abbrev",
        "prj_cd",
        "prj_nm",
        "year",
        "spc",
        "isodate",
    ]

    assert set(expected_keys) == set(observed_keys)

    # check some of hte basic attributes or our payload:
    encounter = encounters[0]

    assert payload[0]["flen"] == encounter.flen
    assert payload[0]["tlen"] == encounter.tlen
    assert payload[0]["dd_lat"] == encounter.dd_lat
    assert payload[0]["dd_lon"] == encounter.dd_lon
    assert payload[0]["spc"] == encounter.species.spc

    # verify that this is application event - not the recapture event:
    assert payload[0]["isodate"] == "2015-04-01"


@pytest.mark.django_db
def test_letter_tagging_event_multiple_tags(client, species, recovery, encounters):
    """Currently - the view does filter by tagdoc - if the tagid and
    species match more than one tagging event (same species, tagid,
    but differnt tagdoc), they should all be returned (for now). Post
    processing on the client side will have to identify which tagging
    event is the one assoicated with the tag recovery.

    """

    # create another mnrf encounter and with the same species and
    # tagid, but a differnt tagdoc -differetn colour or tag type (say)
    project = ProjectFactory(prj_cd="LHA_IA15_001", prj_nm="A Second Fake Project")
    encounter = EncounterFactory(
        project=project,
        species=species,
        tagid="123456",
        tagdoc="99999",
        tagstat="A",
        observation_date=datetime(2015, 4, 1),
    )

    response = client.get(
        reverse(
            "tfat:letter_tagging_event",
            kwargs={
                "tagid": "123456",
                "lake": recovery.lake.abbrev,
                "spc": recovery.species.spc,
            },
        )
    )

    payload = response.json()
    assert len(payload) == 2


@pytest.mark.django_db
def test_letter_tagging_event_invalid_id(client, species, recovery, encounters):
    """If an the tag that does not match any tagging events, the view
    should return an empty dictionary.

    """

    response = client.get(
        reverse(
            "tfat:letter_tagging_event",
            kwargs={
                "tagid": "123",
                "lake": recovery.lake.abbrev,
                "spc": recovery.species.spc,
            },
        )
    )

    payload = response.json()
    assert len(payload) == 0


@pytest.mark.django_db
def test_letter_tag_count(client, encounters):
    """The tag count endpoint should return a single json object
    containing the number of tags applied by the OMNR to the specified
    species in the lake and year in question.

    """

    # this is tagging event that was later recovered by homer:
    encounter = encounters[0]

    response = client.get(
        reverse(
            "tfat:letter_tag_count",
            kwargs={
                "year": encounter.project.year,
                "lake": encounter.project.lake.abbrev,
                "spc": encounter.species.spc,
            },
        )
    )

    payload = response.json()
    assert payload == {"tag_count": 2}


@pytest.mark.django_db
def test_letter_tag_count_empty(client, encounters):
    """If no tags match the species, year, and lake, the response should
    be a json object of the form: {tag_count:0}

    """
    encounter = encounters[0]
    response = client.get(
        reverse(
            "tfat:letter_tag_count",
            kwargs={
                "year": "1999",  # wrong year, no tags applied in 1999
                "lake": encounter.project.lake.abbrev,
                "spc": encounter.species.spc,
            },
        )
    )

    payload = response.json()
    assert payload == {"tag_count": 0}


@pytest.mark.django_db
def test_mnrf_encounters_endpoint(client, species, encounters):
    """The mnrf encounters endpoint returns all of the omnrf tagging and
    recovery events for the given species and lake.  It should not
    include recoveries for different species or lakes.

    It should include the following keys:

    "flen", "tlen", "rwt",
    "sex", "dd_lat", "dd_lon",
    "tagid", "tagdoc", "tagstat",
    "fate", "comment", "year",
    "prj_cd", "prj_nm", "spc",
    "spc_nmco", "observation_date_iso"

    """
    # we need to create a lake superior encoutner too:
    lake = LakeFactory(abbrev="SU", lake_name="Lake Superior")
    project = ProjectFactory(
        lake=lake, prj_cd="LSA_IA15_999", prj_nm="Fake Superior Project"
    )
    EncounterFactory(
        project=project,
        species=species,
        tagid="12345",
        tagstat="A",
        observation_date=datetime(2015, 4, 1),
    )

    # verify that the new encounter is in the database:
    assert Encounter.objects.all().count() == len(encounters) + 1

    encounter = encounters[0]

    response = client.get(
        reverse(
            "tfat:mnrf_encounters",
            kwargs={
                "lake": encounter.project.lake.abbrev,
                "spc": encounter.species.spc,
            },
        )
    )

    payload = response.json()
    assert len(payload) == 3
    observed_keys = payload[0].keys()
    expected_keys = [
        "flen",
        "tlen",
        "rwt",
        "sex",
        "dd_lat",
        "dd_lon",
        "tagid",
        "tagdoc",
        "tagstat",
        "fate",
        "comment",
        "year",
        "prj_cd",
        "prj_nm",
        "spc",
        "spc_nmco",
        "observation_date_iso",
    ]

    assert set(expected_keys) == set(observed_keys)

    # make sure that the lake huron lake trout is not in our response
    observed_spc = [x["spc"] for x in payload]
    assert "081" not in observed_spc

    # make sure that the lake superior walleye is not in the response either
    tagids = [x["tagid"] for x in payload]
    assert "654321" not in tagids


@pytest.mark.django_db
def test_mnrf_encounters_endpoint_no_match(client, encounters):
    """If a species or lake is specified that does match any tag
    recoveries, the endpoint should return an empty list.

    """

    encounter = encounters[0]

    response = client.get(
        reverse(
            "tfat:mnrf_encounters",
            kwargs={
                "lake": "ON",
                "spc": encounter.species.spc,
            },
        )
    )

    payload = response.json()
    assert len(payload) == 0


@pytest.mark.django_db
def test_public_recaptures_endpoint_species(client, recoveries):
    """The public recapture endpoint returns all of the public tag
    recoveries for hte given species and lake.  It should not include
    recoveries for different species or lakes.

    It should include the following keys:

    flen, tlen, rwt, sex, dd_lat, dd_lon, tagid, tagdoc, fate, comment,
    year, spc, spc_nmco, recovery_date_iso

    """

    recovery = recoveries[0]

    response = client.get(
        reverse(
            "tfat:public_recoveries",
            kwargs={
                "lake": recovery.lake.abbrev,
                "spc": recovery.species.spc,
            },
        )
    )

    payload = response.json()
    assert len(payload) == 2

    observed_keys = payload[0].keys()
    expected_keys = [
        "flen",
        "tlen",
        "rwt",
        "sex",
        "dd_lat",
        "dd_lon",
        "tagid",
        "tagdoc",
        "fate",
        "comment",
        "year",
        "spc",
        "spc_nmco",
        "recovery_date_iso",
    ]

    assert set(expected_keys) == set(observed_keys)

    # make sure that the lake huron lake trout is not in our response
    observed_spc = [x["spc"] for x in payload]
    assert "081" not in observed_spc

    # make sure that the lake superior walleye is not in the response either
    tagids = [x["tagid"] for x in payload]
    expected_tags = ["0123", "1234"]
    assert set(tagids) == set(expected_tags)


@pytest.mark.django_db
def test_public_recaptures_endpoint_species_no_match(client, recoveries):
    """If a species or lake is specified that does match any tag
    recoveries, the endpoint should return an empty list.

    """
    recovery = recoveries[0]

    response = client.get(
        reverse(
            "tfat:public_recoveries",
            kwargs={
                "lake": "ON",
                "spc": recovery.species.spc,
            },
        )
    )

    payload = response.json()
    assert len(payload) == 0
