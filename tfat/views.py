from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.http import Http404, HttpResponse
from django.shortcuts import (render_to_response, get_object_or_404,
                              get_list_or_404)
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import ListView

import os
import mimetypes

from geojson import MultiLineString


from tfat.constants import CLIP_CODE_CHOICES
from tfat.models import Species, JoePublic, Report, Recovery, Encounter, Project
from tfat.filters import JoePublicFilter
from tfat.forms import (JoePublicForm, CreateJoePublicForm, ReportForm,
                        RecoveryForm)

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
        projects = Project.objects.filter(Encounters__tagid_isnull=False,
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
    """Display all of the reports associated with an angler.  Returns
    recoveries to template, which are then grouped by report in template.

    Arguments:
    - `request`:
    - `angler_id`:

    """

    angler = get_object_or_404(JoePublic, id=angler_id)

    recoveries = Recovery.objects.filter(report__reported_by=angler).\
                 order_by('report__report_date')

    #the subset of recovery events with both lat and lon (used for plotting)
    recoveries_with_latlon = [x for x in recoveries if x.dd_lat and x.dd_lon]

    return render_to_response('tfat/angler_reports.html',
                              {'angler':angler,
                               'recoveries_with_latlon':recoveries_with_latlon,
                               'recoveries':recoveries},
                              context_instance=RequestContext(request))

def tagid_detail_view(request, tagid):
    """This view returns all of the omnr encounters and any angler
    returns associated with a tag id.

    If there is more than one species or tagdoc associated with this
    tag number, a warning should be issued.

    Arguments:
    - `tagid`:

    """
    #encounter_list = get_list_or_404(Encounter, tagid=tagid)
    encounter_list = Encounter.objects.filter(tagid=tagid).all()

    detail_data = get_tagid_detail_data(tagid, encounter_list)

    return render_to_response('tfat/tagid_details.html',
                              {'tagid':tagid,
                               'encounter_list':encounter_list,
                               'angler_recaps':detail_data.get('angler_recaps'),
                               'mls': detail_data.get('mls'),
                               'spc_warn': detail_data.get('spc_warn'),
                               'tagdoc_warn': detail_data.get('tagdoc_warn'),
                               'max_record_count':MAX_RECORD_CNT,
                               'nobs':detail_data.get('nobs',0),
                           }, context_instance=RequestContext(request))



def report_detail_view(request, report_id):
    """This view returns the detailed information and a summary of tags
    associated with a particular report.

    Arguments:
    - `report_id`:

    """
    report = get_object_or_404(Report, id=report_id)
    #angler = report.reported_by

    return render_to_response('tfat/report_detail.html',
                              {'report':report,
                               #'angler':angler
                           },
                              context_instance=RequestContext(request))


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



def create_report(request, angler_id):
    """This view is used to create a new tag report.
    """

    angler = get_object_or_404(JoePublic, id=angler_id)

    if request.method == 'POST' and angler:
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.associated_file = request.FILES.get('associated_file')
            report.reported_by = angler
            report.save()
            #redirect to report details:
            return redirect('report_detail', report_id=report.id)
    else:
        form = ReportForm(initial={'reported_by':angler})

    return render(request, 'tfat/report_form.html', {'form': form,
                                                     'angler':angler,
                                                     'action': 'Create',})


def edit_report(request, report_id):
    """This view is used to edit an existing tag report.
    """

    report = get_object_or_404(Report, id=report_id)
    angler = report.reported_by
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            #report.associated_file = request.FILES.get('associated_file')
            report.reported_by = angler
            report.save()
            #redirect to report details:
            return redirect('report_detail', report_id=report.id)
    else:
        form = ReportForm(instance=report)

    return render(request, 'tfat/report_form.html', {'form': form,
                                                     'angler':angler,
                                                     'action': 'Edit'})


def create_recovery(request, report_id):
    """This view is used to create a new tag recovery.
    """

    clip_codes = sorted(list(CLIP_CODE_CHOICES), key=lambda x:x[0])
    tag_types = sorted(list(TAG_TYPE_CHOICES), key=lambda x:x[0])
    tag_origin = sorted(list(TAG_ORIGIN_CHOICES), key=lambda x:x[0])
    tag_colours = sorted(list(TAG_COLOUR_CHOICES), key=lambda x:x[0])
    tag_position = sorted(list(TAG_POSITION_CHOICES), key=lambda x:x[0])

    report = get_object_or_404(Report, id=report_id)
    form = RecoveryForm(report_id=report.id, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            recovery = form.save(report=report)
            return redirect('recovery_detail', recovery_id=recovery.id)
    return render(request, 'tfat/recovery_form.html', {'form': form,
                                                       'clip_codes':clip_codes,
                                                       'tag_types':tag_types,
                                                       'tag_origin':tag_origin,
                                                       'tag_colours':tag_colours,
                                                       'tag_position':tag_position,})


def edit_recovery(request, recovery_id):
    """This view is used to edit/update existing tag recoveries.
    """

    clip_codes = sorted(list(CLIP_CODE_CHOICES), key=lambda x:x[0])
    tag_types = sorted(list(TAG_TYPE_CHOICES), key=lambda x:x[0])
    tag_origin = sorted(list(TAG_ORIGIN_CHOICES), key=lambda x:x[0])
    tag_colours = sorted(list(TAG_COLOUR_CHOICES), key=lambda x:x[0])
    tag_position = sorted(list(TAG_POSITION_CHOICES), key=lambda x:x[0])

    recovery = get_object_or_404(Recovery, id=recovery_id)
    report = recovery.report

    form = RecoveryForm(report_id=report.id,
                        instance=recovery, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            recovery = form.save(report)
            return redirect('recovery_detail', recovery_id=recovery.id)
    return render(request, 'tfat/recovery_form.html', {'form': form,
                                                       'clip_codes':clip_codes,
                                                       'tag_types':tag_types,
                                                       'tag_origin':tag_origin,
                                                       'tag_colours':tag_colours,
                                                       'tag_position':tag_position,})



def recovery_detail_view(request, recovery_id):
    """This view returns the detailed information about a recovery event.

    Arguments:
    - `recovery_id`:

    """
    recovery = get_object_or_404(Recovery, id=recovery_id)

    return render_to_response('tfat/recovery_detail.html',
                              {'recovery':recovery,},
                              context_instance=RequestContext(request))



def serve_file(request, filename):
    '''from:http://stackoverflow.com/questions/2464888/
    downloading-a-csv-file-in-django?rq=1

    This function is my first attempt at a function used to
    serve/download files.  It works for basic text files, but seems to
    corrupt pdf and ppt files (maybe other binaries too).  It also
    should be updated to include some error trapping just incase the
    file doesn t actully exist.
    '''

    fname = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.isfile(fname):

        content_type = mimetypes.guess_type(filename)[0]

        filename = os.path.split(filename)[-1]
        #wrapper = FileWrapper(file(fname, 'rb'))
        wrapper = FileWrapper(open(fname, 'rb'))
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Disposition'] = (
            'attachment; filename=%s' % os.path.basename(fname))
        response['Content-Length'] = os.path.getsize(fname)

        return response
    else:
        return render_to_response('pjtk2/MissingFile.html',
                                  { 'filename': filename},
                                  context_instance=RequestContext(request))
