# Generated by Django 5.1.2 on 2024-10-27 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0004_rename_contact_no_customuser_display_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Profile_Pic',
            field=models.ImageField(null=True, upload_to='Media/Profile_Pic'),
        ),
    ]