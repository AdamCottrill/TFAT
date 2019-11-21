"""
=============================================================
c:/1work/Python/djcode/tfat/tfat/utils.py
Created: 19 Jun 2015 14:54:14

DESCRIPTION:



A. Cottrill
=============================================================
"""

from collections import OrderedDict
from datetime import datetime
from django.db.models import Count
from geojson import MultiLineString
from tfat.models import *


def connect_the_dots(pts):
    """given a list of tag pts, convert the point observations to
    poly-lines.  If there is only one pt, return None, otherwise connect
    the dots by copying the points and offseting by 1, producing N-1 line
    segments.

    Arguments: - `pts`: a list of point observations of the
    form [[lat1,lon1],[lat2, lon2], ... ]

    """
    if len(pts) > 1:
        # pts = [(x[1], x[0]) for x in pts]
        pts = [x[1] for x in pts]
        A = pts[:-1]
        B = pts[1:]

        coords = list(zip(A, B))
        return coords
    else:
        return None


def get_multilinestring(observation_lists):  # , applied=None):
    """given a list lists of tag encounters, extract the spatial data,
    'normalize' multiple observations, and return a geojson
    MULTILINESTRING string that can be plotted by leaflet.

    Arguments:
    - `observation_list`:

    """

    tag_path_dict = {}
    for qs in observation_lists:
        tag_path_dict = qs_to_tagdict(qs, tag_path_dict)

    tag_path_dict = sort_tagdict(tag_path_dict)

    # extract the spatial data
    # pts_dict = get_points_dict(encounters, applied)
    tag_paths = {}
    for tag, pts in tag_path_dict.items():
        tag_paths[tag] = connect_the_dots(pts)

    # create a line string for each tag number
    mls = []
    for k, v in tag_paths.items():
        if v:
            mls.append(MultiLineString(v))

    return mls


def spc_warning(qs_list):
    """Return true if the list in qs list refer to more than one species

    Arguments:
    - `qs_list`:
    """
    spc_list = []
    for qs in qs_list:
        spc_list.extend([x.spc.species_code for x in qs])
    ret = False if len(set(spc_list)) == 1 else True
    return ret


def tagdoc_warning(qs_list):
    """Return true if the list in qs_list have more than one tagdoc.

    Arguments:
    - `qs_list`:
    """
    tagdoc_list = []
    for qs in qs_list:
        tagdoc_list.extend([x.tagdoc for x in qs])
    ret = False if len(set(tagdoc_list)) == 1 else True
    return ret


def get_tagid_detail_data(tagid, encounter_list, partial=False):
    """A helper view to compile all of the information needed to render
    the tagid detail page.  These elements include:

    + OMNR Encounters (tag application and any recoveries)

    + Angler recaptures

    + multi-linestring representing the path of tag recoveries in
      chronological order

    + warnings if spc or tagid associated with a tag are not consistent

    Arguments: - `tagid`:

    """

    if partial:
        angler_recaps = Recovery.objects.filter(tagid__contains=tagid)
    else:
        angler_recaps = Recovery.objects.filter(tagid=tagid)

    angler_recaps = angler_recaps.select_related("report", "spc")

    mls = get_multilinestring([encounter_list, angler_recaps])

    spc_warn = spc_warning([encounter_list, angler_recaps])
    tagdoc_warn = tagdoc_warning([encounter_list, angler_recaps])

    nobs = len(angler_recaps) + len(encounter_list)

    return {
        "encounter_list": encounter_list,
        "angler_recaps": angler_recaps,
        "spc_warn": spc_warn,
        "tagdoc_warn": tagdoc_warn,
        "mls": mls,
        "nobs": nobs,
    }


