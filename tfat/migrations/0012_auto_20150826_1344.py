# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0011_auto_20150722_1307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='species',
            options={'ordering': ['common_name']},
        ),
        migrations.RemoveField(
            model_name='recovery',
            name='general_name',
        ),
        migrations.RemoveField(
            model_name='recovery',
            name='specific_name',
        ),
        migrations.AddField(
            model_name='recovery',
            name='general_location',
            field=models.CharField(verbose_name='General Location', null=True, max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='recovery',
            name='specific_location',
            field=models.CharField(verbose_name='Specific Location', null=True, max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(verbose_name='Sex', null=True, blank=True, default='9', choices=[('3', 'Hermaphrodite'), ('9', 'Unknown'), ('2', 'Female'), ('1', 'Male')], max_length=30),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(default='C', null=True, blank=True, db_index=True, choices=[('A', 'Applied'), ('C', 'Existed on Capture')], max_length=4),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='clipc',
            field=models.CharField(verbose_name='Clip Code', null=True, max_length=5, blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='date_flag',
            field=models.IntegerField(verbose_name='Date Flag', choices=[(2, 'Derived'), (1, 'Reported'), (0, 'Unknown')], default=1),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='flen',
            field=models.IntegerField(verbose_name='Fork Length', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='latlon_flag',
            field=models.IntegerField(verbose_name='Spatial Flag', choices=[(2, 'Derived'), (1, 'Reported'), (0, 'Unknown')], default=1),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='rwt',
            field=models.IntegerField(verbose_name='Round Weight', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(verbose_name='Sex', null=True, blank=True, default='9', choices=[('3', 'Hermaphrodite'), ('9', 'Unknown'), ('2', 'Female'), ('1', 'Male')], max_length=30),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_colour',
            field=models.CharField(verbose_name='Tag Colour', choices=[('1', 'Colourless'), ('9', 'Unknown'), ('4', 'Green'), ('5', 'Orange'), ('2', 'Yellow'), ('6', 'Other'), ('3', 'Red')], max_length=3, db_index=True, default='2'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_origin',
            field=models.CharField(verbose_name='Tag Origin', choices=[('13', 'Ontario Hydro'), ('06', 'State of Ohio'), ('19', 'Other'), ('04', 'University of Guelph'), ('10', 'Lakehead University'), ('09', 'State of Minnesota'), ('01', 'Ontario Ministry of Natural Resources'), ('07', 'State of Pennsylvania'), ('03', 'State of Michigan'), ('12', 'Private Club'), ('05', 'University of Toronto'), ('11', 'Sir Sandford Fleming College'), ('99', 'Unknown'), ('02', 'New York State'), ('08', 'Royal Ontario Museum')], max_length=3, db_index=True, default='01'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_position',
            field=models.CharField(verbose_name='Tag Position', choices=[('5', 'Flesh of Back'), ('9', 'Unknown'), ('3', 'Posterior Dorsal'), ('7', 'Snout'), ('4', 'Abdominal Insertion'), ('1', 'Anterior Dorsal'), ('8', 'Anal'), ('2', 'Between Dorsal'), ('6', 'Jaw')], max_length=3, db_index=True, default='1'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tag_type',
            field=models.CharField(verbose_name='Tag Type', choices=[('4', 'Butt End Jaw '), ('3', 'Circular Strap Jaw '), ('A', 'Internal (Radio)'), ('1', 'Streamer'), ('5', 'Anchor'), ('7', 'Strip Vinyl  '), ('2', 'Tubular Vinyl'), ('6', 'Coded Wire'), ('8', 'Secure Tie')], max_length=3, db_index=True, default='1'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tagdoc',
            field=models.CharField(verbose_name='TAGDOC', max_length=6, db_index=True, default='25012'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='tlen',
            field=models.IntegerField(verbose_name='Total Length', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='associated_file',
            field=models.FileField(blank=True, null=True, upload_to='reports'),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(verbose_name='Date Flag', choices=[(2, 'Derived'), (1, 'Reported'), (0, 'Unknown')], default=1),
        ),
        migrations.AlterField(
            model_name='report',
            name='report_date',
            field=models.DateTimeField(verbose_name='Report Date', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(verbose_name='Report Format', choices=[('verbal', 'verbal'), ('letter', 'letter'), ('other', 'other'), ('dcr', 'DCR'), ('e-mail', 'e-mail')], max_length=30, default='verbal'),
        ),
    ]
