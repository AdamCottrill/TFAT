# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0003_auto_20160602_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='recovery',
            name='girth',
            field=models.IntegerField(null=True, blank=True, verbose_name='Round Weight'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(max_length=3, null=True, choices=[('3', 'Hermaphrodite'), ('2', 'Female'), ('1', 'Male'), ('9', 'Unknown')], blank=True, verbose_name='Sex', default='9'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(max_length=4, null=True, choices=[('A', 'Applied'), ('C', 'Existed on Capture')], blank=True, default='C', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_colour',
            field=models.CharField(max_length=3, choices=[('2', 'Yellow'), ('9', 'Unknown'), ('1', 'Colourless'), ('5', 'Orange'), ('6', 'Silver'), ('4', 'Green'), ('3', 'Red')], verbose_name='Tag Colour', db_column='tag_colour', default='2', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_origin',
            field=models.CharField(max_length=3, choices=[('08', 'Royal Ontario Museum'), ('99', 'Unknown'), ('98', 'Other'), ('11', 'Sir Sandford Fleming College'), ('05', 'University of Toronto'), ('01', 'Ontario Ministry of Natural Resources'), ('20', 'USGS'), ('19', 'USWFW'), ('03', 'State of Michigan'), ('13', 'Ontario Hydro'), ('10', 'Lakehead University'), ('07', 'State of Pennsylvania'), ('04', 'University of Guelph'), ('12', 'Private Club'), ('06', 'State of Ohio'), ('09', 'State of Minnesota'), ('02', 'New York State')], verbose_name='Tag Origin', db_column='tag_origin', default='01', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_position',
            field=models.CharField(max_length=3, choices=[('5', 'Flesh of Back'), ('2', 'Between Dorsal'), ('7', 'Snout'), ('3', 'Posterior Dorsal'), ('4', 'Abdominal Insertion'), ('1', 'Anterior Dorsal'), ('9', 'Unknown'), ('8', 'Anal'), ('6', 'Jaw')], verbose_name='Tag Position', db_column='tag_position', default='1', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_type',
            field=models.CharField(max_length=3, choices=[('8', 'Secure Tie'), ('6', 'Coded Wire'), ('2', 'Tubular Vinyl'), ('4', 'Butt End Jaw '), ('7', 'Strip Vinyl  '), ('A', 'Internal (Radio)'), ('3', 'Circular Strap Jaw '), ('B', 'Metal Livestock'), ('5', 'Anchor'), ('1', 'Streamer')], verbose_name='Tag Type', db_column='tag_type', default='1', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='date_flag',
            field=models.IntegerField(default=1, choices=[(1, 'Reported'), (2, 'Derived'), (0, 'Unknown')], verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='latlon_flag',
            field=models.IntegerField(default=1, choices=[(1, 'Reported'), (2, 'Derived'), (0, 'Unknown')], verbose_name='Spatial Flag'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(max_length=3, null=True, choices=[('3', 'Hermaphrodite'), ('2', 'Female'), ('1', 'Male'), ('9', 'Unknown')], blank=True, verbose_name='Sex', default='9'),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(default=1, choices=[(1, 'Reported'), (2, 'Derived'), (0, 'Unknown')], verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(max_length=30, choices=[('letter', 'letter'), ('verbal', 'verbal'), ('other', 'other'), ('dcr', 'DCR'), ('e-mail', 'e-mail')], verbose_name='Report Format', default='verbal'),
        ),
    ]
