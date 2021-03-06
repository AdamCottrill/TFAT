from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify

from django.conf import settings


import os
from textwrap import wrap

import html

from common.models import Lake, Species as CommonSpecies

from .constants import (
    REPORTING_CHOICES,
    FOLLOW_UP_STATUS_CHOICES,
    SEX_CHOICES,
    TAG_TYPE_CHOICES,
    TAG_POSITION_CHOICES,
    TAG_ORIGIN_CHOICES,
    TAG_COLOUR_CHOICES,
    TAGSTAT_CHOICES,
    FATE_CHOICES,
    DATE_FLAG_CHOICES,
    LATLON_FLAG_CHOICES,
    PROVINCES_STATE_CHOICES,
    RECOVERY_LETTER_CHOICES,
)


class SpeciesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tagged=True)


class TaggedSpecies(CommonSpecies):
    """This model uses inherites from the common Species Model and
    reflects the subset of species that will be included in the
    tagging application - we don't need to see lamprey and minnows in
    the drop down lists. If a species is not available in the drop
    down lists of forms, update the appropriate species in the admin
    and they will be included the next time the page renders.
    """

    tagged = models.BooleanField(default=False)

    # return all species for admin page, tagged species by default
    all_objects = models.Manager()
    objects = SpeciesManager()

    class Meta:
        ordering = ["spc_nmco"]
        verbose_name_plural = "Tagged Species"

    def __str__(self):

        if self.spc_nmco:
            common_name = self.spc_nmco.title() + " "
        else:
            common_name = ""

        if self.spc_nmsc:
            return "{}({})".format(common_name, self.spc_nmsc)
        else:
            return "{}".format(common_name.strip())


class JoePublic(models.Model):
    """- a person who is reporting one or more recovered tags
    - first name
    - last name
    - home address (street, town, province, postal code)
    - e-mail address(es)
    - phone number(s)
    - AGAFF

    """

    id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=50)
    initial = models.CharField(max_length=5, blank=True, null=True)
    # the address should should be 1-many with a default/current
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)

    province = models.CharField(
        max_length=12, choices=PROVINCES_STATE_CHOICES, blank=True, null=True
    )

    postal_code = models.CharField(max_length=7, blank=True, null=True)
    # this should be 1-many with a default/current
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    # this should be 1-many with a default/current
    affiliation = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name_plural = "Tag Reporters"
        # unique_together = ('last_name', 'first_name')

    def __str__(self):
        if self.initial and self.first_name:
            display = "{} {}. {}".format(self.first_name, self.initial, self.last_name)
        elif self.first_name:
            display = "{} {}".format(self.first_name, self.last_name)
        else:
            display = "{}".format(self.last_name)
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
    """

    + report of a one or more recoveries - contact event with the general
      public
    + reported by an individual
    + support for different formats
      + phone (verbal),
      + letter,
      + e-mail

      TODO - Add functionality to follow-up with reports

    """

    id = models.AutoField(primary_key=True)

    reported_by = models.ForeignKey(
        JoePublic,
        related_name="Reported_By",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    report_date = models.DateTimeField("Report Date", blank=True, null=True)
    date_flag = models.IntegerField("Date Flag", choices=DATE_FLAG_CHOICES, default=0)
    reporting_format = models.CharField(
        "Report Format", max_length=30, choices=REPORTING_CHOICES, default="verbal"
    )
    dcr = models.CharField(max_length=15, blank=True, null=True)
    effort = models.CharField(max_length=15, blank=True, null=True)
    associated_file = models.FileField(
        upload_to="tfat_tag_reports/", blank=True, null=True
    )
    comment = models.CharField(max_length=500, blank=True, null=True)
    # this should be a model like comments in ticket-tracker -what
    # exactly is the follow up and who is it assigned to, who did it.
    follow_up = models.BooleanField(default=False)

    follow_up_status = models.CharField(
        "Follow Up Status",
        max_length=12,
        db_index=True,
        choices=FOLLOW_UP_STATUS_CHOICES,
        default=None,
        blank=True,
        null=True,
    )

    class Meta:

        ordering = ["-report_date"]

    def __str__(self):
        report = ""
        if self.reported_by and self.report_date:
            return "{} on {}".format(
                self.reported_by, self.report_date.strftime("%b-%d-%Y")
            )
        elif self.reported_by:
            return "{} <Report id={}>".format(self.reported_by, self.id)
        else:
            return "<Report id={}>".format(self.id)

    def get_recoveries(self):
        """Retrun any tags assocated with this report:

        Arguments:
        - `self`:
        """
        tags = self.recoveries.select_related("species")
        return tags

    def get_recoveries_with_latlon(self):
        """Return only those tags with a lat-lon value.  Used for plotting on
        maps.  Additional logic could be added to ensure lat-lon are
        valid coordinates.

        Arguments:
        - `self`:

        """

        tags = self.recoveries.select_related()
        tags = [x for x in tags if x.dd_lat and x.dd_lon]
        return tags


class ReportFollowUp(models.Model):
    """A table to hold the response letter(s) associted with a tag
    recovery event."""

    id = models.AutoField(primary_key=True)

    report = models.ForeignKey(
        Report, related_name="followups", on_delete=models.CASCADE
    )

    comment = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    status = models.CharField(
        "Follow Up Status",
        max_length=12,
        db_index=True,
        choices=FOLLOW_UP_STATUS_CHOICES,
        default="requested",
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["report", "status"], name="unique report_status"
            )
        ]

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        self.timestamp = timezone.now()
        return super(ReportFollowUp, self).save(*args, **kwargs)

    def __str__(self):
        """return the complete file name as the string repr"""

        return "ReportFollowup_{}-{}".format(self.report.id, self.get_status_display())


