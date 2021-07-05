from django.http import JsonResponse
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from ..constants import (
    FATE_CHOICES,
    SEX_CHOICES,
    TAG_COLOUR_CHOICES,
    TAG_ORIGIN_CHOICES,
    TAG_POSITION_CHOICES,
    TAG_TYPE_CHOICES,
    TAGSTAT_CHOICES,
)
from ..filters import (
    EncounterFilter,
    JoePublicFilter,
    ProjectFilter,
    RecoveryFilter,
    ReportFilter,
)
from ..models import Encounter, JoePublic, Project, Recovery, Report
from ..models import TaggedSpecies as Species
from .serializers import (
    AnglerSerializer,
    EncounterSerializer,
    ProjectSerializer,
    RecoverySerializer,
    ReportSerializer,
    SpeciesSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 250
    page_size_query_param = "page_size"
    max_page_size = 1000


def lookups(request):
    """A read-only endpoint that makes all or our constants available in
    the api.  constants are returned in a json object keyed by entity
    type.  Each entity contains an array of key-value pairs. The key can
    be used to filter urls, the values can be used to present human
    readable labels.

    """

    data = {
        "sex": list(SEX_CHOICES),
        "tag_type": list(TAG_TYPE_CHOICES),
        "tag_position": list(TAG_POSITION_CHOICES),
        "tag_origin": list(TAG_ORIGIN_CHOICES),
        "tag_colour": list(TAG_COLOUR_CHOICES),
        "tagstat": list(TAGSTAT_CHOICES),
        "fate": list(FATE_CHOICES),
    }

    return JsonResponse(data)


class SpeciesList(generics.ListAPIView):
    """A read-only endpoint for species that have been either tagged or
    reported with a tag."""

    lookup_field = "spc"
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class AnglerViewSet(viewsets.ModelViewSet):
    """An api endpoint to create, update, delete, and Anglers/people from the
    general public."""

    queryset = JoePublic.objects.all()
    filterset_class = JoePublicFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    serializer_class = AnglerSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """An api endpoint to create, update, delete, and list tag reports from
    the general public, anglers, or outside agencies."""

    queryset = Report.objects.all()
    filterset_class = ReportFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReportSerializer


class RecoveryViewSet(viewsets.ModelViewSet):
    """An api endpoint to create, update, delete, and list tag and fish
    inforamtion from the general public, anglers, or outside
    agencies.
    """

    queryset = (
        Recovery.objects.select_related("species", "lake")
        .defer(
            "lake__geom",
            "lake__geom_ontario",
            "lake__envelope",
            "lake__envelope_ontario",
            "lake__centroid",
            "lake__centroid_ontario",
        )
        .all()
    )
    filterset_class = RecoveryFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = RecoverySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """An api endpoint for OMNR Proejcts that either applied or recovered
    tags.  Elements are fairly basic.  For more comprehensice information,
    see Project Tracker or FN_Portal.
    """

    queryset = (
        Project.objects.select_related("lake")
        .prefetch_related("Encounters", "Encounters__species")
        .defer(
            "lake__geom",
            "lake__geom_ontario",
            "lake__envelope",
            "lake__envelope_ontario",
            "lake__centroid",
            "lake__centroid_ontario",
        )
        .distinct()
    )
    filterset_class = ProjectFilter
    serializer_class = ProjectSerializer
    lookup_field = "prj_cd"
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class EncounterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing OMNR encounters with tagged fish.
    """

    queryset = (
        Encounter.objects.select_related("species", "project", "project__lake")
        .defer(
            "project__lake__geom",
            "project__lake__geom_ontario",
            "project__lake__envelope",
            "project__lake__envelope_ontario",
            "project__lake__centroid",
            "project__lake__centroid_ontario",
        )
        .all()
    )

    filterset_class = EncounterFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EncounterSerializer
