from django.shortcuts import (render_to_response, get_object_or_404,
                              get_list_or_404)
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import ListView
from django.template import RequestContext

from geojson import MultiLineString

from tfat.models import Species, JoePublic, Report, Recovery, Encounter, Project
from tfat.filters import JoePublicFilter

from tfat.utils import *

MAX_RECORD_CNT = 50
REPORT_PAGE_CNT = 20
ANGLER_PAGE_CNT = 50


class ListFilteredMixin(object):
    """
    Mixin that adds support for django-filter
    https://github.com/rasca/django-enhanced-cbv/blob/master/
    enhanced_cbv/views/list.py
    """

    filter_set = None

    def get_filter_set(self):
        if self.filter_set:
            return self.filter_set
        else:
            raise ImproperlyConfigured(
                "ListFilterMixin requires either a definition of "
                "'filter_set' or an implementation of 'get_filter()'")

    def get_filter_set_kwargs(self):
        """
        Returns the keyword arguments for instanciating the filterset.
        """
        return {
            'data': self.request.GET,
            'queryset': self.get_base_queryset(),
        }

    def get_base_queryset(self):
        """
        We can decided to either alter the queryset before or after applying the
        FilterSet
        """
        return super(ListFilteredMixin, self).get_queryset()

    def get_constructed_filter(self):
        # We need to store the instantiated FilterSet cause we use it in
        # get_queryset and in get_context_data
        if getattr(self, 'constructed_filter', None):
            return self.constructed_filter
        else:
            f = self.get_filter_set()(**self.get_filter_set_kwargs())
            self.constructed_filter = f
            return f

    def get_queryset(self):
        return self.get_constructed_filter().qs

    def get_context_data(self, **kwargs):
        kwargs.update({'filter': self.get_constructed_filter()})
        return super(ListFilteredMixin, self).get_context_data(**kwargs)


class RecoveryReportsListView(ListView):
    """
    """

    model = Report
    queryset = Report.objects.all().order_by('-report_date')
    paginate_by = REPORT_PAGE_CNT

report_list = RecoveryReportsListView.as_view()


class AnglerListView(ListFilteredMixin, ListView):
    model = JoePublic
    queryset = JoePublic.objects.all()
    filter_set = JoePublicFilter
    paginage_by = ANGLER_PAGE_CNT
    template_name = 'tfat/angler_list.html'
angler_list = AnglerListView.as_view()


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



def angler_reports_view(request, angler_id):
    """

    Arguments:
    - `request`:
    - `angler_id`:
    """

    angler = get_object_or_404(JoePublic, id=angler_id)
    #reports = Report.objects.filter(reported_by=angler)
    recoveries = Recovery.objects.filter(report__reported_by=angler).\
                 order_by('report__report_date')


    return render_to_response('tfat/angler_reports.html',
                              {'angler':angler, 'recoveries':recoveries},
                              context_instance=RequestContext(request))