def get_points_dict2(observations):
    """This is an improved get_points_dict function that takes a list of
    queryset type objects and returns a list of lat-lon points for each
    tagid.  The points are sorted in chronological order.  The results are
    returned in the form of a dictionary with tagid as the dict key.

    Arguments: - `observations`: list of queryset type objects (dicts)
    that represent observations of tagids.  Each observation must have
    the elements: tagid, date, dd_lat, dd_lon

    Returns a dictiontionary of coordinate pairs sorted by date for each tag id.

    {tag1: [lat1,lon1],[lat2,lon2], tag2: [lat1,lon1],[lat2,lon2], ....}

    """

    pass


def qs_to_tagdict(qs, tag_dict=None):
    """Arguments:

    - `qs`: a queryset-like object with the keys tagid,
      observation_date, dd_lon, and dd_lat

    - `tag_dict`: an optional dictionary the contents of qs will be
      added to.  If tag_dict is not provided, a new dictionary will be
      created.

    """
    if tag_dict is None:
        tag_dict = {}

    for pt in qs:
        # obs_point = [pt['observation_date'], (pt['dd_lon'],pt['dd_lat'])]
        if isinstance(pt.observation_date, datetime):
            obs_point = [pt.observation_date.date(), (pt.dd_lon, pt.dd_lat)]
        else:
            obs_point = [pt.observation_date, (pt.dd_lon, pt.dd_lat)]
        tagid = pt.tagid
        if pt.dd_lat and pt.dd_lon and pt.observation_date:
            if tag_dict.get(tagid):
                tag_dict[tagid].append(obs_point)
            else:
                tag_dict[tagid] = [obs_point]
    return tag_dict


def sort_tagdict(tag_dict):
    """This function takes the results of qs_to_tagdict() and returns the
    contents of each dictionary element sorted in chronological order.

    Arguments:
    - `tag_dict`:

    """

    for k, v in tag_dict.items():
        pts = tag_dict[k]
        pts.sort(key=lambda x: x[0])
        tag_dict[k] = pts
    return tag_dict


def get_points_dict(encounters, applied=None):
    """given a queryset contain encounter objects, return a dictionary of
    tagids and thier associated lat-longs.  The order of the lat-long
    should appear in chronological order that is consistent/determined
    by observation date.

    returns dictionary of the form:
    tagid: [[lat1,lon1],[lat2, lon2], ... ]

    Arguments:
    - `encounters`:

    """
    tags = []
    if applied:
        tags = [[x.tagid, x.dd_lat, x.dd_lon] for x in applied]

    # get the tag and spatial data for our encounter events and turn it
    # into a list of three element lists
    recaps = [[x.tagid, x.dd_lat, x.dd_lon] for x in encounters]

    tags.extend(recaps)

    # stack the encounters by tag id - for each tag, add each
    # additional occurence
    tag_dict = {}
    for tag in tags:
        if tag_dict.get(tag[0]):
            tag_dict[tag[0]].append(tag[1:])
        else:
            tag_dict[tag[0]] = [tag[1:]]

    return tag_dict


def get_omnr_tag_recoveries(project_slug):
    """This is a helper function used by tags_applied_project(). It uses
    raw sql to retrieve all of the subsequent OMNR recoveries of tags
    applied in a particular project.  The sql string uses a self join
    on tfat_encounter.  Only recap's with both a lat and lon and of
    the same species as the original tagging event are returned.

    Arguments:
    - `project_slug`: unique identify for project in which tags were applied

    Returns dictionary with the following elements:
    queryset - a raw sql queryset.
    Nobs - the number of records in the queryset

    """

    sql = """
    SELECT ap.prj_nm as prj_nm, ap.prj_cd as prj_cd,
    spc.common_name as common_name, recap.*
    FROM tfat_encounter recap
       JOIN
       tfat_encounter applied
         ON applied.tagid = recap.tagid
         AND applied.spc_id = recap.spc_id
       JOIN
       tfat_project AS ap ON ap.id = applied.project_id
       join tfat_species spc on spc.id=recap.spc_id
    WHERE ap.slug = %s AND
       applied.tagstat = 'A'
    AND recap.tagstat = 'C'
    AND recap.observation_date >= applied.observation_date
    ORDER BY recap.observation_date"""

    #    #using a subquery to get tagids instead of a join
    #    sql = '''
    #    SELECT * FROM tfat_encounter recap
    #    WHERE recap.tagstat='C' AND tagid IN (
    #      SELECT tagid FROM tfat_encounter applied
    #      JOIN tfat_project proj ON proj.id=applied.project_id
    #      WHERE proj.slug=%s
    #      AND tagstat='A'
    #    ) ORDER BY observation_date'''

    queryset = Encounter.objects.raw(sql, [project_slug])

    nobs = len([x.id for x in queryset])

    return {"queryset": queryset, "nobs": nobs}


