# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0002_auto_20150527_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='project',
            field=models.ForeignKey(to='tfat.Project', related_name='Encounters'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(null=True, max_length=30, choices=[('9', 'Unknown'), ('1', 'Male'), ('2', 'Female'), ('3', 'Hermaphrodite')], verbose_name='Sex', default='9', blank=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagdoc',
            field=models.CharField(null=True, max_length=6, blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagid',
            field=models.CharField(max_length=10, db_index=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(null=True, max_length=4, choices=[('C', 'Existed on Capture'), ('A', 'Applied')], db_index=True, default='C', blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(null=True, max_length=30, choices=[('9', 'Unknown'), ('1', 'Male'), ('2', 'Female'), ('3', 'Hermaphrodite')], verbose_name='Sex', default='9', blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(max_length=30, choices=[('1', 'Colourless'), ('3', 'Red'), ('6', 'Other'), ('5', 'Orange'), ('9', 'Unknown'), ('2', 'Yellow'), ('4', 'Green')], default='2', verbose_name='Tag Colour'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(max_length=30, choices=[('09', 'State of Minnesota'), ('02', 'New York State'), ('08', 'Royal Ontario Museum'), ('10', 'Lakehead University'), ('06', 'State of Ohio'), ('03', 'State of Michigan'), ('99', 'Unknown'), ('13', 'Ontario Hydro'), ('01', 'Ontario Ministry of Natural Resources'), ('11', 'Sir Sandford Fleming College'), ('05', 'University of Toronto'), ('04', 'University of Guelph'), ('07', 'State of Pennsylvania'), ('12', 'Private Club'), ('19', 'Other')], default='01', verbose_name='Tag Origin'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(max_length=30, choices=[('6', 'Jaw'), ('3', 'Posterior Dorsal'), ('4', 'Abdominal Insertion'), ('1', 'Anterior Dorsal'), ('2', 'Between Dorsal'), ('8', 'Anal'), ('7', 'Snout'), ('9', 'Unknown'), ('5', 'Flesh of Back')], default='1', verbose_name='Tag Position'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(max_length=30, choices=[('7', 'Strip Vinyl  '), ('1', 'Streamer'), ('8', 'Secure Tie'), ('A', 'Internal (Radio)'), ('6', 'Coded Wire'), ('X', 'Tag Scar/obvious loss'), ('5', 'Anchor'), ('2', 'Tubular Vinyl'), ('0', 'No tag'), ('3', 'Circular Strap Jaw '), ('9', 'Type Unknown or not applicable'), ('4', 'Butt End Jaw ')], default='1', verbose_name='Tag Type'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(max_length=30, choices=[('verbal', 'verbal'), ('other', 'other'), ('letter', 'letter'), ('e-mail', 'e-mail')], default='verbal', verbose_name='Report Format'),
        ),
    ]
