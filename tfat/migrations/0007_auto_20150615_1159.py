# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0006_auto_20150615_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='fate',
            field=models.CharField(default='C', choices=[('K', 'Killed'), ('R', 'Released')], blank=True, null=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(default='9', verbose_name='Sex', choices=[('2', 'Female'), ('9', 'Unknown'), ('1', 'Male'), ('3', 'Hermaphrodite')], blank=True, null=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(db_index=True, default='C', choices=[('A', 'Applied'), ('C', 'Existed on Capture')], blank=True, null=True, max_length=4),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='date_flag',
            field=models.IntegerField(default=1, verbose_name='Date Flag', choices=[(1, 'Reported'), (0, 'Unknown'), (2, 'Derived')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='fate',
            field=models.CharField(default='R', choices=[('K', 'Killed'), ('R', 'Released')], verbose_name='Fate', max_length=30),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='general_name',
            field=models.CharField(blank=True, null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='latlon_flag',
            field=models.IntegerField(default=1, verbose_name='Spatial Flag', choices=[(1, 'Reported'), (0, 'Unknown'), (2, 'Derived')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(default='9', verbose_name='Sex', choices=[('2', 'Female'), ('9', 'Unknown'), ('1', 'Male'), ('3', 'Hermaphrodite')], blank=True, null=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='specific_name',
            field=models.CharField(blank=True, null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(default='2', choices=[('5', 'Orange'), ('6', 'Other'), ('4', 'Green'), ('1', 'Colourless'), ('9', 'Unknown'), ('2', 'Yellow'), ('3', 'Red')], verbose_name='Tag Colour', max_length=3),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(default='01', choices=[('13', 'Ontario Hydro'), ('19', 'Other'), ('10', 'Lakehead University'), ('09', 'State of Minnesota'), ('05', 'University of Toronto'), ('01', 'Ontario Ministry of Natural Resources'), ('03', 'State of Michigan'), ('04', 'University of Guelph'), ('06', 'State of Ohio'), ('11', 'Sir Sandford Fleming College'), ('07', 'State of Pennsylvania'), ('02', 'New York State'), ('99', 'Unknown'), ('08', 'Royal Ontario Museum'), ('12', 'Private Club')], verbose_name='Tag Origin', max_length=3),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(default='1', choices=[('3', 'Posterior Dorsal'), ('4', 'Abdominal Insertion'), ('8', 'Anal'), ('5', 'Flesh of Back'), ('9', 'Unknown'), ('2', 'Between Dorsal'), ('1', 'Anterior Dorsal'), ('7', 'Snout'), ('6', 'Jaw')], verbose_name='Tag Position', max_length=3),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(default='1', choices=[('2', 'Tubular Vinyl'), ('1', 'Streamer'), ('0', 'No tag'), ('X', 'Tag Scar/obvious loss'), ('4', 'Butt End Jaw '), ('6', 'Coded Wire'), ('A', 'Internal (Radio)'), ('8', 'Secure Tie'), ('7', 'Strip Vinyl  '), ('3', 'Circular Strap Jaw '), ('9', 'Type Unknown or not applicable'), ('5', 'Anchor')], verbose_name='Tag Type', max_length=3),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(default=1, verbose_name='Date Flag', choices=[(1, 'Reported'), (0, 'Unknown'), (2, 'Derived')]),
        ),
    ]
