# Generated by Django 5.1.2 on 2024-10-28 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0007_alter_jobmodel_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiterprofilemodel',
            name='Company_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
