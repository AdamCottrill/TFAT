from django.shortcuts import (render_to_response, get_object_or_404,
                              get_list_or_404)
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import ListView
from django.template import RequestContext

from geojson import MultiLineString

from tfat.models import Species, JoePublic, Report, Recovery, Encounter, Project


MAX_RECORD_CNT = 50



class JoePublicListView(ListView):
    model = JoePublic

class SpeciesListView(ListView):
    model = Species

class ReportListView(ListView):
    model = Report

class RecoveryListView(ListView):
    model = Recovery

class EncounterListView(ListView):
    model = Encounter

class ProjectTagsAppliedListView(ListView):
    model = Project
    template_name = 'tfat/project_applied_list.html'

    def get_queryset(self):
        "projects that re-captured at least one tag"
        projects = Project.objects.filter(Encounters__tagid__isnull=False,
                                          Encounters__tagstat='A').distinct()
        return projects


class ProjectTagsRecoveredListView(ListView):
    model = Project
    template_name = 'tfat/project_recovered_list.html'

    def get_queryset(self):
        "projects that re-captured at least one tag"
        projects = Project.objects.filter(Encounters__tagid__isnull=False,
                                          Encounters__tagstat='C').distinct()
        return projects




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


def tagid_detail_view(request, tagid):
    """

    Arguments:
    - `tagid`:
    """
    encounter_list = get_list_or_404(Encounter, tagid=tagid)

    mls = get_multilinestring(encounter_list)

    return render_to_response('tfat/tagid_contains.html',
                              {'tagid':tagid,
                               'encounter_list':encounter_list,
                               'mls': mls,
                               'max_record_count':MAX_RECORD_CNT
                           }, context_instance=RequestContext(request))


def tagid_quicksearch_view(request):
    partial = request.GET.get('q')
    return redirect('tagid_contains', partial=partial)

def tagid_contains_view(request, partial):
    """

    Arguments:
    - `tagid`:
    """
    encounter_list = Encounter.objects.filter(tagid__icontains=partial)

    if not encounter_list:
        raise Http404
    else:
        encouter_list = encounter_list.order_by('tagid',
                                                'tagstat')[:MAX_RECORD_CNT]
    mls = get_multilinestring(encounter_list)

    return render_to_response('tfat/tagid_contains.html',
                              {'partial':partial,
                               'encounter_list':encounter_list,
                               'mls':mls,
                               'max_record_count':MAX_RECORD_CNT
                           }, context_instance=RequestContext(request))


def tags_applied_project(request, slug):
    '''A view to show the of all tags applied in a particular
    project and their assoiciated recoveries'''
    project = Project.objects.get(slug=slug)

    #getting the tags that were applied is easy enough
    applied = Encounter.objects.filter(tagstat='A', project=project)
    #tagids = [x.tagid for x in applied]
    #recovered = Encounter.objects.filter(tagstat='C', tagid__in=tagids)

    #getting their associated recoveries requires a semi-complicated
    #self join (which means we need to use raw sql)

    sql = """
    SELECT recap.*
    FROM tfat_encounter recap
       JOIN
       tfat_encounter applied ON applied.tagid = recap.tagid
       JOIN
       tfat_project AS ap ON ap.id = applied.project_id
    WHERE ap.slug = %s AND
       applied.tagstat = 'A' AND
       recap.tagstat = 'C'
    ORDER BY recap.tagid"""

    recovered = Encounter.objects.raw(sql,[slug])
    #import pdb;pdb.set_trace()

    try:
        recaps_bool = recovered[0]
    except IndexError as err:
        recaps_bool = False

    if recaps_bool:
        recap_cnt = len([x.id for x in recovered])
    else:
        recap_cnt = 0

    mls = get_multilinestring(recovered,applied)

    return render_to_response('tfat/project_applied_tags.html',
                              {'project':project,
                               'applied':applied,
                               'recovered':recovered,
                               'recaps_bool': recaps_bool,
                               'recap_cnt':recap_cnt,
                               'mls':mls
                           }, context_instance=RequestContext(request))



def tags_recovered_project(request, slug):
    '''A view to show the where recoveries in a particular project originated
    project'''

    project = Project.objects.get(slug=slug)

    recovered = Encounter.objects.filter(tagstat='C', project=project)
    #tagids = [x.tagid for x in recovered]
    #applied = Encounter.objects.filter(tagstat='A', tagid__in=tagids)

    #again - getting the original tagging information for our
    #recaptures is too complicated for the django orm and requires
    #that we us raw sql:

    sql = """
    SELECT applied.*
      FROM tfat_encounter applied
           JOIN
           tfat_encounter recap ON recap.tagid = applied.tagid
           JOIN
           tfat_project AS cp ON cp.id = recap.project_id
     WHERE cp.slug = %s AND
           recap.tagstat = 'C' AND
           applied.tagstat = 'A'
     ORDER BY applied.tagid """


    applied = Encounter.objects.raw(sql,[slug])
    try:
        applied_bool = applied[0]
    except IndexError as err:
        applied_bool = False

    if applied_bool:
        applied_cnt = len([x.id for x in applied])
    else:
        applied_cnt = 0

    mls = get_multilinestring(recovered,applied)

    return render_to_response('tfat/project_recovered_tags.html',
                              {'project':project,
                               'recovered':recovered,
                               'applied':applied,
                               'applied_bool':applied_bool,
                               'applied_cnt':applied_cnt,
                               'mls':mls
                           }, context_instance=RequestContext(request))
