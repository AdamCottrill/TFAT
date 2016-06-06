'''=============================================================
c:/1work/Python/djcode/tfat/utils/backup_tfat.py
Created: 03 Jun 2016 14:17:45

DESCRIPTION:

This script backs up the contents of tfat.  It is intended to be run
regularlly as a scheduled task.  It dumps the contents of the tables in
tfat databases (including tables for users).

The sql dump of the databases tables (tfat.sql) can be used to create
a complete copy of the database by first create an new empty tfat
database (with gis extensions) followed by:

> psql -d tfat -f tfat.sql

USAGE:
> python backup_tfat.py

A. Cottrill
=============================================================

'''

from datetime import datetime
import logging
import psycopg2
import os


trg_dir = 'Y:/Fisheries Management/Assessment/Tagging/tfat_backup'

if not os.path.exists(trg_dir):
    os.makedirs(trg_dir)

LOG_FILENAME = os.path.join(trg_dir, "tfat_backup.log")
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    )
TODAY = datetime.now().strftime("%d-%b-%y %H:%M:%S")

#=====================================
#         INITIATE LOGFILE

msg = "TFAT Backup ({})"
msg = msg.format(TODAY)
logging.info("=" * len(msg))
logging.info(msg)


#=====================================
#         DATABASE DUMP

os.system("set PGPASSWORD=django")

dump_file = os.path.join(trg_dir, 'tfat.sql')
shell_cmd = 'pg_dump -U cottrillad tfat > "{}"'.format(dump_file)
os.system(shell_cmd)
msg = "Done TFAT Backup ({})\n".format(TODAY)
print(msg)
logging.info(msg)
