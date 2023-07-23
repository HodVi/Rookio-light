
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(TimeStamp):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return f'Model Tag - name: {self.name}'


class PersonOwner(TimeStamp):

    PERMISSION_CHOICES = (
        ('PERMISSION1ADMIN', 'Admin/Creator'),  # DO NOT CHANGE the content or order - views.py def add_room(request)
        ('PERMISSION2MOD', 'Moderator'),
        ('PERMISSION3VIEWER', 'Viewer'),
    )

    user_person_owner: User = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    permission = models.CharField(max_length=30, choices=PERMISSION_CHOICES, default='permission3viewer')

    def __str__(self) -> str:
        return f'Model PersonOwner - {self.user_person_owner.first_name} {self.user_person_owner.last_name}'


class Template(TimeStamp):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f'Model Template - name: {self.name}'


class Room(TimeStamp):

    ROOM_TYPE_CHOICES = (
        ('event', 'Event'),
        ('service', 'Service'),
    )

    name = models.CharField(max_length=80)
    owners = models.ManyToManyField(PersonOwner, related_name="rooms")
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    tags = models.ManyToManyField(Tag, related_name="rooms")
    description = models.TextField(max_length=1000)  # default form widget for this field is a Textarea -
    # https://docs.djangoproject.com/en/4.2/ref/forms/widgets/#django.forms.Textarea
    place = models.CharField(max_length=150)
    gps_description = models.CharField(max_length=150, blank=True)
    gps_lat = models.DecimalField(max_digits=9, decimal_places=6,
                                  null=True,
                                  blank=True,
                                  validators=[MinValueValidator(-90), MaxValueValidator(90)])
    gps_lng = models.DecimalField(max_digits=9, decimal_places=6,
                                  null=True,
                                  blank=True,
                                  validators=[MinValueValidator(-180), MaxValueValidator(180)])
    date = models.DateField()
    time = models.TimeField()
    outdoor = models.BooleanField(blank=True, default=False)
    contact_public = models.CharField(max_length=100)
    contact_after_assignment = models.CharField(max_length=100, null=True, blank=True)
    age_restriction = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)],
                                                       null=True, blank=True)
    age_recommendation = models.CharField(max_length=80, null=True, blank=True)
    minimum_participants = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    maximum_participants = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    paid_to_be_unique = models.BooleanField(default=False)
    hidden_from_public = models.BooleanField(default=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="rooms", null=True, blank=True)

    def __str__(self) -> str:
        return f'Model Room - name: {self.name}'


class MenuItem(TimeStamp):
    item_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    duration = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    number_of_pieces = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="menu_items")

    def __str__(self) -> str:
        return f'Model MenuItem - item name: {self.item_name}'


class PersonParticipant(TimeStamp):
    user_person_participant: User = models.OneToOneField(
                                                        User,
                                                        on_delete=models.CASCADE,
                                                        null=True, blank=True,
                                                        related_name='participant_profile')
    nickname_unregistered_participant = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField(blank=True)
    menu_items = models.ManyToManyField(MenuItem, related_name="participants")

    def __str__(self) -> str:
        return f'Model PersonParticipant - ' \
               f'{self.user_person_participant.first_name} {self.user_person_participant.last_name}'

    def clean(self):
        if not self.user_person_participant and not self.nickname_unregistered_participant:
            raise ValidationError('Either username or nickname of the participant must be set.')

    def save(self, *args, **kwargs):
        if not self.user_person_participant and not self.nickname_unregistered_participant:
            raise ValidationError('Either username or nickname of the participant must be set.')
        super().save(*args, **kwargs)


LIMIT_MB = 20
BYTES_PER_LIMIT = 1024 ** 2
SUBTYPE_OF_IMAGE = ['jpeg', 'gif', 'png']


def validate_image(image):
    file_size = image.file.size
    if file_size > LIMIT_MB * BYTES_PER_LIMIT:
        raise ValidationError(f"Max size of file is {LIMIT_MB} MB")
    # check the file MIME type, e.g. image/png
    main, sub = image.content_type.split('/')
    if not (main == 'image' and sub in SUBTYPE_OF_IMAGE):
        raise ValidationError(f'Please use one of these image types: {", ".join(SUBTYPE_OF_IMAGE)}.')


class Image(TimeStamp):
    image_file = models.ImageField(upload_to='images/', validators=[validate_image])
    image_height = models.IntegerField()
    image_width = models.IntegerField()
    description = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    thumbnail = ImageSpecField(source='image_file',  # source referring to the column 'image_file'
                               processors=[ResizeToFill(100, 100)],
                               format='JPEG',
                               options={'quality': 60})

    def __str__(self) -> str:
        return f'Model Image - description: {self.description}'
