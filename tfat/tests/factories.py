import factory

from tfat.models import *



class SpeciesFactory(factory.DjangoModelFactory):
    #FACTORY_FOR = Species
    class Meta:
        model = Species

    species_code = '091'
    common_name = 'Lake Whitefish'
    scientific_name = 'Coregonus clupeaformis'


class ProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = Project

    prj_cd = 'LHA_IS12_123'
    prj_nm = 'My Fake Project'


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
