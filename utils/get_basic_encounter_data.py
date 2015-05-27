'''=============================================================
c:/1work/Python/djcode/tfat/utils/get_basic_encounter_data.py
Created: 26 May 2015 13:43:39


DESCRIPTION:

this script gets the basic encounter information and loads it into the
tfat database.

A. Cottrill
=============================================================

'''
import django_settings
import django
django.setup()

import pyodbc
import psycopg2

from tfat.models import Species, Project, Encounter

PG_USER = 'adam'
PG_DB = 'pjtk2'

PG_HOST = '142.143.160.56'
#PG_HOST = '127.0.0.1'

src_db = 'c:/1work/Python/djcode/tfat/utils/TagRecoveries.mdb'
constr ="DRIVER={{Microsoft Access Driver (*.mdb)}};DBQ={}"


#==========================================
#             SPECIES

#get species and load them into the database

sql = 'select spc, spc_nm, spc_nmsc from spc'

con = pyodbc.connect(constr.format(src_db))
cursor = con.cursor()
cursor.execute(sql)
spc = cursor.fetchall()

for fish in spc:
    species = Species(species_code=fish[0], common_name=fish[1],
                      scientific_name=fish[2])
    species.save()

con.close()
print('Done uploading species.')
#==========================================
#         PROJECT   INFO

#get the projects, and project names from project tracker and load them

pg_constr = "host={0} dbname={1} user={2}".format(PG_HOST, PG_DB, PG_USER)
pgconn = psycopg2.connect(pg_constr)
pgcur = pgconn.cursor()

sql = "select prj_cd, prj_nm from pjtk2_project"

pgcur.execute(sql)

projects = pgcur.fetchall()
#finally get the basic encounter information

for project in projects:
    proj = Project(prj_cd = project[0], prj_nm=project[1])
    proj.save()

print('Done uploading project info.')

#==========================================
#         NEARSHORE ENCOUNTERS

#now get the basic encounter information, but this time, when we
#create the django objects, we will have to get the corresponding spc
#and project object too.

sql = 'exec Nearshore_tags'

con = pyodbc.connect(constr.format(src_db))
cursor = con.cursor()
cursor.execute(sql)
encounters = cursor.fetchall()

for row in encounters:
    prj = Project.objects.filter(prj_cd=row.PRJ_CD).first()
    spc = Species.objects.filter(species_code=row.Spc).first()
    if prj and spc:
        encounter = Encounter(
            project=prj, spc=spc,
            observation_date = row.obs_date,
            sam = row.SAM,
            eff = row.EFF,
            grid = row.GRID,
            dd_lat = row.DD_LAT,
            dd_lon = row.DD_LON,
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
            comment = row.COMMENT5
        )
        encounter.save()
print("Done uploading Nearshore tagging events.")
