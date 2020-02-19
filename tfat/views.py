from django.conf import settings

# from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper
from django.db.models import Q, Count
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import ListView


from django.contrib import messages

import os
import mimetypes
import subprocess
from datetime import datetime


from geojson import MultiLineString

from tfat.constants import CLIP_CODE_CHOICES
from tfat.models import Species, JoePublic, Report, Recovery, Encounter, Project
from tfat.filters import JoePublicFilter
from tfat.forms import JoePublicForm, CreateJoePublicForm, ReportForm, RecoveryForm

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
                "'filter_set' or an implementation of 'get_filter()'"
            )

    def get_filter_set_kwargs(self):
        """
        Returns the keyword arguments for instanciating the filterset.
        """
        return {"data": self.request.GET, "queryset": self.get_base_queryset()}

    def get_base_queryset(self):
        """
        We can decided to either alter the queryset before or after applying the
        FilterSet
        """
        return super(ListFilteredMixin, self).get_queryset()

    def get_constructed_filter(self):
        # We need to store the instantiated FilterSet cause we use it in
        # get_queryset and in get_context_data
        if getattr(self, "constructed_filter", None):
            return self.constructed_filter
        else:
            f = self.get_filter_set()(**self.get_filter_set_kwargs())
            self.constructed_filter = f
            return f

    def get_queryset(self):
        return self.get_constructed_filter().qs

    def get_context_data(self, **kwargs):
        kwargs.update({"filter": self.get_constructed_filter()})
        return super(ListFilteredMixin, self).get_context_data(**kwargs)


class RecoveryReportsListView(ListView):
    """
    """

    model = Report
    queryset = Report.objects.all().order_by("-report_date")
    paginate_by = REPORT_PAGE_CNT


report_list = RecoveryReportsListView.as_view()


class AnglerListView(ListFilteredMixin, ListView):
    """A generic list view of all anglers in our database.  If the view is
    called with an optional report at tag option, instructions will be
    included in the response.
    """

    model = JoePublic
    queryset = (
        JoePublic.objects.order_by("last_name", "first_name")
        .annotate(reports=Count("Reported_By", distinct=True))
        .annotate(tags=Count("Reported_By__Report"))
    )

    filter_set = JoePublicFilter
    paginage_by = ANGLER_PAGE_CNT
    template_name = "tfat/angler_list.html"
    extra_context = {}

    def get_context_data(self, *args, **kwargs):
        context = super(AnglerListView, self).get_context_data(*args, **kwargs)
        context.update(self.extra_context)
        return context


angler_list = AnglerListView.as_view()
report_a_tag_angler_list = AnglerListView.as_view(extra_context={"report_a_tag": True})


class SpeciesListView(ListView):
    model = Species


class ReportListView(ListView):
    model = Report


class RecoveryListView(ListView):
    model = Recovery


class SpatialFollowupListView(ListView):
    model = Recovery
    queryset = (
        Recovery.objects.filter(spatial_followup=True)
        .order_by("-report__report_date")
        .all()
    )
    paginage_by = MAX_RECORD_CNT
    template_name = "tfat/spatial_followup_list.html"


spatial_followup = SpatialFollowupListView.as_view()


class EncounterListView(ListView):
    model = Encounter


def encounter_detail_view(request, encounter_id):
    """This view returns the detailed information about an mnr encounter
    event (i.e. - a 125 record in one of our master databases).

    Arguments:
    - `recovery_id`:

    """
    encounter = get_object_or_404(Encounter, id=encounter_id)

    return render(request, "tfat/encounter_detail.html", {"encounter": encounter})


class ProjectTagsAppliedListView(ListView):
    model = Project
    template_name = "tfat/project_applied_list.html"

    def get_queryset(self):
        "projects that re-captured at least one tag"
        projects = (
            Project.objects.filter(
                Q(Encounters__tagid__isnull=False),
                Q(Encounters__tagstat="A") | Q(Encounters__tagstat="A2"),
            )
            .distinct()
            .annotate(tags=Count("Encounters__tagid"))
        )
        return projects


class ProjectTagsRecoveredListView(ListView):

    model = Project
    template_name = "tfat/project_recovered_list.html"

    def get_queryset(self):
        "projects that re-captured at least one tag"
        projects = (
            Project.objects.filter(
                Encounters__tagid__isnull=False, Encounters__tagstat="C"
            )
            .distinct()
            .annotate(tags=Count("Encounters__tagid"))
        )
        return projects


