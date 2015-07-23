# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0010_auto_20150626_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='associated_file',
            field=models.FileField(null=True, upload_to='', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='dcr',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='effort',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='fate',
            field=models.CharField(max_length=2, null=True, default='C', blank=True, choices=[('K', 'Killed'), ('R', 'Released')]),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(verbose_name='Sex', choices=[('9', 'Unknown'), ('3', 'Hermaphrodite'), ('1', 'Male'), ('2', 'Female')], max_length=30, null=True, default='9', blank=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(choices=[('C', 'Existed on Capture'), ('A', 'Applied')], max_length=4, null=True, default='C', db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='joepublic',
            name='province',
            field=models.CharField(max_length=12, null=True, blank=True, choices=[('ON', 'Ontario'), ('AB', 'Alberta'), ('BC', 'British Columbia'), ('MB', 'Manitoba'), ('NB', 'New Brunswick'), ('NL', 'Newfoundland and Labrador'), ('NS', 'Nova Scotia'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut'), ('PE', 'Prince Edward Island'), ('QC', 'Quebec'), ('SK', 'Saskatchewan'), ('YT', 'Yukon'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='fate',
            field=models.CharField(verbose_name='Fate', choices=[('K', 'Killed'), ('R', 'Released')], max_length=30, null=True, default='R', blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(verbose_name='Sex', choices=[('9', 'Unknown'), ('3', 'Hermaphrodite'), ('1', 'Male'), ('2', 'Female')], max_length=30, null=True, default='9', blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(max_length=3, default='2', verbose_name='Tag Colour', db_index=True, choices=[('3', 'Red'), ('6', 'Other'), ('9', 'Unknown'), ('4', 'Green'), ('2', 'Yellow'), ('5', 'Orange'), ('1', 'Colourless')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(max_length=3, default='01', verbose_name='Tag Origin', db_index=True, choices=[('09', 'State of Minnesota'), ('19', 'Other'), ('02', 'New York State'), ('04', 'University of Guelph'), ('06', 'State of Ohio'), ('08', 'Royal Ontario Museum'), ('07', 'State of Pennsylvania'), ('03', 'State of Michigan'), ('99', 'Unknown'), ('01', 'Ontario Ministry of Natural Resources'), ('05', 'University of Toronto'), ('11', 'Sir Sandford Fleming College'), ('13', 'Ontario Hydro'), ('10', 'Lakehead University'), ('12', 'Private Club')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(max_length=3, default='1', verbose_name='Tag Position', db_index=True, choices=[('6', 'Jaw'), ('7', 'Snout'), ('4', 'Abdominal Insertion'), ('1', 'Anterior Dorsal'), ('9', 'Unknown'), ('5', 'Flesh of Back'), ('3', 'Posterior Dorsal'), ('2', 'Between Dorsal'), ('8', 'Anal')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(max_length=3, default='1', verbose_name='Tag Type', db_index=True, choices=[('4', 'Butt End Jaw '), ('8', 'Secure Tie'), ('5', 'Anchor'), ('3', 'Circular Strap Jaw '), ('7', 'Strip Vinyl  '), ('2', 'Tubular Vinyl'), ('X', 'Tag Scar/obvious loss'), ('1', 'Streamer'), ('A', 'Internal (Radio)'), ('9', 'Type Unknown or not applicable'), ('0', 'No tag'), ('6', 'Coded Wire')]),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(max_length=30, default='verbal', verbose_name='Report Format', choices=[('verbal', 'verbal'), ('dcr', 'DCR'), ('other', 'other'), ('letter', 'letter'), ('e-mail', 'e-mail')]),
        ),
    ]
