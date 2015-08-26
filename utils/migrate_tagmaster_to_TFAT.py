'''=============================================================
c:/1work/Python/djcode/tfat/utils/migrate_tagmaster_to_TFAT.py
Created: 12 Jun 2015 09:20:21

DESCRIPTION:

This script migrates the data from the old fishnet/access tagging
database to the new tfat data model.

I created JoePublic objects from the Angler_master table and then
creates tag reports and tag recovery events from the 121 and 125
tables.

The original databases treated each fishing trip as a net set
(generally with one tag).  The new model ignores fishing trips, but
uses tag report events.  Each event can have one or more associated tags.

If a tag or tag report did not have a date, the date was assumed to be
the last day of the year (but could be changed to anything).
Similarly, if the angler id was not found in the Angler_master update,
it was recoded to 'Unknown'.


A. Cottrill
=============================================================

'''


#import django
#django.setup()

import django_settings

from datetime import datetime
import pyodbc
import pytz

from tfat.models import Species, JoePublic, Report, Recovery

timezone = pytz.timezone('US/Eastern')

src_db = "C:/1work/Python/djcode/tfat/utils/TagMaster.mdb"
constr ="DRIVER={{Microsoft Access Driver (*.mdb)}};DBQ={}"


sql = 'exec _joe_public'

con = pyodbc.connect(constr.format(src_db))
cursor = con.cursor()
cursor.execute(sql)
joe_public = cursor.fetchall()

for person in joe_public:
    joe = JoePublic(
        first_name = person[1].title(),
        last_name = person[2].title(),
        address1 = person[3],
        town = person[4],
        province = person[5],
        postal_code = person[6],
        phone = person[7],
        affiliation = person[8],
        email = person[9],)
    joe.save()

#now we need a way to map the angler id numbers from tag master to the
#id numbers of each JoePublic in the django application

tm_anglers = {}
for person in joe_public:
    if person[1]:
        tm_anglers[person[1].lower() + person[2].lower()] = person[0]
    else:
        tm_anglers[person[2].lower()] = person[0]


joes = JoePublic.objects.all()
tfat_anglers = {}
for person in joes:
    key = person.first_name.lower() + person.last_name.lower()
    tfat_anglers[key] = person.id


#this will create a dictionary that has the tag master id's as the
#keys, and the tfat ids as the values.  This dictionary can then be
#used to get the correct Joe Public from reports generated from
#tag_master
angler_id_map = {}
for k,v in tm_anglers.items():
    angler_id_map[v] = tfat_anglers[k]



#===================================
#       TAG REPORTS

#now get our list of tag reports:
sql = 'exec _tag_reports'

cursor.execute(sql)
reports = cursor.fetchall()

for rep in reports:
    angler_id = angler_id_map.get(rep[0])

    if angler_id:
        joe = JoePublic.objects.get(id=angler_id)
    else:
        joe = JoePublic.objects.get(first_name='N/A')
    date_flag = int(rep[5])
    if rep[2] is None:
        reporting_date = datetime(int(rep[1]),12,31)
        date_flag = 0
    else:
        reporting_date = rep[2]
    tag_report = Report(
        reported_by = joe,
        report_date = timezone.localize(reporting_date),
        date_flag = date_flag,
        reporting_format = rep[3],
        comment = rep[4])

    tag_report.save()


#===================================
#       TAG RECOVERIES

#now get our list of tag recoveries:

sql = 'exec _tag_recovery'
cursor.execute(sql)
recoveries = cursor.fetchall()

# loop over each tag recovery, get it's Report_id using our
#report_id dictionary and insert it into the database.

for record in recoveries:
    angler_id = angler_id_map.get(record[0])
    if angler_id:
        joe = JoePublic.objects.get(id=angler_id)
    else:
        print('problem with angler_id = {}'.format(record[0]))
        joe = JoePublic.objects.get(first_name='N/A')
    report_date = timezone.localize(record[1])
    report  = Report.objects.get(reported_by=joe,
                                report_date__year=report_date.year,
                                report_date__month=report_date.month,
                                report_date__day=report_date.day)
    spc  = Species.objects.get(species_code=record[2])
    if record[3] is None:
        recovery_date = record[1]
        date_flag = 0
    else:
        recovery_date = record[3]
        date_flag = record[4]
    if record[13] is None or record[13]=="NAWAS":
        tagdoc = '99999'
    else:
        tagdoc=record[13]
    recovery = Recovery(
        report = report,
        spc = spc,
        recovery_date = timezone.localize(recovery_date),
        date_flag = date_flag,
        general_location = record[5],
        dd_lat = record[6],
        dd_lon = record[7],
        latlon_flag = int(record[8]),
        flen = record[9],
        tlen = record[10],
        rwt = record[11],
        tagid = record[12],
        tagdoc = tagdoc,
        fate = record[14],
    )
    recovery.save()
msg = '{} tag recoveries successfully added to database!'
print(msg.format(len(recoveries)))

#joe = JoePublic.objects.get(angler_id_map[record[0]])
#report  = Report.objects.get(reported_by=joe,
#                                report_date__year=report_date.year,
#                                report_date__month=report_date.month,
#                                report_date__day=report_date.day
#)
#spc  = Species.objects.get(species_code=record[2])
