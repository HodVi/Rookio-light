# Generated by Django 4.2.2 on 2023-07-28 08:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0008_pers_part_dateof_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personparticipantmenuitem',
            name='count',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
