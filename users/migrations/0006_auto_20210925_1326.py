# Generated by Django 3.1.4 on 2021-09-25 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210922_1022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['date_created']},
        ),
    ]