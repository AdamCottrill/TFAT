from django.contrib import admin

# Register your models here.
from tfat.models import Species, JoePublic


class Admin_Species(admin.ModelAdmin):
    """Admin class for species"""

    list_display = ("common_name", "scientific_name", "species_code", "primary")
    list_filter = ("primary",)
    ordering = ("-primary", "common_name")

    def queryset(self, request):
        return Species.allspecies


class Admin_JoePublic(admin.ModelAdmin):
    """Admin class for species"""

    list_display = ("last_name", "first_name", "town", "province", "email", "phone")
    list_filter = ("first_name", "last_name", "town", "province")
    ordering = ("last_name", "first_name")


admin.site.register(Species, Admin_Species)
admin.site.register(JoePublic, Admin_JoePublic)