def years_with_tags_applied_view(request):
    """Render a list of years in which tags were applied.  The list of
    years should be in descending order and include the number of tags
    applied

    """

    tags_applied = (
        Encounter.objects.filter(Q(tagstat="A") | Q(tagstat="A2"))
        .values_list("project__year")
        .annotate(total=Count("sam"))
        .order_by("-project__year")
    )

    tags_applied_dict = OrderedDict()

    for yr, total in tags_applied:
        tags_applied_dict[yr] = total

    return render(
        request,
        "tfat/years_with_tags_applied.html",
        {"tags_applied": tags_applied_dict},
    )


def years_with_tags_recovered_view(request):
    """Render a list of years in which tags were recovered either by OMNR
    or outside agency.  The list of years should be in descending
    order and include the number of tags recovered by the OMNR and the
    number recovered by the general public or other agencies.
    """

    # calculate the number of recoveries per year:

    tags_recovered = get_recoveries_per_year()

    return render(
        request,
        "tfat/years_with_tags_recovered.html",
        {"tags_recovered": tags_recovered},
    )


def angler_reports_view(request, angler_id, report_a_tag=False):
    """Display all of the reports associated with an angler.  Returns
    recoveries to template, which are then grouped by report in template.

    report_a_tag is used to include additional information in the
    rendered template.

    Arguments:
    - `request`:
    - `angler_id`:

    """

    angler = get_object_or_404(JoePublic, id=angler_id)

    recoveries = (
        Recovery.objects.filter(report__reported_by=angler)
        .order_by("-report__report_date")
        .select_related("report", "spc")
    )

    # the subset of recovery events with both lat and lon (used for plotting)
    recoveries_with_latlon = [x for x in recoveries if x.dd_lat and x.dd_lon]

    return render(
        request,
        "tfat/angler_reports.html",
        {
            "angler": angler,
            "recoveries_with_latlon": recoveries_with_latlon,
            "recoveries": recoveries,
            "report_a_tag": report_a_tag,
        },
    )


def tagid_detail_view(request, tagid):
    """This view returns all of the omnr encounters and any angler
    returns associated with a tag id.

    If there is more than one species or tagdoc associated with this
    tag number, a warning should be issued.

    Arguments:
    - `tagid`:

    """
    # encounter_list = get_list_or_404(Encounter, tagid=tagid)
    encounter_list = (
        Encounter.objects.filter(tagid=tagid)
        .select_related(
            "project",
            "spc"
            #            "project__prj_cd", "project__prj_nm", "project__slug", "spc__common_name"
        )
        .all()
    )

    detail_data = get_tagid_detail_data(tagid, encounter_list)

    return render(
        request,
        "tfat/tagid_details.html",
        {
            "tagid": tagid,
            "encounter_list": encounter_list,
            "angler_recaps": detail_data.get("angler_recaps"),
            "mls": detail_data.get("mls"),
            "spc_warn": detail_data.get("spc_warn"),
            "tagdoc_warn": detail_data.get("tagdoc_warn"),
            "max_record_count": MAX_RECORD_CNT,
            "nobs": detail_data.get("nobs", 0),
        },
    )


def report_detail_view(request, report_id, report_a_tag=False):
    """This view returns the detailed information and a summary of tags
    associated with a particular report.

    Arguments:
    - `report_id`:

    """
    report = get_object_or_404(Report, id=report_id)
    # angler = report.reported_by

    return render(
        request,
        "tfat/report_detail.html",
        {
            "report": report,
            "report_a_tag": report_a_tag
            #'angler':angler
        },
    )


def tagid_quicksearch_view(request):
    """This is a super quick view - if it is called, get the value of q
    and redirect to tagid_contains passing the value of q as a parameter."""

    partial = request.GET.get("q")
    return redirect("tfat:tagid_contains", partial=partial)


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

    if encounter_list:
        encouter_list = encounter_list.order_by("tagid", "tagstat")[:MAX_RECORD_CNT]

    detail_data = get_tagid_detail_data(partial, encounter_list, partial=True)

    return render(
        request,
        "tfat/tagid_contains.html",
        {
            "partial": partial,
            "encounter_list": encounter_list,
            "angler_recaps": detail_data.get("angler_recaps"),
            "mls": detail_data.get("mls"),
            "spc_warn": detail_data.get("spc_warn"),
            "tagdoc_warn": detail_data.get("tagdoc_warn"),
            "max_record_count": MAX_RECORD_CNT,
            "nobs": detail_data.get("nobs", 0),
        },
    )


