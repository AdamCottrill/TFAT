from django.urls import path, re_path

from django.conf import settings
from django.views.static import serve as serve_static

from tfat.views import (
    SpeciesListView,
    ReportListView,
    RecoveryListView,
    EncounterListView,
    ProjectTagsAppliedListView,
    ProjectTagsRecoveredListView,
    tagid_contains_view,
    tagid_detail_view,
    angler_reports_view,
    create_angler,
    update_angler,
    tags_recovered_project,
    tags_applied_project,
    tagid_quicksearch_view,
    encounter_detail_view,
    encounter_data_upload,
    create_report,
    create_report_followup,
    report_follow_ups,
    edit_report,
    report_detail_view,
    create_recovery,
    edit_recovery,
    recovery_detail_view,
    years_with_tags_applied_view,
    years_with_tags_recovered_view,
    tags_applied_year,
    tags_recovered_year,
    report_a_tag_angler_list,
    serve_file,
    tags_recovered_this_year,
    report_list,
    # angler_list,
    report_a_tag_angler_list,
    spatial_followup,
    # temporary api endpoint to replicate existing db queries:
    letter_recovery_detail_view,
    letter_tagging_event_view,
    letter_tag_count_view,
    mnrf_encounters,
    public_recoveries,
)


from . import views

app_name = "tfat"


