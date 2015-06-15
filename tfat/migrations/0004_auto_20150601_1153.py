# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0003_auto_20150601_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='year',
            field=models.IntegerField(default=1111, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='encounter',
            name='fate',
            field=models.CharField(blank=True, max_length=2, choices=[('R', 'Released'), ('K', 'Killed')], null=True, default='C'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(verbose_name='Sex', blank=True, max_length=30, choices=[('2', 'Female'), ('9', 'Unknown'), ('3', 'Hermaphrodite'), ('1', 'Male')], null=True, default='9'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(db_index=True, blank=True, max_length=4, choices=[('A', 'Applied'), ('C', 'Existed on Capture')], null=True, default='C'),
        ),
        migrations.AlterField(
            model_name='project',
            name='prj_cd',
            field=models.CharField(max_length=12, db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='fate',
            field=models.CharField(max_length=30, choices=[('R', 'Released'), ('K', 'Killed')], verbose_name='Fate', default='R'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(verbose_name='Sex', blank=True, max_length=30, choices=[('2', 'Female'), ('9', 'Unknown'), ('3', 'Hermaphrodite'), ('1', 'Male')], null=True, default='9'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(max_length=30, choices=[('3', 'Red'), ('6', 'Other'), ('5', 'Orange'), ('4', 'Green'), ('2', 'Yellow'), ('1', 'Colourless'), ('9', 'Unknown')], verbose_name='Tag Colour', default='2'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(max_length=30, choices=[('11', 'Sir Sandford Fleming College'), ('03', 'State of Michigan'), ('05', 'University of Toronto'), ('07', 'State of Pennsylvania'), ('02', 'New York State'), ('10', 'Lakehead University'), ('13', 'Ontario Hydro'), ('99', 'Unknown'), ('06', 'State of Ohio'), ('01', 'Ontario Ministry of Natural Resources'), ('19', 'Other'), ('09', 'State of Minnesota'), ('04', 'University of Guelph'), ('08', 'Royal Ontario Museum'), ('12', 'Private Club')], verbose_name='Tag Origin', default='01'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(max_length=30, choices=[('8', 'Anal'), ('5', 'Flesh of Back'), ('2', 'Between Dorsal'), ('4', 'Abdominal Insertion'), ('6', 'Jaw'), ('1', 'Anterior Dorsal'), ('7', 'Snout'), ('3', 'Posterior Dorsal'), ('9', 'Unknown')], verbose_name='Tag Position', default='1'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(max_length=30, choices=[('2', 'Tubular Vinyl'), ('6', 'Coded Wire'), ('A', 'Internal (Radio)'), ('3', 'Circular Strap Jaw '), ('5', 'Anchor'), ('X', 'Tag Scar/obvious loss'), ('9', 'Type Unknown or not applicable'), ('1', 'Streamer'), ('8', 'Secure Tie'), ('4', 'Butt End Jaw '), ('7', 'Strip Vinyl  '), ('0', 'No tag')], verbose_name='Tag Type', default='1'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(max_length=30, choices=[('other', 'other'), ('verbal', 'verbal'), ('e-mail', 'e-mail'), ('letter', 'letter')], verbose_name='Report Format', default='verbal'),
        ),
    ]
