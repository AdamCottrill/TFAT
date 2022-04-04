import mimetypes
import os
import subprocess
from datetime import datetime

# from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper

from common.models import Lake, Species
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import (
    CharField,
    Count,
    F,
    Func,
    Q,
    Subquery,
    Value,
    prefetch_related_objects,
)
from django.db.models.functions import ExtractYear
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from geojson import MultiLineString

from tfat.constants import CLIP_CODE_CHOICES, FOLLOW_UP_STATUS_CHOICES
from tfat.filters import (
    EncounterFilter,
    JoePublicFilter,
    ProjectFilter,
    RecoveryFilter,
    ReportFilter,
)
from tfat.forms import (
    CreateJoePublicForm,
    JoePublicForm,
    RecoveryForm,
    ReportFollowUpForm,
    ReportForm,
)
from tfat.models import Encounter, JoePublic, Project, Recovery, Report, ReportFollowUp
from tfat.utils import *

from .forms import EncounterUploadForm
from .data_upload.encounter_upload import process_accdb_upload

MAX_RECORD_CNT = 50
REPORT_PAGE_CNT = 20
ANGLER_PAGE_CNT = 50

# for tables
LARGE_RECORD_CNT = 200


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


# added lake Filter
class RecoveryReportsListView(ListFilteredMixin, ListView):
    """"""

    model = Report
    queryset = (
        Report.objects.all().order_by("-report_date").select_related("reported_by")
    )
    paginate_by = REPORT_PAGE_CNT
    filter_set = ReportFilter

    def get_context_data(self, *args, **kwargs):
        context = super(RecoveryReportsListView, self).get_context_data(*args, **kwargs)
        lake_abbrev = self.request.GET.get("lake")
        if lake_abbrev:
            context["lake"] = Lake.objects.filter(abbrev=lake_abbrev.upper()).first()
        return context


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
        .annotate(tags=Count("Reported_By__recoveries"))
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
report_a_tag_angler_list = login_required(
    AnglerListView.as_view(extra_context={"report_a_tag": True})
)


class SpeciesListView(ListView):
    model = Species


# add lake-filter
class ReportListView(ListView):
    model = Report
    paginate_by = REPORT_PAGE_CNT
    template_name = "tfat/report_list.html"

    def get_queryset(self):

        lake = self.request.GET.get("lake")

        queryset = (
            Report.objects.select_related("reported_by")
            .prefetch_related("recoveries", "recoveries__species", "recoveries__lake")
            .all()
        )
        if lake:
            queryset = queryset.filter(recoveries__lake__abbrev=lake)

        return queryset


# add lake-filter
class RecoveryListView(ListView):
    model = Recovery
    paginate_by = LARGE_RECORD_CNT
    template_name = "tfat/recovery_list.html"

    def get_queryset(self):
        lake = self.request.GET.get("lake")
        queryset = Recovery.objects.select_related("species").all()
        if lake:
            queryset = queryset.filter(lake__abbrev=lake)
        return queryset.order_by("-report__report_date")


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

# added lake List
def report_follow_ups(request):
    """This View will return three tables with all of the outstanding
    followups - one for recoveries that do not have coordinates, one
    that a follow has been requested, but not started, and one of
    reports that have had some initial contact, but the final letter
    has not been sent.

    """

    lake = request.GET.get("lake")

    spatial = (
        Recovery.objects.filter(spatial_followup=True)
        .select_related("species")
        .order_by("-report__report_date")
        .all()
    )

    requested = ReportFollowUp.objects.filter(status="requested")
    started = ReportFollowUp.objects.filter(status="initialized")
    complete = ReportFollowUp.objects.filter(status="completed")

    requested = (
        Report.objects.filter(pk__in=Subquery(requested.values("report_id")))
        .exclude(
            Q(pk__in=Subquery(started.values("report_id")))
            | Q(pk__in=Subquery(complete.values("report_id")))
        )
        .select_related("reported_by")
        .prefetch_related("recoveries", "recoveries__species", "recoveries__lake")
        .order_by("-report_date")
    )

    initiated = (
        Report.objects.filter(pk__in=Subquery(started.values("report_id")))
        .exclude(pk__in=Subquery(complete.values("report_id")))
        .order_by("-report_date")
        .select_related("reported_by")
        .prefetch_related("recoveries", "recoveries__species", "recoveries__lake")
    )

    if lake:
        spatial = spatial.filter(lake__abbrev=lake.upper())
        requested = requested.filter(recoveries__lake__abbrev=lake.upper())
        initiated = initiated.filter(recoveries__lake__abbrev=lake.upper())

    return render(
        request,
        "tfat/outstanding_followups.html",
        {
            "spatial": spatial,
            "requested": requested[:25],
            "initiated": initiated[:25],
            "lake": lake,
        },
    )


