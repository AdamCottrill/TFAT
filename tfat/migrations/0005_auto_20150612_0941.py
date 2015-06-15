# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0004_auto_20150601_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='encounter',
            options={'ordering': ['tagdoc', 'tagid', 'observation_date']},
        ),
        migrations.AddField(
            model_name='joepublic',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='recovery',
            name='date_flag',
            field=models.IntegerField(verbose_name='Date Flag', default=1, choices=[(2, 'Derived'), (1, 'Reported'), (0, 'Unknown')]),
        ),
        migrations.AddField(
            model_name='recovery',
            name='latlon_flag',
            field=models.IntegerField(verbose_name='Spatial Flag', default=1, choices=[(2, 'Derived'), (1, 'Reported'), (0, 'Unknown')]),
        ),
        migrations.AddField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(verbose_name='Date Flag', default=1, choices=[(2, 'Derived'), (1, 'Reported'), (0, 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='fate',
            field=models.CharField(null=True, default='C', blank=True, max_length=2, choices=[('K', 'Killed'), ('R', 'Released')]),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(null=True, blank=True, choices=[('9', 'Unknown'), ('3', 'Hermaphrodite'), ('1', 'Male'), ('2', 'Female')], verbose_name='Sex', default='9', max_length=30),
        ),
        migrations.AlterField(
            model_name='joepublic',
            name='address1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='joepublic',
            name='address2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='joepublic',
            name='affiliation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='joepublic',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='joepublic',
            name='initial',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='joepublic',
            name='postal_code',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='joepublic',
            name='province',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='joepublic',
            name='town',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='dd_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='dd_lon',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='fate',
            field=models.CharField(verbose_name='Fate', default='R', max_length=30, choices=[('K', 'Killed'), ('R', 'Released')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='recovery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(null=True, blank=True, choices=[('9', 'Unknown'), ('3', 'Hermaphrodite'), ('1', 'Male'), ('2', 'Female')], verbose_name='Sex', default='9', max_length=30),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(verbose_name='Tag Colour', default='2', max_length=3, choices=[('2', 'Yellow'), ('9', 'Unknown'), ('3', 'Red'), ('4', 'Green'), ('6', 'Other'), ('5', 'Orange'), ('1', 'Colourless')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(verbose_name='Tag Origin', default='01', max_length=3, choices=[('19', 'Other'), ('11', 'Sir Sandford Fleming College'), ('99', 'Unknown'), ('12', 'Private Club'), ('06', 'State of Ohio'), ('07', 'State of Pennsylvania'), ('08', 'Royal Ontario Museum'), ('02', 'New York State'), ('09', 'State of Minnesota'), ('05', 'University of Toronto'), ('03', 'State of Michigan'), ('13', 'Ontario Hydro'), ('10', 'Lakehead University'), ('01', 'Ontario Ministry of Natural Resources'), ('04', 'University of Guelph')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(verbose_name='Tag Position', default='1', max_length=3, choices=[('4', 'Abdominal Insertion'), ('9', 'Unknown'), ('2', 'Between Dorsal'), ('7', 'Snout'), ('8', 'Anal'), ('6', 'Jaw'), ('1', 'Anterior Dorsal'), ('5', 'Flesh of Back'), ('3', 'Posterior Dorsal')]),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(verbose_name='Tag Type', default='1', max_length=3, choices=[('A', 'Internal (Radio)'), ('8', 'Secure Tie'), ('2', 'Tubular Vinyl'), ('3', 'Circular Strap Jaw '), ('7', 'Strip Vinyl  '), ('1', 'Streamer'), ('5', 'Anchor'), ('X', 'Tag Scar/obvious loss'), ('6', 'Coded Wire'), ('4', 'Butt End Jaw '), ('9', 'Type Unknown or not applicable'), ('0', 'No tag')]),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_reported',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(verbose_name='Report Format', default='verbal', max_length=30, choices=[('letter', 'letter'), ('e-mail', 'e-mail'), ('verbal', 'verbal'), ('other', 'other')]),
        ),
    ]
