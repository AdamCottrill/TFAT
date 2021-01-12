"""These tests verify that the api endpoints developed to replicate
the database connections work as expected. THese api endpoints should
be considered temporary work arounds until a real api can be implemented for TFAT.

"""

import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_letter_recovery_detail(client):
    """the lettter recovery detail accepts a recovery event id and returns
    a json response that contains all of the information about the tag
    recovery report required to populate the Rmarkdown letter

    keys include: general_location, specific_location, tagid, dd_lat,
    dd_lon, tlen, flen, rwt, first_name, last_name, spc, spc_nmco,
    recovery_date_iso

    """
    assert 0 == 1


@pytest.mark.django_db
def test_letter_recovery_detail_invalid_id(client):
    """If an id that does not match a tagging event is submitted, the view
    should return an empty dictionary.

    """
    assert 0 == 1


@pytest.mark.django_db
def test_letter_tagging_event_detail(client):
    """the lettter recovery detail accepts a tagid and lake and returns
    a json response that contains all of the information about the tag
    event required to populate the Rmarkdown letter

    keys include: dd_lat, dd_lon, tlen, flen, sex, rwt, tagdoc, lake_abbrev,
    prj_cd, prj_nm, year, spc, and isodate

    """
    assert 0 == 1


@pytest.mark.django_db
def test_letter_tagging_event_multiple_tags(client):
    """Currently - the view does not include tagdoc - if the tagid and
    species match more than one tagging event (same species, tagid,
    but differnt tagdoc), they should all be returned (for now). Post
    processing on the client side will have to identify which tagging
    event is the one assoicated with the tag recovery.

    """
    assert 0 == 1


@pytest.mark.django_db
def test_letter_tagging_event_invalid_id(client):
    """If an the tag that does not match any tagging events, the view
    should return an empty dictionary.

    """
    assert 0 == 1


@pytest.mark.django_db
def test_letter_tag_count(client):
    """The tag count endpoint should return a single json object
    containing the number of tags applied by the OMNR to the specified
    species in the lake and year in question.

    """
    assert 0 == 1


@pytest.mark.django_db
def test_letter_tag_count_empty(client):
    """If no tags match the species, year, and lake, the response should
    be a json object of the form: {tag_count:0}

    """
    assert 0 == 1


@pytest.mark.django_db
def test_mnrf_encounters_endpoint(client):
    """The mnrf encounters endpoint returns all of theomrn tagging and
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
    assert 0 == 1


@pytest.mark.django_db
def test_mnrf_encounters_endpoint_no_match(client):
    """If a species or lake is specified that does match any tag
    recoveries, the endpoint should return an empty object.

    """
    assert 0 == 1


@pytest.mark.django_db
def test_public_recaptures_endpoint_species(client):
    """The public recapture endpoint returns all of the public tag
    recoveries for hte given species and lake.  It should not include
    recoveries for different species or lakes.

    It should include the following keys:

    flen, tlen, rwt, sex, dd_lat, dd_lon, tagid, tagdoc, fate, comment,
    year, spc, spc_nmco, recovery_date_iso

    """
    assert 0 == 1


@pytest.mark.django_db
def test_public_recaptures_endpoint_species_no_match(client):
    """If a species or lake is specified that does match any tag
    recoveries, the endpoint should return an empty object.

    """
    assert 0 == 1
