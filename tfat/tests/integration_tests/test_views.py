import unittest

#from django.conf import settings
#from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from tfat.tests.factories import *

import pytest

class TestAnlgerList(TestCase):
    '''A simple test to verify that the angler list contains what we think
    it should.'''

    def setUp(self):
        ''''''

        self.client = Client()

        self.angler1 = JoePublicFactory.create(first_name='Homer',
                                               last_name='Simpson')

        self.angler2 = JoePublicFactory.create(first_name='Burns',
                                               last_name='Montgomery')

        self.angler3 = JoePublicFactory.create(first_name='Barney',
                                               last_name='Gumble')

    def test_anglers_render_in_angler_listview(self):
        '''.'''

        response = self.client.get(reverse('angler_list'), follow=True)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'tfat/angler_list.html')
        self.assertContains(response, 'Tag Returnees')


        #make sure that the list of anglers actually appear:
        nm = '{} {}'.format(self.angler1.first_name, self.angler1.last_name)
        self.assertContains(response, nm, True)

        nm = '{} {}'.format(self.angler2.first_name, self.angler2.last_name)
        self.assertContains(response, nm)

        nm = '{} {}'.format(self.angler3.first_name, self.angler3.last_name)
        self.assertContains(response, nm)


    def test_angler_reports(self):
            """

            Arguments:
            - `self`:
            """

        response = self.client.get(reverse('angler_reports',
                                           kwargs = {'angler_id'=self.angler1.id}
                                       ), follow=True)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'tfat/angler_reports.html')
        msg = 'Tags Returned By {} {}'.format(self.angler1.first_name,
                                              self.angler1.last_name)


    def tearDown(self):
        '''Clean up'''
        self.angler3.delete()
        self.angler2.delete()
        self.angler1.delete()
