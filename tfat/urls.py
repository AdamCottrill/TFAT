from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


from tfat.views import (JoePublicListView, SpeciesListView, ReportListView,
                        RecoveryListView, EncounterListView)

urlpatterns = patterns("",

        url(
            regex=r'^joe_public/$',
            view=JoePublicListView.as_view(),
            name='joepublic_list'
            ),

        url(
            regex=r'^species/$',
            view=SpeciesListView.as_view(),
            name='species_list'
            ),

        url(
            regex=r'^reports/$',
            view=ReportListView.as_view(),
            name='report_list'
            ),

        url(
            regex=r'^recovery/$',
            view=JoePublicListView.as_view(),
            name='recovery_list'
            ),

        url(
            regex=r'^encounters/$',
            view=EncounterListView.as_view(),
            name='encounter_list'
            ),


)