# add lake filter
class EncounterListView(ListView):
    model = Encounter


def encounter_detail_view(request, encounter_id):
    """This view returns the detailed information about an mnr encounter
    event (i.e. - a 125 record in one of our master databases).

    Arguments:
    - `recovery_id`:

    """
    encounter = get_object_or_404(Encounter, id=encounter_id)

    mapbounds = get_map_bounds(encounter.project.lake)

    return render(
        request,
        "tfat/encounter_detail.html",
        {"encounter": encounter, "mapBounds": mapbounds},
    )


# added lake filter
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

        lake_abbrev = self.request.GET.get("lake")
        if lake_abbrev:
            projects = projects.filter(lake__abbrev=lake_abbrev)
        return projects

    def get_context_data(self, **kwargs):
        context = super(ProjectTagsAppliedListView, self).get_context_data(**kwargs)
        lake_abbrev = self.request.GET.get("lake")
        if lake_abbrev:
            context["lake"] = Lake.objects.filter(abbrev=lake_abbrev.upper()).first()
        return context


# added lake filter
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

        lake_abbrev = self.request.GET.get("lake")
        if lake_abbrev:
            projects = projects.filter(lake__abbrev=lake_abbrev)
        return projects

    def get_context_data(self, **kwargs):
        context = super(ProjectTagsRecoveredListView, self).get_context_data(**kwargs)
        lake_abbrev = self.request.GET.get("lake")
        if lake_abbrev:
            context["lake"] = Lake.objects.filter(abbrev=lake_abbrev.upper()).first()
        return context


# added lake filter
def years_with_tags_applied_view(request):
    """Render a list of years in which tags were applied.  The list of
    years should be in descending order and include the number of tags
    applied

    """

    lake = None

    tags_applied = Encounter.objects.filter(Q(tagstat="A") | Q(tagstat="A2"))

    lake_abbrev = request.GET.get("lake")
    if lake_abbrev:
        lake = Lake.objects.filter(abbrev=lake_abbrev.upper()).first()

    if lake_abbrev:
        tags_applied = tags_applied.filter(project__lake__abbrev=lake_abbrev.upper())

    tags_applied = (
        tags_applied.values_list("project__year")
        .annotate(total=Count("sam"))
        .order_by("-project__year")
    )

    tags_applied_dict = OrderedDict()

    for yr, total in tags_applied:
        tags_applied_dict[yr] = total

    return render(
        request,
        "tfat/years_with_tags_applied.html",
        {"tags_applied": tags_applied_dict, "lake": lake},
    )


# added lake filter
def years_with_tags_recovered_view(request):
    """Render a list of years in which tags were recovered either by OMNR
    or outside agency.  The list of years should be in descending
    order and include the number of tags recovered by the OMNR and the
    number recovered by the general public or other agencies.
    """

    # calculate the number of recoveries per year:

    lake = None
    lake_abbrev = request.GET.get("lake")
    if lake_abbrev:
        lake = Lake.objects.filter(abbrev=lake_abbrev.upper()).first()

    tags_recovered = get_recoveries_per_year(lake_abbrev)

    return render(
        request,
        "tfat/years_with_tags_recovered.html",
        {"tags_recovered": tags_recovered, "lake": lake},
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
        .select_related("report", "species")
    )

    # the subset of recovery events with both lat and lon (used for plotting)
    recoveries_with_latlon = [x for x in recoveries if x.dd_lat and x.dd_lon]

    lake_ids = [x[0] for x in recoveries.order_by().values_list("lake").distinct()]
    lakes = Lake.objects.filter(pk__in=lake_ids)
    if lakes.count() >= 1:
        mapbounds = get_map_bounds(lakes[0])
    else:
        mapbounds = get_map_bounds("")

    return render(
        request,
        "tfat/angler_reports.html",
        {
            "angler": angler,
            "recoveries_with_latlon": recoveries_with_latlon,
            "recoveries": recoveries,
            "report_a_tag": report_a_tag,
            "mapBounds": mapbounds,
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
            "species"
            #            "project__prj_cd", "project__prj_nm", "project__slug", "spc__common_name"
        )
        .all()
    )

    detail_data = get_tagid_detail_data(tagid, encounter_list)

    lake_ids = [
        x[0] for x in encounter_list.order_by().values_list("project__lake").distinct()
    ]
    lakes = Lake.objects.filter(pk__in=lake_ids)
    if lakes.count() >= 1:
        mapbounds = get_map_bounds(lakes[0])
    else:
        mapbounds = get_map_bounds("")

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
            "mapBounds": mapbounds,
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

    lake_ids = [
        x[0] for x in report.recoveries.order_by().values_list("lake").distinct()
    ]
    lakes = Lake.objects.filter(pk__in=lake_ids)
    if lakes.count() >= 1:
        mapbounds = get_map_bounds(lakes[0])
    else:
        mapbounds = get_map_bounds("")

    return render(
        request,
        "tfat/report_detail.html",
        {
            "report": report,
            "report_a_tag": report_a_tag,
            #'angler':angler
            "mapBounds": mapbounds,
        },
    )


