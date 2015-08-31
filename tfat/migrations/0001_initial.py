# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('master_database', models.CharField(max_length=250)),
                ('path', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Master Database',
            },
        ),
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sam', models.CharField(max_length=5)),
                ('eff', models.CharField(max_length=3)),
                ('grp', models.CharField(max_length=3)),
                ('fish', models.CharField(max_length=10)),
                ('observation_date', models.DateField()),
                ('grid', models.CharField(max_length=4)),
                ('dd_lat', models.FloatField()),
                ('dd_lon', models.FloatField()),
                ('flen', models.IntegerField(null=True, blank=True)),
                ('tlen', models.IntegerField(null=True, blank=True)),
                ('rwt', models.IntegerField(null=True, blank=True)),
                ('age', models.IntegerField(null=True, blank=True)),
                ('sex', models.CharField(verbose_name='Sex', default='9', blank=True, choices=[('2', 'Female'), ('9', 'Unknown'), ('3', 'Hermaphrodite'), ('1', 'Male')], null=True, max_length=3)),
                ('clipc', models.CharField(null=True, max_length=5, blank=True)),
                ('tagid', models.CharField(db_index=True, max_length=10)),
                ('tagdoc', models.CharField(null=True, db_index=True, max_length=6, blank=True)),
                ('tagstat', models.CharField(default='C', blank=True, choices=[('C', 'Existed on Capture'), ('A', 'Applied')], null=True, db_index=True, max_length=4)),
                ('fate', models.CharField(choices=[('K', 'Killed'), ('R', 'Released')], null=True, default='C', max_length=2, blank=True)),
                ('comment', models.CharField(null=True, max_length=500, blank=True)),
            ],
            options={
                'ordering': ['tagdoc', 'tagid', 'observation_date'],
            },
        ),
        migrations.CreateModel(
            name='JoePublic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=50)),
                ('initial', models.CharField(null=True, max_length=5, blank=True)),
                ('address1', models.CharField(null=True, max_length=50, blank=True)),
                ('address2', models.CharField(null=True, max_length=50, blank=True)),
                ('town', models.CharField(null=True, max_length=50, blank=True)),
                ('province', models.CharField(choices=[('ON', 'Ontario'), ('AB', 'Alberta'), ('BC', 'British Columbia'), ('MB', 'Manitoba'), ('NB', 'New Brunswick'), ('NL', 'Newfoundland and Labrador'), ('NS', 'Nova Scotia'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut'), ('PE', 'Prince Edward Island'), ('QC', 'Quebec'), ('SK', 'Saskatchewan'), ('YT', 'Yukon'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], null=True, max_length=12, blank=True)),
                ('postal_code', models.CharField(null=True, max_length=7, blank=True)),
                ('email', models.CharField(null=True, max_length=50, blank=True)),
                ('phone', models.CharField(null=True, max_length=15, blank=True)),
                ('affiliation', models.CharField(null=True, max_length=50, blank=True)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('year', models.IntegerField(db_index=True)),
                ('prj_cd', models.CharField(db_index=True, max_length=12)),
                ('prj_nm', models.CharField(max_length=100)),
                ('slug', models.SlugField(editable=False, blank=True)),
                ('dbase', models.ForeignKey(to='tfat.Database')),
            ],
            options={
                'ordering': ['-year', 'prj_cd'],
            },
        ),
        migrations.CreateModel(
            name='Recovery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('recovery_date', models.DateField(null=True, blank=True)),
                ('date_flag', models.IntegerField(choices=[(2, 'Derived'), (1, 'Reported'), (0, 'Unknown')], verbose_name='Date Flag', default=1)),
                ('general_location', models.CharField(verbose_name='General Location', null=True, max_length=50, blank=True)),
                ('specific_location', models.CharField(verbose_name='Specific Location', null=True, max_length=50, blank=True)),
                ('dd_lat', models.FloatField(null=True, blank=True)),
                ('dd_lon', models.FloatField(null=True, blank=True)),
                ('latlon_flag', models.IntegerField(choices=[(2, 'Derived'), (1, 'Reported'), (0, 'Unknown')], verbose_name='Spatial Flag', default=1)),
                ('flen', models.IntegerField(verbose_name='Fork Length', null=True, blank=True)),
                ('tlen', models.IntegerField(verbose_name='Total Length', null=True, blank=True)),
                ('rwt', models.IntegerField(verbose_name='Round Weight', null=True, blank=True)),
                ('sex', models.CharField(verbose_name='Sex', default='9', blank=True, choices=[('2', 'Female'), ('9', 'Unknown'), ('3', 'Hermaphrodite'), ('1', 'Male')], null=True, max_length=3)),
                ('clipc', models.CharField(verbose_name='Clip Code', null=True, max_length=5, blank=True)),
                ('tagid', models.CharField(db_index=True, max_length=10)),
                ('_tag_origin', models.CharField(verbose_name='Tag Origin', default='01', db_column='tag_origin', choices=[('08', 'Royal Ontario Museum'), ('12', 'Private Club'), ('05', 'University of Toronto'), ('09', 'State of Minnesota'), ('11', 'Sir Sandford Fleming College'), ('13', 'Ontario Hydro'), ('06', 'State of Ohio'), ('04', 'University of Guelph'), ('02', 'New York State'), ('10', 'Lakehead University'), ('19', 'Other'), ('99', 'Unknown'), ('07', 'State of Pennsylvania'), ('01', 'Ontario Ministry of Natural Resources'), ('03', 'State of Michigan')], db_index=True, max_length=3)),
                ('_tag_position', models.CharField(verbose_name='Tag Position', default='1', db_column='tag_position', choices=[('1', 'Anterior Dorsal'), ('9', 'Unknown'), ('7', 'Snout'), ('2', 'Between Dorsal'), ('8', 'Anal'), ('4', 'Abdominal Insertion'), ('6', 'Jaw'), ('5', 'Flesh of Back'), ('3', 'Posterior Dorsal')], db_index=True, max_length=3)),
                ('_tag_type', models.CharField(verbose_name='Tag Type', default='1', db_column='tag_type', choices=[('3', 'Circular Strap Jaw '), ('1', 'Streamer'), ('8', 'Secure Tie'), ('6', 'Coded Wire'), ('4', 'Butt End Jaw '), ('A', 'Internal (Radio)'), ('7', 'Strip Vinyl  '), ('2', 'Tubular Vinyl'), ('5', 'Anchor')], db_index=True, max_length=3)),
                ('_tag_colour', models.CharField(verbose_name='Tag Colour', default='2', db_column='tag_colour', choices=[('9', 'Unknown'), ('3', 'Red'), ('4', 'Green'), ('6', 'Other'), ('1', 'Colourless'), ('2', 'Yellow'), ('5', 'Orange')], db_index=True, max_length=3)),
                ('tagdoc', models.CharField(verbose_name='TAGDOC', default='25012', db_index=True, max_length=6)),
                ('tag_removed', models.BooleanField(default=False)),
                ('fate', models.CharField(verbose_name='Fate', default='R', blank=True, choices=[('K', 'Killed'), ('R', 'Released')], null=True, max_length=3)),
                ('comment', models.CharField(null=True, max_length=500, blank=True)),
            ],
            options={
                'ordering': ['tagdoc', 'tagid'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('report_date', models.DateTimeField(verbose_name='Report Date', null=True, blank=True)),
                ('date_flag', models.IntegerField(choices=[(2, 'Derived'), (1, 'Reported'), (0, 'Unknown')], verbose_name='Date Flag', default=1)),
                ('reporting_format', models.CharField(choices=[('verbal', 'verbal'), ('letter', 'letter'), ('dcr', 'DCR'), ('e-mail', 'e-mail'), ('other', 'other')], verbose_name='Report Format', default='verbal', max_length=30)),
                ('dcr', models.CharField(null=True, max_length=15, blank=True)),
                ('effort', models.CharField(null=True, max_length=15, blank=True)),
                ('associated_file', models.FileField(null=True, upload_to='reports', blank=True)),
                ('comment', models.CharField(null=True, max_length=500, blank=True)),
                ('follow_up', models.BooleanField(default=False)),
                ('reported_by', models.ForeignKey(to='tfat.JoePublic', blank=True, null=True, related_name='Reported_By')),
            ],
            options={
                'ordering': ['-report_date'],
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('species_code', models.IntegerField(unique=True)),
                ('common_name', models.CharField(max_length=40)),
                ('scientific_name', models.CharField(null=True, max_length=50, blank=True)),
            ],
            options={
                'ordering': ['common_name'],
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
            field=models.ForeignKey(related_name='Encounters', to='tfat.Project'),
        ),
        migrations.AddField(
            model_name='encounter',
            name='spc',
            field=models.ForeignKey(to='tfat.Species'),
        ),
        migrations.AlterIndexTogether(
            name='recovery',
            index_together=set([('tagid', 'tagdoc', 'spc')]),
        ),
        migrations.AlterIndexTogether(
            name='encounter',
            index_together=set([('tagid', 'tagdoc', 'spc')]),
        ),
    ]
