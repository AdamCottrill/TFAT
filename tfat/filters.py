"""
=============================================================
c:/1work/Python/djcode/tfat/tfat/filters.py
Created: 19 Jun 2015 10:27:17

DESCRIPTION:

Filters for tfat models

A. Cottrill
=============================================================
"""

import django_filters
from django.db import models
from tfat.models import JoePublic, Recovery, Report, Project, Encounter


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class JoePublicFilter(django_filters.FilterSet):
    class Meta:
        model = JoePublic
        # fields = {
        #    "first_name": ["exact", "icontains"],
        #    "last_name": ["exact", "icontains"],
        #    "phone": ["exact", "icontains"],
        #    #'email':['icontains']
        # }

        order_by = ["first_name", "last_name"]
        fields = ["first_name", "last_name", "phone"]
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {"lookup_expr": "icontains"},
            }
        }


class ReportFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="recoveries__lake__abbrev", lookup_expr="in")
    spc = ValueInFilter(field_name="recoveries__species__spc", lookup_expr="in")

    year = django_filters.NumberFilter(field_name="report_date", lookup_expr="year__in")
    first_year = django_filters.NumberFilter(
        field_name="report_date", lookup_expr="year__gte"
    )
    last_year = django_filters.NumberFilter(
        field_name="report_date", lookup_expr="year__lte"
    )

    from_dcr = django_filters.BooleanFilter(
        field_name="dcr", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = Report
        fields = [
            "recoveries__lake__abbrev",
            "recoveries__species__spc",
            "report_date",
            "dcr",
        ]


class RecoveryFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")

    from_dcr = django_filters.BooleanFilter(
        field_name="report__dcr", lookup_expr="isnull", exclude=True
    )

    year = django_filters.NumberFilter(
        field_name="recovery_date", lookup_expr="year__in"
    )
    first_year = django_filters.NumberFilter(
        field_name="recovery_date", lookup_expr="year__gte"
    )
    last_year = django_filters.NumberFilter(
        field_name="recovery_date", lookup_expr="year__lte"
    )
    spc = ValueInFilter(field_name="species__spc", lookup_expr="in")
    tagid = ValueInFilter(field_name="tagid", lookup_expr="in")
    tagid_like = django_filters.CharFilter(field_name="tagid", lookup_expr="icontains")

    tagdoc = ValueInFilter(field_name="tagdoc", lookup_expr="in")
    tagdoc_like = django_filters.CharFilter(
        field_name="tagdoc", lookup_expr="icontains"
    )

    tag_origin = ValueInFilter(field_name="_tag_origin", lookup_expr="in")
    tag_position = ValueInFilter(field_name="_tag_position", lookup_expr="in")
    tag_type = ValueInFilter(field_name="_tag_type", lookup_expr="in")
    tag_colour = ValueInFilter(field_name="_tag_colour", lookup_expr="in")

    class Meta:
        model = Recovery
        fields = [
            "lake__abbrev",
            "species__spc",
            "report__dcr",
            "recovery_date",
            "tagid",
            "tagdoc",
            "tag_origin",
            "tag_position",
            "tag_type",
            "tag_colour",
        ]


class ProjectFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")
    first_year = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    last_year = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    prj_cd = django_filters.CharFilter(lookup_expr="icontains")

    prj_cd_in = ValueInFilter(field_name="prj_cd")

    prj_cd_like = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="icontains"
    )
    suffix = django_filters.CharFilter(field_name="prj_cd", lookup_expr="endswith")

    spc = ValueInFilter(field_name="Encounters__species__spc", lookup_expr="in")
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


class EncounterFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="project__lake__abbrev", lookup_expr="in")

    year = django_filters.NumberFilter(field_name="project__year")

    first_year = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="gte"
    )
    last_year = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="lte"
    )
    prj_cd = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="icontains"
    )

    prj_cd_in = ValueInFilter(field_name="project__prj_cd")

    prj_cd_like = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="icontains"
    )

    suffix = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="endswith"
    )

    # attributes of fish here:
    spc = ValueInFilter(field_name="species__spc", lookup_expr="in")

    tlen = django_filters.NumberFilter(field_name="tlen")
    tlen_gte = django_filters.NumberFilter(field_name="tlen", lookup_expr="gte")
    tlen_lte = django_filters.NumberFilter(field_name="tlen", lookup_expr="lte")

    flen = django_filters.NumberFilter(field_name="flen")
    flen_gte = django_filters.NumberFilter(field_name="flen", lookup_expr="gte")
    flen_lte = django_filters.NumberFilter(field_name="flen", lookup_expr="lte")

    rwt = django_filters.NumberFilter(field_name="rwt")
    rwt_null = django_filters.BooleanFilter(field_name="rwt", lookup_expr="isnull")
    rwt_gte = django_filters.NumberFilter(field_name="rwt", lookup_expr="gte")
    rwt_lte = django_filters.NumberFilter(field_name="rwt", lookup_expr="lte")

    sex = ValueInFilter(field_name="sex")
    clipc = ValueInFilter(field_name="clipc")

    # attributes of tag here
    tagid = ValueInFilter(field_name="tagid", lookup_expr="in")
    tagid_like = django_filters.CharFilter(field_name="tagid", lookup_expr="icontains")

    tagstat = ValueInFilter(field_name="tagstat", lookup_expr="in")

    tagdoc = ValueInFilter(field_name="tagdoc", lookup_expr="in")
    tagdoc_like = django_filters.CharFilter(
        field_name="tagdoc", lookup_expr="icontains"
    )

    tag_origin = ValueInFilter(field_name="_tag_origin", lookup_expr="in")
    tag_position = ValueInFilter(field_name="_tag_position", lookup_expr="in")
    tag_type = ValueInFilter(field_name="_tag_type", lookup_expr="in")
    tag_colour = ValueInFilter(field_name="_tag_colour", lookup_expr="in")

    class Meta:
        model = Encounter
        fields = [
            "project__lake__abbrev",
            "project__year",
            "project__prj_cd",
            "species__spc",
            "tlen",
            "flen",
            "rwt",
            "sex",
            "clipc",
            "tagid",
            "tagdoc",
            "tagstat",
            "tag_origin",
            "tag_position",
            "tag_type",
            "tag_colour",
        ]
