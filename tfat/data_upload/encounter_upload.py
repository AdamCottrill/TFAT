"""
=============================================================
~/utils/project_upload.py
Created: Aug-12-2021 08:49
DESCRIPTION:



=============================================================
"""

# import argparse

import os

import logging

from django.db import transaction, DatabaseError

# from django.db.models import OuterRef, Subquery, Count

from common.models import Species

from tfat.models import Project, Encounter

import tfat.data_upload.data_prep as prep

import tfat.data_upload.fetch_utils as fetch

from tfat.data_upload.target_utils import (
    get_id_cache,
)


logger = logging.getLogger(__name__)


def process_accdb_upload(SRC_DIR: str, SRC_DB: str):

    spc_cache = get_id_cache(Species, ["spc"])

    # for each of the encounter records we need to loop over them, pop
    # off project code, and species code and them replace with their
    # associated id's

    SRC = os.path.join(SRC_DIR, SRC_DB)
    src_con = fetch.get_mdb_connection(SRC)
    try:

        logger.debug("Fetching Encounter records")
        stmt = fetch.get_encounters_stmt()
        rs = fetch.execute_select(src_con, stmt)

        # get prj_cd cache here see if the project code exists in project
        # tracker - if not create a dummy place holder for now.
        prj_cds = list(set([x["prj_cd"] for x in rs]))
        projects_list = fetch.make_project_cache(prj_cds)

        project_cache = {x["slug"]: (i + 1) for i, x in enumerate(projects_list)}
        project_inverse = {v: k for k, v in project_cache.items()}

        species_cache = get_id_cache(Species, ["spc"])
        encounters = prep.encounters(rs, project_cache, species_cache)
        if encounters.get("errors"):
            return {"status": "error", "errors": encounters.get("errors")}

    finally:
        src_con.close()

    # if there are any error stop and report them here...

    # =========================================================
    # insert our data

    try:
        with transaction.atomic():

            # delete our old project data:
            Project.objects.filter(prj_cd__in=prj_cds).delete()
            logger.debug("Creating Projects records...")
            items = []
            for item in projects_list:
                obj = Project(**item)
                items.append(obj)
            Project.objects.bulk_create(items)
            filters = {"prj_cd__in": prj_cds}
            project_map = get_id_cache(Project, filters=filters)

            # =========================
            #        Encounters

            # data = prep.fn011(fn011, lake_cache, protocol_cache, user_cache)
            logger.debug("Creating Encounter records...")
            items = []

            for i, item in enumerate(encounters["data"]):
                tmp = item.dict()
                project_id = tmp["project_id"]
                tmp["project_id"] = project_map[project_inverse[project_id]]
                obj = Encounter(**tmp)
                items.append(obj)
            Encounter.objects.bulk_create(items)
            logger.debug("Done creating records...")

            return {"status": "success", "prj_cds": prj_cds}

    except DatabaseError as error:
        return {"status": "insert-error", "errors": error}
