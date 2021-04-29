"""Serializers for models in tfat"""

from common.models import Lake
from rest_framework import serializers
from tfat.models import Encounter, Project, Recovery, Report
from tfat.models import TaggedSpecies as Species


# Serializers define the API representation.
class LakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lake
        lookup_field = "abbrev"
        fields = ("lake_name", "abbrev")


# Serializers define the API representation.
class SpeciesSerializer(serializers.ModelSerializer):
    """A simple model serializer for species that have been tagged, or
    have been recovered with tags."""

    class Meta:
        model = Species
        lookup_field = "spc"
        fields = ("spc", "spc_nmco", "spc_nmsc")


class ReportSerializer(serializers.ModelSerializer):
    """A model serializer for tag recovery reports from the general
    public, anglers, or other agencies.

    """

    class Meta:
        model = Report
        # todo Add in lake:
        fields = (
            "id",
            "reported_by",
            "report_date",
            "date_flag",
            "reporting_format",
            "dcr",
            "effort",
            "associated_file",
            "comment",
            "follow_up",
            "follow_up_status",
        )


class RecoverySerializer(serializers.ModelSerializer):
    """Serializer class for tag recoveries reported by anglers, the
    general public, or other agencies.  Includes nested serializer for
    lake and species.
    """

    lake = LakeSerializer(many=False)
    species = SpeciesSerializer(many=False)

    class Meta:
        model = Recovery
        # todo Add in lake:
        fields = (
            "id",
            "report_id",
            "species",
            "lake",
            "recovery_date",
            "date_flag",
            "general_location",
            "specific_location",
            "dd_lat",
            "dd_lon",
            "latlon_flag",
            "spatial_followup",
            "flen",
            "tlen",
            "rwt",
            "girth",
            "sex",
            "clipc",
            "tagid",
            "_tag_origin",
            "_tag_position",
            "_tag_type",
            "_tag_colour",
            "tagdoc",
            "fate",
            "comment",
        )


class ProjectSerializer(serializers.ModelSerializer):

    lake = LakeSerializer(many=False)

    class Meta:
        model = Project
        # todo Add in lake:
        lookup_field = "prj_cd"
        fields = ("year", "prj_cd", "prj_nm", "slug", "lake")


class EncounterSerializer(serializers.ModelSerializer):
    """Serializer class for MNR encounter objects. Includes nested
    serializers fro species and a read-only model method that return
    the formatted FishLabel (FNKey).
    """

    species = SpeciesSerializer(many=False)
    project = ProjectSerializer(many=False)
    fish_label = serializers.SerializerMethodField()

    class Meta:
        model = Encounter

        # lookup_field = "prj_cd"
        fields = (
            "id",
            "fish_label",
            "project",
            "species",
            "sam",
            "eff",
            "grp",
            "fish",
            "observation_date",
            "grid",
            "dd_lat",
            "dd_lon",
            "flen",
            "tlen",
            "rwt",
            "age",
            "sex",
            "clipc",
            "tagid",
            "tagdoc",
            "tagstat",
            "fate",
            "comment",
        )

    def get_fish_label(self, obj):
        """A custom field to return the fish Label (FN125 Key Fields) in a
        standardized format that is consistent with record in other databases.
        (If we ever add FishLabel to the Tfat model, this method can be removed)"""

        base_string = "{}-{}-{}-{}-{}-{}"
        fish_label = base_string.format(
            obj.project.prj_cd,
            obj.sam,
            obj.eff,
            obj.species.spc,
            obj.grp,
            obj.fish,
        )
        return fish_label
