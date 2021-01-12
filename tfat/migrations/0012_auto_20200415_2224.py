# Generated by Django 2.2.10 on 2020-04-16 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0011_auto_20200415_2158'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Species',
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(blank=True, choices=[('1', 'Male'), ('9', 'Unknown'), ('2', 'Female'), ('3', 'Hermaphrodite')], default='9', max_length=3, null=True, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='tagstat',
            field=models.CharField(blank=True, choices=[('C', 'Existed on Capture'), ('A', 'Applied')], db_index=True, default='C', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_colour',
            field=models.CharField(choices=[('3', 'Red'), ('6', 'Silver'), ('2', 'Yellow'), ('9', 'Unknown'), ('4', 'Green'), ('5', 'Orange'), ('7', 'White'), ('1', 'Colourless')], db_column='tag_colour', db_index=True, default='2', max_length=3, verbose_name='Tag Colour'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_origin',
            field=models.CharField(choices=[('10', 'Lakehead'), ('20', 'USGS'), ('07', 'Penn.'), ('02', 'NY'), ('98', 'Other'), ('08', 'ROM'), ('11', 'SSFC'), ('25', 'AOFRC'), ('06', 'Ohio'), ('26', 'GLLFAS'), ('03', 'Mich.'), ('09', 'Minn.'), ('12', 'Priv'), ('13', 'OntHydro'), ('01', 'MNRF'), ('24', 'CORA'), ('19', 'USFWS'), ('04', 'UofG'), ('99', 'Unkn'), ('05', 'UofT')], db_column='tag_origin', db_index=True, default='01', max_length=3, verbose_name='Tag Origin'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_position',
            field=models.CharField(choices=[('4', 'Abdominal Insertion'), ('7', 'Snout'), ('8', 'Anal'), ('9', 'Unknown'), ('3', 'Posterior Dorsal'), ('6', 'Jaw'), ('2', 'Between Dorsal'), ('1', 'Anterior Dorsal'), ('5', 'Flesh of Back')], db_column='tag_position', db_index=True, default='1', max_length=3, verbose_name='Tag Position'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_type',
            field=models.CharField(choices=[('7', 'Strip Vinyl  '), ('B', 'Metal Livestock'), ('2', 'Tubular Vinyl'), ('5', 'Anchor'), ('C', 'Cinch'), ('P', 'PIT tag'), ('4', 'Butt End Jaw '), ('3', 'Circular Strap Jaw '), ('8', 'Secure Tie'), ('A', 'Internal (Radio)'), ('6', 'Coded Wire'), ('1', 'Streamer')], db_column='tag_type', db_index=True, default='1', max_length=3, verbose_name='Tag Type'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='date_flag',
            field=models.IntegerField(choices=[(0, 'Unknown'), (1, 'Reported'), (2, 'Derived')], default=1, verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='latlon_flag',
            field=models.IntegerField(choices=[(0, 'Unknown'), (1, 'Reported'), (2, 'Derived')], default=1, verbose_name='Spatial Flag'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(blank=True, choices=[('1', 'Male'), ('9', 'Unknown'), ('2', 'Female'), ('3', 'Hermaphrodite')], default='9', max_length=3, null=True, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(choices=[(0, 'Unknown'), (1, 'Reported'), (2, 'Derived')], default=0, verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(choices=[('other', 'other'), ('letter', 'letter'), ('verbal', 'verbal'), ('e-mail', 'e-mail'), ('dcr', 'DCR')], default='verbal', max_length=30, verbose_name='Report Format'),
        ),
    ]