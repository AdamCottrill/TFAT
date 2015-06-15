from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from .constants import (REPORTING_CHOICES, SEX_CHOICES,
                        TAG_TYPE_CHOICES,
                        TAG_POSITION_CHOICES,
                        TAG_ORIGIN_CHOICES,
                        TAG_COLOUR_CHOICES,
                        TAGSTAT_CHOICES,
                        FATE_CHOICES,
                        DATE_FLAG_CHOICES,
                        LATLON_FLAG_CHOICES)




class Species(models.Model):
    species_code = models.IntegerField(unique=True)
    common_name = models.CharField(max_length=30)
    scientific_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['species_code']

    def __str__(self):
        if self.scientific_name:
            spc_unicode = "{} ({})".format(self.common_name,
                                          self.scientific_name)
        else:
            spc_unicode =  "{}".format(self.common_name)
        return spc_unicode


class JoePublic(models.Model):
    '''- a person who is reporting one or more recovered tags
    - first name
    - last name
    - home address (street, town, province, postal code)
    - e-mail address(es)
    - phone number(s)
    - AGAFF

    '''


    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=50)
    initial = models.CharField(max_length=50, blank=True, null=True)
    # the address should should be 1-many with a default/current
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    town = models.CharField(max_length=50,blank=True, null=True)
    #this could be a lookup
    province = models.CharField(max_length=12,blank=True, null=True)
    postal_code = models.CharField(max_length=7,blank=True, null=True)
    #this should be 1-many with a default/current
    email = models.CharField(max_length=50,blank=True, null=True)
    phone = models.CharField(max_length=15,blank=True, null=True)
    #this should be 1-many with a default/current
    affiliation = models.CharField(max_length=50,blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        #unique_together = ('last_name', 'first_name')

    def __str__(self):
        if self.initial and self.first_name:
            display = '{} {} {}'.format(self.first_name, self.initial,
                                        self.last_name)
        elif self.first_name:
            display = '{} {}'.format(self.first_name, self.last_name)
        else:
            display = '{} {}'.format(self.last_name)
        return display



class Report(models.Model):
    '''

  + report of a one or more recoveries - contact event with the general
    public
  + reported by an individual
  + support for different formats
    + phone (verbal),
    + letter,
    + e-mail

    TODO - Add functionality to follow-up with reports

    '''

    reported_by  = models.ForeignKey(JoePublic, related_name="Reported_By",
                                  blank=True, null=True)
    date_reported = models.DateTimeField(blank=True, null=True)
    date_flag = models.IntegerField("Date Flag",
                               choices=DATE_FLAG_CHOICES, default=1)
    reporting_format = models.CharField("Report Format", max_length=30,
                               choices=REPORTING_CHOICES, default="verbal")
    comment = models.CharField(max_length=500, blank=True, null=True)
    #this should be a model like comments in ticket-tracker -what
    #exactly is the follow up and who is it assigned to, who did it.
    follow_up  = models.BooleanField(default=False)

    def __str__(self):
        return '{} on {}'.format(self.reported_by,
                                 self.date_reported.strftime('%b-%d-%Y'))

class Recovery(models.Model):
    '''

  + recovery event of an actual tag number
  + child of report (one-many relationship)
    + where, when
    + tag number and attributes
    + species, size, gender,
    + clipc
    + fate
    + comment

    '''

    report  = models.ForeignKey(Report, related_name="Report")
    spc  = models.ForeignKey(Species, related_name="Species")

    recovery_date = models.DateField(blank=True, null=True)
    date_flag = models.IntegerField("Date Flag",
                               choices=DATE_FLAG_CHOICES, default=1)
    general_name = models.CharField(max_length=50,blank=True, null=True)
    specific_name = models.CharField(max_length=50,blank=True, null=True)
    #eventually this will be an optional map widget
    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)
    latlon_flag = models.IntegerField("Spatial Flag",
                               choices=LATLON_FLAG_CHOICES, default=1)

    flen = models.IntegerField(blank=True, null=True)
    tlen = models.IntegerField(blank=True, null=True)
    rwt = models.IntegerField(blank=True, null=True)

    sex  = models.CharField("Sex", max_length=30,
                            choices=SEX_CHOICES, default="9",
                            null=True, blank=True)
    #clip information may need to be in a child table and presented as
    #multi-checkbox widget (ie - check all that apply - then calculate
    #clipc from that.)
    clipc = models.CharField(max_length=5,blank=True, null=True)
    tagid = models.CharField(max_length=10)
    tag_origin  = models.CharField("Tag Origin", max_length=3,
                               choices=TAG_ORIGIN_CHOICES, default="01")

    tag_position  = models.CharField("Tag Position", max_length=3,
                               choices=TAG_POSITION_CHOICES, default="1")
    tag_type  = models.CharField("Tag Type", max_length=3,
                               choices=TAG_TYPE_CHOICES, default="1")

    tag_colour = models.CharField("Tag Colour", max_length=3,
                               choices=TAG_COLOUR_CHOICES, default="2")

    #tagdoc will be caclulated from tag type, position, origin and
    #colour following fishnet-II definitions
    tagdoc =  models.CharField(max_length=6,blank=True, null=True)

    tag_removed = models.BooleanField(default=False)
    fate = models.CharField("Fate", max_length=30, blank=True, null=True,
                               choices=FATE_CHOICES, default="R")

    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['tagdoc', 'tagid']

    def __str__(self):
        recovery_date = self.recovery_date.strftime('%b-%d-%Y')
        return '{}<{}>({})'.format(self.tagid, self.tagdoc, recovery_date)


    def save(self, *args, **kwargs):
        '''We will need a custom save method to generate tagdoc from tag type,
        colour, position and orgin'''

