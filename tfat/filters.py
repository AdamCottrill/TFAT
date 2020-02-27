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

    class Meta:
        model = Report
        fields = ["recoveries__lake__abbrev"]


class RecoveryFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")

    class Meta:
        model = Recovery
        fields = ["lake__abbrev"]


class ProjectFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="lake__abbrev", lookup_expr="in")

    class Meta:
        model = Project
        fields = ["lake__abbrev"]


class EncounterFilter(django_filters.FilterSet):

    lake = ValueInFilter(field_name="project__lake__abbrev", lookup_expr="in")

    class Meta:
        model = Encounter
        fields = ["project__lake__abbrev"]
