'''
=============================================================
c:/1work/Python/djcode/tfat/tfat/filters.py
Created: 19 Jun 2015 10:27:17

DESCRIPTION:

Filters for tfat models

A. Cottrill
=============================================================
'''

import django_filters
from django.db import models
from tfat.models import JoePublic

class JoePublicFilter(django_filters.FilterSet):

    filter_overrides = {
        models.CharField: {
            'filter_class': django_filters.CharFilter,
            'extra': lambda f: {
                'lookup_type': 'icontains',
            }
        }
    }

    class Meta:
        model = JoePublic
        #fields = {'first_name':['exact', 'icontains'],
        #          'last_name':['exact', 'icontains'],
        #          'phone':['exact', 'icontains'],
                  #'email':['icontains']
        #}

        fields = ['first_name', 'last_name', 'phone']
        order_by = ['first_name', 'last_name']
