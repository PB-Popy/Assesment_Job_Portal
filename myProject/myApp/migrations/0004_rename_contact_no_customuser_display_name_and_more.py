# Generated by Django 5.1.2 on 2024-10-27 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_seekerprofilemodel_skills'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='contact_no',
            new_name='display_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='Profile_Pic',
        ),
    ]
