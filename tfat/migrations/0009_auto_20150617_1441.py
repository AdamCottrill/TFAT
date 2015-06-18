# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0008_auto_20150615_1204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='date_reported',
            new_name='report_date',
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(blank=True, max_length=30, verbose_name='Sex', default='9', null=True, choices=[('2', 'Female'), ('9', 'Unknown'), ('3', 'Hermaphrodite'), ('1', 'Male')]),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(blank=True, max_length=4, default='C', null=True, choices=[('A', 'Applied'), ('C', 'Existed on Capture')], db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(blank=True, max_length=30, verbose_name='Sex', default='9', null=True, choices=[('2', 'Female'), ('9', 'Unknown'), ('3', 'Hermaphrodite'), ('1', 'Male')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(verbose_name='Tag Colour', default='2', max_length=3, choices=[('6', 'Other'), ('5', 'Orange'), ('3', 'Red'), ('1', 'Colourless'), ('9', 'Unknown'), ('4', 'Green'), ('2', 'Yellow')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(verbose_name='Tag Origin', default='01', max_length=3, choices=[('99', 'Unknown'), ('09', 'State of Minnesota'), ('12', 'Private Club'), ('11', 'Sir Sandford Fleming College'), ('13', 'Ontario Hydro'), ('02', 'New York State'), ('19', 'Other'), ('06', 'State of Ohio'), ('07', 'State of Pennsylvania'), ('10', 'Lakehead University'), ('08', 'Royal Ontario Museum'), ('05', 'University of Toronto'), ('04', 'University of Guelph'), ('01', 'Ontario Ministry of Natural Resources'), ('03', 'State of Michigan')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(verbose_name='Tag Position', default='1', max_length=3, choices=[('7', 'Snout'), ('1', 'Anterior Dorsal'), ('5', 'Flesh of Back'), ('3', 'Posterior Dorsal'), ('4', 'Abdominal Insertion'), ('2', 'Between Dorsal'), ('9', 'Unknown'), ('8', 'Anal'), ('6', 'Jaw')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(verbose_name='Tag Type', default='1', max_length=3, choices=[('0', 'No tag'), ('7', 'Strip Vinyl  '), ('4', 'Butt End Jaw '), ('8', 'Secure Tie'), ('1', 'Streamer'), ('6', 'Coded Wire'), ('9', 'Type Unknown or not applicable'), ('5', 'Anchor'), ('X', 'Tag Scar/obvious loss'), ('A', 'Internal (Radio)'), ('3', 'Circular Strap Jaw '), ('2', 'Tubular Vinyl')]),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(verbose_name='Report Format', default='verbal', max_length=30, choices=[('letter', 'letter'), ('verbal', 'verbal'), ('e-mail', 'e-mail'), ('other', 'other')]),
        ),
    ]
