"""
=============================================================
~/pydantic_playground/schemas/utils.py
Created: Jul-17-2021 17:44
DESCRIPTION:

    pydantic models used to parse and validate incoming records.

A. Cottrill
=============================================================
"""


from typing import Optional

from pydantic.validators import str_validator


def string_to_float(v) -> Optional[float]:
    """A validator that will convert floats passed in as strings to a python float"""
    if v is None:
        return v
    else:
        try:
            val = float(v)
        except ValueError:
            val = None
    return val


def string_to_int(v) -> Optional[int]:
    """A validator that will convert floats passed in as strings to a python float"""
    if v is None:
        return v
    else:
        try:
            val = int(v)
        except ValueError:
            val = None
    return val
