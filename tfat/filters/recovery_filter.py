"""
=============================================================

~/tfat/filters/recovery_filter.py
Created: Jul-05-2021 16:27

DESCRIPTION:

Filters for TFAT Tag Recoveries

A. Cottrill
=============================================================
"""


import django_filters
from tfat.models import Recovery

from ..utils import ValueInFilter


class RecoveryFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")
    lake__not = ValueInFilter(field_name="lake__abbrev", exclude=True)

    spc = ValueInFilter(field_name="species__spc", lookup_expr="in")
    spc_not = ValueInFilter(field_name="species__spc", exclude=True)

    from_dcr = django_filters.BooleanFilter(
        field_name="report__dcr", lookup_expr="isnull", exclude=True
    )

    year = django_filters.NumberFilter(field_name="recovery_date", lookup_expr="year")

    year__gte = django_filters.NumberFilter(
        field_name="recovery_date", lookup_expr="year__gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="recovery_date", lookup_expr="year__lte"
    )

    year__gt = django_filters.NumberFilter(
        field_name="recovery_date", lookup_expr="year__gt"
    )
    year__lt = django_filters.NumberFilter(
        field_name="recovery_date", lookup_expr="year__lt"
    )

    tagid = ValueInFilter(field_name="tagid", lookup_expr="in")
    tagid__like = django_filters.CharFilter(field_name="tagid", lookup_expr="icontains")

    tagdoc = ValueInFilter(field_name="tagdoc")
    tagdoc__not = ValueInFilter(field_name="tagdoc", exclude=True)
    tagdoc__like = django_filters.CharFilter(
        field_name="tagdoc", lookup_expr="icontains"
    )

    tag_origin = ValueInFilter(field_name="_tag_origin", lookup_expr="in")
    tag_origin__not = ValueInFilter(field_name="_tag_origin", exclude=True)

    tag_position = ValueInFilter(field_name="_tag_position", lookup_expr="in")
    tag_position__not = ValueInFilter(field_name="_tag_position", exclude=True)

    tag_type = ValueInFilter(field_name="_tag_type", lookup_expr="in")
    tag_type__not = ValueInFilter(field_name="_tag_type", exclude=True)

    tag_colour = ValueInFilter(field_name="_tag_colour", lookup_expr="in")
    tag_colour__not = ValueInFilter(field_name="_tag_colour", exclude=True)

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
