import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from .models import (
    Tag, PersonOwner, Template, Room, MenuItem, PersonParticipant,
    PersonParticipantMenuItem, Image
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda a: f'{a.username}@gmail.com')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f'tag{n}')


class PersonOwnerFactory(DjangoModelFactory):
    class Meta:
        model = PersonOwner

    user_person_owner = factory.SubFactory(UserFactory)
    date_of_birth = factory.Faker('date_of_birth')
    permission = 'PERMISSION3VIEWER'


class TemplateFactory(DjangoModelFactory):
    class Meta:
        model = Template

    name = factory.Sequence(lambda n: f'template{n}')


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room

    name = factory.Sequence(lambda n: f'room{n}')
    room_type = 'event'
    description = factory.Faker('text', max_nb_chars=1000)
    place = factory.Faker('address')
    gps_description = factory.Faker('address')
    gps_lat = factory.Faker('latitude')
    gps_lng = factory.Faker('longitude')
    date = factory.Faker('future_date')
    time = factory.Faker('time')
    contact_public = factory.Faker('email')
    template = factory.SubFactory(TemplateFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            self.tags.add(TagFactory())

    @factory.post_generation
    def owners(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for owner in extracted:
                self.owners.add(owner)
        else:
            self.owners.add(PersonOwnerFactory())


class MenuItemFactory(DjangoModelFactory):
    class Meta:
        model = MenuItem

    item_name = factory.Sequence(lambda n: f'item{n}')
    price = factory.Faker('pydecimal', left_digits=6, right_digits=2, positive=True)
    duration = factory.Faker('random_int', min=1, max=1000)
    number_of_pieces = factory.Faker('random_int', min=1, max=1000)
    room = factory.SubFactory(RoomFactory)


class PersonParticipantFactory(DjangoModelFactory):
    class Meta:
        model = PersonParticipant

    user_person_participant = factory.SubFactory(UserFactory)
    nickname_unregistered_participant = factory.Sequence(lambda n: f'nickname{n}')

    @factory.post_generation
    def menu_items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for menu_item in extracted:
                self.menu_items.add(menu_item)
        else:
            self.menu_items.add(MenuItemFactory())


class PersonParticipantMenuItemFactory(DjangoModelFactory):
    class Meta:
        model = PersonParticipantMenuItem

    participant = factory.SubFactory(PersonParticipantFactory)
    menu_item = factory.SubFactory(MenuItemFactory)
    count = factory.Faker('random_int', min=1, max=5)


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    image_file = factory.django.ImageField()
    image_height = factory.Faker('random_int', min=100, max=1000)
    image_width = factory.Faker('random_int', min=100, max=1000)
    description = factory.Faker('sentence')
    room = factory.SubFactory(RoomFactory)

