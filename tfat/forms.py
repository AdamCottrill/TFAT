'''
=============================================================
c:/1work/Python/djcode/tfat/tfat/forms.py
Created: 15 Jul 2015 14:13:02


DESCRIPTION:

Forms for TFAT

A. Cottrill
=============================================================
'''

from django import forms
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.db.models.fields import BLANK_CHOICE_DASH
from tfat.models import JoePublic, Report, Recovery

from datetime import datetime

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


class JoePublicForm(ModelForm):
    '''A form to capture basic contact information about an angler or
    member of the general public who are reporting a recovered tag.
    '''

    province = forms.ChoiceField(choices=BLANK_CHOICE_DASH +
                                 list(PROVINCES_STATE_CHOICES),
                                 widget=forms.Select(attrs={'class':'form-control'}),
                                 required=False)

    def __init__(self, *args, **kwargs):
        super(JoePublicForm, self).__init__(*args, **kwargs)

    class Meta:
        model = JoePublic
        fields = [
            'first_name',
            'initial',
            'last_name',
            'address1',
            'address2',
            'town',
            'province',
            'postal_code',
            'email',
            'phone',
            'affiliation',]


class CreateJoePublicForm(JoePublicForm):
    '''A form to capture basic contact information about an angler or
    member of the general public who are reporting a recovered tag
    when creating a new user.  This form inherits from the basic
    JoePublic model form and adds a checkbox widget and additional
    logic to catch users with the same first and last name.  The first
    time it is called, the widget is hidden and the form will fail if
    a user by that name already exists.  When the form is returned to
    the user, the checkbox is made visible and must be checked for the
    form to work - in which case a user with the same first and last
    name is created.

    '''

    same_name = forms.BooleanField(widget=HiddenInput(attrs={'value':False}),
                                   initial=False, required=False)


    def clean(self):
        cleaned_data = super(JoePublicForm, self).clean()
        same_name = cleaned_data.get('same_name', False)
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        anglers = JoePublic.objects.filter(first_name__iexact=first_name,
                                           last_name__iexact=last_name).all()

        if not same_name and len(anglers)>0:
            self.fields['same_name'].widget = forms.CheckboxInput()
            msg = ('{} {} already exists. Do you want to use one of the '
                   ' existing anglers with that name or create another?')
            raise forms.ValidationError(msg.format(first_name, last_name))
        return cleaned_data


class ReportForm(ModelForm):
    '''A form to capture information with a report of one or more
    recaptured tags.'''

    dcr = forms.CharField(required=False)
    eff_num = forms.CharField(required=False)
    report_file = forms.FileField(required=False)

    class Meta:
        model = Report
        fields = ['report_date', 'date_flag', 'reporting_format', 'comment',
                  'follow_up']

        widgets = {
            'report_date':forms.DateInput(attrs={'class':'datepicker'}),
            'reporting_format':forms.Select(attrs={'class':'form-control'}),
            'date_flag':forms.Select(attrs={'class':'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 10}),
        }

    def clean(self):
        cleaned_data = super(ReportForm, self).clean()
        report_date = cleaned_data.get('report_date')
        if not report_date:
            cleaned_data['date_flag'] = 0 #unknown
            cleaned_data['report_date'] = datetime.today().date()
        return cleaned_data



#    reported_by  = forms.ForeignKey(JoePublic, related_name="Reported_By",
#                                  blank=True, null=True)
#    report_date = forms.DateTimeField(blank=True, null=True)
#    date_flag = forms.IntegerField("Date Flag",
#                               choices=DATE_FLAG_CHOICES, default=1)
#    reporting_format = forms.CharField("Report Format", max_length=30,
#                               choices=REPORTING_CHOICES, default="verbal")
#    comment = forms.CharField(max_length=500, blank=True, null=True)
#    #this should be a model like comments in ticket-tracker -what
#    #exactly is the follow up and who is it assigned to, who did it.
#    follow_up  = forms.BooleanField(default=False)


class RecoveryForm(forms.Form):
    '''A form to capture the information associated with a recaptured tag
    reported by an angler'''

    pass


#    report  = forms.ForeignKey(Report, related_name="Report")
#    spc  = forms.ForeignKey(Species, related_name="Species")
#
#    recovery_date = forms.DateField(blank=True, null=True)
#    date_flag = forms.IntegerField("Date Flag",
#                               choices=DATE_FLAG_CHOICES, default=1)
#    general_name = forms.CharField(max_length=50,blank=True, null=True)
#    specific_name = forms.CharField(max_length=50,blank=True, null=True)
#    #eventually this will be an optional map widget
#    dd_lat = forms.FloatField(blank=True, null=True)
#    dd_lon = forms.FloatField(blank=True, null=True)
#    latlon_flag = forms.IntegerField("Spatial Flag",
#                               choices=LATLON_FLAG_CHOICES, default=1)
#
#    flen = forms.IntegerField(blank=True, null=True)
#    tlen = forms.IntegerField(blank=True, null=True)
#    rwt = forms.IntegerField(blank=True, null=True)
#
#    sex  = forms.CharField("Sex", max_length=30,
#                            choices=SEX_CHOICES, default="9",
#                            null=True, blank=True)
#    #clip information may need to be in a child table and presented as
#    #multi-checkbox widget (ie - check all that apply - then calculate
#    #clipc from that.)
#    clipc = forms.CharField(max_length=5,blank=True, null=True)
#    tagid = forms.CharField(max_length=10, db_index=True)
#    tag_origin  = forms.CharField("Tag Origin", max_length=3,db_index=True,
#                               choices=TAG_ORIGIN_CHOICES, default="01")
#
#    tag_position = forms.CharField("Tag Position", max_length=3, db_index=True,
#                                    choices=TAG_POSITION_CHOICES, default="1")
#    tag_type = forms.CharField("Tag Type", max_length=3, db_index=True,
#                               choices=TAG_TYPE_CHOICES, default="1")
#
#    tag_colour = forms.CharField("Tag Colour", max_length=3, db_index=True,
#                               choices=TAG_COLOUR_CHOICES, default="2")
#
#    #tagdoc will be caclulated from tag type, position, origin and
#    #colour following fishnet-II definitions
#    tagdoc =  forms.CharField(max_length=6,blank=True, null=True,
#                               db_index=True)
#
#    tag_removed = forms.BooleanField(default=False)
#    fate = forms.CharField("Fate", max_length=30, blank=True, null=True,
#                               choices=FATE_CHOICES, default="R")
#    comment = forms.CharField(max_length=500, blank=True, null=True)
