from django.db import models

from django.template.defaultfilters import slugify



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
    initial = models.CharField(max_length=50)
    # the address should should be 1-many with a default/current
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    #this could be a lookup
    province = models.CharField(max_length=12)
    postal_code = models.CharField(max_length=7)
    #this should be 1-many with a default/current
    email = models.CharField(max_length=50)
    #this should be 1-many with a default/current
    affiliation = models.CharField(max_length=50)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        if self.initial:
            display = '{} {} {}'.format(self.first_name, self.initial,
                                        self.last_name)
        else:
            display = '{} {}'.format(self.first_name, self.last_name)
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

    REPORTING_CHOICES = {
        ('verbal', 'verbal'),
        ('e-mail', 'e-mail'),
        ('letter', 'letter'),
        ('other', 'other'),
    }


    reported_by  = models.ForeignKey(JoePublic, related_name="Reported_By",
                                  blank=True, null=True)
    date_reported = models.DateTimeField()
    reporting_format = models.CharField("Report Format", max_length=30,
                               choices=REPORTING_CHOICES, default="verbal")
    comment = models.CharField(max_length=500)
    #this should be a model like comments in ticket-tracker -what
    #exactly is the follow up and who is it assigned to, who did it.
    follow_up  = models.BooleanField(default=False)

    def __str__(self):
        return '{} on {}'.format(self.reported_by, self.date_reported)


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

    TAG_TYPE_CHOICES = {
        ('0', 'No tag'),
        ('1', 'Streamer'),
        ('2', 'Tubular Vinyl'),
        ('3', 'Circular Strap Jaw '),
        ('4', 'Butt End Jaw '),
        ('5', 'Anchor'),
        ('6', 'Coded Wire'),
        ('7', 'Strip Vinyl  '),
        ('8', 'Secure Tie'),
        ('9', 'Type Unknown or not applicable'),
        ('A', 'Internal (Radio)'),
        ('X', 'Tag Scar/obvious loss'),
    }

    TAG_POSITION_CHOICES = {
        ('1', 'Anterior Dorsal'),
        ('2', 'Between Dorsal'),
        ('3', 'Posterior Dorsal'),
        ('4', 'Abdominal Insertion'),
        ('5', 'Flesh of Back'),
        ('6', 'Jaw'),
        ('7', 'Snout'),
        ('8', 'Anal'),
        ('9', 'Unknown')
    }


    TAG_ORIGIN_CHOICES = {
        ('01', 'Ontario Ministry of Natural Resources'),
        ('02', 'New York State'),
        ('03', 'State of Michigan'),
        ('04', 'University of Guelph'),
        ('05', 'University of Toronto'),
        ('06', 'State of Ohio'),
        ('07', 'State of Pennsylvania'),
        ('08', 'Royal Ontario Museum'),
        ('09', 'State of Minnesota'),
        ('10', 'Lakehead University'),
        ('11', 'Sir Sandford Fleming College'),
        ('12', 'Private Club'),
        ('13', 'Ontario Hydro'),
        ('19', 'Other'),
        ('99', 'Unknown')
    }

    TAG_COLOUR_CHOICES = {
        ('1', 'Colourless'),
        ('2', 'Yellow'),
        ('3', 'Red'),
        ('4', 'Green'),
        ('5', 'Orange'),
        ('6', 'Other'),
        ('9', 'Unknown')
    }


    SEX_CHOICES = {
        ('1', 'Male'),
        ('2', 'Female'),
        ('3', 'Hermaphrodite'),
        ('9', 'Unknown')
    }

    FATE_CHOICES = {
        ('R', 'Released'),
        ('K', 'Killed'),
    }


    report  = models.ForeignKey(Report, related_name="Report")
    spc  = models.ForeignKey(Species, related_name="Species")

    recovery_date = models.DateField()
    general_name = models.CharField(max_length=50)
    specific_name = models.CharField(max_length=50)
    #eventually this will be an optional map widget
    dd_lat = models.FloatField()
    dd_lon = models.FloatField()

    flen = models.IntegerField()
    tlen = models.IntegerField()
    rwt = models.IntegerField()

    sex  = models.CharField("Sex", max_length=30,
                            choices=SEX_CHOICES, default="9",
                            null=True, blank=True)
    #clip information may need to be in a child table and presented as
    #multi-checkbox widget (ie - check all that apply - then calculate
    #clipc from that.)
    clipc = models.CharField(max_length=5)
    tagid = models.CharField(max_length=10)
    tag_origin  = models.CharField("Tag Origin", max_length=30,
                               choices=TAG_ORIGIN_CHOICES, default="01")

    tag_position  = models.CharField("Tag Position", max_length=30,
                               choices=TAG_POSITION_CHOICES, default="1")
    tag_type  = models.CharField("Tag Type", max_length=30,
                               choices=TAG_TYPE_CHOICES, default="1")

    tag_colour = models.CharField("Tag Colour", max_length=30,
                               choices=TAG_COLOUR_CHOICES, default="2")

    #tagdoc will be caclulated from tag type, position, origin and
    #colour following fishnet-II definitions
    tagdoc =  models.CharField(max_length=6)

    tag_removed = models.BooleanField(default=False)
    fate = models.CharField("Fate", max_length=30,
                               choices=FATE_CHOICES, default="R")

    comment = models.CharField(max_length=500)

    class Meta:
        ordering = ['tagdoc', 'tagid']


    def __str__(self):
        return '{}<{}>({})'.format(self.tagid, self.tagdoc, self.recovery_date)

    def save(self):
        '''We will need a custom save method to generate tagdoc from tag type,
        colour, position and orgin'''
        pass


class Project(models.Model):
    '''A model to hold basic information about the project in which tags
    were deployed or recovered'''

    prj_cd = models.CharField(max_length=12)
    prj_nm = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, editable=False)

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

    SEX_CHOICES = {
        ('1', 'Male'),
        ('2', 'Female'),
        ('3', 'Hermaphrodite'),
        ('9', 'Unknown')
    }

    project  = models.ForeignKey(Project, related_name="Project")
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
    tagid = models.CharField(max_length=10)
    tagdoc =  models.CharField(max_length=6, null=True, blank=True)

    class Meta:
        ordering = ['tagdoc', 'tagid']


    def __str__(self):
        return '{}<{}>({})'.format(self.tagid, self.tagdoc,
                                   self.observation_date)
