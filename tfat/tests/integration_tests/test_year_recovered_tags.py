"""=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/integration_tests/test_year_recovered_tags.py
Created: 01 Jun 2016 13:52:30


DESCRIPTION:

A series of integraion tests to verify that the views that render
summaries of tags recovered in a particular year contain all of the
necessary elements.

The expected elements include:

- "Tags recovered in {{year}}"
- a link to tags applied in the same year

- a summary (and count) of tags recoved by the omnr "UGMLU Encounters" (N=X)

- a summary (and count) of tags recoved by the general public "Non-MNR
  Recoveries (N=Z)"

If no tags were recovered in that year, the response should contain
some meaningful messages:

- No tags were recovered in any UGMLU project in {{ year }}.

- "There were no reports of tags from the general public or other
  agencies in {{ year }}."


If the view is called from tags_recovered_this_year(), the contents
will be slightly different.

- "Tags recovered so far in {{year}}"
- "No tags have been recovered yet in any UGMLU project in {{ year }}."

- "There haven't been any reports of tags from the general public or
  other agencies in {{ year }} yet."


A. Cottrill
=============================================================

"""


import pytest
import pytz

from django.urls import reverse


from tfat.tests.factories import (
    ProjectFactory,
    SpeciesFactory,
    JoePublicFactory,
    ReportFactory,
    RecoveryFactory,
    EncounterFactory,
)

from datetime import datetime


@pytest.fixture()
def project():
    return ProjectFactory(year=2015, prj_cd="LHA_IA15_999", prj_nm="Fake Project")


@pytest.fixture()
def species():
    return SpeciesFactory()


@pytest.fixture()
def report_date():
    return datetime(2015, 10, 10).replace(tzinfo=pytz.UTC)


@pytest.fixture()
def angler():
    return JoePublicFactory(first_name="Homer", last_name="Simpson")


@pytest.fixture()
def report(angler, report_date):
    return ReportFactory(report_date=report_date, reported_by=angler)


@pytest.mark.django_db
def test_tags_recovered_year(client):
    """Verify that we can navigate to the tags recovered year page
    with status code=200 and that the template is the one we think it is.
    """

    url = reverse("tfat:tags_recovered_in_year", kwargs={"year": 2010})
    response = client.get(url)

    assert response.status_code == 200

    template_name = "tfat/year_recovered_tags.html"
    assert template_name in [x.name for x in response.templates]


@pytest.mark.django_db
def test_tags_recovered_year_contains_year(client):
    """The tags recovered in a year page should include a header
    stating that this page contains the tags recovered in {{year}}
    """

    yr = 2008
    url = reverse("tfat:tags_recovered_in_year", kwargs={"year": yr})
    response = client.get(url)
    content = str(response.content)

    msg = "Tags recovered in {}".format(yr)
    assert msg in content


@pytest.mark.django_db
def test_tags_recovered_year_contains_link_to_applied(client):
    """The tags recovered in a year page should include a link to tags
    applied in the same year.  """

    yr = 2008
    url = reverse("tfat:tags_recovered_in_year", kwargs={"year": yr})
    response = client.get(url)
    content = str(response.content)

    print(content)

    # these two asserts are part of one long string that is wrapped in
    # template (but not in the html). django-pytest does not currently
    # have an equivalent to assertContains(html=True), so we will test
    # both parts separately.
    msg = "A summary of tags applied in {} can be found".format(yr)
    assert msg in content

    url = reverse("tfat:tags_applied_in_year", kwargs={"year": yr})
    msg = '<a href= "{}" >here.</a>'.format(url)
    assert msg in content


@pytest.mark.django_db
def test_tags_recovered_year_no_ugmlu_encounters(client):
    """The tags recovered in a year page should include a meaningful
    message if no omnr/uglmu encounters have been observed to date.

    """

    yr = 2008
    url = reverse("tfat:tags_recovered_in_year", kwargs={"year": yr})
    response = client.get(url)
    content = str(response.content)

    msg = "No tags were recovered in any UGMLU project in {}."

    assert msg.format(yr) in content


@pytest.mark.django_db
def test_tags_recovered_year_no_public_recoveries(client):
    """The tags recovered in a year page should include a meaningful
    message if no non-omnr/public recoveries were reported in that year.
    """

    yr = 2008
    url = reverse("tfat:tags_recovered_in_year", kwargs={"year": yr})
    response = client.get(url)
    content = str(response.content)

    msg = (
        "There were no reports of tags from the general public "
        + "or other agencies in {}."
    )

    assert msg.format(yr) in content


@pytest.mark.django_db
def test_tags_recovered_year_mnr_encounters(client, project, species):
    """The tags recovered in a year page should include a message that
    states the number of omnr encounters.
    """

    # create a couple of omnr encounters
    encounter = EncounterFactory(project=project, spc=species)
    encounter2 = EncounterFactory(project=project, spc=species)

    yr = 2015  # the year of the project
    url = reverse("tfat:tags_recovered_in_year", kwargs={"year": yr})
    response = client.get(url)
    content = str(response.content)

    msg = "UGLMU Encounters (N = 2)"
    assert msg in content


@pytest.mark.django_db
def test_tags_recovered_year_public_recoveries(client, report, species):
    """The tags recovered in a year page should include a message that
    states the number of non-omnr/public recoveries.
    """

    yr = 2015  # the year of the recoveries
    recovery_date = datetime(yr, 10, 10)

    # create a couple of public tag recoveries
    recovery = RecoveryFactory(report=report, spc=species, recovery_date=recovery_date)
    recovery2 = RecoveryFactory(report=report, spc=species, recovery_date=recovery_date)

    url = reverse("tfat:tags_recovered_in_year", kwargs={"year": yr})
    response = client.get(url)
    content = str(response.content)

    msg = "Non-MNR Recoveries (N = 2)"
    assert msg in content


# =================================================
#          TAGS RECOVERED THIS YEAR


@pytest.mark.django_db
def test_tags_recovered_this_year(client):
    """Verify that we can navigate to the tags recovered this year page
    with status code=200 and that the template is the one we think it is.
    """

    url = reverse("tfat:home")
    response = client.get(url)

    template_name = "tfat/year_recovered_tags.html"
    assert template_name in [x.name for x in response.templates]
    assert response.status_code == 200


@pytest.mark.django_db
def test_tags_recovered_this_year_so_far(client):
    """The tags recovered so far this year should include a header
    that states that the page contains the tags for recovered 'so far'
    in the current year
    """

    url = reverse("tfat:home")
    response = client.get(url)
    content = str(response.content)

    yr = datetime.now().year
    msg = "Tags recovered so far in {}".format(yr)
    assert msg in content


@pytest.mark.django_db
def test_tags_recovered_this_year_no_ugmlu_encounters(client):
    """The tags recovered in this year page should include a meaningful
    message if no omnr/uglmu encounters have been observed to date.

    """

    url = reverse("tfat:home")
    response = client.get(url)
    content = str(response.content)

    yr = datetime.now().year
    msg = "No tags have been recovered yet in any UGMLU project in {}."
    assert msg.format(yr) in content


@pytest.mark.django_db
def test_tags_recovered_this_year_no_public_recoveries(client):
    """The tags recovered this year page should include a meaningful
    message if no non-omnr/public recoveries were reported in that year.
    """

    url = reverse("tfat:home")
    response = client.get(url)
    content = str(response.content)

    yr = datetime.now().year
    msg = (
        "There haven\\'t been any reports of tags from the general "
        + "public or other agencies in {} yet."
    )
    assert msg.format(yr) in content
