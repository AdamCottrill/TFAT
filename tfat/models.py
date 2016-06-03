from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

import os

import html

from .constants import (REPORTING_CHOICES, SEX_CHOICES,
                        TAG_TYPE_CHOICES,
                        TAG_POSITION_CHOICES,
                        TAG_ORIGIN_CHOICES,
                        TAG_COLOUR_CHOICES,
                        TAGSTAT_CHOICES,
                        FATE_CHOICES,
                        DATE_FLAG_CHOICES,
                        LATLON_FLAG_CHOICES,
                        PROVINCES_STATE_CHOICES)


class ActiveSpecies(models.Manager):
    '''only return those species where primary is true - keeps dropdowns
    reasonably small'''
    def get_queryset(self):
        #use_for_related_fields = True
        return super(ActiveSpecies, self).get_queryset().filter(primary=True)


class AllSpecies(models.Manager):
    '''only return all species currently in database. Used primary in
    admin or shell'''
    def get_queryset(self):
        #use_for_related_fields = True
        return super(AllSpecies, self).get_queryset()


class Species(models.Model):
    species_code = models.IntegerField(unique=True)
    common_name = models.CharField(max_length=40)
    scientific_name = models.CharField(max_length=50, null=True, blank=True)
    primary = models.BooleanField(default=False)

    objects = ActiveSpecies()
    allspecies = AllSpecies()

    class Meta:
        ordering = ['-primary', 'common_name']
        verbose_name_plural = "Species"

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
    initial = models.CharField(max_length=5, blank=True, null=True)
    # the address should should be 1-many with a default/current
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    town = models.CharField(max_length=50,blank=True, null=True)

    province = models.CharField(max_length=12, choices=PROVINCES_STATE_CHOICES,
                                blank=True, null=True)

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
            display = '{} {}. {}'.format(self.first_name,
                                         self.initial, self.last_name)
        elif self.first_name:
            display = '{} {}'.format(self.first_name, self.last_name)
        else:
            display = '{}'.format(self.last_name)
        return display

    def report_count(self):
        """Return the number of reports filed by this particular person.

        Arguments:
        - `self`:
        """
        return len(Report.objects.filter(reported_by=self))

    def tag_count(self):
        """Return the number of tags returned by this particular person.

        Arguments:
        - `self`:
        """
        return len(Recovery.objects.filter(report__reported_by=self))



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
    report_date = models.DateTimeField('Report Date', blank=True, null=True)
    date_flag = models.IntegerField("Date Flag",
                               choices=DATE_FLAG_CHOICES, default=1)
    reporting_format = models.CharField("Report Format", max_length=30,
                               choices=REPORTING_CHOICES, default="verbal")
    dcr =  models.CharField(max_length=15, blank=True, null=True)
    effort =  models.CharField(max_length=15, blank=True, null=True)
    associated_file = models.FileField(upload_to='reports', blank=True,
                                       null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    #this should be a model like comments in ticket-tracker -what
    #exactly is the follow up and who is it assigned to, who did it.
    follow_up  = models.BooleanField(default=False)

    class Meta:
        ordering = ['-report_date']
        verbose_name_plural = "JoePublic"

    def __str__(self):
        report = ""
        if self.reported_by and self.report_date:
            return '{} on {}'.format(self.reported_by,
                                 self.report_date.strftime('%b-%d-%Y'))
        elif self.reported_by:
            return '{} <Report id={}>'.format(self.reported_by,
                                 self.id)
        else:
            return '<Report id={}>'.format(self.id)

    def get_recoveries(self):
        """Retrun any tags assocated with this report:

        Arguments:
        - `self`:
        """
        tags = self.Report.select_related('spc__common_name')
        return tags

    def get_recoveries_with_latlon(self):
        """Return only those tags with a lat-lon value.  Used for plotting on
        maps.  Additional logic could be added to ensure lat-lon are
        valid coordinates.

        Arguments:
        - `self`:

        """

        tags = self.Report.select_related()
        tags = [x for x in tags if x.dd_lat and x.dd_lon]
        return tags



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
    general_location = models.CharField("General Location", max_length=200,
                                    blank=True, null=True)
    specific_location = models.CharField("Specific Location", max_length=200,
                                     blank=True, null=True)
    #eventually this will be an optional map widget
    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)
    latlon_flag = models.IntegerField("Spatial Flag",
                               choices=LATLON_FLAG_CHOICES, default=1)
    spatial_followup = models.BooleanField(default=False)

    flen = models.IntegerField("Fork Length", blank=True, null=True)
    tlen = models.IntegerField("Total Length", blank=True, null=True)
    rwt = models.IntegerField("Round Weight", blank=True, null=True)
    girth = models.IntegerField("Girth", blank=True, null=True)

    sex  = models.CharField("Sex", max_length=3,
                            choices=SEX_CHOICES, default="9",
                            null=True, blank=True)
    #clip information may need to be in a child table and presented as
    #multi-checkbox widget (ie - check all that apply - then calculate
    #clipc from that.)
    clipc = models.CharField("Clip Code", max_length=5,blank=True, null=True)
    tagid = models.CharField(max_length=10, db_index=True)
    _tag_origin = models.CharField("Tag Origin",
                                  max_length=3,db_index=True,
                                  db_column="tag_origin",
                                  choices=TAG_ORIGIN_CHOICES,
                                  default="01")

    _tag_position = models.CharField("Tag Position", max_length=3,
                                     db_index=True,
                                     db_column="tag_position",
                                     choices=TAG_POSITION_CHOICES,
                                     default="1")

    _tag_type = models.CharField("Tag Type", max_length=3,
                                 db_index=True, db_column="tag_type",
                                 choices=TAG_TYPE_CHOICES, default="1")

    _tag_colour = models.CharField("Tag Colour", max_length=3,
                                   db_index=True, db_column="tag_colour",
                                   choices=TAG_COLOUR_CHOICES,
                                   default="2")

    tagdoc =  models.CharField('TAGDOC', max_length=6,
                               #blank=True, null=True,
                               db_index=True, default='25012')

    tag_removed = models.BooleanField(default=False)
    fate = models.CharField("Fate", max_length=3, blank=True, null=True,
                               choices=FATE_CHOICES, default="R")

    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['tagdoc', 'tagid']
        index_together = ['tagid', 'tagdoc', 'spc']

    def _get_observation_date(self):
        """An aliase for recovery date - if recovery date is available use it,
        if not use report date, otherwise return None.
        """
        if self.recovery_date:
            return self.recovery_date
        elif self.report.report_date:
            return self.report.report_date
        else:
            return None

    observation_date = property(_get_observation_date)

    def __str__(self):
        if self.recovery_date:
            recovery_date = self.recovery_date.strftime('%b-%d-%Y')
            return '{}<{}>({})'.format(self.tagid, self.tagdoc, recovery_date)
        else:
            return '{}<{}>'.format(self.tagid, self.tagdoc)

    def get_tagid_url(self):
        '''return the url for this tag id'''
        url = reverse('tfat.views.tagid_detail_view',
                      kwargs={'tagid':self.tagid})
        return url


    def popup_text(self):
        '''A method to return the information that will appear on leaflet
        markers:

        TagID: XXXXX TagDoc: %%%%
        Date: MMM-DD-YYY
        Species: Common Name (Species Code)
        Reported by: first_name last_name
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
                       '    <td>{recovery_date}</td>' +
                       '</tr>' +
                       '    <tr>' +
                       '        <td>Species: </td>' +
                       '        <td>{common_name} ({species_code})</td>' +
                       '    </tr>' +
                       '    <tr>' +
                       '        <td>Repored By:</td>' +
                       '        <td>{first_name} {last_name}</td>' +
                       '    </tr>' +
                       '    <tr>' +
                       '        <td>Comments:</td>' +
                       '        <td>{comments}</td>' +
                       '    </tr>' +

                       '</table>')

        if self.recovery_date:
            recovery_date = self.recovery_date.strftime('%b-%d-%Y')
        else:
            recovery_date = 'Unknown'

        comments = self.get_comments()
        last_name = html.escape(self.report.reported_by.last_name)
        href = '<a href="{}">{}</a>'.format(self.get_tagid_url(), self.tagid)

        encounter_dict = {'tagid': href,
                          'tagdoc':self.tagdoc,
                          'recovery_date':recovery_date,
                          'common_name':self.spc.common_name,
                          'species_code':self.spc.species_code,
                          'first_name':self.report.reported_by.first_name,
                          'last_name':last_name,
                          'comments':comments}

        popup = base_string.format(**encounter_dict)

        return popup



    def get_tagid_url(self):
        '''return the url for this tag id'''
        url = reverse('tfat.views.tagid_detail_view',
                      kwargs={'tagid':self.tagid})
        return url


    def get_comments(self):
        """

        Arguments:
        - `self`:
        """

        comments = ""
        if self.general_location:
            comments += html.escape(self.general_location)
        if self.specific_location:
            comments += html.escape('({})'.format(self.specific_location))
        if self.comment:
            comments += '<br>' + html.escape('{}'.format(self.comment))
        return comments


    def tlen_inches(self, digits=1):
        if self.tlen:
            length = round(self.tlen * 0.03937, digits)
        else:
            length = None
        return length


    def flen_inches(self, digits=1):
        if self.flen:
            length = round(self.flen * 0.03937, digits)
        else:
            length = None
        return length


    def girth_inches(self, digits=1):
        if self.girth:
            length = round(self.girth * 0.03937, digits)
        else:
            length = None
        return length


    def pounds(self, digits=1):
        if self.rwt:
            wt = round(self.rwt * 0.00220462, digits)
        else:
            wt = None
        return  wt


    def has_latlon(self):
        if self.dd_lat and self.dd_lon:
            return True
        else:
            return False


    def tagstat(self):
        '''By definintion, all of the recoveries from other agencies/the
        general public will have the tag on capture.  This method will ensure
        that the appropriate code is returned for rending in templates.
        '''
        return 'C'

    @property
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

    @tag_colour.setter
    def tag_colour(self, value):
        self._tag_colour = value

    @property
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

    @tag_type.setter
    def tag_type(self, value):
        self._tag_type = value

    @property
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


    @tag_position.setter
    def tag_position(self, value):
        self._tag_position = value


    @property
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


    @tag_origin.setter
    def tag_origin(self, value):
        self._tag_origin = value


    def save(self, *args, **kwargs):
        '''We will need a custom save method to generate tagdoc from tag type,
        colour, position and orgin'''

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



class Database(models.Model):
    '''A lookup table to hole list of master databases.'''
    master_database = models.CharField(max_length=250)
    path = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Master Database"

    def __str__(self):
        '''return the database name as its string representation'''

        return  self.master_database


class Project(models.Model):
    '''A model to hold basic information about the project in which tags
    were deployed or recovered'''

    dbase  = models.ForeignKey(Database)
    year = models.IntegerField(db_index=True)
    prj_cd = models.CharField(db_index=True, max_length=12)
    prj_nm = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True, blank=True, editable=False)

    class Meta:
        ordering = ['-year', 'prj_cd']

    def __str__(self):
        return '{} ({})'.format(self.prj_cd, self.prj_nm)


    #@models.permalink
    def get_absolute_url(self):
        '''return the url for the project'''
        #url = reverse('pjtk2.views.project_detail', kwargs={'slug':self.slug})
        url = 'http://142.143.160.56:8000/projects/projectdetail/{}/'
        url = url.format(slug)
        return url

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
        #super(Project, self).save()


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
    grp = models.CharField(max_length=3)
    fish = models.CharField(max_length=10)
    observation_date = models.DateField()
    grid = models.CharField(max_length=4)
    dd_lat = models.FloatField()
    dd_lon = models.FloatField()

    flen = models.IntegerField(null=True, blank=True)
    tlen = models.IntegerField(null=True, blank=True)
    rwt = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    sex  = models.CharField("Sex", max_length=3,
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
        index_together = ['tagid', 'tagdoc', 'spc']

    def has_latlon(self):
        if self.dd_lat and self.dd_lon:
            return True
        else:
            return False

    def fn_key(self):
        """

        Arguments:
        - `self`:
        """
        base_string = '{}-{}-{}-{}-{}-{}'
        fn_key = base_string.format(self.project.prj_cd, self.sam,
                                    self.eff, self.spc.species_code,
                                    self.grp, self.fish)
        return fn_key




    def __str__(self):
        return '{}<{}>({})'.format(self.tagid, self.tagdoc,
                                   self.observation_date)

    def flen_inches(self):
        if self.flen:
            length = round(self.flen * 0.03937, 1)
        else:
            length = None
        return length

    def tlen_inches(self):
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
                       '        <td>{fn_key}</td>' +
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
                          'fn_key':self.fn_key()}

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
