# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='primary',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='fate',
            field=models.CharField(max_length=2, default='C', blank=True, choices=[('R', 'Released'), ('K', 'Killed')], null=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(max_length=3, verbose_name='Sex', choices=[('9', 'Unknown'), ('3', 'Hermaphrodite'), ('2', 'Female'), ('1', 'Male')], blank=True, null=True, default='9'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(max_length=4, choices=[('A', 'Applied'), ('C', 'Existed on Capture')], blank=True, null=True, default='C', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_colour',
            field=models.CharField(max_length=3, verbose_name='Tag Colour', choices=[('1', 'Colourless'), ('3', 'Red'), ('4', 'Green'), ('9', 'Unknown'), ('2', 'Yellow'), ('6', 'Silver'), ('5', 'Orange')], db_column='tag_colour', default='2', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_origin',
            field=models.CharField(max_length=3, verbose_name='Tag Origin', choices=[('99', 'Unknown'), ('19', 'USWFW'), ('09', 'State of Minnesota'), ('13', 'Ontario Hydro'), ('06', 'State of Ohio'), ('03', 'State of Michigan'), ('04', 'University of Guelph'), ('20', 'USGS'), ('10', 'Lakehead University'), ('98', 'Other'), ('01', 'Ontario Ministry of Natural Resources'), ('08', 'Royal Ontario Museum'), ('02', 'New York State'), ('12', 'Private Club'), ('07', 'State of Pennsylvania'), ('11', 'Sir Sandford Fleming College'), ('05', 'University of Toronto')], db_column='tag_origin', default='01', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_position',
            field=models.CharField(max_length=3, verbose_name='Tag Position', choices=[('7', 'Snout'), ('5', 'Flesh of Back'), ('3', 'Posterior Dorsal'), ('9', 'Unknown'), ('4', 'Abdominal Insertion'), ('1', 'Anterior Dorsal'), ('2', 'Between Dorsal'), ('8', 'Anal'), ('6', 'Jaw')], db_column='tag_position', default='1', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_type',
            field=models.CharField(max_length=3, verbose_name='Tag Type', choices=[('7', 'Strip Vinyl  '), ('8', 'Secure Tie'), ('4', 'Butt End Jaw '), ('5', 'Anchor'), ('2', 'Tubular Vinyl'), ('1', 'Streamer'), ('3', 'Circular Strap Jaw '), ('6', 'Coded Wire'), ('A', 'Internal (Radio)'), ('B', 'Metal Livestock')], db_column='tag_type', default='1', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='date_flag',
            field=models.IntegerField(verbose_name='Date Flag', default=1, choices=[(0, 'Unknown'), (2, 'Derived'), (1, 'Reported')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='fate',
            field=models.CharField(max_length=3, verbose_name='Fate', choices=[('R', 'Released'), ('K', 'Killed')], blank=True, null=True, default='R'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='latlon_flag',
            field=models.IntegerField(verbose_name='Spatial Flag', default=1, choices=[(0, 'Unknown'), (2, 'Derived'), (1, 'Reported')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(max_length=3, verbose_name='Sex', choices=[('9', 'Unknown'), ('3', 'Hermaphrodite'), ('2', 'Female'), ('1', 'Male')], blank=True, null=True, default='9'),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(verbose_name='Date Flag', default=1, choices=[(0, 'Unknown'), (2, 'Derived'), (1, 'Reported')]),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(max_length=30, verbose_name='Report Format', default='verbal', choices=[('dcr', 'DCR'), ('other', 'other'), ('e-mail', 'e-mail'), ('verbal', 'verbal'), ('letter', 'letter')]),
        ),
    ]
