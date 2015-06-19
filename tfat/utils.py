'''
=============================================================
c:/1work/Python/djcode/tfat/tfat/utils.py
Created: 19 Jun 2015 14:54:14


DESCRIPTION:



A. Cottrill
=============================================================
'''

from geojson import MultiLineString
from tfat.models import *


def connect_the_dots(encounters):
    """given a list of tag encounters, convert the point observations to
    poly-lines.  If there is only one pt, return None, otherwise connect
    the dots by copying the points and offseting by 1, producing N-1 line
    segments.

    Arguments: - `encounters`: a list of point observations of the
    form [[lat1,lon1],[lat2, lon2], ... ]

    """

    if len(encounters)>1:
        pts = [(x[1], x[0]) for x in encounters]
        A = pts[:-1]
        B = pts[1:]

        coords = list(zip(A,B))
        return coords
    else:
        return None



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

    #get the tag and spatial data for our encounter events and turn it
    #into a list of three element lists
    recaps = [[x.tagid, x.dd_lat, x.dd_lon] for x in encounters]

    tags.extend(recaps)

    #stack the encounters by tag id - for each tag, add each
    #additional occurence
    tag_dict = {}
    for tag in tags:
        if tag_dict.get(tag[0]):
            tag_dict[tag[0]].append(tag[1:])
        else:
            tag_dict[tag[0]] = [tag[1:]]

    return tag_dict


def get_multilinestring(encounters, applied=None):
    """given a list of tag encounters, extract the spatial data,
    'normalize' multiple obserations, and return a geojson
    MULTILINESTRING string that can be plotted by leaflet.

    Arguments:
    - `encounters`:

    """
    tag_paths = {}
    #extract the spatial data
    pts_dict = get_points_dict(encounters, applied)
    for tag,pts in pts_dict.items():
        tag_paths[tag] = connect_the_dots(pts)

    #create a line string for each tag number
    mls = []
    for k,v in tag_paths.items():
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
    ret = False if len(set(spc_list))==1 else True
    return ret


def tagdoc_warning(qs_list):
    """Return true if the list in qs_list have more than one tagdoc.

    Arguments:
    - `qs_list`:
    """
    tagdoc_list = []
    for qs in qs_list:
        tagdoc_list.extend([x.tagdoc for x in qs])
    ret = False if len(set(tagdoc_list))==1 else True
    return ret




def get_tagid_detail_data(tagid, encounter_list):
    """A helper view to compile all of the information needed to render
    the tagid detial page.  These elements include:

    + OMNR Encounters (tag application and any recoveries)
    + Angler recaptures

    + multi-linestring representing the path of tag recoveries in
      chronological order

    + warnings if spc or tagid associated with a tag are not consistent

    Arguments: - `tagid`:

    """

    angler_recaps = Recovery.objects.filter(tagid=tagid)

    spc_warn = spc_warning([encounter_list, angler_recaps])
    tagdoc_warn = tagdoc_warning([encounter_list, angler_recaps])

    mls = get_multilinestring(encounter_list)

    return {'encounter_list': encounter_list,
            'angler_recaps':angler_recaps,
            'spc_warn':spc_warn, 'tagdoc_warn':tagdoc_warn,
            'mls':mls}
