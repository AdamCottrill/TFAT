"""=============================================================
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
- specific location
- rwt
- girth
- fish fate
- tag removed
- sex

A. Cottrill
=============================================================

"""


from django.urls import reverse

import pytest
import pytz
from datetime import datetime, timedelta

from tfat.models import Recovery
from tfat.tests.factories import *


@pytest.fixture()
def db_setup():
    """
    """

    report_date = datetime(2010, 10, 10).replace(tzinfo=pytz.UTC)

    angler = JoePublicFactory.create(first_name="Homer", last_name="Simpson")

    # associated tags to test conditional elements
    report = ReportFactory(reported_by=angler, follow_up=False, report_date=report_date)


@pytest.fixture()
def tag_data():
    """A fixture to hold basic minimal data requirements for each
    test. Updated as needed in each test.
    """
    spc = SpeciesFactory()
    lake = LakeFactory()

    tag_data = {
        "tagdoc": "25012",
        "tagid": "1234",
        "spc": spc.id,
        "date_flag": 0,
        "lake": lake.id,
    }
    # tag_data["spc"] = spc.id
    return tag_data


@pytest.mark.django_db
def test_can_create_recovery_url(client, db_setup):
    """Verify that the form and its correct elements are rendered when we
    call the create_recovery form"""

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})
    response = client.get(url)
    assert response.status_code == 200
    content = str(response.content)

    assert "Tag Recovery Event" in content
    assert "Tag Recovery Details" in content
    assert "Tagid:" in content
    assert "Spc:" in content
    assert "TAGDOC" in content

    assert "Recovery Location" in content
    assert "Latitude:" in content
    assert "Longitude:" in content

    assert "Fish Attributes" in content


@pytest.mark.django_db
def test_basic_data(client, db_setup, tag_data):
    """verify that we can post the form with the minimal data elements and
    a tag recovery object will be created in the database.

    """

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 0

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tagid = "12345"
    tagdoc = "25012"
    tag_data["tagid"] = tagid
    tag_data["tagdoc"] = tagdoc

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    fname = "c:/Users/COTTRILLAD/1work/scrapbook/wtf.html"
    with open(fname, "wb") as f:
        f.write(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].tagid == tagid
    assert recoveries[0].tagdoc == tagdoc


@pytest.mark.django_db
def test_basic_data_add_another(client, db_setup, tag_data):
    """When we create a new tag recovery object, a button should appear on the
    associated details page allowing us to add another tag recovery.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tagid = "12345"
    tagdoc = "25012"
    tag_data["tagid"] = tagid
    tag_data["tagdoc"] = tagdoc

    response = client.post(url, tag_data, follow=True)

    content = str(response.content)
    assert "Add Another Tag" in content


@pytest.mark.django_db
def test_missing_tagid(client, db_setup, tag_data):
    """tagid is a required field.  If the form is submitted without it, a
    meaningful error message should be generated.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    foo = tag_data.pop("tagid")

    response = client.post(url, tag_data, follow=True)

    content = str(response.content)
    msg = "This field is required."
    assert msg in content


@pytest.mark.django_db
def test_missing_species(client, db_setup, tag_data):
    """fish species is a required field.  If the form is submitted without it, a
    meaningful error message should be generated.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    foo = tag_data.pop("spc")

    response = client.post(url, tag_data, follow=True)

    content = str(response.content)
    msg = "This field is required."
    assert msg in content


@pytest.mark.django_db
def test_invalid_species(client, db_setup, tag_data):
    """species is a required field.  If the form is submitted with a
    species that does not exist, a meaningful error message should be
    generated.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["spc"] = 999

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Select a valid choice. " "That choice is not one of the available choices."
    assert msg in content