urlpatterns = [
    path("", view=tags_recovered_this_year, name="home"),
    path("recovery_reports/", view=report_list, name="recovery_report_list"),
    path("species/", view=SpeciesListView.as_view(), name="species_list"),
    path("anglers/", views.angler_list, name="angler_list"),
    path(
        "angler_reports/<int:angler_id>/",
        view=angler_reports_view,
        name="angler_reports",
    ),
    path("reports/", view=ReportListView.as_view(), name="report_list"),
    path("recovery/", view=RecoveryListView.as_view(), name="recovery_list"),
    path("encounters/", view=EncounterListView.as_view(), name="encounter_list"),
    path(
        "encounter_data_upload/",
        view=encounter_data_upload,
        name="upload_encounter_data",
    ),
    path(
        "tagid_contains/<str:partial>/",
        view=tagid_contains_view,
        name="tagid_contains",
    ),
    path(
        "tagid/<str:tagid>/",
        view=tagid_detail_view,
        name="tagid_detail_view",
    ),
    path("tagid_q/", view=tagid_quicksearch_view, name="tagid_quicksearch"),
    # TAGGED AND RECOVERED IN A PROJECT
    path(
        "project_list/tagged_in/",
        view=ProjectTagsAppliedListView.as_view(),
        name="projectlist_taggedin",
    ),
    path(
        "project_list/recovered_in/",
        view=ProjectTagsRecoveredListView.as_view(),
        name="projectlist_recoveredin",
    ),
    re_path(
        r"^recovered_in/(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/$",
        view=tags_recovered_project,
        name="tags_recovered_in_project",
    ),
    re_path(
        r"^applied_in/(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/$",
        view=tags_applied_project,
        name="tags_applied_in_project",
    ),
    # TAGGED AND RECOVERED IN A YEAR
    path(
        "years/tagged_in/",
        view=years_with_tags_applied_view,
        name="yearlist_taggedin",
    ),
    path(
        "years/recovered_in/",
        view=years_with_tags_recovered_view,
        name="yearlist_recoveredin",
    ),
    re_path(
        r"^recovered_in/(?P<year>\d{4})/$",
        view=tags_recovered_year,
        name="tags_recovered_in_year",
    ),
    re_path(
        r"^applied_in/(?P<year>\d{4})/$",
        view=tags_applied_year,
        name="tags_applied_in_year",
    ),
    path(
        "encounter_detail/<int:encounter_id>/",
        view=encounter_detail_view,
        name="encounter_detail",
    ),
    # CRUD Anglers
    path("create_angler/", view=create_angler, name="create_angler"),
    path(
        "update_angler/<int:angler_id>/",
        view=update_angler,
        name="update_angler",
    ),
    # TAG REPORTS
    path(
        "report_detail/<int:report_id>/",
        view=report_detail_view,
        name="report_detail",
    ),
    path(
        "create_report/<int:angler_id>/",
        view=create_report,
        name="create_report",
    ),
    path("edit_report/<int:report_id>/", view=edit_report, name="edit_report"),
    path(
        "report_followup/<int:report_id>/",
        view=create_report_followup,
        name="create_report_followup",
    ),
    path("report_followups/", view=report_follow_ups, name="report_follow_ups"),
    # TAG RECOVERIES
    path(
        "create_recovery/<int:report_id>/",
        view=create_recovery,
        name="create_recovery",
    ),
    path(
        "edit_recovery/<int:recovery_id>/",
        view=edit_recovery,
        name="edit_recovery",
    ),
    path(
        "recovery_detail/<int:recovery_id>/",
        view=recovery_detail_view,
        name="recovery_detail",
    ),
    path(
        "recovery_detail/new/<int:recovery_id>/",
        recovery_detail_view,
        {"add_another": True},
        "new_recovery_detail",
    ),
    path(
        "recoveries/spatial_followup/",
        view=spatial_followup,
        name="spatial_followup",
    ),
    # REPORT-A-TAG
    # same as urls above but with additional argument
    path(
        "report_a_tag/",
        view=report_a_tag_angler_list,
        name="report_a_tag_angler_list",
    ),
    path(
        "report_a_tag/create_angler/",
        create_angler,
        {"report_a_tag": True},
        name="report_a_tag_new_angler",
    ),
    path(
        "report_a_tag/angler_reports/<int:angler_id>/",
        angler_reports_view,
        {"report_a_tag": True},
        name="report_a_tag_angler_reports",
    ),
    path(
        "report_a_tag/create_report/<int:angler_id>/",
        create_report,
        {"report_a_tag": True},
        name="report_a_tag_create_report",
    ),
    path(
        "report_a_tag/report_detail/<int:report_id>/",
        report_detail_view,
        {"report_a_tag": True},
        name="report_a_tag_report_detail",
    ),
    # this function is used to download reports and files from project pages
    re_path(r"^serve_file/(?P<filename>.+)$", serve_file, name="serve_file"),
    # path("serve_file/<str:filename>/", serve_file, name="serve_file"),
    # path(
    #     r"^^serve_file/<int:path>.*)$",
    #     serve_static,
    #     {"document_root": settings.MEDIA_ROOT},
    #     name="serve_file",
    # ),
    # Readonly API endpoints to for recovery letters:
    # recovery event details
    path(
        "letter/recovery_detail/<int:recovery_id>/",
        view=letter_recovery_detail_view,
        name="letter_recovery_detail",
    ),
    # tagging event details
    re_path(
        r"^letter/tagging_event/(?P<lake>[A-Za-z]{2})/(?P<spc>\d{3})/(?P<tagid>.+)/$",
        view=letter_tagging_event_view,
        name="letter_tagging_event",
    ),
    # recovery letter - number of tagges applied that year, species and lake
    re_path(
        r"^letter/tag_count/(?P<lake>[A-Za-z]{2})/(?P<year>\d{4})/(?P<spc>\d{3})/$",
        view=letter_tag_count_view,
        name="letter_tag_count",
    ),
    # mnr_encounters - developed for lake huron walleye management plan
    re_path(
        r"^mnrf_encounters/(?P<lake>[A-Za-z]{2})/(?P<spc>\d{3})/$",
        view=mnrf_encounters,
        name="mnrf_encounters",
    ),
    # mnr_encounters - developed for lake huron walleye management plan
    re_path(
        r"^public_recoveries/(?P<lake>[A-Za-z]{2})/(?P<spc>\d{3})/$",
        view=public_recoveries,
        name="public_recoveries",
    ),
]