def get_angler_tag_recoveries(project_slug, tagstat="A"):
    """This is a helper function used by tags_applied_project(). It uses
    raw sql to retrieve all of the non-MNR recoveries of tags applied
    in a particular project.  Only recap's with both a lat and lon and
    of the same species as the original tagging event are returned.

    Arguments:
    - `project_slug`: unique identify for project in which tags were applied

    - `tagstat`: the tag status of the tags in project identified by
      project slug.  'A' returns agler recaps of tags applied in the
      project, 'C' will return angler recaps of tags also recaptured
      by the OMNR

    Returns dictionary with the following elements:
    queryset - a raw sql queryset.
    Nobs - the number of records in the queryset


    TODO - TEST tagstat argument

    """

    sql = """
    SELECT spc.common_name as common_name,
    angler.first_name || ' ' || angler.last_name as reported_by,
    angler.id as reported_by_id,
    recovery.*
    FROM tfat_recovery recovery
    join tfat_report report on report.id=recovery.report_id
    join tfat_joepublic angler on angler.id=report.reported_by_id
    JOIN tfat_encounter encounter
        ON encounter.tagid=recovery.tagid
        AND encounter.spc_id=recovery.spc_id
    JOIN tfat_project proj ON proj.id=encounter.project_id
    join tfat_species spc on spc.id=recovery.spc_id
    WHERE encounter.tagstat='{tagstat}'
    AND proj.slug=%s
    ORDER BY recovery.recovery_date


"""
    #    sql = '''
    #    select recovery.* from tfat_recovery recovery where tagid in (
    #    select tagid from tfat_encounter encounter join tfat_project project on project.id=encounter.project_id where slug=%s and tagstat='{tagstat}'
    #    ) order by recovery_date
    #    '''

    sql = sql.format(**{"tagstat": tagstat})

    queryset = Recovery.objects.raw(sql, [project_slug])

    nobs = len([x.id for x in queryset])

    return {"queryset": queryset, "nobs": nobs}


def get_other_omnr_recoveries(project_slug):
    """This is a helper function used by tags_recovered_project(). It uses
    raw sql to retrieve all of the other MNR recoveries of tags
    recovered in a particular project.  Only recap's of the same
    species as the original tagging event are returned where tagstat
    is C on both encounters and the project code on other occurences is
    different than 'slug'.

    Arguments:
    - `project_slug`: unique identify for project in which tags were recovered

    Returns a dictionary containing a raw sql queryset and the number
    of observations in the queryeset

    """

    #    sql = """
    #    SELECT recap2.*
    #      FROM tfat_encounter recap2
    #         JOIN
    #         tfat_encounter recap1
    #           ON recap1.tagid = recap2.tagid
    #           AND recap1.spc_id = recap2.spc_id
    #         JOIN tfat_project AS prj1 ON prj1.id = recap1.project_id
    #         JOIN tfat_project AS prj2 ON prj2.id = recap2.project_id
    #      WHERE prj1.slug = %s AND
    #         recap1.tagstat = 'C'
    #      AND recap2.tagstat = 'C'
    #      and prj1.slug!=prj2.slug
    #      ORDER BY recap2.observation_date
    #
    #    """
    #

    sql = """
    SELECT prj1.prj_nm AS prj_nm,
           prj1.prj_cd AS prj_cd,
           prj1.slug AS slug,
           spc.common_name AS common_name,
           recap2.*
    FROM tfat_encounter recap2
      JOIN tfat_encounter recap1
        ON recap1.tagid = recap2.tagid
       AND recap1.spc_id = recap2.spc_id
      JOIN tfat_project AS prj1 ON prj1.id = recap1.project_id
      JOIN tfat_project AS prj2 ON prj2.id = recap2.project_id
      JOIN tfat_species AS spc ON recap1.spc_id = spc.id
    WHERE prj1.slug = %s
    AND   recap1.tagstat = 'C'
    AND   recap2.tagstat = 'C'
    AND   prj1.slug != prj2.slug
    and   recap2.observation_date >= recap1.observation_date
    ORDER BY recap2.observation_date

    """

    queryset = Encounter.objects.raw(sql, [project_slug])

    nobs = len([x.id for x in queryset])

    return {"queryset": queryset, "nobs": nobs}


