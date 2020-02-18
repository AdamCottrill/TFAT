"""=============================================================
~/djcode/tfat/utils/get_superior_encounters.py
Created: 18 Feb 2020 12:38:07

DESCRIPTION:

this script gets the basic UGLMU encounter information from the lake
superior Master databases and loads it into the tfat database.

 Encounter information is compile by an array of associated ms access
 databases - one for each data source.

**NOTE** - tagid is currently truncated to 10 to accomodate field size
  limitation in TFAT.  This will be addressed in the next verions of
  TFAT (soon).

A. Cottrill
=============================================================

"""

import os


SETTINGS_FILE = "main.settings.local"
# SETTINGS_FILE = "main.settings.production"

# SECRET should be set when virtualenv as activated.  Just incase its not
os.environ["SECRET_KEY"] = "\xb1>\xf3\x10\xd3p\x07\x8fS\x94'\xe3g\xc6cZ4\xb0R"

# taken from manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_FILE)


import django_settings
import django

django.setup()

import pyodbc
import psycopg2


from tfat.models import Species, Project, Encounter, Database

pyodbc.lowercase = True

pgpars = {
    "PG_USER": "adam",
    "PG_DB": "superior",
    "PG_PASS": "django",
    "PG_HOST": "142.143.160.56",
    # PG_HOST": '127.0.0.1'
}

# add an array of tag sources:
SRC_DIR = "x:/scrapbook/Superior_TFAT"
SRC_DBS = [
    os.path.join(SRC_DIR, "BBW_TFAT.accdb"),
    os.path.join(SRC_DIR, "BRK_TFAT.accdb"),
    os.path.join(SRC_DIR, "CF_TFAT.accdb"),
    os.path.join(SRC_DIR, "CIN_TFAT.accdb"),
]


def yr_from_prjcd(prj_cd):
    """

    Arguments:
    - `prj_cd`:
    """
    yr = prj_cd[6:8]
    if int(yr) < 50:
        return int("20" + yr)
    else:
        return int("19" + yr)


def get_project_info(prj_cd, conpars):
    """Connect to prject tracker and return the project name associated
    with a project code.  If one does not exists, return None.

    Arguments:
    - `prj_cd`:
    - `conpars`:

    """

    pgsql = """select prj_cd, prj_nm
              from pjtk2_project where prj_cd=%s;
    """

    pg_constr = "host={PG_HOST} dbname={PG_DB} user={PG_USER} password={PG_PASS}"
    project = None
    try:
        pgconn = psycopg2.connect(pg_constr.format(**conpars))
        pgcur = pgconn.cursor()
        pgcur.execute(pgsql, (prj_cd,))
        project = pgcur.fetchone()
    finally:
        pgconn.close()

    return project


def run_access_query(sql, dbase):
    """Connect to our target data (dbase) and run the sql.  If it returns
a recordset, return a 2-element list contians the record set and
column names. otherwise, return a 2-elemnt list of None's

    Arguments:
    - `sql`:
    - `dbase`:

    """

    constr = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={}"

    val = [None, None]
    try:
        con = pyodbc.connect(constr.format(src_db))
        cursor = con.cursor()
        cursor.execute(sql)
        rs = cursor.fetchall()
        colnames = [x[0] for x in cursor.description]
        val = [rs, colnames]
    finally:
        con.close()

    return val


# for each data source, get the encounter information, get the unique
# project codes and then delete the tag recoveries from those projects:

# see if there is any data about that project in project tracker and
# create a Tfat propejct record.


# for now:
missing_db = Database.objects.get(master_database="Not Applicable")


species_lookup = {str(x.species_code).zfill(3): x for x in Species.objects.all()}

for src_db in SRC_DBS:

    # ============================================
    #          PROJECT DATA

    sql = "exec Get_all_ProjectCodes"
    projects, colnames = run_access_query(sql, src_db)
    prj_cds = [x[0] for x in projects]

    # delete all of the projects and encounters in TFAT that are associated
    # with these project codes:
    Project.objects.filter(prj_cd__in=prj_cds).delete()

    for project in projects:
        prj_cd = project[0]
        projtracker = get_project_info(prj_cd, pgpars)
        if projtracker is None:
            prj = Project(
                prj_cd=prj_cd,
                year=yr_from_prjcd(prj_cd),
                prj_nm="Missing from Project Tracker!",
                # dbase=project[1],
                dbase=missing_db,
            )
        else:
            prj = Project(
                prj_cd=prj_cd,
                year=yr_from_prjcd(prj_cd),
                prj_nm=projtracker[1],
                # dbase=project[1],
                dbase=missing_db,
            )
        prj.save()

    # ==========================================
    #         UGLMU TAG ENCOUNTERS

    # now get the basic encounter information, but this time, when we
    # create the django objects, we will have to get the corresponding spc
    # and project object too.

    sql = "exec Get_All_Encounters"
    encounters, colnames = run_access_query(sql, src_db)

    for encounter in encounters:
        row = {k: v for k, v in zip(colnames, encounter)}

        prj = Project.objects.get(prj_cd=row.get("prj_cd"))

        spc = species_lookup.get(row.get("spc"))

        if spc is None:
            print("Unknown species code: {}".format(spc_code))

        comment = ""
        if row.get("grid") and row.get("dd_lat") and row.get("dd_lon"):
            grid = row.get("grid")
            dd_lat = row.get("dd_lat")
            dd_lon = row.get("dd_lon")
        else:
            tmp = "" if row.get("comment5") is None else row.get("comment5")
            comment = "NOTE:Actual recap location missing or compromized.\n" + tmp
            grid = row.get("grid") if row.get("grid") else 1461
            dd_lat = row.get("dd_lat") if row.get("dd_lat") else 48.2
            dd_lon = row.get("dd_lon") if row.get("dd_lon") else -87.3

        if prj and spc:
            encounter = Encounter(
                project=prj,
                spc=spc,
                observation_date=row.get("obs_date"),
                sam=row.get("sam"),
                eff=row.get("eff"),
                grp=row.get("grp"),
                fish=row.get("fish"),
                grid=grid,
                dd_lat=dd_lat,
                dd_lon=dd_lon,
                flen=row.get("flen"),
                tlen=row.get("tlen"),
                rwt=row.get("rwt"),
                age=row.get("age"),
                sex=row.get("sex"),
                clipc=row.get("clipc"),
                tagid=row.get("tagid")[-10:],
                tagdoc=row.get("tagdoc"),
                tagstat=row.get("tagstat"),
                fate=row.get("fate"),
                comment=comment,
            )
            encounter.save()

    print("Done uploading tag encounters from {}.".format(os.path.split(src_db)[1]))
