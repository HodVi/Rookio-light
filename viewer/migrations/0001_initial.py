# Generated by Django 4.2.2 on 2023-07-08 21:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import viewer.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('duration', models.PositiveSmallIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('number_of_pieces', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_of_birth', models.DateField(blank=True)),
                ('permission', models.CharField(choices=[('permission1admin', 'Admin/Creator'), ('permission2mod', 'Moderator'), ('permission3viewer', 'Viewer')], default='permission3viewer', max_length=30)),
                ('user_person_owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
                ('room_type', models.CharField(choices=[('event', 'Event'), ('service', 'Service')], max_length=20)),
                ('description', models.TextField(max_length=1000)),
                ('place', models.CharField(max_length=150)),
                ('gps_description', models.CharField(blank=True, max_length=150)),
                ('gps_lat', models.DecimalField(blank=True, decimal_places=6, max_digits=9, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('gps_lng', models.DecimalField(blank=True, decimal_places=6, max_digits=9, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('outdoor', models.BooleanField(blank=True)),
                ('contact_public', models.CharField(max_length=100)),
                ('contact_after_assignment', models.CharField(blank=True, max_length=100)),
                ('age_restriction', models.PositiveSmallIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)])),
                ('age_recommendation', models.CharField(blank=True, max_length=80)),
                ('minimum_participants', models.PositiveSmallIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('maximum_participants', models.PositiveSmallIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('paid_to_be_unique', models.BooleanField(default=False)),
                ('hidden_from_public', models.BooleanField(default=True)),
                ('owners', models.ManyToManyField(related_name='rooms', to='viewer.personowner')),
                ('tags', models.ManyToManyField(related_name='rooms', to='viewer.tag')),
                ('template', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='viewer.template')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nickname_unregistered_participant', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('date_of_birth', models.DateField(blank=True)),
                ('menu_items', models.ManyToManyField(related_name='participants', to='viewer.menuitem')),
                ('user_person_participant', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='menuitem',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='viewer.room'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_file', models.ImageField(upload_to='images/', validators=[viewer.models.validate_image])),
                ('image_height', models.IntegerField()),
                ('image_width', models.IntegerField()),
                ('description', models.CharField(max_length=50)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='viewer.room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
