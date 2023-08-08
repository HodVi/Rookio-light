# Generated by Django 4.2.2 on 2023-07-27 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0004_menuitem_nameprice_attributes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personparticipant',
            name='menu_items',
        ),
        migrations.CreateModel(
            name='PersonParticipantMenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.menuitem')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.personparticipant')),
            ],
            options={
                'unique_together': {('participant', 'menu_item')},
            },
        ),
    ]