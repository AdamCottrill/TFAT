'''
=============================================================
c:/1work/Python/djcode/pjtk2/pjtk2/tests/test_urls.py
Created: 07 Aug 2015 15:22:49


DESCRIPTION:



A. Cottrill
=============================================================
'''

import pytest

from django.core.urlresolvers import resolve

from tfat.views import *


def test_root_url_resolves_to_home_page_view():
    found = resolve('/tfat/project_list/tagged_in')
    assert found.func == ProjectTagsAppliedListView
