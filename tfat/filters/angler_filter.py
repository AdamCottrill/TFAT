"""
=============================================================

~/tfat/filters/angler_filter.py
Created: Jul-05-2021 16:27

DESCRIPTION:

Filters for TFAT Angler/Joe Public Model

A. Cottrill
=============================================================
"""

import django_filters
from tfat.models import JoePublic

from ..utils import ValueInFilter


class JoePublicFilter(django_filters.FilterSet):

    first_name = django_filters.CharFilter(
        field_name="first_name", lookup_expr="iexact"
    )
    first_name__like = django_filters.CharFilter(
        field_name="first_name", lookup_expr="icontains"
    )
    last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="iexact")
    last_name__like = django_filters.CharFilter(
        field_name="last_name", lookup_expr="icontains"
    )
    phone = django_filters.CharFilter(field_name="phone")
    phone__like = django_filters.CharFilter(field_name="phone", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="iexact")
    email__like = django_filters.CharFilter(field_name="email", lookup_expr="icontains")

    lake = ValueInFilter(
        field_name="Reported_By__recoveries__lake__abbrev", lookup_expr="in"
    )
    lake__not = ValueInFilter(
        field_name="Reported_By__recoveries__lake__abbrev", exclude=True
    )
    spc = ValueInFilter(
        field_name="Reported_By__recoveries__species__spc", lookup_expr="in"
    )
    spc__not = ValueInFilter(
        field_name="Reported_By__recoveries__species__spc", exclude=True
    )

    report_year = django_filters.NumberFilter(
        field_name="Reported_By__report_date", lookup_expr="year"
    )
    report_year__gte = django_filters.NumberFilter(
        field_name="Reported_By__report_date", lookup_expr="year__gte"
    )
    report_year__lte = django_filters.NumberFilter(
        field_name="Reported_By__report_date", lookup_expr="year__lte"
    )

    report_year__gt = django_filters.NumberFilter(
        field_name="Reported_By__report_date", lookup_expr="year__gt"
    )
    report_year__lt = django_filters.NumberFilter(
        field_name="Reported_By__report_date", lookup_expr="year__lt"
    )

    from_dcr = django_filters.BooleanFilter(
        field_name="Reported_By__dcr", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = JoePublic
        fields = ["first_name", "last_name", "phone", "email"]
