from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


from tfat.views import (SpeciesListView, ReportListView,
                        RecoveryListView, EncounterListView,
                        ProjectTagsAppliedListView,ProjectTagsRecoveredListView,
                        tagid_contains_view, tagid_detail_view,
                        angler_reports_view, create_angler, update_angler,
                        tags_recovered_project, tags_applied_project,
                        tagid_quicksearch_view, encounter_detail_view,
                        create_report, edit_report, report_detail_view,
                        create_recovery, edit_recovery, recovery_detail_view,
                        years_with_tags_applied_view,
                        years_with_tags_recovered_view,
                        tags_applied_year,
                        tags_recovered_year,
                        report_a_tag,
                        serve_file)

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
            r'^angler_reports/report_a_tag/(?P<angler_id>\d+)/$',
            angler_reports_view,
            {'report_a_tag':True},
            name='angler_report_a_tag',

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


       #TAGGED AND RECOVERED IN A PROJECT
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



       #TAGGED AND RECOVERED IN A YEAR
        url(
            regex=r'^years/tagged_in$',
            view=years_with_tags_applied_view,
            name='yearlist_taggedin'
            ),


        url(
            regex=r'^years/recovered_in$',
            view=years_with_tags_recovered_view,
            name='yearlist_recoveredin'
            ),


        url(
            regex=(r'^recovered_in/(?P<year>\d{4})/$'),
            view=tags_recovered_year,
            name='tags_recovered_in_year'
            ),


        url(
            regex=(r'^applied_in/(?P<year>\d{4})/$'),
            view=tags_applied_year,
            name='tags_applied_in_year'
            ),





        url(
            regex=r'^encounter_detail/(?P<encounter_id>\d+)/$',
            view=encounter_detail_view,
            name='encounter_detail'
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



        #TAG REPORTS
        url(
            regex=r'^report_detail/(?P<report_id>\d+)/$',
            view=report_detail_view,
            name='report_detail'
            ),

        url(
            regex=r'^create_report/(?P<angler_id>\d+)/$',
            view=create_report,
            name='create_report'
            ),

        url(
            regex=r'^edit_report/(?P<report_id>\d+)/$',
            view=edit_report,
            name='edit_report'
            ),


        url(
            regex=r'^report_a_tag/$',
            view = 'tfat.views.report_a_tag',
            name='report_a_tag'
            ),


        #TAG RECOVERIES
        url(
            regex=r'^create_recovery/(?P<report_id>\d+)/$',
            view=create_recovery,
            name='create_recovery'
            ),


        url(
            regex=r'^edit_recovery/(?P<recovery_id>\d+)/$',
            view=edit_recovery,
            name='edit_recovery'
            ),


        url(
            regex=r'^recovery_detail/(?P<recovery_id>\d+)/$',
            view=recovery_detail_view,
            name='recovery_detail'
            ),




        #this function is used to download reports and files from project pages
        url(r'^serve_file/(?P<filename>.+)/$', serve_file, name='serve_file'),


)
