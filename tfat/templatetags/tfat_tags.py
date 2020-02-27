"""
=============================================================
c:/1work/Python/djcode/tfat/tfat/templatetags/tfat_tags.py
Created: 25 Aug 2015 15:19:00


DESCRIPTION:



A. Cottrill
=============================================================
"""


from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def dd2ddm(x):
    """A little helper function that takes a coordinate in decimal
    degrees and splits it into degrees, decimal minutes.  Values are
    returned as a dictionary that can then be used in string
    formatting"""

    from math import floor

    negative = 1 if x > 0 else -1

    x = abs(x)
    degrees = floor(x)
    minutes = (x - degrees) * 60
    degrees = degrees * negative

    return {"degrees": degrees, "minutes": minutes}


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


@register.filter(is_safe=True)
def status_button_class(x):
    """A little helper function that takes a status value and returns a
    bootstrap button class so that report follow up are displayed
    consistently across the site.

    Options here reflect status choices in tfat.models:

    STATUS_CHOICES = [
        # (0, "Not Requested"),
        ("requested", "Requested"),
        ("initialized", "Initialized"),
        ("completed", "Completed"),
    ]

    """

    if x == "requested":
        btnClass = "btn-danger"
    elif x == "initialized":
        btnClass = "btn-warning"
    elif x == "completed":
        btnClass = "btn-success"
    else:
        btnClass = "btn-default"

    return btnClass


@register.simple_tag(takes_context=True)
def query_transform(context, include_page=False, **kwargs):
    """
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.

    E.g: given the querystring ?foo=1&bar=2
    {% query_transform bar=3 %} outputs ?foo=1&bar=3
    {% query_transform foo='baz' %} outputs ?foo=baz&bar=2
    {% query_transform foo='one' bar='two' baz=99 %}
    outputs ?foo=one&bar=two&baz=99

    A RequestContext is required for access to the current querystring.

    from: https://gist.github.com/benbacardi/d6cd0fb8c85e1547c3c60f95f5b2d5e1

    if page is true, we will return the page number tag too, if it is
    false, we want to strip it out and reset our filters to page 1.
    This allows the same template tag to be used in paginators and
    'refinement' widgets.  Without, refinement widgets may point to a
    page that doesn't exist after the new filter has been applied.

    """

    query = context["request"].GET.copy()
    for k, v in kwargs.items():
        query[k] = v

    if query.get("page") and not include_page:
        query.pop("page")
    return query.urlencode()


@register.simple_tag(takes_context=True)
def strip_parameter(context, param):
    """
    A template tag to remove the specified parameter from the url
    string.  If there are no parameter left, it returns the bare
    url (without any parameters or ?-mark)
    """

    query = context["request"].GET.copy()

    query.pop(param, None)

    if len(query):
        return "?" + query.urlencode()
    else:
        return context["request"].path
