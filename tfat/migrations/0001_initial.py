# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sam', models.CharField(max_length=5)),
                ('eff', models.CharField(max_length=3)),
                ('observation_date', models.DateField()),
                ('grid', models.CharField(max_length=4)),
                ('dd_lat', models.FloatField()),
                ('dd_lon', models.FloatField()),
                ('flen', models.IntegerField(blank=True, null=True)),
                ('tlen', models.IntegerField(blank=True, null=True)),
                ('rwt', models.IntegerField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('sex', models.CharField(blank=True, null=True, choices=[('3', 'Hermaphrodite'), ('2', 'Female'), ('1', 'Male'), ('9', 'Unknown')], verbose_name='Sex', default='9', max_length=30)),
                ('clipc', models.CharField(blank=True, null=True, max_length=5)),
                ('tagid', models.CharField(max_length=10)),
                ('tagdoc', models.CharField(blank=True, null=True, max_length=6)),
                ('tagstat', models.CharField(blank=True, choices=[('C', 'Existed on Capture'), ('A', 'Applied')], null=True, max_length=4, default='C')),
                ('fate', models.CharField(blank=True, choices=[('R', 'Released'), ('K', 'Killed')], null=True, max_length=2, default='C')),
                ('comment', models.CharField(blank=True, null=True, max_length=500)),
            ],
            options={
                'ordering': ['tagdoc', 'tagid'],
            },
        ),
        migrations.CreateModel(
            name='JoePublic',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=50)),
                ('initial', models.CharField(max_length=50)),
                ('address1', models.CharField(max_length=50)),
                ('address2', models.CharField(max_length=50)),
                ('town', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=12)),
                ('postal_code', models.CharField(max_length=7)),
                ('email', models.CharField(max_length=50)),
                ('affiliation', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('prj_cd', models.CharField(max_length=12)),
                ('prj_nm', models.CharField(max_length=30)),
                ('slug', models.SlugField(editable=False, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recovery',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('recovery_date', models.DateField()),
                ('general_name', models.CharField(max_length=50)),
                ('specific_name', models.CharField(max_length=50)),
                ('dd_lat', models.FloatField()),
                ('dd_lon', models.FloatField()),
                ('flen', models.IntegerField()),
                ('tlen', models.IntegerField()),
                ('rwt', models.IntegerField()),
                ('sex', models.CharField(blank=True, null=True, choices=[('3', 'Hermaphrodite'), ('2', 'Female'), ('1', 'Male'), ('9', 'Unknown')], verbose_name='Sex', default='9', max_length=30)),
                ('clipc', models.CharField(max_length=5)),
                ('tagid', models.CharField(max_length=10)),
                ('tag_origin', models.CharField(choices=[('06', 'State of Ohio'), ('12', 'Private Club'), ('10', 'Lakehead University'), ('04', 'University of Guelph'), ('01', 'Ontario Ministry of Natural Resources'), ('11', 'Sir Sandford Fleming College'), ('07', 'State of Pennsylvania'), ('05', 'University of Toronto'), ('13', 'Ontario Hydro'), ('09', 'State of Minnesota'), ('99', 'Unknown'), ('08', 'Royal Ontario Museum'), ('19', 'Other'), ('02', 'New York State'), ('03', 'State of Michigan')], verbose_name='Tag Origin', default='01', max_length=30)),
                ('tag_position', models.CharField(choices=[('5', 'Flesh of Back'), ('6', 'Jaw'), ('2', 'Between Dorsal'), ('8', 'Anal'), ('3', 'Posterior Dorsal'), ('7', 'Snout'), ('4', 'Abdominal Insertion'), ('1', 'Anterior Dorsal'), ('9', 'Unknown')], verbose_name='Tag Position', default='1', max_length=30)),
                ('tag_type', models.CharField(choices=[('3', 'Circular Strap Jaw '), ('1', 'Streamer'), ('A', 'Internal (Radio)'), ('8', 'Secure Tie'), ('9', 'Type Unknown or not applicable'), ('6', 'Coded Wire'), ('7', 'Strip Vinyl  '), ('5', 'Anchor'), ('X', 'Tag Scar/obvious loss'), ('2', 'Tubular Vinyl'), ('0', 'No tag'), ('4', 'Butt End Jaw ')], verbose_name='Tag Type', default='1', max_length=30)),
                ('tag_colour', models.CharField(choices=[('5', 'Orange'), ('6', 'Other'), ('3', 'Red'), ('4', 'Green'), ('1', 'Colourless'), ('2', 'Yellow'), ('9', 'Unknown')], verbose_name='Tag Colour', default='2', max_length=30)),
                ('tagdoc', models.CharField(max_length=6)),
                ('tag_removed', models.BooleanField(default=False)),
                ('fate', models.CharField(choices=[('R', 'Released'), ('K', 'Killed')], verbose_name='Fate', default='R', max_length=30)),
                ('comment', models.CharField(blank=True, null=True, max_length=500)),
            ],
            options={
                'ordering': ['tagdoc', 'tagid'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date_reported', models.DateTimeField()),
                ('reporting_format', models.CharField(choices=[('other', 'other'), ('letter', 'letter'), ('e-mail', 'e-mail'), ('verbal', 'verbal')], verbose_name='Report Format', default='verbal', max_length=30)),
                ('comment', models.CharField(blank=True, null=True, max_length=500)),
                ('follow_up', models.BooleanField(default=False)),
                ('reported_by', models.ForeignKey(blank=True, null=True, related_name='Reported_By', to='tfat.JoePublic')),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('species_code', models.IntegerField(unique=True)),
                ('common_name', models.CharField(max_length=30)),
                ('scientific_name', models.CharField(blank=True, null=True, max_length=50)),
            ],
            options={
                'ordering': ['species_code'],
            },
        ),
        migrations.AddField(
            model_name='recovery',
            name='report',
            field=models.ForeignKey(related_name='Report', to='tfat.Report'),
        ),
        migrations.AddField(
            model_name='recovery',
            name='spc',
            field=models.ForeignKey(related_name='Species', to='tfat.Species'),
        ),
        migrations.AddField(
            model_name='encounter',
            name='project',
            field=models.ForeignKey(related_name='Project', to='tfat.Project'),
        ),
        migrations.AddField(
            model_name='encounter',
            name='spc',
            field=models.ForeignKey(to='tfat.Species'),
        ),
    ]
