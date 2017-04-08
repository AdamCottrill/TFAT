
#from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

#IP = 'localhost'
IP = '142.143.160.73:8000'



def test_selenium_setup(browser):
    """
    """
    url = 'http://{}/tfat'.format(IP)
    browser.get(url)
    assert 'TFAT' in browser.title


#from django.core.urlresolvers import reverse
#
#class NewVisitorTest(StaticLiveServerTestCase):
#
#    def setUp(self):
#        self.browser = webdriver.Firefox()
#        self.browser.implicitly_wait(3)
#
#    def tearDown(self):
#        self.browser.quit()
#
#    def test_can_start_a_list_and_retrieve_it_later(self):
#        url = reverse('home')
#        self.browser.get(url)
