# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0007_auto_20150615_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(default='9', verbose_name='Sex', blank=True, choices=[('3', 'Hermaphrodite'), ('9', 'Unknown'), ('2', 'Female'), ('1', 'Male')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(default='C', blank=True, db_index=True, choices=[('C', 'Existed on Capture'), ('A', 'Applied')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='date_flag',
            field=models.IntegerField(default=1, verbose_name='Date Flag', choices=[(2, 'Derived'), (0, 'Unknown'), (1, 'Reported')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='fate',
            field=models.CharField(default='R', verbose_name='Fate', blank=True, choices=[('K', 'Killed'), ('R', 'Released')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='latlon_flag',
            field=models.IntegerField(default=1, verbose_name='Spatial Flag', choices=[(2, 'Derived'), (0, 'Unknown'), (1, 'Reported')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(default='9', verbose_name='Sex', blank=True, choices=[('3', 'Hermaphrodite'), ('9', 'Unknown'), ('2', 'Female'), ('1', 'Male')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(default='2', verbose_name='Tag Colour', max_length=3, choices=[('6', 'Other'), ('1', 'Colourless'), ('3', 'Red'), ('5', 'Orange'), ('2', 'Yellow'), ('4', 'Green'), ('9', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(default='01', verbose_name='Tag Origin', max_length=3, choices=[('09', 'State of Minnesota'), ('01', 'Ontario Ministry of Natural Resources'), ('13', 'Ontario Hydro'), ('03', 'State of Michigan'), ('11', 'Sir Sandford Fleming College'), ('12', 'Private Club'), ('08', 'Royal Ontario Museum'), ('04', 'University of Guelph'), ('05', 'University of Toronto'), ('99', 'Unknown'), ('06', 'State of Ohio'), ('07', 'State of Pennsylvania'), ('10', 'Lakehead University'), ('02', 'New York State'), ('19', 'Other')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(default='1', verbose_name='Tag Position', max_length=3, choices=[('4', 'Abdominal Insertion'), ('7', 'Snout'), ('6', 'Jaw'), ('2', 'Between Dorsal'), ('5', 'Flesh of Back'), ('3', 'Posterior Dorsal'), ('8', 'Anal'), ('9', 'Unknown'), ('1', 'Anterior Dorsal')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(default='1', verbose_name='Tag Type', max_length=3, choices=[('2', 'Tubular Vinyl'), ('5', 'Anchor'), ('8', 'Secure Tie'), ('3', 'Circular Strap Jaw '), ('X', 'Tag Scar/obvious loss'), ('9', 'Type Unknown or not applicable'), ('7', 'Strip Vinyl  '), ('A', 'Internal (Radio)'), ('1', 'Streamer'), ('0', 'No tag'), ('4', 'Butt End Jaw '), ('6', 'Coded Wire')]),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(default=1, verbose_name='Date Flag', choices=[(2, 'Derived'), (0, 'Unknown'), (1, 'Reported')]),
        ),
    ]
