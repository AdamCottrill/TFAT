from datetime import date
from typing import Optional
from enum import Enum, IntEnum
from pydantic import conint, confloat, validator, constr

from .TfatBase import TfatBase, prj_cd_regex
from .utils import string_to_int, string_to_float


class FateEnum(str, Enum):
    killed = "K"
    released = "R"


class TagStatEnum(str, Enum):
    on_capture = "C"
    tag_applied = "A"


class SexEnum(IntEnum):
    male = 1
    female = 2
    hermaphrodite = 3
    unknown = 9


class MatEnum(IntEnum):
    immature = 1
    mature = 2
    unknown = 9


# see the data dictionary for valid goncodes
gon_regex = r"(^[1-4|9]$)|(^([1-5]0)|(2[1-3])|(99))[2-8A-E]?$"


class Encounter(TfatBase):
    """Pydanic model for TFAT Tag encounters.

    most of the fields in a biological sample are optional, but if they
    are provided, they are subject to constraints.

    """

    project_id: int
    species_id: int
    sam: constr(max_length=5)
    eff: constr(max_length=3)
    grp: constr(max_length=3)
    fish: constr(max_length=10)
    observation_date: date
    grid: constr(regex=r"^\d{4}$", min_length=4, max_length=4)

    dd_lat: Optional[confloat(ge=41.6, le=49.1)] = None
    dd_lon: Optional[confloat(ge=-89.6, le=-76.3)] = None

    rwt: Optional[confloat(gt=0)] = None
    flen: Optional[conint(gt=0)] = None
    tlen: Optional[conint(gt=0)] = None
    age: Optional[conint(gt=0)] = None
    sex: Optional[SexEnum]
    clipc: Optional[constr(max_length=5)]
    tagid: str
    tagdoc: constr(regex="^([A-Z0-9]{5})$", min_length=5, max_length=5)
    tagstat: TagStatEnum = "A"
    fate: FateEnum = FateEnum.killed
    comment: Optional[str]

    class Config:
        validate_assignment = True

    _string_to_int = validator("tlen", "flen", allow_reuse=True, pre=True)(
        string_to_int
    )

    _string_to_float = validator("rwt", allow_reuse=True, pre=True)(string_to_float)

    @validator("fate", pre=True)
    def set_fate(cls, fate):
        if fate:
            return fate
        else:
            return "K"

    @validator("tlen")
    @classmethod
    def check_flen_vs_tlen(cls, v, values):
        flen = values.get("flen")
        if flen is not None and v is not None:
            if flen > v:
                msg = f"TLEN ({v}) must be greater than or equal to FLEN ({flen})"
                raise ValueError(msg)
        return v

    @validator("tlen", "flen")
    @classmethod
    def check_condition(cls, v, values, **kwargs):
        rwt = values.get("rwt")
        if rwt is not None and v is not None:
            k = 100000 * rwt / (v ** 3)
            if k > 3.5:
                msg = f"FLEN/TLEN ({v}) is too short for the round weight (RWT={rwt}) (K={k:.3f})"
                raise ValueError(msg)
            if k < 0.2:
                msg = f"FLEN/TLEN ({v}) is too large for the round weight (RWT={rwt}) (K={k:.3f})"
                raise ValueError(msg)
        return v

    @validator("clipc")
    @classmethod
    def check_clip_codes(cls, value, values):
        if value is not None:
            allowed = "01234567ABCDEFG"
            unknown = [c for c in value if c not in allowed]
            if unknown:
                msg = f"Unknown clip code ({','.join(unknown)}) found in clipa/clipc ({value})"
                raise ValueError(msg)
        return value

    @validator("clipc")
    @classmethod
    def check_ascii_sort(cls, value, values):
        if value is not None:
            val = list(value)
            val.sort()
            val = "".join(val)
            if val != value:
                msg = f"Found non-ascii sorted value ({value}) found in clipa/clipc/agest or tissue (it should be: {val})"
                raise ValueError(msg)
        return value
