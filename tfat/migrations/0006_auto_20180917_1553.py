# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("tfat", "0005_auto_20180917_1549")]

    operations = [
        migrations.AlterField(
            model_name="encounter",
            name="sex",
            field=models.CharField(
                verbose_name="Sex",
                blank=True,
                null=True,
                default="9",
                max_length=3,
                choices=[
                    ("2", "Female"),
                    ("3", "Hermaphrodite"),
                    ("9", "Unknown"),
                    ("1", "Male"),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="_tag_colour",
            field=models.CharField(
                verbose_name="Tag Colour",
                db_index=True,
                default="2",
                db_column="tag_colour",
                max_length=3,
                choices=[
                    ("7", "White"),
                    ("4", "Green"),
                    ("9", "Unknown"),
                    ("5", "Orange"),
                    ("1", "Colourless"),
                    ("3", "Red"),
                    ("6", "Silver"),
                    ("2", "Yellow"),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="_tag_origin",
            field=models.CharField(
                verbose_name="Tag Origin",
                db_index=True,
                default="01",
                db_column="tag_origin",
                max_length=3,
                choices=[
                    ("08", "Royal Ontario Museum"),
                    ("20", "USGS"),
                    ("11", "Sir Sandford Fleming College"),
                    ("03", "State of Michigan"),
                    ("07", "State of Pennsylvania"),
                    ("26", "GLLFAS"),
                    ("98", "Other"),
                    ("05", "University of Toronto"),
                    ("19", "USWFW"),
                    ("06", "State of Ohio"),
                    ("02", "New York State"),
                    ("99", "Unknown"),
                    ("12", "Private Club"),
                    ("09", "State of Minnesota"),
                    ("13", "Ontario Hydro"),
                    ("01", "Ontario Ministry of Natural Resources"),
                    ("25", "AOFRC"),
                    ("10", "Lakehead University"),
                    ("04", "University of Guelph"),
                    ("24", "CORA"),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="_tag_position",
            field=models.CharField(
                verbose_name="Tag Position",
                db_index=True,
                default="1",
                db_column="tag_position",
                max_length=3,
                choices=[
                    ("2", "Between Dorsal"),
                    ("3", "Posterior Dorsal"),
                    ("7", "Snout"),
                    ("6", "Jaw"),
                    ("1", "Anterior Dorsal"),
                    ("9", "Unknown"),
                    ("8", "Anal"),
                    ("4", "Abdominal Insertion"),
                    ("5", "Flesh of Back"),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="_tag_type",
            field=models.CharField(
                verbose_name="Tag Type",
                db_index=True,
                default="1",
                db_column="tag_type",
                max_length=3,
                choices=[
                    ("2", "Tubular Vinyl"),
                    ("C", "Cinch"),
                    ("5", "Anchor"),
                    ("8", "Secure Tie"),
                    ("P", "PIT tag"),
                    ("6", "Coded Wire"),
                    ("7", "Strip Vinyl  "),
                    ("4", "Butt End Jaw "),
                    ("A", "Internal (Radio)"),
                    ("3", "Circular Strap Jaw "),
                    ("1", "Streamer"),
                    ("B", "Metal Livestock"),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="date_flag",
            field=models.IntegerField(
                default=1,
                verbose_name="Date Flag",
                choices=[(2, "Derived"), (0, "Unknown"), (1, "Reported")],
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="latlon_flag",
            field=models.IntegerField(
                default=1,
                verbose_name="Spatial Flag",
                choices=[(2, "Derived"), (0, "Unknown"), (1, "Reported")],
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="sex",
            field=models.CharField(
                verbose_name="Sex",
                blank=True,
                null=True,
                default="9",
                max_length=3,
                choices=[
                    ("2", "Female"),
                    ("3", "Hermaphrodite"),
                    ("9", "Unknown"),
                    ("1", "Male"),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="recoveryletter",
            name="recovery",
            field=models.ForeignKey(
                to="tfat.Recovery",
                related_name="recovery_letters",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="date_flag",
            field=models.IntegerField(
                default=1,
                verbose_name="Date Flag",
                choices=[(2, "Derived"), (0, "Unknown"), (1, "Reported")],
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="reporting_format",
            field=models.CharField(
                default="verbal",
                verbose_name="Report Format",
                max_length=30,
                choices=[
                    ("other", "other"),
                    ("dcr", "DCR"),
                    ("letter", "letter"),
                    ("verbal", "verbal"),
                    ("e-mail", "e-mail"),
                ],
            ),
        ),
    ]
