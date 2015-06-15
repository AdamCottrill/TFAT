# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='fate',
            field=models.CharField(null=True, max_length=2, choices=[('K', 'Killed'), ('R', 'Released')], blank=True, default='C'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(choices=[('1', 'Male'), ('9', 'Unknown'), ('3', 'Hermaphrodite'), ('2', 'Female')], blank=True, null=True, max_length=30, verbose_name='Sex', default='9'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(null=True, max_length=4, choices=[('A', 'Applied'), ('C', 'Existed on Capture')], blank=True, default='C'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='fate',
            field=models.CharField(max_length=30, choices=[('K', 'Killed'), ('R', 'Released')], verbose_name='Fate', default='R'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(choices=[('1', 'Male'), ('9', 'Unknown'), ('3', 'Hermaphrodite'), ('2', 'Female')], blank=True, null=True, max_length=30, verbose_name='Sex', default='9'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(max_length=30, choices=[('3', 'Red'), ('4', 'Green'), ('6', 'Other'), ('1', 'Colourless'), ('9', 'Unknown'), ('5', 'Orange'), ('2', 'Yellow')], verbose_name='Tag Colour', default='2'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(max_length=30, choices=[('04', 'University of Guelph'), ('12', 'Private Club'), ('99', 'Unknown'), ('10', 'Lakehead University'), ('13', 'Ontario Hydro'), ('11', 'Sir Sandford Fleming College'), ('03', 'State of Michigan'), ('09', 'State of Minnesota'), ('05', 'University of Toronto'), ('19', 'Other'), ('07', 'State of Pennsylvania'), ('01', 'Ontario Ministry of Natural Resources'), ('06', 'State of Ohio'), ('02', 'New York State'), ('08', 'Royal Ontario Museum')], verbose_name='Tag Origin', default='01'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(max_length=30, choices=[('8', 'Anal'), ('4', 'Abdominal Insertion'), ('5', 'Flesh of Back'), ('9', 'Unknown'), ('7', 'Snout'), ('3', 'Posterior Dorsal'), ('6', 'Jaw'), ('1', 'Anterior Dorsal'), ('2', 'Between Dorsal')], verbose_name='Tag Position', default='1'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(max_length=30, choices=[('X', 'Tag Scar/obvious loss'), ('0', 'No tag'), ('9', 'Type Unknown or not applicable'), ('8', 'Secure Tie'), ('6', 'Coded Wire'), ('3', 'Circular Strap Jaw '), ('7', 'Strip Vinyl  '), ('4', 'Butt End Jaw '), ('A', 'Internal (Radio)'), ('1', 'Streamer'), ('5', 'Anchor'), ('2', 'Tubular Vinyl')], verbose_name='Tag Type', default='1'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(max_length=30, choices=[('letter', 'letter'), ('other', 'other'), ('e-mail', 'e-mail'), ('verbal', 'verbal')], verbose_name='Report Format', default='verbal'),
        ),
    ]
