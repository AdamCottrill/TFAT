# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0006_auto_20180917_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='recoveryletter',
            name='method',
            field=models.CharField(choices=[('custom_letter', 'Custom Letter'), ('tfat_template', 'TFAT Template')], max_length=30, default='tfat_template', verbose_name='Generated By'),
        ),
        migrations.AddField(
            model_name='recoveryletter',
            name='zoom',
            field=models.IntegerField(blank=True, verbose_name='Map Zoom', null=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(choices=[('3', 'Hermaphrodite'), ('1', 'Male'), ('2', 'Female'), ('9', 'Unknown')], default='9', verbose_name='Sex', null=True, max_length=3, blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_colour',
            field=models.CharField(choices=[('4', 'Green'), ('2', 'Yellow'), ('1', 'Colourless'), ('7', 'White'), ('3', 'Red'), ('5', 'Orange'), ('9', 'Unknown'), ('6', 'Silver')], default='2', db_column='tag_colour', max_length=3, verbose_name='Tag Colour', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_origin',
            field=models.CharField(choices=[('09', 'State of Minnesota'), ('25', 'AOFRC'), ('08', 'Royal Ontario Museum'), ('19', 'USWFW'), ('13', 'Ontario Hydro'), ('11', 'Sir Sandford Fleming College'), ('03', 'State of Michigan'), ('26', 'GLLFAS'), ('12', 'Private Club'), ('02', 'New York State'), ('05', 'University of Toronto'), ('99', 'Unknown'), ('20', 'USGS'), ('01', 'Ontario Ministry of Natural Resources'), ('98', 'Other'), ('06', 'State of Ohio'), ('07', 'State of Pennsylvania'), ('04', 'University of Guelph'), ('24', 'CORA'), ('10', 'Lakehead University')], default='01', db_column='tag_origin', max_length=3, verbose_name='Tag Origin', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_position',
            field=models.CharField(choices=[('6', 'Jaw'), ('5', 'Flesh of Back'), ('1', 'Anterior Dorsal'), ('4', 'Abdominal Insertion'), ('7', 'Snout'), ('3', 'Posterior Dorsal'), ('8', 'Anal'), ('9', 'Unknown'), ('2', 'Between Dorsal')], default='1', db_column='tag_position', max_length=3, verbose_name='Tag Position', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_type',
            field=models.CharField(choices=[('P', 'PIT tag'), ('8', 'Secure Tie'), ('C', 'Cinch'), ('A', 'Internal (Radio)'), ('5', 'Anchor'), ('4', 'Butt End Jaw '), ('2', 'Tubular Vinyl'), ('1', 'Streamer'), ('6', 'Coded Wire'), ('7', 'Strip Vinyl  '), ('B', 'Metal Livestock'), ('3', 'Circular Strap Jaw ')], default='1', db_column='tag_type', max_length=3, verbose_name='Tag Type', db_index=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='date_flag',
            field=models.IntegerField(choices=[(1, 'Reported'), (2, 'Derived'), (0, 'Unknown')], default=1, verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='latlon_flag',
            field=models.IntegerField(choices=[(1, 'Reported'), (2, 'Derived'), (0, 'Unknown')], default=1, verbose_name='Spatial Flag'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(choices=[('3', 'Hermaphrodite'), ('1', 'Male'), ('2', 'Female'), ('9', 'Unknown')], default='9', verbose_name='Sex', null=True, max_length=3, blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(choices=[(1, 'Reported'), (2, 'Derived'), (0, 'Unknown')], default=1, verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(choices=[('dcr', 'DCR'), ('other', 'other'), ('letter', 'letter'), ('e-mail', 'e-mail'), ('verbal', 'verbal')], max_length=30, default='verbal', verbose_name='Report Format'),
        ),
    ]