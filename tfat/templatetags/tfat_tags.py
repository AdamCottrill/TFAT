'''
=============================================================
c:/1work/Python/djcode/tfat/tfat/templatetags/tfat_tags.py
Created: 25 Aug 2015 15:19:00


DESCRIPTION:



A. Cottrill
=============================================================
'''


from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def dd2ddm(x):
    '''A little helper function that takes a coordinate in decimal
    degrees and splits it into degrees, decimal minutes.  Values are
    returned as a dictionary that can then be used in string
    formatting'''

    from math import floor

    negative = 1 if x > 0 else -1

    x = abs(x)
    degrees = floor(x)
    minutes = (x - degrees) * 60
    degrees = degrees * negative

    return({'degrees':degrees, 'minutes':minutes})


@register.filter(is_safe=True)
def ddm(x, digits=3):
    """format the dictionary returned by dd2ddm into an html fomatted
    string with the correct number of digits.

    If x cannot be parsed into degrees and minutes and then formated,
    x is returned unchanged.

    Arguments:
    - `x`: - lat or lon as a decimal degree.

    """

    try:
        ddm_dict = dd2ddm(x)
        base_string = "{degrees}&#186; {minutes:." + str(digits) + "f}&#39;"

        return mark_safe(base_string.format(**ddm_dict))
    except TypeError:
        return x
