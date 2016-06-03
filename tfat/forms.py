'''=============================================================
c:/1work/Python/djcode/tfat/tfat/forms.py
Created: 15 Jul 2015 14:13:02

DESCRIPTION:

Forms for TFAT including forms to create/edit anglers, reports, and
recovery events.

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
                        CLIP_CODE_CHOICES,
                        DATE_FLAG_CHOICES,
                        LATLON_FLAG_CHOICES,
                        PROVINCES_STATE_CHOICES)

FATE_CHOICES_WITH_UNKN = [('', 'Unknown')] + FATE_CHOICES


TODAY = datetime.today().date()

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
    efffort = forms.CharField(required=False)
    associated_file = forms.FileField(required=False)

    class Meta:
        model = Report
        fields = ['reported_by', 'report_date', 'date_flag', 'reporting_format',
                  'comment', 'associated_file', 'dcr', 'effort', 'follow_up']

        widgets = {
            'reported_by':forms.HiddenInput(),
            'report_date':forms.DateInput(attrs={'class':
                                                 'form-control datepicker',
                                                 'placeholder':TODAY}),
            'date_flag':forms.Select(attrs={'class':'form-control'}),
            'reporting_format':forms.Select(attrs={'class':'form-control'}),
            'dcr':forms.TextInput(attrs={'class':'form-control'}),
            'effort':forms.TextInput(attrs={'class':'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['reporting_format'].required = False
        self.fields['date_flag'].required = False

    def clean_reporting_format(self):
        """Provide a default value if it is null.

        Arguments:
        - `self`:
        """
        report_format = self.cleaned_data['reporting_format']

        if report_format is None or report_format == '':
            report_format = 'verbal'
        return report_format


    def clean_report_date(self):
        """dates in the future are not allowed!

        Arguments:
        - `self`:
        """
        report_date = self.cleaned_data['report_date']
        today = datetime.today()

        if report_date:
            if report_date.date() > today.date():
                err_msg = 'Dates in the future are not allowed.'
                raise forms.ValidationError(err_msg)
        return report_date


    def clean_dcr(self):
        """If dcr contains and empty string, return None, otherwise return
        it's value.'

        Arguments:
        - `self`:

        """
        dcr = self.cleaned_data['dcr']
        if dcr == '':
            return None
        return dcr


    def clean_effort(self):
        """If the effort contains and empty string, return None otherwise
        return it's value.'

        Arguments:
        - `self`:

        """
        effort = self.cleaned_data['effort']
        if effort == '':
            return None
        return effort



    def clean_date_flag(self):
        """Provide a default value if it is null.
        Arguments:
        - `self`:
        """
        date_flag = self.cleaned_data['date_flag']
        if date_flag is None or date_flag == '':
            date_flag = 0
        return date_flag


    def clean(self):
        cleaned_data = super(ReportForm, self).clean()
        report_date = cleaned_data.get('report_date')

        report_format = cleaned_data.get('reporting_format')
        dcr = cleaned_data.get('dcr')
        effort = cleaned_data.get('effort')

        if report_format =='dcr':
            if dcr is None or dcr=='':
                err_msg = 'DCR number is required if reported by "DCR".'
                raise forms.ValidationError(err_msg)
            if effort is None or effort=='':
                err_msg = 'Effort number is required if reported by "DCR".'
                raise forms.ValidationError(err_msg)
        else:
            if dcr and dcr!='':
                err_msg = 'DCR should be empty if Report Format is not "DCR".'
                raise forms.ValidationError(err_msg)
            if effort and effort!='':
                err_msg = 'Effort should be empty if Report Format is not "DCR".'
                raise forms.ValidationError(err_msg)

        if not report_date:
            cleaned_data['date_flag'] = 0 #unknown
            cleaned_data['report_date'] = datetime.today().date()

        return cleaned_data


class RecoveryForm(ModelForm):
    '''A form to capture the information associated with a recaptured tag
    reported by an angler'''

    latlon_flag = forms.ChoiceField(label = "Spatial Flag", required = False,
                                    choices = LATLON_FLAG_CHOICES,
                                    widget=forms.RadioSelect(
                                        attrs={'class':'radio-inline'}),
                                    initial=1)

    fate = forms.TypedChoiceField(choices=FATE_CHOICES_WITH_UNKN,
                                  initial='K',
                                  required=False)

    class Meta:
        model = Recovery
        fields = [ 'tagid', 'spc', 'recovery_date', 'date_flag',
                   'general_location', 'specific_location', 'dd_lat', 'dd_lon',
                   'latlon_flag', 'spatial_followup',
                    'tagdoc', 'tag_removed', 'fate',
                    'flen', 'tlen', 'rwt', 'sex', 'clipc',
                   'comment',]

        widgets = {

            'tagid':forms.TextInput(attrs={'class':'form-control'}),
            'spc':forms.Select(attrs={'class':'form-control'}),
            'recovery_date':forms.DateInput(attrs={'class':
                                                 'form-control datepicker',
                                                 'placeholder':TODAY}),
            'date_flag':forms.Select(attrs={'class':'form-control'},),

            'tagdoc':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'25012'}),
            'specific_location':forms.TextInput(attrs={'class':'form-control'}),
            'general_location':forms.TextInput(attrs={'class':'form-control'}),
            'dd_lat':forms.TextInput(attrs={'class':'form-control'}),
            'dd_lon':forms.TextInput(attrs={'class':'form-control'}),
            'tag_removed':forms.CheckboxInput(attrs={'class':'form-control'}),
            #'fate':forms.Select(attrs={'class':'form-control'}),
            'flen':forms.TextInput(attrs={'class':'form-control metric',
                                          'placeholder':'mm'}),
            'tlen':forms.TextInput(attrs={'class':'form-control metric',
                                          'placeholder':'mm'}),
            'rwt':forms.TextInput(attrs={'class':'form-control metric',
                                         'placeholder':'grams'}),
            'sex':forms.Select(attrs={'class':'form-control'}),
            'clipc':forms.TextInput(attrs={'class':'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 10}),
        }


    def __init__(self, *args, **kwargs):
        self.report_id = kwargs.pop('report_id')
        super(RecoveryForm, self).__init__(*args, **kwargs)


    def save(self, report, *args, **kwargs):
        recovery = super(RecoveryForm, self).save(commit=False)
        recovery.report = report
        recovery.save()
        return recovery

    def clean_tagdoc(self):
        '''tagdoc is a required field.  It must be 5 characters long.  Its
        constituent parts must correspond to values in the lookup tables for
        tag type, tag position, tag origins. and tag colour'''

        tagdoc = self.cleaned_data['tagdoc']

        if len(tagdoc) != 5:
            err_msg = 'TAGDOC must be 5 characters long.'
            raise forms.ValidationError(err_msg)
        tag_type = tagdoc[0]
        tag_position = tagdoc[1]
        tag_origins = tagdoc[2:4]
        tag_colour = tagdoc[4]

        if tag_type not in [x[0] for x in TAG_TYPE_CHOICES]:
            err_msg = '{} is not a valid tag type code.'.format(tag_type)
            raise forms.ValidationError(err_msg)

        elif tag_position not in [x[0] for x in TAG_POSITION_CHOICES]:
            err_msg = '{} is not a valid tag position code.'
            err_msg = err_msg.format(tag_position)
            raise forms.ValidationError(err_msg)

        elif tag_origins not in [x[0] for x in TAG_ORIGIN_CHOICES]:
            err_msg = '{} is not a valid agency code.'.format(tag_origins)
            raise forms.ValidationError(err_msg)

        elif tag_colour not in [x[0] for x in TAG_COLOUR_CHOICES]:
            err_msg = '{} is not a valid colour code.'.format(tag_colour)
            raise forms.ValidationError(err_msg)
        else:
            return tagdoc


    def clean_clipc(self):
        '''if clipc is populated, all of its elements must be valid clips
        (i.e. - in the lookup table).  Elements must not repeat, and
        if the clipc contains 0, it can be only 0.  Finally, clipc
        code is returned in ascii sort order, regardless of how it is
        passed in.
        '''
        clipc = self.cleaned_data['clipc']
        clips = list(clipc)
        unique_clips = set(clips)
        valid_clips = [x[0] for x in CLIP_CODE_CHOICES]
        invalid_clips = unique_clips - set(valid_clips)

        if '0' in clipc and len(clipc) > 1:
            err_msg = 'CLIPC cannot contain 0 and other clip codes.'
            raise forms.ValidationError(err_msg)

        #check for clip codes that are not in our list of valid clips:
        elif invalid_clips:
            invalid_clips = list(invalid_clips)
            invalid_clips.sort()
            invalid_clips = ','.join(invalid_clips)
            err_msg = 'Invalid clip codes: {}'.format(invalid_clips)
            raise forms.ValidationError(err_msg)

        elif len(list(unique_clips)) != len(clips):
            err_msg = 'Clip codes cannot repeat.'
            raise forms.ValidationError(err_msg)
        else:
            clips.sort()
            return ''.join(clips)


    def clean_date_flag(self):
        """Provide a default value if it is null.
        Arguments:
        - `self`:
        """
        date_flag = self.cleaned_data['date_flag']
        if date_flag is None or date_flag == '':
            date_flag = 0
        return date_flag


    def clean_recovery_date(self):
        """dates in the future are not allowed!

        Arguments:
        - `self`:
        """
        recovery_date = self.cleaned_data['recovery_date']
        today = datetime.today()

        try:
            report_date = Report.objects.values_list('report_date')\
                                        .get(id=self.report_id)[0]
        except Report.DoesNotExist:
            report_date = None


        if recovery_date:
            if recovery_date > today.date():
                err_msg = 'Dates in the future are not allowed.'
                raise forms.ValidationError(err_msg)
            if report_date:
                if recovery_date > report_date.date():
                    err_msg = 'Recovery date occurs after report date.'
                    raise forms.ValidationError(err_msg)
        return recovery_date


    def clean_dd_lon(self):
        '''if dd_lon is populated it must be between -90 and 90.  If dd_lat is
        populated, dd_lon is also required.'''

        dd_lon = self.cleaned_data.get('dd_lon')
        if dd_lon:
            if dd_lon < -180 or dd_lon >180:
                err_msg = 'dd_lon must be numeric and lie between -180 and 180'
                raise forms.ValidationError(err_msg)
        return dd_lon


    def clean_dd_lat(self):
        '''if dd_lat is populated it must be between -90 and 90.  If ddlon is
        populated, dd_lat is also required.'''

        dd_lat = self.cleaned_data.get('dd_lat')

        if dd_lat:
            if dd_lat < -90 or dd_lat >90:
                err_msg = 'dd_lat must be numeric and lie between -90 and 90'
                raise forms.ValidationError(err_msg)
        return dd_lat


    def clean(self):
        """

        Arguments:
        - `self`:
        """

        cleaned_data = self.cleaned_data

        ## DD_LAT DD_LON
        dd_lat = cleaned_data.get('dd_lat')
        dd_lon = cleaned_data.get('dd_lon')
        latlon_flag = cleaned_data.get('latlon_flag')

        if dd_lat is None and dd_lon is None:
            cleaned_data['latlon_flag'] = 0
        elif dd_lat is None and dd_lon is not None:
            err_msg = 'If dd_lon is populated,  dd_lat must be populated too'
            raise forms.ValidationError(err_msg)
        elif dd_lat is not None and dd_lon is None:
            err_msg = 'If dd_lat is populated,  dd_lon must be populated too'
            raise forms.ValidationError(err_msg)
        else:
            cleaned_data['latlon_flag'] = latlon_flag

        #if lat-long is derived, make sure comment contains something
        #(hopefully an explanation).
        comment = cleaned_data.get('comment')

        if latlon_flag=='2' and (comment is None or comment == ''):
            err_msg = 'Describe how location was derived.'
            raise forms.ValidationError(err_msg)

        #  RECOVERY DATE vs DATE_FLAG
        # if no date is provided, date_flag cannot be reported:
        recovery_date = cleaned_data.get('recovery_date')
        date_flag = cleaned_data['date_flag']
        if (recovery_date is None or recovery_date=='') and date_flag != 0:
            err_msg = 'Date flag must be "Unknown" if no date is provided.'
            raise forms.ValidationError(err_msg)

        ## TLEN vs FLEN
        flen = cleaned_data.get('flen')
        tlen = cleaned_data.get('tlen')
        if flen and tlen:
            if flen > tlen:
                err_msg = ("Total length (tlen) cannot be less than "
                           "fork length (flen).")
                raise forms.ValidationError(err_msg)

        return cleaned_data
