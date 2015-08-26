import factory
from datetime import datetime


from tfat.models import *


class SpeciesFactory(factory.DjangoModelFactory):
    #FACTORY_FOR = Species
    class Meta:
        model = Species

    species_code = '091'
    common_name = 'Lake Whitefish'
    scientific_name = 'Coregonus clupeaformis'


class JoePublicFactory(factory.DjangoModelFactory):
    class Meta:
        model = JoePublic

    first_name ='Homer'
    last_name = 'Simpson'
    # the address should should be 1-many with a default/current
    address1 = '742 Evergreen Tarrace'
    address2 = 'Box 123'
    town = 'Springfield'
    #this could be a lookup
    province = 'Ontario'
    postal_code = 'N0W2T2'
    email = 'hsimpson@hotmail.com'
    phone = '555-321-1234'


class ReportFactory(factory.DjangoModelFactory):
    class Meta:
        model = Report

    reported_by = factory.SubFactory(JoePublicFactory)
    report_date = datetime(2013,11,11)
    reporting_format = 'e-mail'


class RecoveryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Recovery

    report = factory.SubFactory(ReportFactory)
    spc = factory.SubFactory(SpeciesFactory)

    recovery_date = datetime(2013,10,10)
    general_location = "Off my dock"
    specific_location = "The very end."
    dd_lat = 45.00
    dd_lon = -81.00
    tlen = 500
    flen = 484
    clipc = 5
    tagid = '123456'
    tagdoc = '25012'
    tag_type = '2'
    tag_position = '5'
    tag_origin = '01'
    tag_colour = '2'
    fate = 'K'



class ProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = Project

    year = '2012'
    prj_cd = 'LHA_IS12_123'
    prj_nm = 'My Fake Project'

    #slug = factory.LazyAttribute(lambda o: o.prj_cd.lower())


class EncounterFactory(factory.DjangoModelFactory):
    class Meta:
        model = Encounter

    project = factory.SubFactory(ProjectFactory)
    spc = factory.SubFactory(SpeciesFactory)

    sam = '1001'
    eff = '001'
    observation_date = '2013-11-11'
    grid = '1940'
    dd_lat = 45.550
    dd_lon = -80.125

    flen = 525
    tlen = 535
    rwt = 2500
    age = 12
    sex  = '2'
    clipc = 0
    tagid = '1234'
    tagdoc =  '25012'