@pytest.mark.django_db
def test_missing_tagdoc(client, db_setup, tag_data):
    """tagdoc is a required field.  If the form is submitted without it, a
    meaningful error message should be generated.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    foo = tag_data.pop("tagdoc")

    response = client.post(url, tag_data, follow=True)

    content = str(response.content)
    msg = "This field is required."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_short(client, db_setup, tag_data):
    """if the tagdoc is provided, it must be exacly 5 characters long.
    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["tagdoc"] = "2501"
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)
    msg = "TAGDOC must be 5 characters long."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_long(client, db_setup, tag_data):
    """if the tagdoc is provided, it must be exacly 5 characters long.
    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["tagdoc"] = "250129"
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)
    msg = "TAGDOC must be 5 characters long."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_bad_tag_type(client, db_setup, tag_data):
    """if the tagdoc is provided, the 1st character must correspond to a
    valid, exising tag_type.  if not, an error will be thrown.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["tagdoc"] = "Y5012"
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)
    msg = "Y is not a valid tag type code."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_good_tag_type(client, db_setup, tag_data):
    """if the tagdoc is provided, the 1st character must correspond to a
    valid, exising tag_type.  When the recovery is saved, the tag_type
    will be updated to reflect the value of the 1st character in
    tagdoc.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tagdoc = "35012"
    tag_data["tagdoc"] = tagdoc

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].tagdoc == tagdoc


@pytest.mark.django_db
def test_tagdoc_bad_tag_position(client, db_setup, tag_data):
    """if the tagdoc is provided, the 2nd character must correspond to a
    valid, exising tag_position.  if not, an error will be thrown.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["tagdoc"] = "2Y012"
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)
    msg = "Y is not a valid tag position code."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_good_tag_position(client, db_setup, tag_data):
    """if the tagdoc is provided, the 2nd character must correspond to a
    valid, exising tag_position.  When the recovery is saved, the tag_position
    will be updated to reflect the value of the 2nd character in
    tagdoc.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tagdoc = "25012"
    tag_data["tagdoc"] = tagdoc

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].tagdoc == tagdoc


@pytest.mark.django_db
def test_tagdoc_bad_agency(client, db_setup, tag_data):
    """if the tagdoc is provided, the 3rd and 4th characters must
    correspond to a valid, exising agency.  If not, an error will be
    thrown.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["tagdoc"] = "25XX2"

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "XX is not a valid agency code."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_bad_colour(client, db_setup, tag_data):
    """if the tagdoc is provided, the 5th character must correspond to a
    valid, exising colour.  if not, an error will be thrown.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tagdoc = "2501X"
    tag_data["tagdoc"] = tagdoc

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "X is not a valid colour code."
    assert msg in content


@pytest.mark.django_db
def test_good_clipc(client, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  All of the elements must exist
    in the clip code lookup table.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    clipc = "14"
    tag_data["clipc"] = clipc

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].clipc == clipc


@pytest.mark.django_db
def test_good_clipc_0(client, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  Clip code '0' is used to
    indicate the absence of other clips and should be acceptable as a
    valid clip when the form is processed.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    clipc = "0"
    tag_data["clipc"] = clipc

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].clipc == clipc


@pytest.mark.django_db
def test_bad_clipc_includes_0(client, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  Clip code '0' is used to
    indicate the absence of other clips.  As such, and clipc value
    that includes 0 along with any other clip code should return an
    error.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    clipc = "140"
    tag_data["clipc"] = clipc

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "CLIPC cannot contain 0 and other clip codes."
    assert msg in content


@pytest.mark.django_db
def test_bad_clipc_includes_duplicates(client, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  All of the elements must exist
    in the clip code lookup table and appear only once.  If a clip
    code appears more than once in clipc, a meaningfull error message
    should be thrown. (eg. 11 is not valid.)

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    clipc = "114"
    tag_data["clipc"] = clipc

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Clip codes cannot repeat."
    assert msg in content


@pytest.mark.django_db
def test_bad_clipc_includes_wrong_order(client, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured. All of the elements are to be
    saved in ascii-sort order.  If a clip code is reported in the
    wrong order, it will be save in the correct order.  (eg 532 will
    be saved as 235)

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    clipc = "532"
    tag_data["clipc"] = clipc

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].clipc == "235"


@pytest.mark.django_db
def test_bad_clipc_nonexistant_clip(client, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  If one of the elements does exist
    in the clip code lookup table an error should be thrown.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    clipc = "15X"
    tag_data["clipc"] = clipc

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Invalid clip codes: X"
    assert msg in content


@pytest.mark.django_db
def test_bad_clipc_multiple_nonexistant_clips(client, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  If more than one of the
    elements does exist in the clip code lookup table an error should
    be thrown and the error message should contain a comma separated
    list of those elements.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    clipc = "15XZ"
    tag_data["clipc"] = clipc

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200
    content = str(response.content)

    msg = "Invalid clip codes: X,Z"
    assert msg in content


@pytest.mark.django_db
def test_missing_recovery_date(client, db_setup, tag_data):
    """It's not clear what should happen if date is not populated.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].recovery_date is None
    assert recoveries[0].date_flag is 0


