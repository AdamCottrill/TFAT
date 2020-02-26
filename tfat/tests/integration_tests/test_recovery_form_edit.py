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
from tfat.tests.factories import (
    UserFactory,
    JoePublicFactory,
    LakeFactory,
    SpeciesFactory,
    ReportFactory,
    RecoveryFactory,
)


@pytest.fixture()
def user():
    """
    """
    user = UserFactory(email="mickey@disney.com")
    user.set_password("Abcd1234")
    user.save()

    return user


@pytest.fixture()
def species():
    spc = SpeciesFactory()
    return spc


@pytest.fixture()
def lake():
    lake = LakeFactory()
    return lake


@pytest.fixture()
def angler():
    angler = JoePublicFactory.create(first_name="Homer", last_name="Simpson")
    return angler


@pytest.fixture()
def db_setup(angler, species, lake):
    """
    """

    report_date = datetime(2010, 10, 10).replace(tzinfo=pytz.UTC)
    # associated tags to test conditional elements
    report = ReportFactory(reported_by=angler, follow_up=False, report_date=report_date)
    RecoveryFactory(report=report, spc=species, lake=lake)


@pytest.fixture()
def tag_data(species, lake):
    """A fixture to hold basic minimal data requirements for each
    test. Updated as needed in each test.
    """

    tag_data = {
        "tagdoc": "25012",
        "tagid": "1234",
        "spc": species.id,
        "lake": lake.id,
        "date_flag": 0,
    }

    return tag_data


