from django.shortcuts import (render_to_response, get_object_or_404,
                              get_list_or_404)
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import ListView
from django.template import RequestContext

from geojson import MultiLineString

from tfat.models import Species, JoePublic, Report, Recovery, Encounter, Project
from tfat.filters import JoePublicFilter
from tfat.forms import JoePublicForm, CreateJoePublicForm

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

    return render_to_response('tfat/tagid_contains.html',
                              {'tagid':tagid,
                               'encounter_list':encounter_list,
                               'angler_recaps':detail_data.get('angler_recaps'),
                               'mls': detail_data.get('mls'),
                               'spc_warn': detail_data.get('spc_warn'),
                               'tagdoc_warn': detail_data.get('tagdoc_warn'),
                               'max_record_count':MAX_RECORD_CNT,
                               'nobs':detail_data.get('nobs',0),
                           }, context_instance=RequestContext(request))



def tagid_quicksearch_view(request):
    '''This is a super quick view - if it is called, get the value of q
    and redirect to tagid_contains passing the value of q as a parameter.'''

    partial = request.GET.get('q')
    return redirect('tagid_contains', partial=partial)



def tagid_contains_view(request, partial):
    """
    This view returns all of the omnr encounters and any angler
    returns associated with tagid that contain <partial>
    partial '123' will return tags '1234' and '5123'.

    If there is more than one species or tagdoc associated with this
    tag number, a warning should be issued.

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
                               'max_record_count':MAX_RECORD_CNT,
                               'nobs':detail_data.get('nobs',0),
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
    angler_recaps = get_angler_tag_recoveries(slug, 'A')

    mls = get_multilinestring([applied, recovered.get('queryset'),
                               angler_recaps.get('queryset')])

    return render_to_response('tfat/project_applied_tags.html',
                              {'project':project,
                               'applied':applied,
                               'recovered':recovered,
                               'angler_recaps':angler_recaps,
                               'mls':mls,
                           }, context_instance=RequestContext(request))



def tags_recovered_project(request, slug):
    '''A view to show the where recoveries in a particular project originated

    Required data elements:

    - tags recovered in this project
    - application events (ie. - OMNR encounters were tagstat=A)
    - subsequent recoveries of those tags:
      + in other UGLMU Projects (tagstat=C, id different that this event)
      + in recaptured by anglers/non-mnr sources
    - mls line connecting encounters with the same tagid

    Only recaptures/application events of the same species will be
    included - no warning is issued if multiple tagdocs are returned -
    this is only relevant on an individual tag id basis (there could
    very well be more than one tagdoc deployed and subsequently
    recovered in a project)

    '''

    project = Project.objects.get(slug=slug)

    recovered = Encounter.objects.filter(tagstat='C', project=project)

    applied = get_omnr_tag_application(slug)
    other_recoveries = get_other_omnr_recoveries(slug)
    angler_recaps = get_angler_tag_recoveries(slug, tagstat='C')

    mls = get_multilinestring([applied.get('queryset'), recovered,
                               other_recoveries.get('queryset'),
                               angler_recaps.get('queryset')])

    return render_to_response('tfat/project_recovered_tags.html',
                              {'project':project,
                               'recovered':recovered,
                               'other_recoveries':other_recoveries,
                               'angler_recaps':angler_recaps,
                               'applied':applied,
                               'mls':mls
                           }, context_instance=RequestContext(request))



def update_angler(request, angler_id):
    """This view is used to update or edit an existing tag reporter / angler.

    """
    angler = get_object_or_404(JoePublic, id=angler_id)
    form = JoePublicForm(request.POST or None, instance = angler)

    if form.is_valid():
        form.save()
        return redirect('angler_reports', angler_id=angler.id)
    else:
        return render(request, 'tfat/angler_form.html', {'form': form,
                                                         'action':'Edit '})

def create_angler(request):
    """This view is used to create a new tag reporter / angler.

    when we create a new angler, we do not want to duplicate entries
    with the same first name and last name by default.  If there
    already angers with the same first and last name, add them to the
    reponse we will return with the form and ask the user to confirm
    that this new user really does have the same name as and existing
    (but different) angler.

    """

    if request.method == 'POST':
        form = CreateJoePublicForm(request.POST)
        if form.is_valid():
            angler = form.save()
            return redirect('angler_reports', angler_id=angler.id)
        else:
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            anglers = JoePublic.objects.filter(first_name__iexact=first_name,
                                           last_name__iexact=last_name).all()
            if len(anglers):
                return render(request, 'tfat/angler_form.html',
                              {'form': form, 'anglers':anglers,
                               'action':'Create New '})
    else:
        form = CreateJoePublicForm()

    return render(request, 'tfat/angler_form.html', {'form': form,
                                                     'action':'Create New '})