def get_omnr_tag_application(project_slug):
    """This is a helper function used by tags_recovered_project(). It uses
    raw sql to retrieve all of the OMNR tag application events tags
    recovered in a particular project.  The sql string uses a self
    join on tfat_encounter.  Only encounter events with tagstat A, and
    matching tagid and spc code are returned.

    Arguments:
    - `project_slug`: unique identify for project in which tags were applied

    Returns dictionary with the following elements:
    queryset - a raw sql queryset.
    Nobs - the number of records in the queryset

    """

    sql = """
    SELECT DISTINCT
    cp.prj_nm AS prj_nm,
           cp.prj_cd AS prj_cd,
           cp.slug AS slug,
           spc.common_name AS common_name,
    applied.*
      FROM tfat_encounter applied
           JOIN tfat_encounter recap
             ON recap.tagid = applied.tagid
             AND recap.spc_id = applied.spc_id
           JOIN tfat_project AS cp
             ON cp.id = recap.project_id
           join tfat_species spc on spc.id=applied.spc_id
     WHERE cp.slug = %s AND
           recap.tagstat = 'C' AND
           applied.tagstat = 'A'
     ORDER BY applied.tagid """

    queryset = Encounter.objects.raw(sql, [project_slug])

    nobs = len([x.id for x in queryset])

    return {"queryset": queryset, "nobs": nobs}


def get_recoveries_per_year():
    """A helper function used by years_with_tag_recoveries view.  returns
    a set of nested dictionaries.  The outer dictionary is ordered and
    keyed by year.  The inner dictionaries contain the keys 'anglers'
    and 'omnr', each containing the number of tags recoverd by source
    for that year.

    """
    omnr_recaps = (
        Encounter.objects.filter(tagstat="C")
        .values_list("project__year")
        .annotate(total=Count("sam"))
        .order_by("project__year")
    )

    omnr_recap_dict = {k: v for k, v in omnr_recaps}

    # get our angler reports - use the report date if the recovery date
    # is not provided.
    angler_recoveries = Recovery.objects.exclude(
        report__report_date__isnull=True, recovery_date__isnull=True
    ).values_list("report__report_date", "recovery_date")
    # create a list that contain the year of the report:
    years = []
    for x in angler_recoveries:
        if x[1] is None:
            years.append(x[0].year)
        else:
            years.append(x[1].year)

    recovery_dict = dict()
    for yr in years:
        if recovery_dict.get(yr):
            recovery_dict[yr] += 1
        else:
            recovery_dict[yr] = 1

        # tags_recovered[yr] = dict('encounters':N, 'recoveries':N)
    tags_recovered = OrderedDict()
    yrs = list(set(recovery_dict.keys()).union(set(omnr_recap_dict.keys())))
    yrs.sort(reverse=True)
    for yr in yrs:
        omnr = omnr_recap_dict.get(yr) if omnr_recap_dict.get(yr) else 0
        anglers = recovery_dict.get(yr) if recovery_dict.get(yr) else 0
        tags_recovered[yr] = dict(omnr=omnr, anglers=anglers)

    return tags_recovered
