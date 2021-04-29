# Generated by Django 2.2.17 on 2021-01-08 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0002_auto_20200619_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(blank=True, choices=[('9', 'Unknown'), ('2', 'Female'), ('3', 'Hermaphrodite'), ('1', 'Male')], default='9', max_length=3, null=True, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(blank=True, choices=[('C', 'Existed on Capture'), ('A', 'Applied')], db_index=True, default='C', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_colour',
            field=models.CharField(choices=[('4', 'Green'), ('2', 'Yellow'), ('3', 'Red'), ('1', 'Colourless'), ('6', 'Silver'), ('7', 'White'), ('9', 'Unknown'), ('5', 'Orange')], db_column='tag_colour', db_index=True, default='2', max_length=3, verbose_name='Tag Colour'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_origin',
            field=models.CharField(choices=[('20', 'USGS'), ('26', 'GLLFAS'), ('10', 'Lakehead'), ('25', 'AOFRC'), ('02', 'NY'), ('08', 'ROM'), ('13', 'OntHydro'), ('06', 'Ohio'), ('03', 'Mich.'), ('09', 'Minn.'), ('12', 'Priv'), ('24', 'CORA'), ('99', 'Unkn'), ('11', 'SSFC'), ('07', 'Penn.'), ('19', 'USFWS'), ('01', 'MNRF'), ('04', 'UofG'), ('05', 'UofT'), ('98', 'Other')], db_column='tag_origin', db_index=True, default='01', max_length=3, verbose_name='Tag Origin'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_position',
            field=models.CharField(choices=[('6', 'Jaw'), ('1', 'Anterior Dorsal'), ('3', 'Posterior Dorsal'), ('4', 'Abdominal Insertion'), ('2', 'Between Dorsal'), ('5', 'Flesh of Back'), ('7', 'Snout'), ('9', 'Unknown'), ('8', 'Anal')], db_column='tag_position', db_index=True, default='1', max_length=3, verbose_name='Tag Position'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_type',
            field=models.CharField(choices=[('7', 'Strip Vinyl  '), ('1', 'Streamer'), ('6', 'Coded Wire'), ('P', 'PIT tag'), ('C', 'Cinch'), ('3', 'Circular Strap Jaw '), ('A', 'Internal (Radio)'), ('2', 'Tubular Vinyl'), ('8', 'Secure Tie'), ('5', 'Anchor'), ('4', 'Butt End Jaw '), ('B', 'Metal Livestock')], db_column='tag_type', db_index=True, default='1', max_length=3, verbose_name='Tag Type'),
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
            field=models.CharField(blank=True, choices=[('9', 'Unknown'), ('2', 'Female'), ('3', 'Hermaphrodite'), ('1', 'Male')], default='9', max_length=3, null=True, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(choices=[(1, 'Reported'), (2, 'Derived'), (0, 'Unknown')], default=0, verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(choices=[('verbal', 'verbal'), ('dcr', 'DCR'), ('other', 'other'), ('e-mail', 'e-mail'), ('letter', 'letter')], default='verbal', max_length=30, verbose_name='Report Format'),
        ),
    ]