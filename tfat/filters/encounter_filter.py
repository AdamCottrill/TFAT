"""
=============================================================

~/tfat/filters/encounter_filter.py
Created: Jul-05-2021 16:27

DESCRIPTION:

Filters for OMNR tagging/recovery events (encounters) in TFAT

A. Cottrill
=============================================================
"""


import django_filters
from tfat.models import Encounter

from ..utils import ValueInFilter


class EncounterFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="project__lake__abbrev", lookup_expr="in")
    lake__not = ValueInFilter(field_name="project__lake__abbrev", exclude=True)

    year = django_filters.CharFilter(field_name="project__year", lookup_expr="exact")
    year__gte = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="lte"
    )
    year__gt = django_filters.NumberFilter(field_name="project__year", lookup_expr="gt")
    year__lt = django_filters.NumberFilter(field_name="project__year", lookup_expr="lt")

    prj_cd = ValueInFilter(field_name="project__prj_cd")
    prj_cd__not = ValueInFilter(field_name="project__prj_cd", exclude=True)

    prj_cd__like = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="icontains"
    )
    prj_cd__not_like = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="icontains", exclude=True
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="endswith"
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="endswith", exclude=True
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="project__prj_nm", lookup_expr="icontains"
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="project__prj_nm", lookup_expr="icontains", exclude=True
    )

    spc = ValueInFilter(field_name="species__spc", lookup_expr="in")
    spc_not = ValueInFilter(field_name="species__spc", exclude=True)

    tagstat = ValueInFilter(field_name="tagstat")
    tagstat__not = ValueInFilter(field_name="tagstat", exclude=True)

    tagid = ValueInFilter(field_name="tagid", lookup_expr="in")
    tagid__like = django_filters.CharFilter(field_name="tagid", lookup_expr="icontains")

    tagdoc = ValueInFilter(field_name="tagdoc")
    tagdoc__not = ValueInFilter(field_name="tagdoc", exclude=True)
    tagdoc__like = django_filters.CharFilter(
        field_name="tagdoc", lookup_expr="icontains"
    )

    # TODO: refactor encounter model to include separate fields for tag attributes
    # tag_origin = ValueInFilter(field_name="_tag_origin", lookup_expr="in")
    # tag_origin__not = ValueInFilter(field_name="_tag_origin", exclude=True)

    # tag_position = ValueInFilter(field_name="_tag_position", lookup_expr="in")
    # tag_position__not = ValueInFilter(field_name="_tag_position", exclude=True)

    # tag_type = ValueInFilter(field_name="_tag_type", lookup_expr="in")
    # tag_type__not = ValueInFilter(field_name="_tag_type", exclude=True)

    # tag_colour = ValueInFilter(field_name="_tag_colour", lookup_expr="in")
    # tag_colour__not = ValueInFilter(field_name="_tag_colour", exclude=True)

    tlen = django_filters.NumberFilter(field_name="tlen")  # , lookup_expr="exact")
    tlen__gte = django_filters.NumberFilter(field_name="tlen", lookup_expr="gte")
    tlen__lte = django_filters.NumberFilter(field_name="tlen", lookup_expr="lte")
    tlen__gt = django_filters.NumberFilter(field_name="tlen", lookup_expr="gt")
    tlen__lt = django_filters.NumberFilter(field_name="tlen", lookup_expr="lt")

    flen = django_filters.NumberFilter(field_name="flen")
    flen__gte = django_filters.NumberFilter(field_name="flen", lookup_expr="gte")
    flen__lte = django_filters.NumberFilter(field_name="flen", lookup_expr="lte")
    flen__gt = django_filters.NumberFilter(field_name="flen", lookup_expr="gt")
    flen__lt = django_filters.NumberFilter(field_name="flen", lookup_expr="lt")

    rwt = django_filters.NumberFilter(field_name="rwt")
    rwt__null = django_filters.BooleanFilter(field_name="rwt", lookup_expr="isnull")
    rwt__gte = django_filters.NumberFilter(field_name="rwt", lookup_expr="gte")
    rwt__lte = django_filters.NumberFilter(field_name="rwt", lookup_expr="lte")
    rwt__gt = django_filters.NumberFilter(field_name="rwt", lookup_expr="gt")
    rwt__lt = django_filters.NumberFilter(field_name="rwt", lookup_expr="lt")

    sex = ValueInFilter(field_name="sex")
    sex__not = ValueInFilter(field_name="sex", exclude=True)
    sex__null = django_filters.BooleanFilter(field_name="sex", lookup_expr="isnull")

    clipc = ValueInFilter(field_name="clipc")
    clipc__not = ValueInFilter(field_name="clipc", exclude=True)
    clipc__null = django_filters.BooleanFilter(field_name="clipc", lookup_expr="isnull")
    clipc__like = django_filters.CharFilter(field_name="clipc", lookup_expr="icontains")
    clipc__not_like = django_filters.CharFilter(
        field_name="clipc", lookup_expr="icontains", exclude=True
    )

    fate = ValueInFilter(field_name="fate")
    fate__not = ValueInFilter(field_name="fate", exclude=True)

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
            # "tag_origin",
            # "tag_position",
            # "tag_type",
            # "tag_colour",
        ]
