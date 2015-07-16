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
from tfat.models import JoePublic, Recovery


class JoePublicForm(ModelForm):
    '''A form to capture basic contact information about an angler or
    member of the general public who are reporting a recovered tag.
    '''

    force_save = forms.BooleanField(initial=False, widget=HiddenInput())

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


    def clean(self):

        force = self.cleaned_data.get('force_save',False)
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        anglers = JoePublic.objects.filter(first_name=first_name,
                                           last_name=last_name).all()
        if not force and len(anglers)>0:
            self.fields['force_save'] = forms.BooleanField(initial = True,
                                                           widget=HiddenInput())
            msg = '{} {} already exists? View existing anglers with that name or create another?'
            raise forms.ValidationError(msg.format(first_name, last_name))
        return self.cleaned_data


#    first_name = forms.CharField(max_length=15)
#    last_name = forms.CharField(max_length=50)
#    initial = forms.CharField(max_length=50)
#    # the address should should be 1-many with a default/current
#    address1 = forms.CharField(max_length=50)
#    address2 = forms.CharField(max_length=50)
#    town = forms.CharField(max_length=50)
#    #this could be a lookup
#    province = forms.CharField(max_length=12)
#    postal_code = forms.CharField(max_length=7)
#    #this should be 1-many with a default/current
#    email = forms.EmailField()
#    phone = forms.CharField(max_length=15)
#    affiliation = forms.CharField(max_length=50)
#

class ReportForm(forms.Form):
    '''A form to capture information with a report of one or more
    recaptured tags.'''
    pass

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