class Recovery(models.Model):
    """

    + recovery event of an actual tag number
    + child of report (one-many relationship)
      + where, when
      + tag number and attributes
      + species, size, gender,
      + clipc
      + fate
      + comment

    """

    id = models.AutoField(primary_key=True)

    report = models.ForeignKey(
        Report, related_name="recoveries", on_delete=models.CASCADE
    )
    # spc = models.ForeignKey(
    #    Species, related_name="recoveries", on_delete=models.CASCADE
    # )

    species = models.ForeignKey(
        TaggedSpecies, related_name="recoveries", on_delete=models.CASCADE
    )

    lake = models.ForeignKey(
        Lake, related_name="recoveries", on_delete=models.CASCADE, default=1
    )

    recovery_date = models.DateField(blank=True, null=True)
    date_flag = models.IntegerField("Date Flag", choices=DATE_FLAG_CHOICES, default=1)
    general_location = models.CharField(
        "General Location", max_length=200, blank=True, null=True
    )
    specific_location = models.CharField(
        "Specific Location", max_length=200, blank=True, null=True
    )
    # eventually this will be an optional map widget
    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)
    latlon_flag = models.IntegerField(
        "Spatial Flag", choices=LATLON_FLAG_CHOICES, default=1
    )
    spatial_followup = models.BooleanField(default=False)

    flen = models.IntegerField("Fork Length", blank=True, null=True)
    tlen = models.IntegerField("Total Length", blank=True, null=True)
    rwt = models.IntegerField("Round Weight", blank=True, null=True)
    girth = models.IntegerField("Girth", blank=True, null=True)

    sex = models.CharField(
        "Sex", max_length=3, choices=SEX_CHOICES, default="9", null=True, blank=True
    )
    # clip information may need to be in a child table and presented as
    # multi-checkbox widget (ie - check all that apply - then calculate
    # clipc from that.)
    clipc = models.CharField("Clip Code", max_length=5, blank=True, null=True)
    tagid = models.CharField(max_length=20, db_index=True)
    _tag_origin = models.CharField(
        "Tag Origin",
        max_length=3,
        db_index=True,
        db_column="tag_origin",
        choices=TAG_ORIGIN_CHOICES,
        default="01",
    )

    _tag_position = models.CharField(
        "Tag Position",
        max_length=3,
        db_index=True,
        db_column="tag_position",
        choices=TAG_POSITION_CHOICES,
        default="1",
    )

    _tag_type = models.CharField(
        "Tag Type",
        max_length=3,
        db_index=True,
        db_column="tag_type",
        choices=TAG_TYPE_CHOICES,
        default="1",
    )

    _tag_colour = models.CharField(
        "Tag Colour",
        max_length=3,
        db_index=True,
        db_column="tag_colour",
        choices=TAG_COLOUR_CHOICES,
        default="2",
    )

    tagdoc = models.CharField(
        "TAGDOC",
        max_length=6,
        # blank=True, null=True,
        db_index=True,
        default="25012",
    )

    tag_removed = models.BooleanField(default=False)
    fate = models.CharField(
        "Fate", max_length=3, blank=True, null=True, choices=FATE_CHOICES, default="R"
    )

    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ["tagdoc", "tagid"]
        index_together = ["tagid", "tagdoc", "species"]

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
            recovery_date = self.recovery_date.strftime("%b-%d-%Y")
            return "{}<{}>({})".format(self.tagid, self.tagdoc, recovery_date)
        else:
            return "{}<{}>".format(self.tagid, self.tagdoc)

    def get_tagid_url(self):
        """return the url for this tag id"""
        url = reverse("tfat:tagid_detail_view", kwargs={"tagid": self.tagid})
        return url

    def tag_applied(self):
        """does this tagid appear in the list of tags that have been applied
        by the OMNR?, returns yes if they species and tagid match a
        tag that has been applied, false otherwise.

        """

        mnr = (
            Encounter.objects.filter(tagid=self.tagid, spc=self.species)
            .filter(Q(tagstat="A") | Q(tagstat="A2"))
            .first()
        )
        if mnr:
            return True
        else:
            return False

    def popup_text(self):
        """A method to return the information that will appear on leaflet
        markers:

        TagID: XXXXX TagDoc: %%%%
        Date: MMM-DD-YYY
        Species: Common Name (Species Code)
        Reported by: first_name last_name
        """

        base_string = (
            "<table>"
            + "    <tr>"
            + "        <td><strong>TagID:</strong></td>"
            + "        <td>{tagid}</td>"
            + "    </tr>"
            + "    <tr>"
            + "        <td><strong>TagDoc:</strong></td>"
            + "        <td>{tagdoc}</td>"
            + "    </tr>"
            + "<tr>"
            + "    <td><strong>Date:</strong></td>"
            + "    <td>{recovery_date}</td>"
            + "</tr>"
            + "    <tr>"
            + "        <td><strong>Species:</strong></td>"
            + "        <td>{common_name} ({species_code})</td>"
            + "    </tr>"
            + "    <tr>"
            + "        <td><strong>Repored By</strong>:</td>"
            + "        <td>{first_name} {last_name}</td>"
            + "    </tr>"
            + "    <tr>"
            + '        <td style="vertical-align: top;"> '
            + "          <strong>Comments:<\strong> "
            + "        </td>"
            + '        <td style="white-space:pre">{comments}</td>'
            + "    </tr>"
            + "</table>"
        )

        if self.recovery_date:
            recovery_date = self.recovery_date.strftime("%b-%d-%Y")
        else:
            recovery_date = "Unknown"

        comments = self.get_comments()
        last_name = html.escape(self.report.reported_by.last_name)
        href = '<a href="{}">{}</a>'.format(self.get_tagid_url(), self.tagid)

        encounter_dict = {
            "tagid": href,
            "tagdoc": self.tagdoc,
            "recovery_date": recovery_date,
            "common_name": self.species.spc_nmco,
            "species_code": self.species.spc,
            "first_name": self.report.reported_by.first_name,
            "last_name": last_name,
            "comments": comments,
        }

        popup = base_string.format(**encounter_dict)

        return popup

    def get_tagid_url(self):
        """return the url for this tag id"""
        url = reverse("tfat:tagid_detail_view", kwargs={"tagid": self.tagid})
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
            comments += html.escape("({})".format(self.specific_location))
        comments = "\\n".join(wrap(comments, 40))
        if self.comment:
            tmp = "\\n".join(wrap(self.comment, 40))
            comments += "<br />" + html.escape("{}".format(tmp))
        comments = comments.replace(os.linesep, "<br />")

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
        return wt

    def has_latlon(self):
        if self.dd_lat and self.dd_lon:
            return True
        else:
            return False

    def tagstat(self):
        """By definintion, all of the recoveries from other agencies/the
        general public will have the tag on capture.  This method will ensure
        that the appropriate code is returned for rending in templates.
        """
        return "C"

    @property
    def tag_colour(self):
        """a little function to parse tag doc and return the tag colour as a
        string."""
        colour = "Unknown"
        if self.tagdoc:
            try:
                key = self.tagdoc[4]
            except IndexError as e:
                key = "9"  # unknown
            choice_dict = {k: v for k, v in TAG_COLOUR_CHOICES}
            colour = choice_dict.get(key, "Unknown")
        return colour

    @tag_colour.setter
    def tag_colour(self, value):
        self._tag_colour = value

    @property
    def tag_type(self):
        """a little function to parse tag doc and return the tag type as a
        string."""
        tag_type = "Unknown"
        if self.tagdoc:
            try:
                key = self.tagdoc[0]
            except IndexError as e:
                key = "9"  # unknown
            choice_dict = {k: v for k, v in TAG_TYPE_CHOICES}
            tag_type = choice_dict.get(key, "Unknown")
        return tag_type

    @tag_type.setter
    def tag_type(self, value):
        self._tag_type = value

    @property
    def tag_position(self):
        """a little function to parse tag doc and return the tag position as a
        string."""
        tag_position = "Unknown"
        if self.tagdoc:
            try:
                key = self.tagdoc[1]
            except IndexError as e:
                key = "9"  # unknown
            choice_dict = {k: v for k, v in TAG_POSITION_CHOICES}
            tag_position = choice_dict.get(key, "Unknown")
        return tag_position

    @tag_position.setter
    def tag_position(self, value):
        self._tag_position = value

    @property
    def tag_origin(self):
        """a little function to parse tag doc and return the tag origin as a
        string."""
        tag_origin = "Unknown"
        if self.tagdoc:
            try:
                key = self.tagdoc[2:4]
            except IndexError as e:
                key = "9"  # unknown
            choice_dict = {k: v for k, v in TAG_ORIGIN_CHOICES}
            tag_origin = choice_dict.get(key, "Unknown")
        return tag_origin

    @tag_origin.setter
    def tag_origin(self, value):
        self._tag_origin = value

    def save(self, *args, **kwargs):
        """We will need a custom save method to generate tagdoc from tag type,
        colour, position and orgin"""

        if len(self.tagdoc) != 5:
            self.tag_type = "9"
            self.tag_position = "9"
            self.tag_origin = "99"
            self.tag_colour = "9"
        else:
            self.tag_type = self.tagdoc[0]
            self.tag_position = self.tagdoc[1]
            self.tag_origin = self.tagdoc[2:4]
            self.tag_colour = self.tagdoc[4]
        super(Recovery, self).save(*args, **kwargs)


