'''=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_recovery_form_create.py
Created: 05 Aug 2015 11:51:12

DESCRIPTION:

A series of tests to verify that the recovery form works as expected
when used to create tag recovery events.

required data elements:
- tag id
- species
- tagdoc

optional data elements:

- ddlat and ddlon
- flen and tlen
- clipc
- general location
- specific locaion
- rwt
- fish fate
- tag removed
- sex

A. Cottrill
=============================================================

'''

import pytest

from tfat.models import Recovery
from tfat.tests.factories import *


@pytest.fixture(scope='class')
def db_setup():
    """
    """

    report_date = datetime(2010,10,10)
    spc = SpeciesFactory()

    angler = JoePublicFactory.create(first_name='Homer',
                                      last_name='Simpson')

    #associated tags to test conditional elements
    report = ReportFactory(reported_by=angler, follow_up=False,
                                report_date = report_date)



@pytest.mark.django_db
def test_can_create_recovery_url(client, db_setup):
    """Verify that the form and its correct elements are rendered when we
    call the create_recovery form"""

    report = Report.objects.get(reported_by__first_name='Homer')
    url = reverse('create_recovery', kwargs={'report_id':report.id})
    response = client.get(url)
    assert response.status_code == 200
    content = str(response.content)

    assert 'Tag Recovery Event' in content
    assert 'Tag Recovery Details' in content
    assert 'Tagid:' in content
    assert 'Spc:' in content
    assert 'TAGDOC' in content

    assert 'Recovery Location' in content
    assert 'Latitude:' in content
    assert 'Longitude:' in content

    assert 'Fish Attributes' in content


