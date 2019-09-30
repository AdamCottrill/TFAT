# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("tfat", "0004_auto_20160603_1135")]

    operations = [
        migrations.CreateModel(
            name="RecoveryLetter",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                        auto_created=True,
                    ),
                ),
                ("letter", models.FileField(upload_to="tag_return_letters/")),
            ],
        ),
        migrations.AlterField(
            model_name="encounter",
            name="sex",
            field=models.CharField(
                choices=[
                    ("2", "Female"),
                    ("9", "Unknown"),
                    ("1", "Male"),
                    ("3", "Hermaphrodite"),
                ],
                verbose_name="Sex",
                max_length=3,
                null=True,
                blank=True,
                default="9",
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="_tag_colour",
            field=models.CharField(
                choices=[
                    ("7", "White"),
                    ("1", "Colourless"),
                    ("4", "Green"),
                    ("9", "Unknown"),
                    ("6", "Silver"),
                    ("5", "Orange"),
                    ("3", "Red"),
                    ("2", "Yellow"),
                ],
                db_index=True,
                verbose_name="Tag Colour",
                max_length=3,
                db_column="tag_colour",
                default="2",
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="_tag_origin",
            field=models.CharField(
                choices=[
                    ("04", "University of Guelph"),
                    ("26", "GLLFAS"),
                    ("05", "University of Toronto"),
                    ("24", "CORA"),
                    ("98", "Other"),
                    ("25", "AOFRC"),
                    ("12", "Private Club"),
                    ("10", "Lakehead University"),
                    ("09", "State of Minnesota"),
                    ("19", "USWFW"),
                    ("02", "New York State"),
                    ("08", "Royal Ontario Museum"),
                    ("03", "State of Michigan"),
                    ("01", "Ontario Ministry of Natural Resources"),
                    ("07", "State of Pennsylvania"),
                    ("99", "Unknown"),
                    ("20", "USGS"),
                    ("11", "Sir Sandford Fleming College"),
                    ("06", "State of Ohio"),
                    ("13", "Ontario Hydro"),
                ],
                db_index=True,
                verbose_name="Tag Origin",
                max_length=3,
                db_column="tag_origin",
                default="01",
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="_tag_position",
            field=models.CharField(
                choices=[
                    ("6", "Jaw"),
                    ("3", "Posterior Dorsal"),
                    ("4", "Abdominal Insertion"),
                    ("9", "Unknown"),
                    ("1", "Anterior Dorsal"),
                    ("7", "Snout"),
                    ("5", "Flesh of Back"),
                    ("2", "Between Dorsal"),
                    ("8", "Anal"),
                ],
                db_index=True,
                verbose_name="Tag Position",
                max_length=3,
                db_column="tag_position",
                default="1",
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="_tag_type",
            field=models.CharField(
                choices=[
                    ("4", "Butt End Jaw "),
                    ("P", "PIT tag"),
                    ("C", "Cinch"),
                    ("3", "Circular Strap Jaw "),
                    ("7", "Strip Vinyl  "),
                    ("A", "Internal (Radio)"),
                    ("5", "Anchor"),
                    ("B", "Metal Livestock"),
                    ("2", "Tubular Vinyl"),
                    ("6", "Coded Wire"),
                    ("8", "Secure Tie"),
                    ("1", "Streamer"),
                ],
                db_index=True,
                verbose_name="Tag Type",
                max_length=3,
                db_column="tag_type",
                default="1",
            ),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="girth",
            field=models.IntegerField(blank=True, verbose_name="Girth", null=True),
        ),
        migrations.AlterField(
            model_name="recovery",
            name="sex",
            field=models.CharField(
                choices=[
                    ("2", "Female"),
                    ("9", "Unknown"),
                    ("1", "Male"),
                    ("3", "Hermaphrodite"),
                ],
                verbose_name="Sex",
                max_length=3,
                null=True,
                blank=True,
                default="9",
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="reporting_format",
            field=models.CharField(
                choices=[
                    ("letter", "letter"),
                    ("verbal", "verbal"),
                    ("other", "other"),
                    ("e-mail", "e-mail"),
                    ("dcr", "DCR"),
                ],
                verbose_name="Report Format",
                default="verbal",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="recoveryletter",
            name="recovery",
            field=models.ForeignKey(
                to="tfat.Report",
                related_name="recovery_letters",
                on_delete=models.CASCADE,
            ),
        ),
    ]