@pytest.mark.django_db
def test_future_date(client, db_setup, tag_data):
    """a tag recovery event cannot be reported from the future.  A
    recovery event cannot be recorded if it has not happened yet.  If a
    date in the future is submitted, an appropriate error message should
    be returned.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    next_week = datetime.today() + timedelta(days=7)

    tag_data["recovery_date"] = next_week.date()

    response = client.post(url, tag_data)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Dates in the future are not allowed."
    assert msg in content


@pytest.mark.django_db
def test_recovery_date_greater_than_report_date(client, db_setup, tag_data):
    """a tag recovery event cannot occur after the reporting date.  A
    recovery event cannot be recorded if it had not happened when the
    report was created.  If the recovery date is a head of the report
    date, an appropriate error message should be returned.

    This test currently fails because I am unable to access the report
    object from within the form when validateing a new recovery
    object.  See clean_recovery_date() method of RecoveryForm.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    week_late = report.report_date + timedelta(days=7)

    tag_data["recovery_date"] = week_late.date()

    response = client.post(url, tag_data)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Recovery date occurs after report date."
    assert msg in content


@pytest.mark.xfail
@pytest.mark.django_db
def test_recapture_date_ahead_of_report_date(client, db_setup, tag_data):
    """a tag recovery event cannot occur more recently than the reporting
    date. If this happens an error should be raised.

    """

    # NOT IMPLEMENTED YET
    assert 0 == 1


@pytest.mark.django_db
def test_no_date_and_dateflag_is_reported(client, db_setup, tag_data):
    """If no date is provided, then date_flag must be set to 'unknown'.
    Issue an error if that is not the case.
    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["recovery_date"] = ""
    tag_data["date_flag"] = 1  # reported

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Date flag must be &quot;Unknown&quot; if no date is provided."
    assert msg in content


@pytest.mark.django_db
def test_tlen_greater_than_flen(client, db_setup, tag_data):
    """both tlen and flen can be provided as long as flen is less than tlen.
    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tlen = 450
    flen = 440

    tag_data["flen"] = flen
    tag_data["tlen"] = tlen

    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].tlen == tlen
    assert recoveries[0].flen == flen


@pytest.mark.django_db
def test_tlen_less_than_flen(client, db_setup, tag_data):
    """if both total length and fork length are provided and fork length
    is greater than total length, raise an error.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tlen = 440
    flen = 450

    tag_data["flen"] = flen
    tag_data["tlen"] = tlen

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200
    content = str(response.content)

    msg = "Total length (tlen) cannot be less than fork length (flen)."
    assert msg in content


@pytest.mark.django_db
def test_ddlat_ddlon(client, db_setup, tag_data):
    """ddlat and ddlon are optional fields.  If they are included in the
    posted data, they will be correctly associated with the recovery
    object in the database.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    dd_lat = 45.25
    dd_lon = -81.1

    tag_data["dd_lat"] = dd_lat
    tag_data["dd_lon"] = dd_lon

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].dd_lat == dd_lat
    assert recoveries[0].dd_lon == dd_lon

    assert recoveries[0].latlon_flag is not None
    assert recoveries[0].latlon_flag != 0


