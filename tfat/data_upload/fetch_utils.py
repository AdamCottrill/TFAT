"""
=============================================================
~\tfat\data_upload\fetch_utils.py
Created: 11 Jan 2022 11:55:59


DESCRIPTION:

    fetch Encounters


A. Cottrill
=============================================================
"""


import pyodbc

import requests

from django.conf import settings


def get_prj_nms(prj_cds):

    # using the request library connect to the project tracker endpoint
    # and fetch the project names for the proejcts in our uploaded
    # data.

    url = settings.PROJECT_TRACKER_API_URL
    params = ",".join(prj_cds)
    response = requests.get(url, params={"prj_cd": params})

    if response.status_code == 200:
        data = response.json()
        return {x["prj_cd"]: x["prj_nm"] for x in data["results"]}
    else:
        msg = "Unable to Access Project Tracker"
        return {x["prj_cd"]: msg for x in prj_cds}


def make_project_cache(prj_cds):
    """Given a list of project codes, return a list of dictionaries with
    all of the information need to create project values in teh TFAT
    project Table.  Get the proejct name from project tracker, if it
    does not exist, give it a name that indicates that.

    """
    prj_nms = get_prj_nms(prj_cds)
    null_name = "Project Could not be found in project tracker."
    projects = []

    for prj_cd in prj_cds:
        yr = int(prj_cd[6:8])
        project_dict = {
            "prj_cd": prj_cd,
            "year": f"20{yr}" if yr < 50 else f"19{yr}",
            "slug": prj_cd.lower(),
            "prj_nm": prj_nms.get(prj_cd, null_name),
        }
        projects.append(project_dict)
    return projects


def get_mdb_connection(mdb):
    """

    Arguments:
    - `mdb`: path to either a *.mdb or *.accdb file.

    """
    constring = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s"
    con = pyodbc.connect(constring % mdb)
    return con


def execute_select(con, stmt):

    dat = []
    with con.cursor() as cursor:
        cursor.execute(stmt)
        rs = cursor.fetchall()
        colnames = [x[0].lower() for x in cursor.description]
        for row in rs:
            row_dict = {k: v for k, v in zip(colnames, row)}
            dat.append(row_dict)
    return dat


def get_encounters_stmt():

    stmt = """select
                 PRJ_CD,
                 SAM,
                 EFF,
                 Spc,
                 GRP,
                 FISH,
                 observation_date,
                 GRID,
                 DD_LON,
                 DD_LAT,
                 FLEN,
                 TLEN,
                 RWT,
                 AGE,
                 SEX,
                 TAGID,
                 TAGSTAT,
                 TAGDOC,
                 CLIPC,
                 FATE,
                 COMMENT5
    FROM Encounters;"""

    return stmt
