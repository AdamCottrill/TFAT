"""=============================================================
c:/1work/Python/djcode/tfat/utils/get_basic_encounter_data.py
Created: 26 May 2015 13:43:39


DESCRIPTION:

this script gets the basic UGLMU encounter information and loads it
into the tfat database.

 Encounter information is compile by an associated ms access database.

The first part of the script contains code to get all projects codes
and database information from project tracker and the list of species
from the look-up table master.  This part of the script has been
commented out because it should only be necessary for a complete
rebuild - not a routine refresh.

USAGE:

- to rebuild everything, leave FIRST_YEAR and LAST_YEAR set to
  None. To get specific years, specify a two element array containing
  first and last years to refresh or replace.

- if only FIRST_YEAR is defined, all years >= FIRST_YEAR will be updated.

- if only LAST_YEAR is defined, all years <= FIRST_YEAR will be updated.

- if both FIRST_YEAR and LAST_YEAR are defined, all years >= FIRST_YEAR
  and <= LAST_YEAR will be updated.


TODOs:
    - add source array


A. Cottrill
=============================================================

"""

import os
from datetime import datetime

# SETTINGS_FILE = 'main.settings.local'
SETTINGS_FILE = "main.settings.production"

# SECRET should be set when virtualenv as activated.  Just incase its not
os.environ["SECRET_KEY"] = "\xb1>\xf3\x10\xd3p\x07\x8fS\x94'\xe3g\xc6cZ4\xb0R"

# taken from manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_FILE)


import django_settings
import django

django.setup()

import pyodbc
import psycopg2

from utils.tfat_helpers import get_db_years, build_years_array, get_encounters

from tfat.models import Species, Project, Encounter, Database

# year or None
FIRST_YEAR = 2018
LAST_YEAR = None


PG_USER = "adam"
PG_DB = "pjtk2"
PG_PASS = "django"

PG_HOST = "142.143.160.56"
# PG_HOST = '127.0.0.1'

src_db = "c:/Users/COTTRILLAD/1work/Python/djcode/tfat/utils/" + "TagRecoveries.accdb"
constr = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={}"


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


#  #==========================================
#  #             SPECIES
#
#  #get species and load them into the database
#
#  sql = 'select spc, spc_nm, spc_nmsc from spc'
#
#  con = pyodbc.connect(constr.format(src_db))
#  cursor = con.cursor()
#  cursor.execute(sql)
#  spc = cursor.fetchall()
#
#  for fish in spc:
#      species = Species(species_code=fish[0], common_name=fish[1],
#                        scientific_name=fish[2])
#      species.save()
#
#  con.close()
#  print('Done uploading species.')
#
#
# ==========================================
#    PROJECT and DATBASE   INFO

# get the projects, and project names from project tracker and load them

pg_constr = "host={0} dbname={1} user={2} password={3}".format(
    PG_HOST, PG_DB, PG_USER, PG_PASS
)
pgconn = psycopg2.connect(pg_constr)
pgcur = pgconn.cursor()

# sql = "select master_database, path from pjtk2_database"
#
# pgcur.execute(sql)
#
# dbases = pgcur.fetchall()
# for db in dbases:
#    dbase = Database(master_database=db[0], path=db[1])
#    dbase.save()
#
# print('Done uploading database info.')

# sql = "select prj_cd, prj_nm from pjtk2_project"

sql = """select prj_cd, prj_nm, master_database
          from pjtk2_project prj join pjtk2_database dbase
          on prj.master_database_id=dbase.id
"""

pgcur.execute(sql)

projects = pgcur.fetchall()

# add only new projects:
for project in projects:
    try:
        proj = Project.objects.get(prj_cd=project[0])
    except (Project.DoesNotExist, Project.MultipleObjectsReturned) as err:
        if "does not exist" in err.args[0]:
            msg = "Adding {} ({})".format(project[1], project[0])
            print(msg)
            db = Database.objects.get(master_database=project[2])
            proj = Project(
                prj_cd=project[0],
                prj_nm=project[1],
                year=yr_from_prjcd(project[0]),
                dbase=db,
            )
            proj.save()
            next  # new
        else:
            msg = "Multiple projects found with prj_cd={}".format()
            print(msg)
            next  # new
    # new - this will update the TFAT name if it does
    # not match project tracker. NOT RUN YET.
    if proj.prj_nm != project[1]:
        proj.prj_nm = project[1]
        proj.save()


print("Done uploading project info.")
pgcur.close()
pgconn.close()


# ==========================================
#         UGLMU TAG ENCOUNTERS

# now get the basic encounter information, but this time, when we
# create the django objects, we will have to get the corresponding spc
# and project object too.


# a couple of elements to help when we trip over un-documented projects
wtf = []
missing_db = Database.objects.get(master_database="Not Applicable")

project_lookup = {x.prj_cd: x for x in Project.objects.all()}
species_lookup = {"{:03d}".format(x.species_code): x for x in Species.objects.all()}

# create a cursor that will be used to connect to our source database:
years = get_db_years(src_db)
years = build_years_array(years, FIRST_YEAR, LAST_YEAR)

for year in years:
    Encounter.objects.filter(project__year=year).delete()
    encounters = get_encounters(src_db, year)
    print("Found {} encounters in {}.".format(len(encounters), year))
    objects = []

    for row in encounters:

        prj = project_lookup.get(row["PRJ_CD"])
        if prj is None:
            wtf.append(row["PRJ_CD"])
            prj_cd = row["PRJ_CD"]
            prj = Project(
                prj_cd=prj_cd,
                year=yr_from_prjcd(prj_cd),
                prj_nm="Missing from Project Tracker!",
                dbase=missing_db,
            )
            prj.save()

        observation_date = datetime.strptime(row["OBS_DATE"], "%Y/%m/%d")

        if row["GRID"] and row["DD_LAT"] and row["DD_LON"]:
            comment = row["COMMENT5"]
            grid = row["GRID"]
            dd_lat = row["DD_LAT"]
            dd_lon = row["DD_LON"]
        else:
            tmp = "" if row["COMMENT5"] is None else row["COMMENT5"]
            comment = "NOTE:Actual recap location missing or compromized.\n" + tmp
            grid = row["GRID"] if row["GRID"] else 1638
            dd_lat = row["DD_LAT"] if row["DD_LAT"] else 45.01
            dd_lon = row["DD_LON"] if row["DD_LON"] else -81.01

        if prj and spc:
            encounter = Encounter(
                project=prj,
                spc=species_lookup[row["SPC"]],
                observation_date=observation_date,
                sam=row["SAM"],
                eff=row["EFF"],
                grp=row["GRP"],
                fish=row["FISH"],
                grid=grid,
                dd_lat=dd_lat,
                dd_lon=dd_lon,
                flen=row["FLEN"],
                tlen=row["TLEN"],
                rwt=row["RWT"],
                age=row["AGE"],
                sex=row["SEX"],
                clipc=row["CLIPC"],
                tagid=row["TAGID"],
                tagdoc=row["TAGDOC"],
                tagstat=row["TAGSTAT"],
                fate=row["FATE"],
                comment=comment,
            )
            objects.append(encounter)
    Encounter.objects.bulk_create(objects)


print("There where {} issues.".format(len(wtf)))
print("Done uploading UGLMU tag encounters.")