def tags_recovered_year(request, year, this_year=False):
    """A view to show the where recoveries in a particular year originated

    Required data elements:

    - tags recovered in this year
    - application events (ie. - OMNR encounters were tagstat=A)
    - subsequent recoveries of those tags:
      + in other UGLMU Years (tagstat=C, id different that this event)
      + in recaptured by anglers/non-mnr sources
    - mls line connecting encounters with the same tagid

    Only recaptures/application events of the same species will be
    included - no warning is issued if multiple tagdocs are returned -
    this is only relevant on an individual tag id basis (there could
    very well be more than one tagdoc deployed and subsequently
    recovered in a year)

    """

    encounter_list = Encounter.objects.filter(tagstat="C", project__year=year)

    encounter_list = encounter_list.select_related(
        "project",
        "spc"
        # "project__prj_cd", "project__prj_nm", "project__slug", "spc__common_name"
    )

    # applied = get_omnr_tag_application(slug)
    # other_recoveries = get_other_omnr_recoveries(slug)

    angler_recaps = Recovery.objects.filter(recovery_date__year=year).select_related(
        # "report__reported_by", "spc__common_name"
        "report",
        "spc",
    )

    # mls = get_multilinestring([applied.get('queryset'), recovered,
    #                           other_recoveries.get('queryset'),
    #                           angler_recaps.get('queryset')])

    return render(
        request,
        "tfat/year_recovered_tags.html",
        {
            "year": year,
            "encounter_list": encounter_list,
            #'other_recoveries':other_recoveries,
            "angler_recaps": angler_recaps,
            #'applied':applied,
            #'mls':mls
            "this_year": this_year,
        },
    )


def tags_recovered_this_year(request):
    """Pass the current year into the tags recovered view.  THis will
    be the TFAT home page.  """

    this_year = datetime.now().year

    return tags_recovered_year(request, this_year, this_year=True)


def tags_applied_year(request, year):
    """A view to show the of all tags applied in a particular
    year and their assoiciated recoveries

    Required data elements:

    - tags applied in this year
    - subsequent recoveries of those tags:
      + in other UGLMU Years
      + in recaptured by anglers/non-mnr sources
    - mls line connecting encounters with the same tagid

    Only recaptures of the same species will be included - no warning
    is issued if multiple tagdocs are returned - this is only relevant
    on an individual tag id basis (there could very well be more than
    one tagdoc deployed and subsequently recovered in a year)

    """

    applied = Encounter.objects.filter(
        Q(tagstat="A") | Q(tagstat="A2"), project__year=year
    )

    applied = applied.select_related(
        "project",
        "spc",
        # "project__prj_cd", "project__prj_nm", "spc__common_name"
    )

    # recovered = get_omnr_tag_recoveries(slug)
    # angler_recaps = get_angler_tag_recoveries(slug, 'A')

    # mls = get_multilinestring([applied, recovered.get('queryset'),
    #                           angler_recaps.get('queryset')])

    return render(
        request,
        "tfat/year_applied_tags.html",
        {
            "year": year,
            "applied": applied,
            #'recovered':recovered,
            #'angler_recaps':angler_recaps,
            #'mls':mls,
        },
    )


def tags_applied_project(request, slug):
    """A view to show the of all tags applied in a particular
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

    """
    project = Project.objects.get(slug=slug)
    applied = Encounter.objects.filter(
        Q(tagstat="A") | Q(tagstat="A2"), Q(project=project)
    )

    applied = applied.select_related(
        "project",
        "spc"
        # "project__prj_cd", "project__prj_nm", "spc__common_name"
    )

    recovered = get_omnr_tag_recoveries(slug)
    angler_recaps = get_angler_tag_recoveries(slug, "A")

    mls = get_multilinestring(
        [applied, recovered.get("queryset"), angler_recaps.get("queryset")]
    )

    return render(
        request,
        "tfat/project_applied_tags.html",
        {
            "project": project,
            "applied": applied,
            "recovered": recovered,
            "angler_recaps": angler_recaps,
            "mls": mls,
        },
    )


