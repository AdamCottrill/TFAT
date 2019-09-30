"""
=============================================================
c:/1work/Python/djcode/tfat/conftest.py
Created: 07 Aug 2015 14:19:30


DESCRIPTION:



A. Cottrill
=============================================================
"""


import pytest
import os

# from selenium import webdriver
#
# BROWSERS = {
#    'firefox': webdriver.Firefox,
##    'chrome': webdriver.Chrome,
# }
#
#
# IP = '142.143.160.73:8000'
# WEBDRIVER_ENDPOINT = 'http://{}'.format(IP)
#
#
# @pytest.fixture(scope='session',
#                params=BROWSERS.keys())
# def driver(request):
##    if 'DISPLAY' not in os.environ:
##        pytest.skip('Test requires display server (export DISPLAY)')
#
#    b = BROWSERS[request.param]()
#
#    request.addfinalizer(lambda *args: b.quit())
#
#    return b
#
# @pytest.fixture
# def browser(driver, url):
#    browser = driver
#    browser.set_window_size(1200, 800)
#    browser.get(url)
#
#    return browser
#
#
# def pytest_addoption(parser):
#    parser.addoption('--url', action='store',
#                     default='http://localhost/portal/portal.html')
#
# @pytest.fixture(scope='session')
# def url(request):
#    return request.config.option.url
#
