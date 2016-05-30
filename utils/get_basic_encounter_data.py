'''=============================================================
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

A. Cottrill
=============================================================

'''

import django_settings
import django
django.setup()

import pyodbc
import psycopg2

from tfat.models import Species, Project, Encounter, Database

PG_USER = 'adam'
PG_DB = 'pjtk2'
PG_PASS = 'django'

PG_HOST = '142.143.160.56'
#PG_HOST = '127.0.0.1'

src_db = 'c:/1work/Python/djcode/tfat/utils/TagRecoveries.mdb'
constr ="DRIVER={{Microsoft Access Driver (*.mdb)}};DBQ={}"


def yr_from_prjcd(prj_cd):
    """

    Arguments:
    - `prj_cd`:
    """
    yr = prj_cd[6:8]
    if int(yr) < 50:
        return int('20' + yr)
    else:
        return int('19' + yr)


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
#  #==========================================
#  #    PROJECT and DATBASE   INFO
#
#  #get the projects, and project names from project tracker and load them
#
#  pg_constr = "host={0} dbname={1} user={2} password={3}".\
#              format(PG_HOST, PG_DB, PG_USER, PG_PASS)
#  pgconn = psycopg2.connect(pg_constr)
#  pgcur = pgconn.cursor()
#
#  sql = "select master_database, path from pjtk2_database"
#
#  pgcur.execute(sql)
#
#  dbases = pgcur.fetchall()
#  for db in dbases:
#      dbase = Database(master_database=db[0], path=db[1])
#      dbase.save()
#
#  print('Done uploading database info.')
#
#  #sql = "select prj_cd, prj_nm from pjtk2_project"
#
#  sql = """select prj_cd, prj_nm, master_database
#            from pjtk2_project prj join pjtk2_database dbase
#            on prj.master_database_id=dbase.id
#  """
#
#  pgcur.execute(sql)
#
#  projects = pgcur.fetchall()
#
#  for project in projects:
#      db = Database.objects.get(master_database=project[2])
#      proj = Project(prj_cd = project[0], prj_nm=project[1],
#                     year=yr_from_prjcd(project[0]), dbase=db)
#      proj.save()
#
#  print('Done uploading project info.')
#
#  pgcur.close()
#  pgconn.close()


#==========================================
#         UGLMU TAG ENCOUNTERS

#now get the basic encounter information, but this time, when we
#create the django objects, we will have to get the corresponding spc
#and project object too.

#clear out existing encounter objects:
foo = Encounter.objects.all().delete()

sql = 'exec Get_All_Encounters'

con = pyodbc.connect(constr.format(src_db))
cursor = con.cursor()
cursor.execute(sql)
encounters = cursor.fetchall()

#a couple of elements to help when we trip over un-documented projects
wtf = []
missing_db = Database.objects.get(master_database='Not Applicable')

for row in encounters:
    try:
        prj = Project.objects.get(prj_cd=row.PRJ_CD)
    except Project.DoesNotExist:
        wtf.append(row.PRJ_CD)
        prj_cd=row.PRJ_CD
        prj = Project(prj_cd=prj_cd, year=yr_from_prjcd(prj_cd),
                      prj_nm="Missing from Project Tracker!", dbase=missing_db)
        prj.save()
    spc = Species.objects.filter(species_code=row.Spc).first()

    if row.GRID and row.DD_LAT and row.DD_LON:
        comment=row.COMMENT5
        grid=row.GRID
        dd_lat=row.DD_LAT
        dd_lon=row.DD_LON
    else:
        tmp = "" if row.COMMENT5 is None else row.COMMENT5
        comment='NOTE:Actual recap location missing or compromized.\n' + tmp
        grid= row.GRID if row.GRID else 1638
        dd_lat= row.DD_LAT if row.DD_LAT else 45.01
        dd_lon= row.DD_LON if row.DD_LON else -81.01

    if prj and spc:
        encounter = Encounter(
            project=prj, spc=spc,
            observation_date = row.obs_date,
            sam = row.SAM,
            eff = row.EFF,
            grp = row.GRP,
            fish = row.FISH,
            grid = grid,
            dd_lat = dd_lat,
            dd_lon = dd_lon,
            flen = row.FLEN,
            tlen = row.TLEN,
            rwt = row.RWT,
            age = row.AGE,
            sex  = row.SEX,
            clipc = row.CLIPC,
            tagid = row.TAGID,
            tagdoc =  row.TAGDOC,
            tagstat =  row.TAGSTAT,
            fate = row.FATE,
            comment = comment
        )
        encounter.save()

print("Done uploading UGLMU tag encounters.")
