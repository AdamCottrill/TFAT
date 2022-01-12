"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN125.py
 Created: 26 Aug 2021 16:43:50

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN125
  objects validate as expected.

  The script includes:

  1.  a dictionary that representes complete, valid data.

  2. a list of fields and associated modifications that should be
     automatically tranformed by Pydantic (e.g. trimming whitespaces
     and converting to title case)

  3. a list of required fields that are systematically omitted,

  4. and finally a list of changes to the dictionary of good data that
     invalidates it in a known way and verifies that pydantic raises
     the expected exception.

 A. Cottrill
=============================================================

"""


import pytest
from pydantic import ValidationError

from tfat.data_upload.schemas import Encounter


@pytest.fixture()
def data():
    data = {
        "project_id": 1,
        "species_id": 2,
        "sam": 10,
        "eff": "051",
        "grp": "00",
        "fish": 12,
        "observation_date": "2020-02-15",
        "grid": "1234",
        "dd_lat": 45,
        "dd_lon": -81,
        "rwt": 1100,
        "flen": 440,
        "tlen": 450,
        "age": 5,
        "sex": "1",
        "clipc": "5",
        "tagid": "123654A",
        "tagdoc": "25012",
        "tagstat": "A",
        "fate": "K",
        "comment": "FN125 comment",
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = Encounter(**data)

    assert item.project_id == data["project_id"]
    assert item.tagid == data["tagid"]


required_fields = [
    "project_id",
    "species_id",
    "sam",
    "eff",
    "grp",
    "fish",
    "observation_date",
    "fish",
    "tagid",
    "tagdoc",
    "tagstat",
]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.

    This tests does not work for required fields that have a default
    value (e.g. fate).

    Arguments:
    - `data`:

    """

    data[fld] = None

    with pytest.raises(ValidationError) as excinfo:
        Encounter(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "dd_lat",
    "dd_lon",
    "rwt",
    "flen",
    "tlen",
    "sex",
    "clipc",
    "age",
    "comment",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the Encounter item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = Encounter(**data)
    assert item.tagid == data["tagid"]
    assert item.tagdoc == data["tagdoc"]


mode_list = [
    # field, input, output
    ("tlen", "", None),
    ("flen", "", None),
    ("rwt", "", None),
]


@pytest.mark.parametrize("fld,value_in,value_out", mode_list)
def test_valid_alternatives(data, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some fo the
    fields.  GRP should be a two letter code made from uppercase
    letters or digits.  The pydantic model should convert any letters
    to uppercase automatically. Uppercase letters and any numbers
    should be returned unchanged.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    item = Encounter(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    (
        "dd_lat",
        40.6,
        "ensure this value is greater than or equal to 41.6",
    ),
    (
        "dd_lat",
        49.5,
        "ensure this value is less than or equal to 49.1",
    ),
    (
        "dd_lon",
        -90.1,
        "ensure this value is greater than or equal to -89.6",
    ),
    (
        "dd_lon",
        -75.0,
        "ensure this value is less than or equal to -76.3",
    ),
    (
        "grid",
        "123",
        "ensure this value has at least 4 characters",
    ),
    (
        "grid",
        "12345",
        "ensure this value has at most 4 characters",
    ),
    (
        "grid",
        "123A",
        "string does not match regex",
    ),
    (
        "eff",
        "12345",
        "ensure this value has at most 3 characters",
    ),
    (
        "flen",
        -4,
        "ensure this value is greater than 0",
    ),
    (
        "tlen",
        -4,
        "ensure this value is greater than 0",
    ),
    (
        "rwt",
        -4,
        "ensure this value is greater than 0",
    ),
    (
        "sex",
        8,
        "value is not a valid enumeration member;",
    ),
    (
        "clipc",
        "14Q",
        "Unknown clip code (Q) found in clipa/clipc (14Q)",
    ),
    # flen vs tlen
    (
        "flen",
        "500",
        "TLEN (450) must be greater than or equal to FLEN (500)",
    ),
    # condition
    (
        "rwt",
        "120",
        "FLEN/TLEN (440) is too large for the round weight (RWT=120.0)",
    ),
    (
        "rwt",
        "120",
        "FLEN/TLEN (450) is too large for the round weight (RWT=120.0)",
    ),
    (
        "rwt",
        "4000",
        "FLEN/TLEN (440) is too short for the round weight (RWT=4000.0)",
    ),
    (
        "rwt",
        "4000",
        "FLEN/TLEN (450) is too short for the round weight (RWT=4000.0)",
    ),
    # ascii-sorting:
    (
        "clipc",
        "41",
        "Found non-ascii sorted value (41) found in clipa/clipc/agest or tissue (it should be: 14",
    ),
    ("tagstat", "X", "value is not a valid enumeration member;"),
    ("tagdoc", "X", "ensure this value has at least 5 characters"),
    ("tagdoc", "1234567", "ensure this value has at most 5 characters"),
    ("tagdoc", "1234*", 'string does not match regex "^([A-Z0-9]{5})$"'),
    ("fate", "X", "value is not a valid enumeration member;"),
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    with pytest.raises(ValidationError) as excinfo:
        Encounter(**data)

    assert msg in str(excinfo.value)
