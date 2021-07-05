"""
=============================================================

~/tfat/filters/report_filter.py
Created: Jul-05-2021 16:27

DESCRIPTION:

Filters for TFAT Tag Reports

A. Cottrill
=============================================================
"""


import django_filters
from tfat.models import Report

from ..utils import ValueInFilter


class ReportFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="recoveries__lake__abbrev", lookup_expr="in")
    lake__not = ValueInFilter(field_name="recoveries__lake__abbrev", exclude=True)

    spc = ValueInFilter(field_name="recoveries__species__spc", lookup_expr="in")
    spc__not = ValueInFilter(field_name="recoveries__species__spc", exclude=True)

    report_year = django_filters.NumberFilter(
        field_name="report_date", lookup_expr="year"
    )
    report_year__gte = django_filters.NumberFilter(
        field_name="report_date", lookup_expr="year__gte"
    )
    report_year__lte = django_filters.NumberFilter(
        field_name="report_date", lookup_expr="year__lte"
    )

    report_year__gt = django_filters.NumberFilter(
        field_name="report_date", lookup_expr="year__gt"
    )
    report_year__lt = django_filters.NumberFilter(
        field_name="report_date", lookup_expr="year__lt"
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