class RecoveryLetter(models.Model):
    """A table to hold the response letter(s) associted with a tag
    recovery event."""

    id = models.AutoField(primary_key=True)

    recovery = models.ForeignKey(
        Recovery, related_name="recovery_letters", on_delete=models.CASCADE
    )
    # file will be uploaded to MEDIA_ROOT/uploads
    letter = models.FileField(upload_to="tag_return_letters/")

    zoom = models.IntegerField("Map Zoom", null=True, blank=True)
    method = models.CharField(
        "Generated By",
        max_length=30,
        choices=RECOVERY_LETTER_CHOICES,
        default="tfat_template",
    )
    # TODO:
    # uploaded_by = ForeignKey(User)

    def __str__(self):
        """return the complete file name as the string repr"""

        return "Tagid_{}-{}".format(self.recovery.tagid, str(self.letter))


class Database(models.Model):
    """A lookup table to hold list of master databases."""

    id = models.AutoField(primary_key=True)
    master_database = models.CharField(max_length=250)
    path = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Master Database"

    def __str__(self):
        """return the database name as its string representation"""

        return self.master_database


class Project(models.Model):
    """A model to hold basic information about the project in which tags
    were deployed or recovered"""

    id = models.AutoField(primary_key=True)

    lake = models.ForeignKey(
        Lake, related_name="Projects", on_delete=models.CASCADE, default=1
    )
    dbase = models.ForeignKey(Database, on_delete=models.CASCADE, blank=True, null=True)
    year = models.IntegerField(db_index=True)
    prj_cd = models.CharField(db_index=True, max_length=12)
    prj_nm = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True, blank=True, editable=False)

    class Meta:
        ordering = ["-year", "prj_cd"]

    def __str__(self):
        return "{} ({})".format(self.prj_cd, self.prj_nm)

    # @models.permalink
    def get_absolute_url(self):
        """return the url for the project"""
        # url = reverse('pjtk2.views.project_detail', kwargs={'slug':self.slug})
        PJTK2_DOMAIN = settings.PJTK2_DOMAIN
        url = "{}/projects/projectdetail/{}/"
        url = url.format(PJTK2_DOMAIN, self.slug)
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

        super(Project, self).save(*args, **kwargs)
        # super(Project, self).save()