#        if self.tagdoc is None:
#            #see if we have all of the peices to build it:
#            #self.build_tagdoc()
#            pass
#        else:
#            #verify that it is the correct length and then parse it up
#            #into its components:
        if len(self.tagdoc) != 5:
            self.tag_type = '9'
            self.tag_position = '9'
            self.tag_origin = '99'
            self.tag_colour = '9'
        else:
            self.tag_type = self.tagdoc[0]
            self.tag_position = self.tagdoc[1]
            self.tag_origin = self.tagdoc[2:4]
            self.tag_colour = self.tagdoc[4]
        super(Recovery, self).save(*args, **kwargs)


class Project(models.Model):
    '''A model to hold basic information about the project in which tags
    were deployed or recovered'''

    year = models.IntegerField(db_index=True)
    prj_cd = models.CharField(db_index=True, max_length=12)
    prj_nm = models.CharField(max_length=30)
    slug = models.SlugField(db_index=True, blank=True, editable=False)

    def __str__(self):
        return '{} ({})'.format(self.prj_cd, self.prj_nm)


    #@models.permalink
    def get_absolute_url(self):
        '''return the url for the project'''
        #url = reverse('pjtk2.views.project_detail', kwargs={'slug':self.slug})
        url = 'http://142.143.160.56:8000/projects/projectdetail/{}/'

        return url.format(slug)

    def save(self, *args, **kwargs):
        """
        from:http://stackoverflow.com/questions/7971689/
             generate-slug-field-in-existing-table
        Slugify name if it doesn't exist. IMPORTANT: doesn't check to see
        if slug is a dupicate!
        """
        if not self.slug:
            self.slug = slugify(self.prj_cd)

        super(Project, self).save( *args, **kwargs)


