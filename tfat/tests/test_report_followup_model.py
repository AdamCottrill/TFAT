from tfat.models import Report

from tfat.tests.factories import *

import pytest


@pytest.mark.django_db
def test_report_str_complete():
    """The default string representation for a tag report is the anglers
    fist and last name plus the date the report was filed.
    """

    elements = {
        "first_name": "Homer",
        "last_name": "Simpson",
        "obs_date": datetime(2013, 10, 16),
    }

    angler = JoePublicFactory(
        first_name=elements["first_name"], last_name=elements["last_name"]
    )

    report = Report(reported_by=angler, report_date=elements["obs_date"])

    # convert our date the expected string format
    elements["obs_date"] = elements["obs_date"].strftime("%b-%d-%Y")

    should_be = "{first_name} {last_name} on {obs_date}"

    assert str(report) == should_be.format(**elements)
