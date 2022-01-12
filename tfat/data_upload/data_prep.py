"""
=============================================================
~/tfat/data_upload/data_prep.py
Created: 11 Jan 2022 11:55:34

DESCRIPTION:

  Functions that take the raw data from our sql
  queries and perform final transformations before creating
  Django objects.

  TODO: consider replacing these fucntions with Pydantic Models.


A. Cottrill
=============================================================
"""

from pydantic.error_wrappers import ValidationError

from .schemas import Encounter


def make_slug(item):
    """concatenate the key fields of item into a hyphen separated
    string."""

    slug = (
        f'{item["prj_cd"]}-{item["sam"]}-{item["eff"]}'
        + f'-{item["spc"]}-{item["grp"]}-{item["fish"]}'
    )

    return slug.lower()


def encounters(data, project_cache, species_cache):
    valid = []
    errors = []

    for item in data:

        item["slug"] = make_slug(item)

        prj_cd = item.pop("prj_cd")
        spc = item.pop("spc")

        item["project_id"] = project_cache.get(prj_cd.lower())
        item["species_id"] = species_cache.get(spc)

        # any additional transformation here:
        try:
            tmp = Encounter(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}