@pytest.mark.django_db
def test_basic_data(client, db_setup):
    """verify that we can post the form with the minimal data elements and
    a tag recovery object will be created in the database.

    """

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 0

    report = Report.objects.get(reported_by__first_name='Homer')
    url = reverse('create_recovery', kwargs={'report_id':report.id})

    tag_data= {'tagdoc':'25012', 'tagid':'12345', 'spc':1, 'date_flag':0}
    response = client.post(url, tag_data)

    assert response.status_code == 200
    content = str(response.content)

    with open('C:/1work/scrapbook/wft2.html', 'wb') as f:
        f.write(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1



def test_missing_tagid():
    """tagid is a required field.  If the form is submitted without it, a
    meaningful error message should be generated.

    """
    pass


def test_missing_species():
    """fish species is a required field.  If the form is submitted without it, a
    meaningful error message should be generated.

    """
    pass

def test_invalid_species():
    """species is a required field.  If the form is submitted with a
    species that does not exist, a meaningful error message should be
    generated.

    """
    pass


def test_missing_tagdoc():
    """tagdoc is a required field.  If the form is submitted without it, a
    meaningful error message should be generated.

    """
    pass


def test_tagdoc_short():
    """if the tagdoc is provided, it must be exacly 5 characters long.
    """
    pass

def test_tagdoc_long():
    """if the tagdoc is provided, it must be exacly 5 characters long.
    """
    pass


def test_tagdoc_bad_tag_type():
    """if the tagdoc is provided, the 1st character must correspond to a
    valid, exising tag_type.  if not, an error will be thrown.

    """
    pass

def test_tagdoc_good_tag_type():
    """if the tagdoc is provided, the 1st character must correspond to a
    valid, exising tag_type.  When the recovery is saved, the tag_type
    will be updated to reflect the value of the 1st character in
    tagdoc.

    """
    pass


def test_tagdoc_bad_tag_position():
    """if the tagdoc is provided, the 2nd character must correspond to a
    valid, exising tag_position.  if not, an error will be thrown.

    """
    pass

def test_tagdoc_good_tag_position():
    """if the tagdoc is provided, the 2nd character must correspond to a
    valid, exising tag_position.  When the recovery is saved, the tag_position
    will be updated to reflect the value of the 2nd character in
    tagdoc.

    """
    pass



def test_tagdoc_bad_agency():
    """if the tagdoc is provided, the 3rd and 4th characters must
    correspond to a valid, exising agency.  If not, an error will be
    thrown.

    """
    pass

def test_tagdoc_good_agency():
    """if the tagdoc is provided, the 3rd and 4th characters must
    correspond to a valid, exising agency.  When the recovery is
    saved, the tag_agency will be updated to reflect the value of the
    3rd and 4th character in tagdoc.

    """
    pass


def test_tagdoc_bad_colour():
    """if the tagdoc is provided, the 5th character must correspond to a
    valid, exising colour.  if not, an error will be thrown.

    """
    pass

def test_tagdoc_good_colour():
    """if the tagdoc is provided, the 5th character must correspond to a
    valid, exising colour.  When the recovery is saved, the tag_colour
    will be updated to reflect the value of the 5th character in
    tagdoc.

    """
    pass



def test_good_clipc():
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  All of the elements must exist
    in the clip code lookup table.

    """
    pass


def test_good_clipc_0():
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  Clip code '0' is used to
    indicate the absence of other clips and should be acceptable as a
    valid clip when the form is processed.

    """
    pass



def test_bad_clipc_includes_0():
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  Clip code '0' is used to
    indicate the absence of other clips.  As such, and clipc value
    that includes 0 along with any other clip code should return an
    error.

    """
    pass

def test_bad_clipc_includes_duplicates():
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  All of the elements must exist
    in the clip code lookup table and appear only once.  If a clip
    code appears more than once in clipc, a meaningfull error message
    should be thrown. (eg. 11 is not valid.)

    """
    pass


def test_bad_clipc_includes_wrong_order():
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured. All of the elements are to be
    saved in ascii-sort order.  If a clip code is reported in the
    wrong order, it will be save in the correct order.  (eg 532 will
    be saved as 235)

    """
    pass


def test_bad_clipc_nonexistant_clip():
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  If one of the elements does exist
    in the clip code lookup table an error should be thrown.

    """
    pass


@pytest.mark.xfail
def test_missing_recovery_date():
    """It's not clear what should happen if data is not populated.

    """
    assert 0==1


def test_future_date():
    """a tag recovery event cannot be reported from the future.  A
    recovery event cannot be recorded if it has not happened yet.  If a
    date in the future is submitted, an appropriate error message should
    be returned.

    """
    pass


def test_recapture_date_ahead_of_report_date():
    """a tag recovery event cannot occur more recently than the reporting
    date. If this happens an error should be raised.

    """
    pass


def test_tlen_greater_than_flen():
    """both tlen and flen can be provided as long as flen is less than tlen.
    """
    pass


def test_tlen_less_than_flen():
    """if both total length and fork length are provided and fork lenght
    is greater than total length, raise an error.

    """
    pass


def test_ddlat_ddlon():
    """ddlat and ddlon are optional fields.  If they are included in the
    posted data, they will be correctly associated with the recovery
    object in the database.

    """
    pass


def test_unknown_ddlat_ddlon():
    """ddlat and ddlon are optional fields.  but if they are null,
    latlon_flag must be unknown.  If a recovery is submitted without
    at latlon_flag==unknown, and error should be thrown.

    """
    pass


def test_derived_ddlat_ddlon_with_comment():
    """ddlat and ddlon are optional fields.  If a recovery is submitted
    with a comment (hopefully explaining how lat long was derived), the
    recovery should be created in the database.
    """
    pass

def test_derived_ddlat_ddlon_with_comment():
    """ddlat and ddlon are optional fields.  If a recovery is submitted
    without a comment an error will be thrown.
    """
    pass



def test_ddlat_without_ddlon():
    """ddlat and ddlon are optional fields, but if one is provided, the
    other must be provided too. If ddlon is omitted, but dd_lat is
    included, an appropriate error message should be generated.

    """
    pass

def test_ddlon_without_ddlat():
    """ddlat and ddlon are optional fields, but if one is provided, the
    other must be provided too. If ddkat is omitted, but dd_lon is
    included, an appropriate error message should be generated.

    """
    pass


def test_ddlat_max_90():
    """ddlat is the latitude and cannot exceed 90 degrees.  If a ddlat
    value is submitted with a latitude greater than 9s, an
    appropriate error message should be generated.

    """

def test_ddlat_min_negative_90():
    """ddlat is the latitude and cannot exceed -90 degrees.  If a ddlat
    value is submitted with a latitude less than -90, an
    appropriate error message should be generated.

    """


def test_ddlon_max_180():
    """ddlon is the longitude and cannot exceed 180 degrees.  If a ddlon
    value is submitted with a longitude greater than 180, an
    appropriate error message should be generated.

    """

def test_ddlon_min_negative_180():
    """ddlon is the lonitude and cannot be less than -180 degrees.  If a ddlon
    value is submitted with a lonitude less than -180s, an
    appropriate error message should be generated.

    """



def test_general_location():
    """general_location is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    pass


def test_specific_location():
    """specific_location is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    pass


def test_fish_fate_released():
    """fish fate is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    pass


def test_fish_fate_killed():
    """fish fate is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    pass


def test_fish_fate_nonexistant():
    """fish fate is an optional field but is constrained to one of
    pre-determined values.  If a non-existant option is included in
    the posted data, an appropriate error will be thrown.

    """
    pass



def test_fish_sex_male():
    """fish sex is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    pass


def test_fish_sex_female():
    """fish sex is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    pass


def test_fish_sex_nonexistant():
    """fish sex is an optional field but is constrained to one of
    pre-determined values.  If a non-existant option is included in
    the posted data, an appropriate error will be thrown.

    """
    pass


def test_fish_tag_removed_false():
    """tag removed is an optional field.  If it is included in the
    posted data as false, it will be false in the associated recovery
    object in the database.

    """
    pass


def test_fish_tag_removed_true():
    """tag removed is an optional field.  If it is included in the
    posted data as true, it will be true in the associated recovery
    object in the database.

    """
    pass


def test_fish_round_weight():
    """fish round weight is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    pass