def tagid_quicksearch_view(request):
    """This is a super quick view - if it is called, get the value of q
    and redirect to tagid_contains passing the value of q as a parameter."""

    partial = request.GET.get("q")
    return redirect("tfat:tagid_contains", partial=partial)


# added lake filter
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

    lake_abbrev = request.GET.get("lake")
    if lake_abbrev:
        lake = Lake.objects.filter(abbrev=lake_abbrev.upper()).first()
    else:
        lake = ""

    encounter_list = Encounter.objects.filter(
        tagid__icontains=partial
    ).prefetch_related("species", "project")

    if lake:
        encounter_list = encounter_list.filter(project__lake=lake)

    if encounter_list:
        encounter_list = encounter_list.order_by("tagid", "tagstat")[:MAX_RECORD_CNT]

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
            "lake": lake,
            "mapBounds": get_map_bounds(lake),
        },
    )


# add lake filter
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

    lake_abbrev = request.GET.get("lake")
    if lake_abbrev:
        lake = Lake.objects.filter(abbrev=lake_abbrev.upper()).first()
    else:
        lake = ""

    encounter_list = Encounter.objects.filter(
        tagstat="C", project__year=year
    ).select_related("project", "species")

    # applied = get_omnr_tag_application(slug)
    # other_recoveries = get_other_omnr_recoveries(slug)

    angler_recaps = Recovery.objects.filter(recovery_date__year=year).select_related(
        "report", "species", "report__reported_by"
    )

    if lake_abbrev:
        encounter_list = encounter_list.filter(
            project__lake__abbrev=lake_abbrev.upper()
        )
        angler_recaps = angler_recaps.filter(lake__abbrev=lake_abbrev.upper())

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
            "lake": lake,
            "mapBounds": get_map_bounds(lake),
        },
    )


# add lake filter
def tags_recovered_this_year(request):
    """Pass the current year into the tags recovered view.  THis will
    be the TFAT home page."""

    this_year = datetime.now().year

    return tags_recovered_year(request, this_year, this_year=True)


