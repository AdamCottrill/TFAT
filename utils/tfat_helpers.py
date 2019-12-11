"""
=============================================================
~/tfat/utils/tfat_helpers.py
 Created: 11 Dec 2019 13:33:32

 DESCRIPTION:


 A. Cottrill
=============================================================
"""

import pyodbc


def build_years_array(db_years, first_year=None, last_year=None):
    """The database queries are parameterized to accept a single year of
    data.  This function takes a two element array [db_years] (which
    contains year first and last years in the target database) and two
    optional arguments that specify the earliest and latest year to
    subset that array by.  returns an array of years that encapsulate
    the years inthe database, subsetted by the provided first_year and
    last_year parameters.

    Arguments:
    - `db_years`: [min([year]), max([year])]
    - `first_year`:
    - `last_year`:

    """

    fyear = max(first_year, db_years[0]) if first_year else db_years[0]
    lyear = min(last_year, db_years[1]) if last_year else db_years[1]

    return list(range(fyear, lyear + 1))


def get_db_years(src_db):
    """connect to our source database and get the first and last year in
    the fn011 table. (first and last year in the fn011 table are returned
    by a stored query [get_db_years] that must exist in the database).

    Arguments:
    - `src_db`: full path the source database.

    """

    constring = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={}"
    with pyodbc.connect(constring.format(src_db)) as src_conn:
        src_cur = src_conn.cursor()
        rs = src_cur.execute("execute get_db_years")
        yrs = rs.fetchone()
    return [int(x) for x in yrs]


def get_encounters(src_db, year):
    """Get all of the OMNR tag encounters (application and recovery
    events) from the specified year.  This function returns list of
    dictionaries - each element represents a single row returned by
    the query.

    Arguments:
    - `src_db`: full path the source database.
    - `year`:  the name

    """

    constring = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={}"
    with pyodbc.connect(constring.format(src_db)) as src_conn:
        src_cur = src_conn.cursor()
        rs = src_cur.execute("execute get_all_encounters @yr='{}'".format(year))
        data = rs.fetchall()
        flds = [x[0].upper() for x in src_cur.description]

    records = []
    for record in data:
        records.append({k: v for k, v in zip(flds, record)})

    return records
