# Generated by Django 3.1.4 on 2021-09-21 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210916_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='users.profile'),
        ),
    ]