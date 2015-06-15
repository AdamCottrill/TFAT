# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0005_auto_20150612_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='fate',
            field=models.CharField(default='C', null=True, choices=[('R', 'Released'), ('K', 'Killed')], max_length=2, blank=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(default='9', null=True, max_length=30, blank=True, verbose_name='Sex', choices=[('9', 'Unknown'), ('3', 'Hermaphrodite'), ('2', 'Female'), ('1', 'Male')]),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(default='C', db_index=True, null=True, max_length=4, blank=True, choices=[('C', 'Existed on Capture'), ('A', 'Applied')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='clipc',
            field=models.CharField(null=True, max_length=5, blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='fate',
            field=models.CharField(default='R', verbose_name='Fate', max_length=30, choices=[('R', 'Released'), ('K', 'Killed')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='flen',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='rwt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(default='9', null=True, max_length=30, blank=True, verbose_name='Sex', choices=[('9', 'Unknown'), ('3', 'Hermaphrodite'), ('2', 'Female'), ('1', 'Male')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(default='2', verbose_name='Tag Colour', max_length=3, choices=[('6', 'Other'), ('3', 'Red'), ('5', 'Orange'), ('1', 'Colourless'), ('9', 'Unknown'), ('4', 'Green'), ('2', 'Yellow')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(default='01', verbose_name='Tag Origin', max_length=3, choices=[('05', 'University of Toronto'), ('11', 'Sir Sandford Fleming College'), ('19', 'Other'), ('10', 'Lakehead University'), ('07', 'State of Pennsylvania'), ('01', 'Ontario Ministry of Natural Resources'), ('03', 'State of Michigan'), ('06', 'State of Ohio'), ('13', 'Ontario Hydro'), ('09', 'State of Minnesota'), ('99', 'Unknown'), ('08', 'Royal Ontario Museum'), ('04', 'University of Guelph'), ('12', 'Private Club'), ('02', 'New York State')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(default='1', verbose_name='Tag Position', max_length=3, choices=[('2', 'Between Dorsal'), ('7', 'Snout'), ('8', 'Anal'), ('3', 'Posterior Dorsal'), ('4', 'Abdominal Insertion'), ('6', 'Jaw'), ('5', 'Flesh of Back'), ('9', 'Unknown'), ('1', 'Anterior Dorsal')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(default='1', verbose_name='Tag Type', max_length=3, choices=[('7', 'Strip Vinyl  '), ('8', 'Secure Tie'), ('9', 'Type Unknown or not applicable'), ('0', 'No tag'), ('5', 'Anchor'), ('3', 'Circular Strap Jaw '), ('A', 'Internal (Radio)'), ('1', 'Streamer'), ('4', 'Butt End Jaw '), ('X', 'Tag Scar/obvious loss'), ('2', 'Tubular Vinyl'), ('6', 'Coded Wire')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tagdoc',
            field=models.CharField(null=True, max_length=6, blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tlen',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(default='verbal', verbose_name='Report Format', max_length=30, choices=[('verbal', 'verbal'), ('other', 'other'), ('e-mail', 'e-mail'), ('letter', 'letter')]),
        ),
    ]
