import factory
import pytz
from datetime import datetime

from myusers.models import CustomUser as User
from common.models import Lake

from tfat.models import (
    Species,
    JoePublic,
    Report,
    ReportFollowUp,
    Recovery,
    Encounter,
    Database,
    Project,
)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    first_name = "Micky"
    last_name = "Mouse"
    username = "mmouse"
    email = "micky@disney.com"
    password = "Abcd1234"


class LakeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Lake
        django_get_or_create = ("abbrev",)

    abbrev = "HU"
    lake_name = "Lake Huron"


class SpeciesFactory(factory.DjangoModelFactory):
    # FACTORY_FOR = Species
    class Meta:
        model = Species
        django_get_or_create = ("species_code",)

    species_code = "091"
    common_name = "Lake Whitefish"
    scientific_name = "Coregonus clupeaformis"
    primary = True


class JoePublicFactory(factory.DjangoModelFactory):
    class Meta:
        model = JoePublic

    first_name = "Homer"
    last_name = "Simpson"
    # the address should should be 1-many with a default/current
    address1 = "742 Evergreen Tarrace"
    address2 = "Box 123"
    town = "Springfield"
    # this could be a lookup
    province = "Ontario"
    postal_code = "N0W2T2"
    email = "hsimpson@hotmail.com"
    phone = "555-321-1234"


class ReportFactory(factory.DjangoModelFactory):
    class Meta:
        model = Report

    reported_by = factory.SubFactory(JoePublicFactory)
    report_date = datetime(2013, 11, 11).replace(tzinfo=pytz.UTC)
    reporting_format = "e-mail"
    follow_up_status = None


class ReportFollowUpFactory(factory.DjangoModelFactory):
    class Meta:
        model = ReportFollowUp

    report = factory.SubFactory(JoePublicFactory)
    created_by = factory.SubFactory(UserFactory)
    status = "requested"
    comment = "This is a followup comment."


class RecoveryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Recovery

    report = factory.SubFactory(ReportFactory)
    spc = factory.SubFactory(SpeciesFactory)
    lake = factory.SubFactory(LakeFactory)

    recovery_date = datetime(2013, 10, 10).replace(tzinfo=pytz.UTC)
    general_location = "Off my dock"
    specific_location = "The very end."
    dd_lat = 45.00
    dd_lon = -81.00
    spatial_followup = False
    tlen = 500
    flen = 484
    clipc = 5
    tagid = "123456"
    tagdoc = "25012"
    tag_type = "2"
    tag_position = "5"
    tag_origin = "01"
    tag_colour = "2"
    fate = "K"
    tag_removed = False


class DatabaseFactory(factory.DjangoModelFactory):
    class Meta:
        model = Database

    master_database = "Fake Master"
    path = "C:/Path/to/somedb.mdb"


class ProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = Project

    year = "2012"
    prj_cd = "LHA_IS12_123"
    prj_nm = "My Fake Project"
    dbase = factory.SubFactory(DatabaseFactory)
    lake = factory.SubFactory(LakeFactory)

    # slug = factory.LazyAttribute(lambda o: o.prj_cd.lower())


class EncounterFactory(factory.DjangoModelFactory):
    class Meta:
        model = Encounter

    project = factory.SubFactory(ProjectFactory)
    spc = factory.SubFactory(SpeciesFactory)

    sam = "1001"
    eff = "001"
    # observation_date = '2013-11-11'
    observation_date = datetime(2013, 11, 11).replace(tzinfo=pytz.UTC)
    grid = "1940"
    dd_lat = 45.550
    dd_lon = -80.125

    flen = 525
    tlen = 535
    rwt = 2500
    age = 12
    sex = "2"
    clipc = 0
    tagid = "1234"
    tagdoc = "25012"
