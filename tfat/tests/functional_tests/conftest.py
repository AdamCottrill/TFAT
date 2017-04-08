import pytest
from selenium import webdriver


BROWSERS = {
    #'firefox': DesiredCapabilities.FIREFOX,
    #'chrome': DesiredCapabilities.CHROME,
    'firefox': webdriver.Firefox(),
}

#WEBDRIVER_ENDPOINT = 'http://localhost:4444/wd/hub'


@pytest.yield_fixture(params=BROWSERS.keys())
def browser(request):
    #driver = webdriver.Remote(
    #    command_executor=WEBDRIVER_ENDPOINT,
    #    desired_capabilities=BROWSERS[request.param]
    #)
    driver = BROWSERS[request.param]
    yield driver
    driver.quit()