@pytest.mark.django_db
def test_edit_recovery_form_requires_login(client, user, db_setup):
    """The edit recovery form should be unaccessible to unauthorized users. If
    an unathenticated user tries to access the url, they should be
    rediected to the login page.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_can_edit_recovery_url(client, user, db_setup):
    """Verify that the form and its correct elements are rendered when we
    call the edit_recovery form"""

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")

    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    client.login(username=user.email, password="Abcd1234")
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
def test_basic_data(client, user, db_setup, tag_data):
    """verify that we can post the form with the minimal data elements and
    a tag recovery object will be editd in the database.

    """

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].tagid == tag_data["tagid"]
    assert recoveries[0].tagdoc == tag_data["tagdoc"]


@pytest.mark.django_db
def test_basic_data_no_add_another(client, user, db_setup):
    """If we are editing an existing recovery, when it is submitted, the
    'Add Another Tag' button should not appear in the repsonse.  It is for
    new tags only.

    """

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "33333"
    tagdoc = "25012"
    tag_data = {"tagdoc": tagdoc, "tagid": tagid, "spc": 1, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    content = str(response.content)

    assert "Add Another Tag" not in content


@pytest.mark.django_db
def test_missing_tagid(client, user, db_setup):
    """tagid is a required field.  If the form is submitted without it, a
    meaningful error message should be generated.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagdoc = "25012"
    tag_data = {"tagdoc": tagdoc, "spc": 1, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    content = str(response.content)
    msg = "This field is required."
    assert msg in content


@pytest.mark.django_db
def test_missing_species(client, user, db_setup):
    """fish species is a required field.  If the form is submitted without it, a
    meaningful error message should be generated.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagdoc = "25012"
    tagid = "1234"
    tag_data = {"tagid": tagid, "tagdoc": tagdoc, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    content = str(response.content)
    msg = "This field is required."
    assert msg in content


@pytest.mark.django_db
def test_invalid_species(client, user, db_setup):
    """species is a required field.  If the form is submitted with a
    species that does not exist, a meaningful error message should be
    generated.

    """
    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "12345"
    tagdoc = "25012"
    tag_data = {"tagdoc": tagdoc, "tagid": tagid, "spc": 999, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Select a valid choice. " "That choice is not one of the available choices."
    assert msg in content


@pytest.mark.django_db
def test_missing_tagdoc(client, user, db_setup):
    """tagdoc is a required field.  If the form is submitted without it, a
    meaningful error message should be generated.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "1236"
    tag_data = {"tagid": tagid, "spc": 1, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    content = str(response.content)
    msg = "This field is required."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_short(client, user, db_setup):
    """if the tagdoc is provided, it must be exacly 5 characters long.
    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "12345"
    tagdoc = "2501"
    tag_data = {"tagdoc": tagdoc, "tagid": tagid, "spc": 1, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)
    msg = "TAGDOC must be 5 characters long."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_long(client, user, db_setup):
    """if the tagdoc is provided, it must be exacly 5 characters long.
    """
    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "12345"
    tagdoc = "250129"
    tag_data = {"tagdoc": tagdoc, "tagid": tagid, "spc": 1, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)
    msg = "TAGDOC must be 5 characters long."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_bad_tag_type(client, user, db_setup):
    """if the tagdoc is provided, the 1st character must correspond to a
    valid, exising tag_type.  if not, an error will be thrown.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "12345"
    tagdoc = "Y5012"
    tag_data = {"tagdoc": tagdoc, "tagid": tagid, "spc": 1, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)
    msg = "Y is not a valid tag type code."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_good_tag_type(client, user, db_setup, tag_data):
    """if the tagdoc is provided, the 1st character must correspond to a
    valid, exising tag_type.  When the recovery is saved, the tag_type
    will be updated to reflect the value of the 1st character in
    tagdoc.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "12345"
    tagdoc = "35012"
    tag_data["tagid"] = tagid
    tag_data["tagdoc"] = tagdoc

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].tagdoc == tagdoc


@pytest.mark.django_db
def test_tagdoc_bad_tag_position(client, user, db_setup):
    """if the tagdoc is provided, the 2nd character must correspond to a
    valid, exising tag_position.  if not, an error will be thrown.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "12345"
    tagdoc = "2Y012"
    tag_data = {"tagdoc": tagdoc, "tagid": tagid, "spc": 1, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)
    msg = "Y is not a valid tag position code."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_good_tag_position(client, user, db_setup):
    """if the tagdoc is provided, the 2nd character must correspond to a
    valid, exising tag_position.  When the recovery is saved, the tag_position
    will be updated to reflect the value of the 2nd character in
    tagdoc.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "12345"
    tagdoc = "25012"
    tag_data = {"tagdoc": tagdoc, "tagid": tagid, "spc": 1, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].tagdoc == tagdoc


@pytest.mark.django_db
def test_tagdoc_bad_agency(client, user, db_setup):
    """if the tagdoc is provided, the 3rd and 4th characters must
    correspond to a valid, exising agency.  If not, an error will be
    thrown.

    """
    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "12345"
    tagdoc = "25XX2"
    tag_data = {"tagdoc": tagdoc, "tagid": tagid, "spc": 1, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "XX is not a valid agency code."
    assert msg in content


@pytest.mark.django_db
def test_tagdoc_bad_colour(client, user, db_setup):
    """if the tagdoc is provided, the 5th character must correspond to a
    valid, exising colour.  if not, an error will be thrown.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tagid = "12345"
    tagdoc = "2501X"
    tag_data = {"tagdoc": tagdoc, "tagid": tagid, "spc": 1, "date_flag": 0}

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "X is not a valid colour code."
    assert msg in content


@pytest.mark.django_db
def test_good_clipc(client, user, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  All of the elements must exist
    in the clip code lookup table.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")

    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    clipc = "14"
    tag_data["clipc"] = clipc

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].clipc == clipc


@pytest.mark.django_db
def test_good_clipc_0(client, user, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  Clip code '0' is used to
    indicate the absence of other clips and should be acceptable as a
    valid clip when the form is processed.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    clipc = "0"
    tag_data["clipc"] = clipc

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].clipc == clipc


@pytest.mark.django_db
def test_bad_clipc_includes_0(client, user, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  Clip code '0' is used to
    indicate the absence of other clips.  As such, and clipc value
    that includes 0 along with any other clip code should return an
    error.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    clipc = "140"
    tag_data["clipc"] = clipc

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "CLIPC cannot contain 0 and other clip codes."
    assert msg in content


@pytest.mark.django_db
def test_bad_clipc_includes_duplicates(client, user, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  All of the elements must exist
    in the clip code lookup table and appear only once.  If a clip
    code appears more than once in clipc, a meaningfull error message
    should be thrown. (eg. 11 is not valid.)

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    clipc = "114"
    tag_data["clipc"] = clipc

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Clip codes cannot repeat."
    assert msg in content


@pytest.mark.django_db
def test_bad_clipc_includes_wrong_order(client, user, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured. All of the elements are to be
    saved in ascii-sort order.  If a clip code is reported in the
    wrong order, it will be save in the correct order.  (eg 532 will
    be saved as 235)

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    clipc = "532"
    tag_data["clipc"] = clipc

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].clipc == "235"


@pytest.mark.django_db
def test_bad_clipc_nonexistant_clip(client, user, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  If one of the elements does exist
    in the clip code lookup table an error should be thrown.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    clipc = "15X"
    tag_data["clipc"] = clipc

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Invalid clip codes: X"
    assert msg in content


@pytest.mark.django_db
def test_bad_clipc_multiple_nonexistant_clips(client, user, db_setup, tag_data):
    """clipc is a character field that contains the concatinated clips
    observed on a fish when captured.  If more than one of the
    elements does exist in the clip code lookup table an error should
    be thrown and the error message should contain a comma separated
    list of those elements.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    clipc = "15XZ"
    tag_data["clipc"] = clipc

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200
    content = str(response.content)

    msg = "Invalid clip codes: X,Z"
    assert msg in content


@pytest.mark.django_db
def test_missing_recovery_date(client, user, db_setup, tag_data):
    """It's not clear what should happen if data is not populated.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1

    assert recoveries[0].recovery_date is None
    assert recoveries[0].date_flag is 0


@pytest.mark.django_db
def test_recovery_date_greater_than_report_date(client, user, db_setup, tag_data):
    """a tag recovery event cannot occur after the reporting date.  A
    recovery event cannot be recorded if it had not happened when the
    report was created.  If the recovery date is a head of the report
    date, an appropriate error message should be returned.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    week_late = recovery.report.report_date + timedelta(days=7)

    tag_data["recovery_date"] = week_late.date()

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Recovery date occurs after report date."
    assert msg in content


@pytest.mark.django_db
def test_future_date(client, user, db_setup, tag_data):
    """a tag recovery event cannot be reported from the future.  A
    recovery event cannot be recorded if it has not happened yet.  If a
    date in the future is submitted, an appropriate error message should
    be returned.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    next_week = datetime.today() + timedelta(days=7)

    tag_data["recovery_date"] = next_week.date()

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data)

    assert response.status_code == 200
    content = str(response.content)

    msg = "Dates in the future are not allowed."
    assert msg in content


@pytest.mark.xfail
@pytest.mark.django_db
def test_recapture_date_ahead_of_report_date(client, user, db_setup, tag_data):
    """a tag recovery event cannot occur more recently than the reporting
    date. If this happens an error should be raised.

    """

    # NOT IMPLEMENTED YET
    assert 0 == 1


@pytest.mark.django_db
def test_tlen_greater_than_flen(client, user, db_setup, tag_data):
    """both tlen and flen can be provided as long as flen is less than tlen.
    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tlen = 450
    flen = 440

    tag_data["flen"] = flen
    tag_data["tlen"] = tlen

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)

    assert response.status_code == 200
    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].tlen == tlen
    assert recoveries[0].flen == flen


@pytest.mark.django_db
def test_tlen_less_than_flen(client, user, db_setup, tag_data):
    """if both total length and fork length are provided and fork length
    is greater than total length, raise an error.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tlen = 440
    flen = 450

    tag_data["flen"] = flen
    tag_data["tlen"] = tlen

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200
    content = str(response.content)

    msg = "Total length (tlen) cannot be less than fork length (flen)."
    assert msg in content


@pytest.mark.django_db
def test_ddlat_ddlon(client, user, db_setup, tag_data):
    """ddlat and ddlon are optional fields.  If they are included in the
    posted data, they will be correctly associated with the recovery
    object in the database.

    """
    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    dd_lat = 45.25
    dd_lon = -81.1

    tag_data["dd_lat"] = dd_lat
    tag_data["dd_lon"] = dd_lon

    client.login(username=user.email, password="Abcd1234")
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
def test_unknown_ddlat_ddlon(client, user, db_setup, tag_data):
    """ddlat and ddlon are optional fields.  but if they are null,
    latlon_flag must be unknown.  If a recovery is submitted without
    at latlon_flag==unknown, and error should be thrown.

    This test has the same problem as the sister test in the
    test_recovery_form_create.py file - the model instance does not
    seem to have the value from the cleaned data in the form?

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].latlon_flag == 0  # unknown


@pytest.mark.django_db
def test_derived_ddlat_ddlon_with_comment(client, user, db_setup, tag_data):
    """ddlat and ddlon are optional fields.  If a recovery is submitted
    with a comment (hopefully explaining how lat long was derived), the
    recovery should be edit in the database.
    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    latlon_flag = 2  # derived
    comment = "It was big."

    tag_data["dd_lat"] = 45.25
    tag_data["dd_lon"] = -81.1
    tag_data["latlon_flag"] = latlon_flag
    tag_data["comment"] = comment

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].latlon_flag == latlon_flag
    assert recoveries[0].comment == comment


@pytest.mark.django_db
def test_derived_ddlat_ddlon_without_comment(client, user, db_setup, tag_data):
    """ddlat and ddlon are optional fields.  If a recovery is submitted
    without a comment an error will be thrown.
    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tag_data["dd_lat"] = 45.25
    tag_data["dd_lon"] = -81.1
    tag_data["latlon_flag"] = 2

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "Describe how location was derived."
    assert msg in content


@pytest.mark.django_db
def test_ddlat_without_ddlon(client, user, db_setup, tag_data):
    """ddlat and ddlon are optional fields, but if one is provided, the
    other must be provided too. If ddlon is omitted, but dd_lat is
    included, an appropriate error message should be generated.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tag_data["dd_lat"] = 45.25
    tag_data["dd_lon"] = ""

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "If dd_lat is populated,  dd_lon must be populated too"
    assert msg in content


@pytest.mark.django_db
def test_ddlon_without_ddlat(client, user, db_setup, tag_data):
    """ddlat and ddlon are optional fields, but if one is provided, the
    other must be provided too. If ddkat is omitted, but dd_lon is
    included, an appropriate error message should be generated.

    """
    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tag_data["dd_lat"] = ""
    tag_data["dd_lon"] = -81.1

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "If dd_lon is populated,  dd_lat must be populated too"
    assert msg in content


@pytest.mark.django_db
def test_ddlat_max_90(client, user, db_setup, tag_data):
    """ddlat is the latitude and cannot exceed 90 degrees.  If a ddlat
    value is submitted with a latitude greater than 9s, an
    appropriate error message should be generated.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tag_data["dd_lat"] = 100
    tag_data["dd_lon"] = -81.1

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "dd_lat must be numeric and lie between -90 and 90"
    assert msg in content


@pytest.mark.django_db
def test_ddlat_min_negative_90(client, user, db_setup, tag_data):
    """ddlat is the latitude and cannot be less than -90 degrees.  If a
    ddlat value is submitted with a latitude less than -90, an
    appropriate error message should be generated.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tag_data["dd_lat"] = -100
    tag_data["dd_lon"] = -81.1

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "dd_lat must be numeric and lie between -90 and 90"
    assert msg in content


@pytest.mark.django_db
def test_ddlon_max_180(client, user, db_setup, tag_data):
    """ddlon is the longitude and cannot exceed 180 degrees.  If a ddlon
    value is submitted with a longitude greater than 180, an
    appropriate error message should be generated.
    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tag_data["dd_lat"] = 45.25
    tag_data["dd_lon"] = 281.1

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "dd_lon must be numeric and lie between -180 and 180"
    assert msg in content


@pytest.mark.django_db
def test_ddlon_min_negative_180(client, user, db_setup, tag_data):
    """ddlon is the lonitude and cannot be less than -180 degrees.  If a ddlon
    value is submitted with a lonitude less than -180s, an
    appropriate error message should be generated.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    dd_lat = 45.25
    dd_lon = -281.1

    tag_data["dd_lat"] = dd_lat
    tag_data["dd_lon"] = dd_lon

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    msg = "dd_lon must be numeric and lie between -180 and 180"
    assert msg in content


@pytest.mark.django_db
def test_general_location(client, user, db_setup, tag_data):
    """general_location is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    general_location = "Somewhere out there."
    tag_data["general_location"] = general_location

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].general_location == general_location


@pytest.mark.django_db
def test_specific_location(client, user, db_setup, tag_data):
    """specific_location is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    specific_location = "Right here. Exactly here."
    tag_data["specific_location"] = specific_location

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].specific_location == specific_location


@pytest.mark.django_db
def test_tlen(client, user, db_setup, tag_data):
    """tlen is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tlen = 450
    tag_data["tlen"] = tlen

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].tlen == tlen


@pytest.mark.django_db
def test_flen(client, user, db_setup, tag_data):
    """flen is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    flen = 450
    tag_data["flen"] = flen

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].flen == flen


@pytest.mark.django_db
def test_rwt(client, user, db_setup, tag_data):
    """rwt is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    rwt = 1450
    tag_data["rwt"] = rwt

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].rwt == rwt


@pytest.mark.django_db
def test_girth(client, user, db_setup, tag_data):
    """girth is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    girth = 1450
    tag_data["girth"] = girth

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].girth == girth