def tagid_detail_view(request, tagid):
    """This view returns all of the omnr encounters and any angler
    returns associated with a tag id.

    If there is more than one species or tagdoc associated with this
    tag number, a warning should be issued.

    Arguments:
    - `tagid`:

    """
    encounter_list = get_list_or_404(Encounter, tagid=tagid)

    detail_data = get_tagid_detail_data(tagid, encounter_list)

    #angler_recaps = Recovery.objects.filter(tagid=tagid)
    #mls = get_multilinestring(encounter_list)

    return render_to_response('tfat/tagid_contains.html',
                              {'tagid':tagid,
                               'encounter_list':encounter_list,
                               'angler_recaps':detail_data.get('angler_recaps'),
                               'mls': detail_data.get('mls'),
                               'spc_warn': detail_data.get('spc_warn'),
                               'tagdoc_warn': detail_data.get('tagdoc_warn'),
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

    detail_data = get_tagid_detail_data(partial, encounter_list, partial=True)
    #mls = get_multilinestring([encounter_list])

    return render_to_response('tfat/tagid_contains.html',
                              {'partial':partial,
                               'encounter_list':encounter_list,
                               'angler_recaps':detail_data.get('angler_recaps'),
                               'mls': detail_data.get('mls'),
                               'spc_warn': detail_data.get('spc_warn'),
                               'tagdoc_warn': detail_data.get('tagdoc_warn'),
                               'max_record_count':MAX_RECORD_CNT
                           }, context_instance=RequestContext(request))


def tags_applied_project(request, slug):
    '''A view to show the of all tags applied in a particular
    project and their assoiciated recoveries

    Required data elements:

    - tags applied in this project
    - subsequent recoveries of those tags:
      + in other UGLMU Projects
      + in recaptured by anglers/non-mnr sources
    - mls line connecting encounters with the same tagid

    Only recaptures of the same species will be included - no warning
    is issued if multiple tagdocs are returned - this is only relevant
    on an individual tag id basis (there could very well be more than
    one tagdoc deployed and subsequently recovered in a project)

    '''
    project = Project.objects.get(slug=slug)

    applied = Encounter.objects.filter(tagstat='A', project=project)
    recovered = get_omnr_tag_recoveries(slug)
    angler_recaps = get_angler_tag_recoveries(slug)

    mls = get_multilinestring([applied, recovered.get('queryset'),
                               angler_recaps.get('queryset')])

    return render_to_response('tfat/project_applied_tags.html',
                              {'project':project,
                               'applied':applied,
                               'recovered':recovered,
                               'angler_recaps':angler_recaps,
                               'mls':mls,
                           }, context_instance=RequestContext(request))



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
    SELECT recap.*
    FROM tfat_encounter recap
       JOIN
       tfat_encounter applied
         ON applied.tagid = recap.tagid
         AND applied.spc_id = recap.spc_id
       JOIN
       tfat_project AS ap ON ap.id = applied.project_id
    WHERE ap.slug = %s AND
       applied.tagstat = 'A'
    AND recap.tagstat = 'C'
    AND recap.dd_lat is not null
    AND recap.dd_lon is not null
    ORDER BY recap.observation_date"""

    queryset = Encounter.objects.raw(sql,[project_slug])

    nobs = len([x.id for x in queryset])

    return { 'queryset':queryset, 'nobs':nobs }



def get_angler_tag_recoveries(project_slug):
    """This is a helper function used by tags_applied_project(). It uses
    raw sql to retrieve all of the non-MNR recoveries of tags applied
    in a particular project.  Only recap's with both a lat and lon and
    of the same species as the original tagging event are returned.

    Arguments:
    - `project_slug`: unique identify for project in which tags were applied

    Returns a raw sql queryset.

    """


    sql = """
    SELECT recovery.*
    FROM tfat_recovery recovery
    JOIN tfat_encounter encounter
        ON encounter.tagid=recovery.tagid
        AND encounter.spc_id=recovery.spc_id
    JOIN tfat_project proj ON proj.id=encounter.project_id
    WHERE encounter.tagstat='A'
    -- AND recovery.dd_lat is not null
    -- AND recovery.dd_lon is not null
    AND proj.slug=%s
    ORDER BY recovery.recovery_date
    """

    queryset = Recovery.objects.raw(sql,[project_slug])

    nobs = len([x.id for x in queryset])

    return { 'queryset':queryset, 'nobs':nobs }



def tags_recovered_project(request, slug):
    '''A view to show the where recoveries in a particular project originated'''

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

    mls = get_multilinestring([recovered,applied])

    return render_to_response('tfat/project_recovered_tags.html',
                              {'project':project,
                               'recovered':recovered,
                               'applied':applied,
                               'applied_bool':applied_bool,
                               'applied_cnt':applied_cnt,
                               'mls':mls
                           }, context_instance=RequestContext(request))
