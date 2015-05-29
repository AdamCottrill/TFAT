from django.shortcuts import (render_to_response, get_object_or_404,
                              get_list_or_404)
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import ListView
from django.template import RequestContext

from tfat.models import Species, JoePublic, Report, Recovery, Encounter


MAX_RECORD_CNT = 50



class JoePublicListView(ListView):
    model = JoePublic

class SpeciesListView(ListView):
    model = Species

class ReportListView(ListView):
    model = Report

class RecoveryListView(ListView):
    model = Recovery

class EncounterListView(ListView):
    model = Encounter



def tagid_detail_view(request, tagid):
    """

    Arguments:
    - `tagid`:
    """
    encounter_list = get_list_or_404(Encounter, tagid=tagid)

    return render_to_response('tfat/tagid_contains.html',
                              {'tagid':tagid,
                               'encounter_list':encounter_list,
                               'max_record_count':MAX_RECORD_CNT
                           }, context_instance=RequestContext(request))


def tagid_quicksearch_view(request):
    partial = request.GET.get('q')
    return redirect('tagid_contains', partial=partial)

def tagid_contains_view(request, partial):
    """

    Arguments:
    - `tagid`:
    """
    encounter_list = Encounter.objects.filter(tagid__icontains=partial)

    if not encounter_list:
        raise Http404
    else:
        encouter_list = encounter_list.order_by('tagid',
                                                'tagstat')[:MAX_RECORD_CNT]

    return render_to_response('tfat/tagid_contains.html',
                              {'partial':partial,
                               'encounter_list':encounter_list,
                               'max_record_count':MAX_RECORD_CNT
                           }, context_instance=RequestContext(request))
