import unittest

#from django.conf import settings
#from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from tfat.tests.factories import *

from datetime import datetime
import pytest

class TestAnlgerList(TestCase):
    '''A simple test to verify that the angler list contains what we think
    it should.'''

    def setUp(self):
        ''''''

        self.client = Client()

        spc = SpeciesFactory() #necessary to prevent integrity errors:

        self.angler1 = JoePublicFactory.create(first_name='Homer',
                                               last_name='Simpson')

        self.angler2 = JoePublicFactory.create(first_name='Burns',
                                               last_name='Montgomery')

        self.angler3 = JoePublicFactory.create(first_name='Barney',
                                               last_name='Gumble')

        self.report_date = datetime(2010,10,10)
        self.report = ReportFactory(reported_by=self.angler1,
                                    report_date = self.report_date)

        self.recovery1 = RecoveryFactory(report=self.report,spc=spc,
                                         tagid='11111')

        self.recovery2 = RecoveryFactory(report=self.report,spc=spc,
                                         tagid='22222')

        self.recovery3 = RecoveryFactory(report=self.report,spc=spc,
                                         tagid='33333')


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
        """The list of tag reports filed by an angler should include their
        name and all of the tags they reported, and the date of the report

        Arguments:
        - `self`:
        """
        response = self.client.get(reverse('angler_reports',
                                           kwargs={'angler_id':self.angler1.id}),
                                   follow=True)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'tfat/angler_reports.html')
        msg = 'Tag Reports Filed By {} {}'.format(self.angler1.first_name,
                                              self.angler1.last_name)
        self.assertContains(response, msg)


    def test_angler_details_in_tag_reports(self):
        """The angler details (i.e. - address information) should be displayed
        on the page with tag reports.

        Arguments:
        - `self`:

        """
        response = self.client.get(reverse('angler_reports',
                                           kwargs={'angler_id':self.angler1.id}),
                                   follow=True)

        self.assertContains(response, self.angler1.address1)
        self.assertContains(response, self.angler1.address2)
        self.assertContains(response, self.angler1.town)
        self.assertContains(response, self.angler1.province)
        self.assertContains(response, self.angler1.postal_code)
        self.assertContains(response, self.angler1.phone)
        self.assertContains(response, self.angler1.email)


    def test_angler_reports_without_recoveries(self):
        """If an angler is in the database but not does not have any tags
        associated with them, make sure we handle it properly and
        provide a meaningful message.
        Arguments: - `self`:

        """
        response = self.client.get(reverse('angler_reports',
                                           kwargs={'angler_id':self.angler3.id}),
                                   follow=True)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'tfat/angler_reports.html')
        msg = 'Tag Reports Filed By {} {}'.format(self.angler3.first_name,
                                              self.angler3.last_name)
        self.assertContains(response, msg)
        self.assertContains(response, 'Oops!')

        msg = "There don't seem to be any tag reports associated with this"
        self.assertContains(response, msg)

    def tearDown(self):
        '''Clean up'''
        self.angler3.delete()
        self.angler2.delete()
        self.angler1.delete()