@pytest.mark.django_db
def test_fish_fate_released(client, user, db_setup, tag_data):
    """fish fate is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    fate = "R"
    tag_data["fate"] = fate

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].fate == fate


@pytest.mark.django_db
def test_fish_fate_killed(client, user, db_setup, tag_data):
    """fish fate is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    fate = "K"
    tag_data["fate"] = fate

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].fate == fate


@pytest.mark.django_db
def test_fish_fate_nonexistant(client, user, db_setup, tag_data):
    """fish fate is an optional field but is constrained to one of
    pre-determined values.  If a non-existant option is included in
    the posted data, an appropriate error will be thrown.

    """
    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    fate = "FOO"
    tag_data["fate"] = fate

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200
    content = str(response.content)

    with open("C:/1work/scrapbook/wft2.html", "wb") as f:
        f.write(response.content)

    msg = "Select a valid choice. " "FOO is not one of the available choices."
    assert msg in content


@pytest.mark.django_db
def test_fish_sex_male(client, user, db_setup, tag_data):
    """fish sex is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    sex = "1"
    tag_data["sex"] = sex

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].sex == sex


@pytest.mark.django_db
def test_fish_sex_female(client, user, db_setup, tag_data):
    """fish sex is an optional field.  If it is included in the
    posted data, it will be correctly associated with the recovery
    object in the database.

    """
    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    sex = "2"
    tag_data["sex"] = sex

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].sex == sex


@pytest.mark.django_db
def test_fish_sex_nonexistant(client, user, db_setup, tag_data):
    """fish sex is an optional field but is constrained to one of
    pre-determined values.  If a non-existant option is included in
    the posted data, an appropriate error will be thrown.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    sex = "FOO"
    tag_data["sex"] = sex

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200
    content = str(response.content)

    msg = "Select a valid choice. " "FOO is not one of the available choices."
    assert msg in content


@pytest.mark.django_db
def test_fish_tag_removed_false(client, user, db_setup, tag_data):
    """tag removed is an optional field.  If it is included in the
    posted data as false, it will be false in the associated recovery
    object in the database.

    """
    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tag_removed = False
    tag_data["tag_removed"] = tag_removed

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].tag_removed == tag_removed


@pytest.mark.django_db
def test_fish_tag_removed_true(client, user, db_setup, tag_data):
    """tag removed is an optional field.  If it is included in the
    posted data as true, it will be true in the associated recovery
    object in the database.

    """

    recovery = Recovery.objects.get(report__reported_by__first_name="Homer")
    url = reverse("tfat:edit_recovery", kwargs={"recovery_id": recovery.id})

    tag_removed = True
    tag_data["tag_removed"] = tag_removed

    client.login(username=user.email, password="Abcd1234")
    response = client.post(url, tag_data, follow=True)
    assert response.status_code == 200

    content = str(response.content)
    with open("C:/1work/scrapbook/wtf2.html", "wb") as f:
        f.write(response.content)

    recoveries = Recovery.objects.all()
    assert len(recoveries) == 1
    assert recoveries[0].tag_removed == tag_removed
