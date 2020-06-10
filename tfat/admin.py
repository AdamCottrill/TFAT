from django.contrib import admin

from tfat.models import JoePublic, Report, ReportFollowUp, TaggedSpecies


class AdminSpecies(admin.ModelAdmin):
    """Admin class for species"""

    search_fields = ["spc_nmco", "spc_nmsc", "spc"]

    list_display = ("spc_nmco", "spc_nmsc", "spc", "tagged")
    list_filter = ("tagged",)
    ordering = ("-tagged", "spc_nmco")

    def queryset(self, request):
        return TaggedSpecies.all_objects


class AdminJoePublic(admin.ModelAdmin):
    """Admin class for anglers or the general public"""

    search_fields = ["first_name", "last_name"]

    list_display = ("full_name", "town", "province", "email", "phone")
    list_filter = ("town", "province")
    ordering = ("last_name", "first_name")

    def full_name(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)


class ReportFollowUpInline(admin.TabularInline):
    model = ReportFollowUp
    extra = 1


class AdminReport(admin.ModelAdmin):
    """Admin class for tag recovery reports"""

    date_hierarchy = "report_date"
    search_fields = ["reported_by__first_name", "reported_by__last_name"]
    list_display = (
        "reported_by",
        "report_date",
        "reporting_format",
        "follow_up_status",
    )
    # filter by year:
    list_filter = ("recoveries__lake", "follow_up_status", "reporting_format")
    ordering = ["-report_date"]

    inlines = [ReportFollowUpInline]


admin.site.register(TaggedSpecies, AdminSpecies)
admin.site.register(JoePublic, AdminJoePublic)
admin.site.register(Report, AdminReport)
