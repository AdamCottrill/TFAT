'''=============================================================
c:/1work/Python/djcode/tfat/tfat/tests/test_tfat_tags.py
Created: 25 Aug 2015 15:36:33

DESCRIPTION:

The tests in this file verify that the custom template tags/filters
written for tfat work as expected.

A. Cottrill
=============================================================

'''


import pytest

from tfat.templatetags.tfat_tags import dd2ddm, ddm


def test_dd2ddm():
    """Verify that our function to parse decimal degrees to degrees,
    decimal minutes works as expected.

    Examples:
    45.5 degrees should parsed to 45 degrees, 30 minutes
    -81.25 degrees should parsed to -81 degrees, 15 minutes


    """

    x = 45.5
    ddm_string = dd2ddm(x)
    assert ddm_string['degrees'] == 45
    assert ddm_string['minutes'] == 30.0


    x = 45.25
    ddm_string = dd2ddm(x)
    assert ddm_string['degrees'] == 45
    assert ddm_string['minutes'] == 15.0


    x = 45.0
    ddm_string = dd2ddm(x)
    assert ddm_string['degrees'] == 45
    assert ddm_string['minutes'] == 0.0


    x = -81.5
    ddm_string = dd2ddm(x)
    assert ddm_string['degrees'] == -81
    assert ddm_string['minutes'] == 30.0


    x = -81.25
    ddm_string = dd2ddm(x)
    assert ddm_string['degrees'] == -81
    assert ddm_string['minutes'] == 15.0


    x = -81.0
    ddm_string = dd2ddm(x)
    assert ddm_string['degrees'] == -81
    assert ddm_string['minutes'] == 0.0



def test_ddm():
    """Verify that our function to parse decimal degrees to an html
    fomatted string with the expected number of digits.

    """

    x = 45.5
    ddm_string = ddm(x)
    assert ddm_string == '45&#186; 30.000&#39;'

    x = 45.25
    ddm_string = ddm(x)
    assert ddm_string == '45&#186; 15.000&#39;'

    x = 45.0
    ddm_string = ddm(x)
    assert ddm_string == '45&#186; 0.000&#39;'

    x = -81.5
    ddm_string = ddm(x)
    assert ddm_string == '-81&#186; 30.000&#39;'

    x = -81.25
    ddm_string = ddm(x)
    assert ddm_string == '-81&#186; 15.000&#39;'

    x = -81.0
    ddm_string = ddm(x)
    assert ddm_string == '-81&#186; 0.000&#39;'

    #check the digits options
    x = 45.5
    ddm_string = ddm(x,1)
    assert ddm_string == '45&#186; 30.0&#39;'

    x = 45.5
    ddm_string = ddm(x,4)
    assert ddm_string == '45&#186; 30.0000&#39;'


def test_ddm_not_a_number():
    """If the value passed to ddm is not a number, the original object
    should be returned unchanged.
    """


    x = 'foo'
    ddm_string = ddm(x)
    assert ddm_string == x

    x = 'foo'
    ddm_string = ddm(x,4)
    assert ddm_string == x

    x = {'foo':4, 'bar':'baz'}
    ddm_string = ddm(x,4)
    assert ddm_string == x

    x = None
    ddm_string = ddm(x,4)
    assert ddm_string == x
