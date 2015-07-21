from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


from tfat.views import (SpeciesListView, ReportListView,
                        RecoveryListView, EncounterListView,
                        ProjectTagsAppliedListView,ProjectTagsRecoveredListView,
                        tagid_contains_view, tagid_detail_view,
                        angler_reports_view, create_angler, update_angler,
                        tags_recovered_project, tags_applied_project,
                        tagid_quicksearch_view, create_report)

urlpatterns = patterns("",

        url(
            regex=r'^$',
            view='tfat.views.report_list',
            name='home'
            ),


        url(
            regex=r'^recovery_reports/$',
            view='tfat.views.report_list',
            name='recovery_report_list'
            ),


        url(
            regex=r'^species/$',
            view=SpeciesListView.as_view(),
            name='species_list'
            ),

        url(
            regex=r'^anglers/$',
            view = 'tfat.views.angler_list',
            name='angler_list'
            ),


        url(
            regex=r'^angler_reports/(?P<angler_id>\d+)/$',
            view=angler_reports_view,
            name='angler_reports'
            ),


        url(
            regex=r'^reports/$',
            view=ReportListView.as_view(),
            name='report_list'
            ),

        url(
            regex=r'^recovery/$',
            view=RecoveryListView.as_view(),
            name='recovery_list'
            ),

        url(
            regex=r'^encounters/$',
            view=EncounterListView.as_view(),
            name='encounter_list'
            ),


        url(
            regex=r'^tagid_contains/(?P<partial>.+)/$',
            view=tagid_contains_view,
            name='tagid_contains'
            ),

        url(
            regex=r'^tagid/(?P<tagid>.+)/$',
            view=tagid_detail_view,
            name='tagid_detail_view'
            ),

        url(
            regex=r'^tagid_q/$',
            view=tagid_quicksearch_view,
            name='tagid_quicksearch'
            ),


        url(
            regex=r'^project_list/tagged_in$',
            view=ProjectTagsAppliedListView.as_view(),
            name='projectlist_taggedin'
            ),


        url(
            regex=r'^project_list/recovered_in$',
            view=ProjectTagsRecoveredListView.as_view(),
            name='projectlist_recoveredin'
            ),



        url(
            regex=(r'^recovered_in/'
                    r'(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/$'),
            view=tags_recovered_project,
            name='tags_recovered_in_project'
            ),


        url(
            regex=(r'^applied_in/'
                    r'(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/$'),
            view=tags_applied_project,
            name='tags_applied_in_project'
            ),


        #CRUD Anglers
        url(
            regex=r'^create_angler/$',
            view=create_angler,
            name='create_angler'
            ),

        url(
            regex=r'^update_angler/(?P<angler_id>\d+)/$',
            view=update_angler,
            name='update_angler'
            ),


        #CRUD Tag Reports
        url(
            regex=r'^create_report/(?P<angler_id>\d+)/$',
            view=create_report,
            name='create_report'
            ),

        url(
            regex=r'^update_report/(?P<angler_id>\d+)/(?P<report_id>\d+)/$',
            view=create_report,
            name='update_report'
            ),



)
