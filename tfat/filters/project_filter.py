"""
=============================================================

~/tfat/filters/project_filter.py
Created: Jul-05-2021 16:27

DESCRIPTION:

Filters for OMNR Projects in TFAT

A. Cottrill
=============================================================
"""


import django_filters
from tfat.models import Project

from ..utils import ValueInFilter


class ProjectFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")
    lake__not = ValueInFilter(field_name="lake__abbrev", exclude=True)

    year = django_filters.CharFilter(field_name="year", lookup_expr="exact")
    year__gte = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    year__lte = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    year__gt = django_filters.NumberFilter(field_name="year", lookup_expr="gt")
    year__lt = django_filters.NumberFilter(field_name="year", lookup_expr="lt")

    prj_cd = ValueInFilter(field_name="prj_cd")
    prj_cd__not = ValueInFilter(field_name="prj_cd", exclude=True)
    prj_cd__like = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="icontains"
    )
    prj_cd__not_like = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="icontains", exclude=True
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="iendswith"
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="iendswith", exclude=True
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="prj_nm", lookup_expr="icontains"
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="prj_nm", lookup_expr="icontains", exclude=True
    )

    spc = ValueInFilter(field_name="Encounters__species__spc", lookup_expr="in")
    spc__not = ValueInFilter(field_name="Encounters__species__spc", exclude=True)

    tagstat = ValueInFilter(field_name="Encounters__tagstat", lookup_expr="in")

    class Meta:
        model = Project
        fields = [
            "lake__abbrev",
            "prj_cd",
            "year",
            "Encounters__species__spc",
            "Encounters__tagstat",
        ]
