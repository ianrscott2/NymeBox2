# Generated by Django 3.1.1 on 2020-09-03 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Basic', '0003_auto_20200903_1423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configitem',
            old_name='GIFisChecked',
            new_name='GIF',
        ),
        migrations.RenameField(
            model_name='configitem',
            old_name='JPGisChecked',
            new_name='JPG',
        ),
        migrations.RenameField(
            model_name='configitem',
            old_name='NEFisChecked',
            new_name='NEF',
        ),
    ]