def tags_recovered_project(request, slug):
    """A view to show the where recoveries in a particular project originated

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

    """

    project = Project.objects.get(slug=slug)

    recovered = Encounter.objects.filter(tagstat="C", project=project)

    recovered = recovered.select_related
    (
        "project",
        "spc"
        # "project__prj_cd", "project__prj_nm", "spc__common_name"
    )

    applied = get_omnr_tag_application(slug)
    other_recoveries = get_other_omnr_recoveries(slug)

    angler_recaps = get_angler_tag_recoveries(slug, tagstat="C")

    mls = get_multilinestring(
        [
            applied.get("queryset"),
            recovered,
            other_recoveries.get("queryset"),
            angler_recaps.get("queryset"),
        ]
    )

    return render(
        request,
        "tfat/project_recovered_tags.html",
        {
            "project": project,
            "recovered": recovered,
            "other_recoveries": other_recoveries,
            "angler_recaps": angler_recaps,
            "applied": applied,
            "mls": mls,
        },
    )


def update_angler(request, angler_id):
    """This view is used to update or edit an existing tag reporter / angler.

    """
    angler = get_object_or_404(JoePublic, id=angler_id)
    form = JoePublicForm(request.POST or None, instance=angler)

    if form.is_valid():
        form.save()
        return redirect("tfat:angler_reports", angler_id=angler.id)
    else:
        return render(
            request, "tfat/angler_form.html", {"form": form, "action": "Edit "}
        )


def create_angler(request, report_a_tag=False):
    """This view is used to create a new tag reporter / angler.

    when we create a new angler, we do not want to duplicate entries
    with the same first name and last name by default.  If there
    already angers with the same first and last name, add them to the
    reponse we will return with the form and ask the user to confirm
    that this new user really does have the same name as and existing
    (but different) angler.

    """

    if request.method == "POST":
        form = CreateJoePublicForm(request.POST)
        if form.is_valid():
            angler = form.save()
            if report_a_tag:
                return redirect("tfat:report_a_tag_angler_reports", angler_id=angler.id)
            else:
                return redirect("tfat:angler_reports", angler_id=angler.id)
        else:
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            anglers = JoePublic.objects.filter(
                first_name__iexact=first_name, last_name__iexact=last_name
            ).all()
            if len(anglers):
                return render(
                    request,
                    "tfat/angler_form.html",
                    {
                        "form": form,
                        "anglers": anglers,
                        "report_a_tag": report_a_tag,
                        "action": "Create New ",
                    },
                )
    else:
        form = CreateJoePublicForm()

    return render(
        request,
        "tfat/angler_form.html",
        {"form": form, "report_a_tag": report_a_tag, "action": "Create New "},
    )


def create_report(request, angler_id, report_a_tag=False):
    """This view is used to create a new tag report.
    """

    angler = get_object_or_404(JoePublic, id=angler_id)

    if request.method == "POST" and angler:
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.associated_file = request.FILES.get("associated_file")
            report.reported_by = angler
            report.save()
            # redirect to report details:
            if report_a_tag:
                return redirect("tfat:report_a_tag_report_detail", report_id=report.id)
            else:
                return redirect("tfat:report_detail", report_id=report.id)
    else:
        form = ReportForm(initial={"reported_by": angler})

    return render(
        request,
        "tfat/report_form.html",
        {
            "form": form,
            "angler": angler,
            "report_a_tag": report_a_tag,
            "action": "Create",
        },
    )


def edit_report(request, report_id):
    """This view is used to edit an existing tag report.
    """

    report = get_object_or_404(Report, id=report_id)
    angler = report.reported_by
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = angler
            report.save()
            return redirect("tfat:report_detail", report_id=report.id)
    else:
        form = ReportForm(instance=report)

    return render(
        request,
        "tfat/report_form.html",
        {"form": form, "angler": angler, "action": "Edit"},
    )


