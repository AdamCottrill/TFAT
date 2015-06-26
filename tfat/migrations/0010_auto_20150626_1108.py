# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0009_auto_20150617_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='fate',
            field=models.CharField(max_length=2, default='C', choices=[('R', 'Released'), ('K', 'Killed')], null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(choices=[('9', 'Unknown'), ('2', 'Female'), ('3', 'Hermaphrodite'), ('1', 'Male')], null=True, max_length=30, default='9', verbose_name='Sex', blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='date_flag',
            field=models.IntegerField(default=1, choices=[(1, 'Reported'), (2, 'Derived'), (0, 'Unknown')], verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='fate',
            field=models.CharField(choices=[('R', 'Released'), ('K', 'Killed')], null=True, max_length=30, default='R', verbose_name='Fate', blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='latlon_flag',
            field=models.IntegerField(default=1, choices=[(1, 'Reported'), (2, 'Derived'), (0, 'Unknown')], verbose_name='Spatial Flag'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(choices=[('9', 'Unknown'), ('2', 'Female'), ('3', 'Hermaphrodite'), ('1', 'Male')], null=True, max_length=30, default='9', verbose_name='Sex', blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(max_length=3, default='2', db_index=True, verbose_name='Tag Colour', choices=[('9', 'Unknown'), ('1', 'Colourless'), ('3', 'Red'), ('2', 'Yellow'), ('5', 'Orange'), ('4', 'Green'), ('6', 'Other')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(max_length=3, default='01', db_index=True, verbose_name='Tag Origin', choices=[('99', 'Unknown'), ('10', 'Lakehead University'), ('19', 'Other'), ('04', 'University of Guelph'), ('06', 'State of Ohio'), ('07', 'State of Pennsylvania'), ('05', 'University of Toronto'), ('01', 'Ontario Ministry of Natural Resources'), ('11', 'Sir Sandford Fleming College'), ('13', 'Ontario Hydro'), ('08', 'Royal Ontario Museum'), ('09', 'State of Minnesota'), ('03', 'State of Michigan'), ('12', 'Private Club'), ('02', 'New York State')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(max_length=3, default='1', db_index=True, verbose_name='Tag Position', choices=[('9', 'Unknown'), ('5', 'Flesh of Back'), ('8', 'Anal'), ('1', 'Anterior Dorsal'), ('2', 'Between Dorsal'), ('4', 'Abdominal Insertion'), ('6', 'Jaw'), ('3', 'Posterior Dorsal'), ('7', 'Snout')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(max_length=3, default='1', db_index=True, verbose_name='Tag Type', choices=[('0', 'No tag'), ('3', 'Circular Strap Jaw '), ('2', 'Tubular Vinyl'), ('5', 'Anchor'), ('8', 'Secure Tie'), ('6', 'Coded Wire'), ('9', 'Type Unknown or not applicable'), ('X', 'Tag Scar/obvious loss'), ('7', 'Strip Vinyl  '), ('4', 'Butt End Jaw '), ('1', 'Streamer'), ('A', 'Internal (Radio)')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tagdoc',
            field=models.CharField(max_length=6, db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tagid',
            field=models.CharField(max_length=10, db_index=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(default=1, choices=[(1, 'Reported'), (2, 'Derived'), (0, 'Unknown')], verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(max_length=30, default='verbal', choices=[('other', 'other'), ('letter', 'letter'), ('e-mail', 'e-mail'), ('verbal', 'verbal')], verbose_name='Report Format'),
        ),
    ]
