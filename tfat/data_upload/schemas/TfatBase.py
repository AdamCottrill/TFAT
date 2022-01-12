from pydantic import BaseModel

prj_cd_regex = r"[A-Z]{3}\_[A-Z]{2}\d{2}\_[A-Z0-9]{3}"


class TfatBase(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        use_enum_values = True
        extra = "ignore"