# added lake filter
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

    lake_abbrev = request.GET.get("lake")
    if lake_abbrev:
        lake = Lake.objects.filter(abbrev=lake_abbrev.upper()).first()
    else:
        lake = ""

    applied = Encounter.objects.filter(
        Q(tagstat="A") | Q(tagstat="A2"), project__year=year
    ).select_related(
        "project",
        "species",
        # "project__prj_cd", "project__prj_nm", "spc__common_name"
    )

    # recovered = get_omnr_tag_recoveries(slug)
    # angler_recaps = get_angler_tag_recoveries(slug, 'A')

    # mls = get_multilinestring([applied, recovered.get('queryset'),
    #                           angler_recaps.get('queryset')])

    if lake_abbrev:
        applied = applied.filter(project__lake__abbrev=lake_abbrev.upper())

    return render(
        request,
        "tfat/year_applied_tags.html",
        {
            "year": year,
            "applied": applied,
            #'recovered':recovered,
            #'angler_recaps':angler_recaps,
            #'mls':mls,
            "lake": lake,
            "mapBounds": get_map_bounds(lake),
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
    project = Project.objects.select_related("lake").get(slug=slug)
    applied = Encounter.objects.filter(
        Q(tagstat="A") | Q(tagstat="A2"), Q(project=project)
    )

    applied = applied.prefetch_related(
        "project",
        "species"
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
            "mapBounds": get_map_bounds(project.lake),
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

    project = Project.objects.select_related("lake").get(slug=slug)

    mapbounds = get_map_bounds(project.lake)

    recovered = Encounter.objects.filter(tagstat="C", project=project).prefetch_related(
        "project", "species"
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
            "mapBounds": mapbounds,
        },
    )


@login_required
def update_angler(request, angler_id):
    """This view is used to update or edit an existing tag reporter / angler."""
    angler = get_object_or_404(JoePublic, id=angler_id)
    form = JoePublicForm(request.POST or None, instance=angler)

    if form.is_valid():
        form.save()
        return redirect("tfat:angler_reports", angler_id=angler.id)
    else:
        return render(
            request, "tfat/angler_form.html", {"form": form, "action": "Edit "}
        )


@login_required
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


@login_required
def create_report(request, angler_id, report_a_tag=False):
    """This view is used to create a new tag report."""

    angler = get_object_or_404(JoePublic, id=angler_id)
    follow_up = None

    if request.method == "POST" and angler:
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.associated_file = request.FILES.get("associated_file")
            report.reported_by = angler
            report.save()
            if report.follow_up and report.follow_up_status is None:
                report.follow_up_status = "requested"
                follow_up = ReportFollowUp(
                    report=report, created_by=request.user, status="requested"
                )
                with transaction.atomic():
                    report.save()
                    follow_up.save()
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


@login_required
def edit_report(request, report_id):
    """This view is used to edit an existing tag report."""

    report = get_object_or_404(Report, id=report_id)
    angler = report.reported_by
    follow_up = None

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = angler
            report.save()
            if report.follow_up and report.follow_up_status is None:
                report.follow_up_status = "requested"
                follow_up = ReportFollowUp(
                    report=report, created_by=request.user, status="requested"
                )
                with transaction.atomic():
                    report.save()
                    follow_up.save()
            if follow_up:
                follow_up.save()
            return redirect("tfat:report_detail", report_id=report.id)
    else:
        form = ReportForm(instance=report)

    return render(
        request,
        "tfat/report_form.html",
        {"form": form, "angler": angler, "action": "Edit"},
    )


@login_required
def create_report_followup(request, report_id):
    """This view is used to create a report follow up if one is required."""

    report = get_object_or_404(Report, id=report_id)
    user = request.user

    next_url = request.GET.get("next")

    # remove the required option and trailing d from labels:
    status_choices = [x for x in FOLLOW_UP_STATUS_CHOICES if x[0] != "requested"]

    # if the follow up is already intialized, don't offer that option again.
    if report.follow_up_status == "initialized":
        status_choices = [x for x in status_choices if x[0] != "initialized"]

    if request.method == "POST" and report:
        form = ReportFollowUpForm(request.POST, request.FILES)
        if form.is_valid():
            # this should be in a transaction:
            with transaction.atomic():
                followup = form.save(commit=False)
                followup.report = report
                followup.created_by = user
                followup.save()
                report.follow_up_status = followup.status
                report.save()
            if next_url is not None:
                return redirect(next_url)
            else:
                return redirect("tfat:report_detail", report_id=report.id)
    else:
        form = ReportFollowUpForm(status_choices=status_choices)

    return render(
        request,
        "tfat/report_followup_form.html",
        {"form": form, "next_url": next_url, "report": report},
    )


@login_required
def create_recovery(request, report_id):
    """This view is used to create a new tag recovery."""

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


@login_required
def edit_recovery(request, recovery_id):
    """This view is used to edit/update existing tag recoveries."""

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

    mapbounds = get_map_bounds(recovery.lake)

    return render(
        request,
        "tfat/recovery_detail.html",
        {"recovery": recovery, "mapBounds": mapbounds, "add_another": add_another},
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

    fname = os.path.join(settings.MEDIA_ROOT, filename)

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


# API Readonly endpoints that return data required to create response letters.


def letter_recovery_detail_view(request, recovery_id):
    """Return the basic attributes of the tag recovery event - where,
    when, who, and what.  Values are return as json string.

    """

    recovery = (
        Recovery.objects.filter(id=recovery_id)
        .annotate(
            first_name=F("report__reported_by__first_name"),
            last_name=F("report__reported_by__last_name"),
            spc=F("species__spc"),
            spc_nmco=F("species__spc_nmco"),
            recovery_date_iso=Func(
                F("recovery_date"),
                Value("YYYY-MM-DD"),
                function="to_char",
                output_field=CharField(),
            ),
        )
        .values(
            # conceenate these
            "first_name",
            "last_name",
            "recovery_date_iso",
            "general_location",
            "specific_location",
            "spc",
            "spc_nmco",
            "tagid",
            "dd_lat",
            "dd_lon",
            "tlen",
            "flen",
            "rwt",
        )
        .first()
    )
    return JsonResponse(recovery, safe=False)


def letter_tagging_event_view(request, lake, spc, tagid):
    """A view that gets the tagging event associated with this tagid and
    species.  Returns an json response containing attributes of the
    tagging event required by recovery response letter. Returns an empty
    dictionary if no match is found.  It currently returns all matching
    tagging events - ideatlly there should be only one. If more than one
    is returned, they will have to be post-processed on the knitr/R side.

    """

    tagging_event = (
        Encounter.objects.filter(
            tagid=tagid,
            tagstat__in=("A", "A2"),
            species__spc=spc,
            project__lake__abbrev=lake,
        )
        .select_related("project", "project__lake", "species")
        .annotate(
            lake_abbrev=F("project__lake__abbrev"),
            prj_cd=F("project__prj_cd"),
            prj_nm=F("project__prj_nm"),
            year=F("project__year"),
            spc=F("species__spc"),
            isodate=Func(
                F("observation_date"),
                Value("YYYY-MM-DD"),
                function="to_char",
                output_field=CharField(),
            ),
        )
        .values(
            "lake_abbrev",  # aliase as lake_abbrev
            "prj_cd",
            "prj_nm",
            "year",
            "spc",
            "isodate",
            "dd_lat",
            "dd_lon",
            "tlen",
            "flen",
            "sex",
            "rwt",
            "tagid",
            "tagdoc",
        )
    )

    # return json.dumps(tagging_event)
    return JsonResponse(list(tagging_event), safe=False)


def letter_tag_count_view(request, year, lake, spc):
    """Return a single json object with the number of tag applied in the
    lake to the species in the given year."""

    tag_count = Encounter.objects.filter(
        tagstat__in=("A", "A2"),
        project__lake__abbrev=lake,
        project__year=year,
        species__spc=spc,
    ).count()

    return JsonResponse({"tag_count": tag_count})


def mnrf_encounters(request, lake, spc):
    """This is a read-only api endpoint that was created specifically for
    mark-recapture mapping scripts of the Lake Huron Walleye Managment
    plan. It returns all of the OMNR encounters with tagged fish of
    the given species and lake. This functionality should be replaced
    with a real api endpoint that accepts filters for year(s), region
    of interest, and other attributes.

    """

    mnrf = (
        Encounter.objects.filter(species__spc=spc, project__lake__abbrev=lake)
        .select_related("project", "project__lake", "species")
        .annotate(
            year=F("project__year"),
            prj_cd=F("project__prj_cd"),
            prj_nm=F("project__prj_nm"),
            spc=F("species__spc"),
            spc_nmco=F("species__spc_nmco"),
            observation_date_iso=Func(
                F("observation_date"),
                Value("YYYY-MM-DD"),
                function="to_char",
                output_field=CharField(),
            ),
        )
        .values(
            "year",
            "observation_date_iso",
            "flen",
            "tlen",
            "rwt",
            "spc",
            "spc_nmco",
            "sex",
            "dd_lat",
            "dd_lon",
            "tagid",
            "tagdoc",
            "tagstat",
            "fate",
            "prj_cd",
            "prj_nm",
            "comment",
        )
    )

    return JsonResponse(list(mnrf), safe=False)


def public_recoveries(request, lake, spc):
    """This is a read-only api endpoint that was created specifically for
    mark-recapture mapping scripts of the Lake Huron Walleye Managment
    plan. It returns all of the public tag recoveries for tags of a
    given species in the specifed lake. This functionality should be
    replaced with a real api endpoint that accepts filters for
    year(s), region of interest, and other attributes and includes
    pagination.

    """

    public = (
        Recovery.objects.filter(species__spc=spc, lake__abbrev=lake)
        .select_related("species", "lake")
        .annotate(
            year=ExtractYear("recovery_date"),
            spc=F("species__spc"),
            spc_nmco=F("species__spc_nmco"),
            recovery_date_iso=Func(
                F("recovery_date"),
                Value("YYYY-MM-DD"),
                function="to_char",
                output_field=CharField(),
            ),
        )
        .values(
            "year",
            "recovery_date_iso",
            "flen",
            "tlen",
            "rwt",
            "spc",
            "spc_nmco",
            "sex",
            "dd_lat",
            "dd_lon",
            "tagid",
            "tagdoc",
            # "--upper('C') as tagstat",
            "fate",
            # "--text('Public Returns') as Code",
            "comment",
        )
    )

    return JsonResponse(list(public), safe=False)


# # move this to someplace more appropriate:
def handle_uploaded_file(f):

    upload_dir = settings.UPLOAD_DIR
    fname = os.path.join(upload_dir, f.name)
    if os.path.isfile(fname):
        os.remove(fname)
    with open(fname, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        # now connect to the uploaded file and insert the contents in the appropriate tables...

    data = process_accdb_upload(upload_dir, f.name)
    # delete the file when we are done. if we can.  Not a problem if
    # not, we will periodically nuke the upload directory anyway.
    try:
        os.remove(fname)
    except (PermissionError, OSError):
        pass
    return data


def get_errors(errors):
    """A helper function to extract relavant information from each error
    message so it can be displayed in the template"""
    error_list = []
    for err in errors:
        slug, validation_error = err
        table = validation_error.model.schema().get("title", "")
        for error in validation_error.errors():
            # msg = f"\t{title} => {slug} - {'-'.join(error['loc'])}: {error['msg']}"
            error_dict = {
                "table": table,
                "slug": slug,
                "fields": "-".join(error["loc"]),
                "message": error["msg"],
            }
            error_list.append(error_dict)
    return error_list


@login_required
def encounter_data_upload(request):
    """A view to process data uploads.  It will be only available to logged in users.

    The uploaded file will be check for validity with pydantic.

    """

    if request.method == "POST":

        form = EncounterUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data_file = form.cleaned_data["file_upload"]
                if not (
                    data_file.name.endswith(".accdb") or data_file.name.endswith(".db")
                ):
                    msg = "Choosen file is not an Access (*.accdb) file!"
                    messages.error(request, msg)
                    return HttpResponseRedirect(reverse("tfat:upload_encounter_data"))
                # if file is too large, return
                if data_file.multiple_chunks():
                    filesize = data_file.size / (1000 * 1000)
                    msg = (
                        f"The uploaded file is too big ({filesize:.2f} MB). "
                        + "Compact the database before uploading it or "
                        + "considering splitting it into smaller packets."
                    )
                    messages.error(request, msg)
                    return HttpResponseRedirect(reverse("tfat:upload_encounter_data"))

                upload = handle_uploaded_file(data_file)

                if upload["status"] == "insert-error":

                    messages.error(
                        request,
                        "There was a problem inserting the data from: "
                        + data_file.name
                        + ". "
                        + str(upload["errors"]),
                    )
                    return render(request, "tfat/encounter_upload.html")

                if upload["status"] == "error":
                    msg = (
                        "There was a problem validating the data from: "
                        + data_file.name
                        + " Please address the issues identified below and try again."
                    )
                    messages.error(request, msg)
                    # pass errors to redirect so that they are available in the response.
                    # return HttpResponseRedirect(reverse("tfat:upload_encounter_data"))
                    error_list = get_errors(upload.get("errors"))
                    return render(
                        request,
                        "tfat/encounter_upload.html",
                        {"errors": error_list},
                    )
                else:
                    prj_cds = upload.get("prj_cds")
                    msg = f"MNRF Tag Encounter Data for for {', '.join(prj_cds)} successfully uploaded!"
                    messages.success(request, message=msg)
                    return HttpResponseRedirect(reverse("tfat:home"))

            except Exception as e:
                messages.error(request, "Unable to upload file. " + repr(e))
                return HttpResponseRedirect(reverse("tfat:upload_encounter_data"))
    else:
        form = EncounterUploadForm()
    return render(request, "tfat/encounter_upload.html", {"form": form})