class Encounter(models.Model):
    '''- Encounter
    + OMNR/agency encounter with a particular tag number - represents
    tagging and recovery events in assessment programs
    + compiled dynamically from master datasets
    + includes basic biological and tagging information
        + where, when
        + project code and name
        + tag number and attributes
        + species, size, gender,

    #enough of the fields are common to encounter and recovery that
    #they could be handled using an abstract database model.

    '''

    project  = models.ForeignKey(Project, related_name="Encounters")
    spc  = models.ForeignKey(Species)
    sam = models.CharField(max_length=5)
    eff = models.CharField(max_length=3)
    observation_date = models.DateField()
    grid = models.CharField(max_length=4)
    dd_lat = models.FloatField()
    dd_lon = models.FloatField()

    flen = models.IntegerField(null=True, blank=True)
    tlen = models.IntegerField(null=True, blank=True)
    rwt = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    sex  = models.CharField("Sex", max_length=30,
                            choices=SEX_CHOICES, default="9",
                            null=True, blank=True)
    clipc = models.CharField(max_length=5, null=True, blank=True)
    tagid = models.CharField(db_index=True, max_length=10)
    tagdoc =  models.CharField(db_index=True, max_length=6, null=True,
                               blank=True)
    tagstat = models.CharField(db_index=True, max_length=4,
                            choices=TAGSTAT_CHOICES, default="C",
                            null=True, blank=True)
    fate = models.CharField(max_length=2,
                            choices=FATE_CHOICES, default="C",
                            null=True, blank=True)
    comment = models.CharField(max_length=500,blank=True, null=True)


    class Meta:
        ordering = ['tagdoc', 'tagid', 'observation_date']


    def __str__(self):
        return '{}<{}>({})'.format(self.tagid, self.tagdoc,
                                   self.observation_date)

    def inches(self):
        if self.tlen:
            length = round(self.tlen * 0.03937, 1)
        else:
            length = None
        return length

    def pounds(self):
        if self.rwt:
            wt = round(self.rwt * 0.00220462, 1)
        else:
            wt = None
        return  wt

    def marker_class(self):
        if self.tagstat=='A':
            return 'applied'
        else:
            return 'recap'


    def popup_text(self):
        '''A method to return the information that will appear on leaflet
        markers:

        TagID: XXXXX TagDoc: %%%%
        Date: MMM-DD-YYY
        Species: Common Name (Species Code)
        FN Fields: PRJ_CD-SAM-EFF-SPC-GRP-FISH
        '''

        base_string = ('<table>' +
                       '    <tr>' +
                       '        <td>TagID:</td>' +
                       '        <td>{tagid}</td>' +
                       '    </tr>' +

                       '    <tr>' +
                       '        <td>TagDoc:</td>' +
                       '        <td>{tagdoc}</td>' +
                       '    </tr>' +

                       '<tr>' +
                       '    <td>Date:</td>' +
                       '    <td>{obs_date}</td>' +
                       '</tr>' +
                       '<tr>' +
                       '    <td>Tag Stattus:</td>' +
                       '    <td>{tagstat}</td>' +
                       '</tr>' +
                       '    <tr>' +
                       '        <td>Species: </td>' +
                       '        <td>{common_name} ({species_code})</td>' +
                       '    </tr>' +
                       '    <tr>' +
                       '        <td>FN Fields:</td>' +
                       '        <td>{fn_key}-SAM-EFF-SPC-GRP-FISH)</td>' +
                       '    </tr>' +
                       '</table>')

        obs_date = self.observation_date.strftime('%b-%d-%Y')

        href = '<a href="{}">{}</a>'.format(self.get_tagid_url(), self.tagid)

        encounter_dict = {'tagid': href,
                          'tagdoc':self.tagdoc,
                          'tagstat':self.get_tagstat_display(),
                          'obs_date':obs_date,
                          'common_name':self.spc.common_name,
                          'species_code':self.spc.species_code,
                          'fn_key':self.project.prj_cd}

        popup = base_string.format(**encounter_dict)

        return popup

    def get_tagid_url(self):
        '''return the url for this tag id'''
        url = reverse('tfat.views.tagid_detail_view',
                      kwargs={'tagid':self.tagid})
        return url


    def tag_colour(self):
        '''a little function to parse tag doc and return the tag colour as a
        string.'''
        colour = 'Unknown'
        if self.tagdoc:
            try:
                key = self.tagdoc[4]
            except IndexError as e:
                key = '9'  #unknown
                choice_dict = {k:v for k,v in TAG_COLOUR_CHOICES}
                colour = choice_dict.get(key, 'Unknown')
        return colour


    def tag_type(self):
        '''a little function to parse tag doc and return the tag type as a
        string.'''
        tag_type = 'Unknown'
        if self.tagdoc:
            try:
                key = self.tagdoc[0]
            except IndexError as e:
                key = '9'  #unknown
            choice_dict = {k:v for k,v in TAG_TYPE_CHOICES}
            tag_type = choice_dict.get(key, 'Unknown')
        return tag_type


    def tag_position(self):
        '''a little function to parse tag doc and return the tag position as a
        string.'''
        tag_position = 'Unknown'
        if self.tagdoc:
            try:
                key = self.tagdoc[1]
            except IndexError as e:
                key = '9'  #unknown
            choice_dict = {k:v for k,v in TAG_POSITION_CHOICES}
            tag_position = choice_dict.get(key, 'Unknown')
        return tag_position


    def tag_origin(self):
        '''a little function to parse tag doc and return the tag origin as a
        string.'''
        tag_origin = 'Unknown'
        if self.tagdoc:
            try:
                key = self.tagdoc[2:4]
            except IndexError as e:
                key = '9'  #unknown
            choice_dict = {k:v for k,v in TAG_ORIGIN_CHOICES}
            tag_origin = choice_dict.get(key, 'Unknown')
        return tag_origin