class Encounter(models.Model):
    """- Encounter
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

    """

    id = models.AutoField(primary_key=True)

    project = models.ForeignKey(
        Project, related_name="Encounters", on_delete=models.CASCADE
    )
    # spc = models.ForeignKey(Species, on_delete=models.CASCADE, blank=True, null=True)
    species = models.ForeignKey(TaggedSpecies, on_delete=models.CASCADE)
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

    sex = models.CharField(
        "Sex", max_length=3, choices=SEX_CHOICES, default="9", null=True, blank=True
    )
    clipc = models.CharField(max_length=5, null=True, blank=True)
    tagid = models.CharField(db_index=True, max_length=20)
    tagdoc = models.CharField(db_index=True, max_length=6, null=True, blank=True)
    tagstat = models.CharField(
        db_index=True,
        max_length=4,
        choices=TAGSTAT_CHOICES,
        default="C",
        null=True,
        blank=True,
    )
    fate = models.CharField(
        max_length=2, choices=FATE_CHOICES, default="C", null=True, blank=True
    )
    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ["tagdoc", "tagid", "observation_date"]
        index_together = ["tagid", "tagdoc", "species"]

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
        base_string = "{}-{}-{}-{}-{}-{}"
        fn_key = base_string.format(
            self.project.prj_cd,
            self.sam,
            self.eff,
            self.species.spc,
            self.grp,
            self.fish,
        )
        return fn_key

    def __str__(self):
        return "{}<{}>({})".format(self.tagid, self.tagdoc, self.observation_date)

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
        return wt

    def marker_class(self):
        if self.tagstat == "A":
            return "applied"
        else:
            return "recap"

    def popup_text(self):
        """A method to return the information that will appear on leaflet
        markers:

        TagID: XXXXX TagDoc: %%%%
        Date: MMM-DD-YYY
        Species: Common Name (Species Code)
        FN Fields: PRJ_CD-SAM-EFF-SPC-GRP-FISH
        """

        base_string = (
            "<table>"
            + "    <tr>"
            + "        <td>TagID:</td>"
            + "        <td>{tagid}</td>"
            + "    </tr>"
            + "    <tr>"
            + "        <td>TagDoc:</td>"
            + "        <td>{tagdoc}</td>"
            + "    </tr>"
            + "<tr>"
            + "    <td>Date:</td>"
            + "    <td>{obs_date}</td>"
            + "</tr>"
            + "<tr>"
            + "    <td>Tag Stattus:</td>"
            + "    <td>{tagstat}</td>"
            + "</tr>"
            + "    <tr>"
            + "        <td>Species: </td>"
            + "        <td>{common_name} ({species_code})</td>"
            + "    </tr>"
            + "    <tr>"
            + "        <td>FN Fields:</td>"
            + "        <td>{fn_key}</td>"
            + "    </tr>"
            + "</table>"
        )

        obs_date = self.observation_date.strftime("%b-%d-%Y")

        href = '<a href="{}">{}</a>'.format(self.get_tagid_url(), self.tagid)

        encounter_dict = {
            "tagid": href,
            "tagdoc": self.tagdoc,
            "tagstat": self.get_tagstat_display(),
            "obs_date": obs_date,
            "common_name": self.species.spc_nmco,
            "species_code": self.species.spc,
            "fn_key": self.fn_key(),
        }

        popup = base_string.format(**encounter_dict)

        return popup

    def get_tagid_url(self):
        """return the url for this tag id"""
        url = reverse("tfat:tagid_detail_view", kwargs={"tagid": self.tagid})
        return url

    def tag_colour(self):
        """a little function to parse tag doc and return the tag colour as a
        string."""
        colour = "Unknown"
        if self.tagdoc:
            try:
                key = self.tagdoc[4]
            except IndexError as e:
                key = "9"  # unknown
            choice_dict = {k: v for k, v in TAG_COLOUR_CHOICES}
            colour = choice_dict.get(key, "Unknown")
        return colour

    def tag_type(self):
        """a little function to parse tag doc and return the tag type as a
        string."""
        tag_type = "Unknown"
        if self.tagdoc:
            try:
                key = self.tagdoc[0]
            except IndexError as e:
                key = "9"  # unknown
            choice_dict = {k: v for k, v in TAG_TYPE_CHOICES}
            tag_type = choice_dict.get(key, "Unknown")
        return tag_type

    def tag_position(self):
        """a little function to parse tag doc and return the tag position as a
        string."""
        tag_position = "Unknown"
        if self.tagdoc:
            try:
                key = self.tagdoc[1]
            except IndexError as e:
                key = "9"  # unknown
            choice_dict = {k: v for k, v in TAG_POSITION_CHOICES}
            tag_position = choice_dict.get(key, "Unknown")
        return tag_position

    def tag_origin(self):
        """a little function to parse tag doc and return the tag origin as a
        string."""
        tag_origin = "Unknown"
        if self.tagdoc:
            try:
                key = self.tagdoc[2:4]
            except IndexError as e:
                key = "9"  # unknown
            choice_dict = {k: v for k, v in TAG_ORIGIN_CHOICES}
            tag_origin = choice_dict.get(key, "Unknown")
        return tag_origin
