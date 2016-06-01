'''
=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_joepublic_model.py
Created: 18 Jun 2015 12:05:51


DESCRIPTION:

Tests of the methods associated with the tag report model.

A. Cottrill
=============================================================
'''


from tfat.models import Recovery

from tfat.tests.factories import *

import pytest


@pytest.mark.django_db
def test_str_complete():
    '''if an angler (joe public) has both first name and an initial, the
    __str__ should return {first_name} {initial}. {last_name}'''

    names = {'first_name':'Homer',
                 'initial':'J',
                 'last_name':'Simpson'}

    angler = JoePublicFactory(first_name=names.get('first_name'),
                              initial=names.get('initial'),
                              last_name=names.get('last_name'))

    should_be = '{first_name} {initial}. {last_name}'
    assert str(angler) == should_be.format(**names)




@pytest.mark.django_db
def test_str_no_initial():
    '''if an angler (joe public) has both first name and an initial, the
    __str__ should return {first_name} {last_name}'''

    names = {'first_name':'Homer',
                 'last_name':'Simpson'}

    angler = JoePublicFactory(first_name=names.get('first_name'),
                              initial=None,
                              last_name=names.get('last_name'))
    should_be = '{first_name} {last_name}'

    assert str(angler) == should_be.format(**names)


#@pytest.mark.django_db
#def test_str_last_name_only():
#    '''if an angler (joe public) only has a last_name, the
#    __str__ method should return just the last_name'''
#
#    names = {'last_name':'Simpson'}
#
#    angler = JoePublicFactory(first_name=None,
#                              initial=None,
#                              last_name=names.get('last_name'))
#    assert str(angler) == names['last_name']