def create_recovery(request, report_id):
    """This view is used to create a new tag recovery.
    """

    clip_codes = sorted(list(CLIP_CODE_CHOICES), key=lambda x: x[0])
    tag_types = sorted(list(TAG_TYPE_CHOICES), key=lambda x: x[0])
    tag_origin = sorted(list(TAG_ORIGIN_CHOICES), key=lambda x: x[0])
    tag_colours = sorted(list(TAG_COLOUR_CHOICES), key=lambda x: x[0])
    tag_position = sorted(list(TAG_POSITION_CHOICES), key=lambda x: x[0])

    report = get_object_or_404(Report, id=report_id)
    form = RecoveryForm(report_id=report.id, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            recovery = form.save(report=report)
            return redirect("tfat:new_recovery_detail", recovery_id=recovery.id)
    return render(
        request,
        "tfat/recovery_form.html",
        {
            "form": form,
            "action": "create",
            "clip_codes": clip_codes,
            "tag_types": tag_types,
            "tag_origin": tag_origin,
            "tag_colours": tag_colours,
            "tag_position": tag_position,
        },
    )


def edit_recovery(request, recovery_id):
    """This view is used to edit/update existing tag recoveries.
    """

    clip_codes = sorted(list(CLIP_CODE_CHOICES), key=lambda x: x[0])
    tag_types = sorted(list(TAG_TYPE_CHOICES), key=lambda x: x[0])
    tag_origin = sorted(list(TAG_ORIGIN_CHOICES), key=lambda x: x[0])
    tag_colours = sorted(list(TAG_COLOUR_CHOICES), key=lambda x: x[0])
    tag_position = sorted(list(TAG_POSITION_CHOICES), key=lambda x: x[0])

    recovery = get_object_or_404(Recovery, id=recovery_id)
    report = recovery.report

    form = RecoveryForm(
        report_id=report.id, instance=recovery, data=request.POST or None
    )
    if request.method == "POST":
        if form.is_valid():
            recovery = form.save(report)
            return redirect("tfat:recovery_detail", recovery_id=recovery.id)
    return render(
        request,
        "tfat/recovery_form.html",
        {
            "form": form,
            "action": "edit",
            "clip_codes": clip_codes,
            "tag_types": tag_types,
            "tag_origin": tag_origin,
            "tag_colours": tag_colours,
            "tag_position": tag_position,
        },
    )


def recovery_detail_view(request, recovery_id, add_another=False):
    """This view returns the detailed information about a recovery event.

    Arguments:
    - `recovery_id`:
    - `add_another`: a flag to control if an add another button should
    be dispalyed
    """
    recovery = get_object_or_404(Recovery, id=recovery_id)

    return render(
        request,
        "tfat/recovery_detail.html",
        {"recovery": recovery, "add_another": add_another},
    )


def serve_file(request, filename):
    """from:http://stackoverflow.com/questions/2464888/
    downloading-a-csv-file-in-django?rq=1

    This function is my first attempt at a function used to
    serve/download files.  It works for basic text files, but seems to
    corrupt pdf and ppt files (maybe other binaries too).  It also
    should be updated to include some error trapping just incase the
    file doesn t actully exist.
    """

    fname = os.path.join(settings.MEDIA_ROOT, "tag_return_letters", filename)

    if os.path.isfile(fname):

        content_type = mimetypes.guess_type(filename)[0]

        filename = os.path.split(filename)[-1]
        # wrapper = FileWrapper(file(fname, 'rb'))
        wrapper = FileWrapper(open(fname, "rb"))
        response = HttpResponse(wrapper, content_type=content_type)
        response["Content-Disposition"] = "attachment; filename=%s" % os.path.basename(
            fname
        )
        response["Content-Length"] = os.path.getsize(fname)

        return response
    else:
        return render(request, "tfat/missing_file.html", {"filename": filename})


def make_recovery_letter(request, recovery_id, zoom):
    """This view calls R and passes the recovery id and zoom into a
    R-markdown template that is processed into a recoverly letter
    complete with a map showing tagging and recovery location.

    """

    recovery = get_object_or_404(Recovery, id=recovery_id)

    knitcmd = "Rscript --vanilla ./tfat/recovery_letter_rmd/make_letter.r {} {}"

    # if recovery event does not exist, return 404
    # if zoom is not an interger between 1-20 throw an error

    cmd = knitcmd.format(recovery_id, zoom)

    r = subprocess.call(cmd, shell=True)
    print(r)

    # when the sub-process finishes, check to see if the newly created
    # report is there.  If a report by that name is already associated
    # with this recovery event, simple return to the detail page, if
    # not add a tag report letter before returning to the detail page.

    # the file nameing convention used by the markdown document is:

    report_format = "Event-{}_{}.docx"

    today = datetime.now().strftime("%Y-%m-%d")

    fname = os.path.join(
        settings.MEDIA_ROOT,
        "tag_return_letters",
        report_format.format(recovery_id, today),
    )

    if os.path.isfile(fname):
        filename = os.path.split(fname)[1]
        obj, created = RecoveryLetter.objects.get_or_create(
            recovery=recovery, letter=filename
        )
        # we don't want to create a new object if it has a different
        # zoom, just update the existing one:
        obj.zoom = zoom
        obj.save()
    else:
        # this should be written to a log file:
        msg = "Something is wrong - can't find our letter! \n -> {}"
        print(msg.format(fname))

    return redirect("tfat:recovery_detail", recovery_id=recovery.id)