@pytest.mark.xfail
@pytest.mark.django_db
def test_unknown_ddlat_ddlon(client, db_setup, tag_data):
    """ddlat and ddlon are optional fields.  but if they are null,
    latlon_flag must be unknown.  If a recovery is submitted without
    at latlon_flag==unknown, and error should be thrown.



    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    # this is not working as expected - I have no idea why latlon_flag
    # is being saved as 1
    assert recoveries[0].latlon_flag == 0  # unknown


@pytest.mark.django_db
def test_derived_ddlat_ddlon_with_comment(client, db_setup, tag_data):
    """ddlat and ddlon are optional fields.  If a recovery is submitted
    with a comment (hopefully explaining how lat long was derived), the
    recovery should be created in the database.
    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    latlon_flag = 2  # derived
    comment = "It was big."

    tag_data["dd_lat"] = 45.25
    tag_data["dd_lon"] = -81.1
    tag_data["latlon_flag"] = latlon_flag
    tag_data["comment"] = comment

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].latlon_flag == latlon_flag
    assert recoveries[0].comment == comment


@pytest.mark.django_db
def test_derived_ddlat_ddlon_without_comment(client, db_setup, tag_data):
    """ddlat and ddlon are optional fields.  If a recovery is submitted
    without a comment an error will be thrown.
    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["dd_lat"] = 45.25
    tag_data["dd_lon"] = -81.1
    tag_data["latlon_flag"] = 2

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "Describe how location was derived."
    assert msg in content


@pytest.mark.django_db
def test_ddlat_without_ddlon(client, db_setup, tag_data):
    """ddlat and ddlon are optional fields, but if one is provided, the
    other must be provided too. If ddlon is omitted, but dd_lat is
    included, an appropriate error message should be generated.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["dd_lat"] = 45.25
    tag_data["dd_lon"] = ""

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "If dd_lat is populated,  dd_lon must be populated too"
    assert msg in content


@pytest.mark.django_db
def test_ddlon_without_ddlat(client, db_setup, tag_data):
    """ddlat and ddlon are optional fields, but if one is provided, the
    other must be provided too. If ddkat is omitted, but dd_lon is
    included, an appropriate error message should be generated.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["dd_lat"] = ""
    tag_data["dd_lon"] = -81.1

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "If dd_lon is populated,  dd_lat must be populated too"
    assert msg in content


@pytest.mark.django_db
def test_ddlat_max_90(client, db_setup, tag_data):
    """ddlat is the latitude and cannot exceed 90 degrees.  If a ddlat
    value is submitted with a latitude greater than 9s, an
    appropriate error message should be generated.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["dd_lat"] = 100
    tag_data["dd_lon"] = -81.1

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "dd_lat must be numeric and lie between -90 and 90"
    assert msg in content


@pytest.mark.django_db
def test_ddlat_min_negative_90(client, db_setup, tag_data):
    """ddlat is the latitude and cannot be less than -90 degrees.  If a
    ddlat value is submitted with a latitude less than -90, an
    appropriate error message should be generated.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["dd_lat"] = -100
    tag_data["dd_lon"] = -81.1

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "dd_lat must be numeric and lie between -90 and 90"
    assert msg in content


@pytest.mark.django_db
def test_ddlon_max_180(client, db_setup, tag_data):
    """ddlon is the longitude and cannot exceed 180 degrees.  If a ddlon
    value is submitted with a longitude greater than 180, an
    appropriate error message should be generated.
    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_data["dd_lat"] = 45.25
    tag_data["dd_lon"] = 281.1

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "dd_lon must be numeric and lie between -180 and 180"
    assert msg in content


