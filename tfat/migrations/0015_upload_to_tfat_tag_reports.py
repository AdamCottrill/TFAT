# Generated by Django 2.2.10 on 2020-06-10 12:54

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('tfat', '0014_auto_20200416_1049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='joepublic',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name_plural': 'Tag Reporters'},
        ),
        migrations.AlterModelOptions(
            name='taggedspecies',
            options={'ordering': ['spc_nmco'], 'verbose_name_plural': 'Tagged Species'},
        ),
        migrations.AlterModelManagers(
            name='taggedspecies',
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='encounter',
            name='sex',
            field=models.CharField(blank=True, choices=[('3', 'Hermaphrodite'), ('2', 'Female'), ('1', 'Male'), ('9', 'Unknown')], default='9', max_length=3, null=True, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_colour',
            field=models.CharField(choices=[('7', 'White'), ('6', 'Silver'), ('1', 'Colourless'), ('4', 'Green'), ('3', 'Red'), ('9', 'Unknown'), ('2', 'Yellow'), ('5', 'Orange')], db_column='tag_colour', db_index=True, default='2', max_length=3, verbose_name='Tag Colour'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_origin',
            field=models.CharField(choices=[('26', 'GLLFAS'), ('03', 'Mich.'), ('99', 'Unkn'), ('13', 'OntHydro'), ('20', 'USGS'), ('98', 'Other'), ('02', 'NY'), ('04', 'UofG'), ('19', 'USFWS'), ('25', 'AOFRC'), ('05', 'UofT'), ('24', 'CORA'), ('09', 'Minn.'), ('10', 'Lakehead'), ('08', 'ROM'), ('11', 'SSFC'), ('07', 'Penn.'), ('06', 'Ohio'), ('01', 'MNRF'), ('12', 'Priv')], db_column='tag_origin', db_index=True, default='01', max_length=3, verbose_name='Tag Origin'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_position',
            field=models.CharField(choices=[('6', 'Jaw'), ('5', 'Flesh of Back'), ('2', 'Between Dorsal'), ('8', 'Anal'), ('4', 'Abdominal Insertion'), ('1', 'Anterior Dorsal'), ('9', 'Unknown'), ('3', 'Posterior Dorsal'), ('7', 'Snout')], db_column='tag_position', db_index=True, default='1', max_length=3, verbose_name='Tag Position'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='_tag_type',
            field=models.CharField(choices=[('8', 'Secure Tie'), ('5', 'Anchor'), ('6', 'Coded Wire'), ('A', 'Internal (Radio)'), ('B', 'Metal Livestock'), ('C', 'Cinch'), ('P', 'PIT tag'), ('2', 'Tubular Vinyl'), ('4', 'Butt End Jaw '), ('3', 'Circular Strap Jaw '), ('1', 'Streamer'), ('7', 'Strip Vinyl  ')], db_column='tag_type', db_index=True, default='1', max_length=3, verbose_name='Tag Type'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='date_flag',
            field=models.IntegerField(choices=[(1, 'Reported'), (0, 'Unknown'), (2, 'Derived')], default=1, verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='latlon_flag',
            field=models.IntegerField(choices=[(1, 'Reported'), (0, 'Unknown'), (2, 'Derived')], default=1, verbose_name='Spatial Flag'),
        ),
        migrations.AlterField(
            model_name='recovery',
            name='sex',
            field=models.CharField(blank=True, choices=[('3', 'Hermaphrodite'), ('2', 'Female'), ('1', 'Male'), ('9', 'Unknown')], default='9', max_length=3, null=True, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='report',
            name='associated_file',
            field=models.FileField(blank=True, null=True, upload_to='tfat_tag_reports'),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_flag',
            field=models.IntegerField(choices=[(1, 'Reported'), (0, 'Unknown'), (2, 'Derived')], default=0, verbose_name='Date Flag'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_format',
            field=models.CharField(choices=[('e-mail', 'e-mail'), ('other', 'other'), ('letter', 'letter'), ('dcr', 'DCR'), ('verbal', 'verbal')], default='verbal', max_length=30, verbose_name='Report Format'),
        ),
    ]