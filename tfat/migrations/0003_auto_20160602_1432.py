# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0002_auto_20160531_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-report_date'], 'verbose_name_plural': 'JoePublic'},
        ),
        migrations.AlterModelOptions(
            name='species',
            options={'ordering': ['-primary', 'common_name'], 'verbose_name_plural': 'Species'},
        ),
        migrations.AddField(
            model_name='recovery',
            name='spatial_followup',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(choices=[('3', 'Hermaphrodite'), ('2', 'Female'), ('9', 'Unknown'), ('1', 'Male')], verbose_name='Sex', blank=True, default='9', null=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(choices=[('C', 'Existed on Capture'), ('A', 'Applied')], max_length=4, blank=True, default='C', db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_colour',
            field=models.CharField(choices=[('6', 'Silver'), ('5', 'Orange'), ('2', 'Yellow'), ('4', 'Green'), ('3', 'Red'), ('9', 'Unknown'), ('1', 'Colourless')], max_length=3, verbose_name='Tag Colour', default='2', db_index=True, db_column='tag_colour'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_origin',
            field=models.CharField(choices=[('02', 'New York State'), ('20', 'USGS'), ('13', 'Ontario Hydro'), ('05', 'University of Toronto'), ('10', 'Lakehead University'), ('06', 'State of Ohio'), ('98', 'Other'), ('11', 'Sir Sandford Fleming College'), ('08', 'Royal Ontario Museum'), ('19', 'USWFW'), ('12', 'Private Club'), ('99', 'Unknown'), ('04', 'University of Guelph'), ('07', 'State of Pennsylvania'), ('09', 'State of Minnesota'), ('01', 'Ontario Ministry of Natural Resources'), ('03', 'State of Michigan')], max_length=3, verbose_name='Tag Origin', default='01', db_index=True, db_column='tag_origin'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_position',
            field=models.CharField(choices=[('4', 'Abdominal Insertion'), ('6', 'Jaw'), ('5', 'Flesh of Back'), ('3', 'Posterior Dorsal'), ('2', 'Between Dorsal'), ('7', 'Snout'), ('8', 'Anal'), ('9', 'Unknown'), ('1', 'Anterior Dorsal')], max_length=3, verbose_name='Tag Position', default='1', db_index=True, db_column='tag_position'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_type',
            field=models.CharField(choices=[('3', 'Circular Strap Jaw '), ('A', 'Internal (Radio)'), ('8', 'Secure Tie'), ('4', 'Butt End Jaw '), ('7', 'Strip Vinyl  '), ('5', 'Anchor'), ('1', 'Streamer'), ('6', 'Coded Wire'), ('2', 'Tubular Vinyl'), ('B', 'Metal Livestock')], max_length=3, verbose_name='Tag Type', default='1', db_index=True, db_column='tag_type'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='general_location',
            field=models.CharField(blank=True, null=True, verbose_name='General Location', max_length=200),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(choices=[('3', 'Hermaphrodite'), ('2', 'Female'), ('9', 'Unknown'), ('1', 'Male')], verbose_name='Sex', blank=True, default='9', null=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='specific_location',
            field=models.CharField(blank=True, null=True, verbose_name='Specific Location', max_length=200),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(default='verbal', choices=[('verbal', 'verbal'), ('dcr', 'DCR'), ('other', 'other'), ('letter', 'letter'), ('e-mail', 'e-mail')], verbose_name='Report Format', max_length=30),
        ),
    ]