@pytest.mark.django_db
def test_ddlon_min_negative_180(client, db_setup, tag_data):
    """ddlon is the lonitude and cannot be less than -180 degrees.  If a ddlon
    value is submitted with a lonitude less than -180s, an
    appropriate error message should be generated.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    dd_lat = 45.25
    dd_lon = -281.1

    tag_data["dd_lat"] = dd_lat
    tag_data["dd_lon"] = dd_lon

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "dd_lon must be numeric and lie between -180 and 180"
    assert msg in content


@pytest.mark.django_db
def test_general_location(client, db_setup, tag_data):
    """general_location is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    general_location = "Somewhere out there."
    tag_data["general_location"] = general_location

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].general_location == general_location


@pytest.mark.django_db
def test_specific_location(client, db_setup, tag_data):
    """specific_location is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    specific_location = "Right here. Exactly here."
    tag_data["specific_location"] = specific_location

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].specific_location == specific_location


@pytest.mark.django_db
def test_tlen(client, db_setup, tag_data):
    """tlen is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tlen = 450
    tag_data["tlen"] = tlen

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].tlen == tlen


@pytest.mark.django_db
def test_flen(client, db_setup, tag_data):
    """flen is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    flen = 450
    tag_data["flen"] = flen

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].flen == flen


@pytest.mark.django_db
def test_rwt(client, db_setup, tag_data):
    """rwt is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    rwt = 1450
    tag_data["rwt"] = rwt

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].rwt == rwt


@pytest.mark.django_db
def test_girth(client, db_setup, tag_data):
    """girth is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    girth = 1450
    tag_data["girth"] = girth

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].girth == girth


@pytest.mark.django_db
def test_fish_fate_released(client, db_setup, tag_data):
    """fish fate is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    fate = "R"
    tag_data["fate"] = fate

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].fate == fate


@pytest.mark.django_db
def test_fish_fate_killed(client, db_setup, tag_data):
    """fish fate is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    fate = "K"
    tag_data["fate"] = fate

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].fate == fate


@pytest.mark.django_db
def test_fish_fate_nonexistant(client, db_setup, tag_data):
    """fish fate is an optional field but is constrained to one of
    pre-determined values.  If a non-existant option is included in
    the posted data, an appropriate error will be thrown.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    fate = "FOO"
    tag_data["fate"] = fate

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200
    content = str(response.content)

    with open("C:/1work/scrapbook/wft2.html", "wb") as f:
        f.write(response.content)

    msg = "Select a valid choice. " "FOO is not one of the available choices."
    assert msg in content


@pytest.mark.django_db
def test_fish_sex_male(client, db_setup, tag_data):
    """fish sex is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    sex = "1"
    tag_data["sex"] = sex

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].sex == sex


@pytest.mark.django_db
def test_fish_sex_female(client, db_setup, tag_data):
    """fish sex is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    sex = "2"
    tag_data["sex"] = sex

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].sex == sex


@pytest.mark.django_db
def test_fish_sex_nonexistant(client, db_setup, tag_data):
    """fish sex is an optional field but is constrained to one of
    pre-determined values.  If a non-existant option is included in
    the posted data, an appropriate error will be thrown.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    sex = "FOO"
    tag_data["sex"] = sex

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200
    content = str(response.content)

    msg = "Select a valid choice. " "FOO is not one of the available choices."
    assert msg in content


@pytest.mark.django_db
def test_fish_tag_removed_false(client, db_setup, tag_data):
    """tag removed is an optional field.  If it is included in the
    posted data as false, it will be false in the associated recovery
    object in the database.

    """
    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_removed = False
    tag_data["tag_removed"] = tag_removed

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].tag_removed == tag_removed


@pytest.mark.django_db
def test_fish_tag_removed_true(client, db_setup, tag_data):
    """tag removed is an optional field.  If it is included in the
    posted data as true, it will be true in the associated recovery
    object in the database.

    """

    report = Report.objects.get(reported_by__first_name="Homer")
    url = reverse("tfat:create_recovery", kwargs={"report_id": report.id})

    tag_removed = True
    tag_data["tag_removed"] = tag_removed

    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].tag_removed == tag_removed
