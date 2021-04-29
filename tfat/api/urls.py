from django.urls import include, path
from rest_framework import routers

from .views import (
    EncounterViewSet,
    ProjectViewSet,
    RecoveryViewSet,
    ReportViewSet,
    SpeciesList,
    lookups,
)

app_name = "tfat_api"


# # Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register("report", ReportViewSet)
router.register("recovery", RecoveryViewSet)
router.register("project", ProjectViewSet)
router.register("encounter", EncounterViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("species_list/", SpeciesList.as_view(), name="species-list"),
    path("lookups/", lookups, name="lookup-values"),
]
