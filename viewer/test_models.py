from django.test import TestCase
from viewer.factories import (
    UserFactory, TagFactory, PersonOwnerFactory, TemplateFactory, RoomFactory,
    MenuItemFactory, PersonParticipantFactory, PersonParticipantMenuItemFactory,
    ImageFactory
)
from viewer.models import (
    Tag, PersonOwner, Template, Room, MenuItem, PersonParticipant,
    PersonParticipantMenuItem, Image
)


class TagModelTest(TestCase):

    def test_tag_creation(self):
        tag = TagFactory()
        self.assertIsInstance(tag, Tag)
        self.assertEqual(Tag.objects.count(), 1)


class RoomModelTest(TestCase):

    def test_room_creation_with_tags(self):
        tags = TagFactory.create_batch(3)
        room = RoomFactory(tags=tags)

        self.assertIsInstance(room, Room)
        self.assertEqual(room.tags.count(), 3)


class FirstRoomModelRelationshipTest(TestCase):

    def test_room_tags_relationship(self):
        room = RoomFactory()
        tags = TagFactory.create_batch(3)

        # Associate tags with the room
        room.tags.set(tags)
        room.save()

        # check if room has exactly 3 tags associated with it
        self.assertEqual(room.tags.count(), 3)
        # check if frist tag is indeed associated with the room
        self.assertIn(tags[0], room.tags.all())

        # Remove a tag and verify if the rest(2) of the rooms tag are there
        room.tags.remove(tags[0])
        room.save()
        self.assertEqual(room.tags.count(), 2)
        self.assertNotIn(tags[0], room.tags.all())


# class MenuItemModelRelationshipTest(TestCase):
#
#     def test_menu_item_room_relationship(self):
#         # create an isnstance and save it to the database
#         room = RoomFactory()
#         # setting room ForeignKey relationship to the previously created Room instance
#         menu_item = MenuItemFactory(room=room)
#
#         # check if the room attribute(foreign key) of the menu_item is the same as the room created above
#         self.assertEqual(menu_item.room, room)
#
#         # Delete the room and verify menu item deletion behavior > if it was deleted too
#         room.delete()
#         # checking the raised exception if the associated MenuItem is reloaded from database
#         with self.assertRaises(MenuItem.DoesNotExist):
#             menu_item.refresh_from_db()

class UserModelTest(TestCase):

    def test_user_creation(self):
        user = UserFactory()
        self.assertIsNotNone(user.id)


class PersonOwnerModelTest(TestCase):

    def test_person_owner_creation(self):
        person_owner = PersonOwnerFactory()
        self.assertIsNotNone(person_owner.id)


class TemplateModelTest(TestCase):

    def test_template_creation(self):
        template = TemplateFactory()
        self.assertIsNotNone(template.id)


class SecondRoomModelRelationshipTest(TestCase):

    def test_room_tag_relationship(self):
        tag = TagFactory()
        room = RoomFactory(tags=[tag])
        self.assertIn(tag, room.tags.all())

    def test_room_owners_relationship(self):
        owner = PersonOwnerFactory()
        room = RoomFactory(owners=[owner])
        self.assertIn(owner, room.owners.all())

    def test_room_template_relationship(self):
        template = TemplateFactory()
        room = RoomFactory(template=template)
        self.assertEqual(room.template, template)


class MenuItemModelRelationshipTest(TestCase):

    def test_menu_item_room_relationship(self):
        room = RoomFactory()
        menu_item = MenuItemFactory(room=room)
        self.assertEqual(menu_item.room, room)


class PersonParticipantModelRelationshipTest(TestCase):

    def test_person_participant_menu_item_relationship(self):
        menu_item = MenuItemFactory()
        participant = PersonParticipantFactory(menu_items=[menu_item])
        self.assertIn(menu_item, participant.menu_items.all())


class PersonParticipantMenuItemModelRelationshipTest(TestCase):

    def test_person_participant_menu_item_relationship(self):
        participant = PersonParticipantFactory()
        menu_item = MenuItemFactory()
        pivot = PersonParticipantMenuItemFactory(participant=participant, menu_item=menu_item)

        self.assertEqual(pivot.participant, participant)
        self.assertEqual(pivot.menu_item, menu_item)


class ImageModelRelationshipTest(TestCase):

    def test_image_room_relationship(self):
        room = RoomFactory()
        image = ImageFactory(room=room)
        self.assertEqual(image.room, room)


class RoomTagAddRemoveTest(TestCase):

    def test_add_remove_tag(self):
        room = RoomFactory()
        tag1, tag2 = TagFactory(), TagFactory()

        # Add tags
        room.tags.add(tag1, tag2)
        room.refresh_from_db()
        self.assertIn(tag1, room.tags.all())
        self.assertIn(tag2, room.tags.all())

        # Remove tags
        room.tags.remove(tag1)
        room.refresh_from_db()
        self.assertNotIn(tag1, room.tags.all())
        self.assertIn(tag2, room.tags.all())


class RoomOwnerAddRemoveTest(TestCase):

    def test_add_remove_owner(self):
        room = RoomFactory()
        owner1, owner2 = PersonOwnerFactory(), PersonOwnerFactory()

        # Add owners
        room.owners.add(owner1, owner2)
        room.refresh_from_db()
        self.assertIn(owner1, room.owners.all())
        self.assertIn(owner2, room.owners.all())

        # Remove owners
        room.owners.remove(owner1)
        room.refresh_from_db()
        self.assertNotIn(owner1, room.owners.all())
        self.assertIn(owner2, room.owners.all())


class ParticipantMenuItemAddRemoveTest(TestCase):

    def test_add_remove_menu_item(self):
        participant = PersonParticipantFactory()
        menu_item1, menu_item2 = MenuItemFactory(), MenuItemFactory()

        # Add menu items
        participant.menu_items.add(menu_item1, menu_item2)
        participant.refresh_from_db()
        self.assertIn(menu_item1, participant.menu_items.all())
        self.assertIn(menu_item2, participant.menu_items.all())

        # Remove menu items
        participant.menu_items.remove(menu_item1)
        participant.refresh_from_db()
        self.assertNotIn(menu_item1, participant.menu_items.all())
        self.assertIn(menu_item2, participant.menu_items.all())


class ForeignKeyDeletionTest(TestCase):

    def test_room_deletion_cascades(self):
        room = RoomFactory()
        menu_item = MenuItemFactory(room=room)
        image = ImageFactory(room=room)

        room_id, menu_item_id, image_id = room.id, menu_item.id, image.id

        room.delete()

        with self.assertRaises(MenuItem.DoesNotExist):
            MenuItem.objects.get(id=menu_item_id)

        with self.assertRaises(Image.DoesNotExist):
            Image.objects.get(id=image_id)

    def test_participant_deletion_cascades(self):
        participant = PersonParticipantFactory()
        menu_item = MenuItemFactory()
        pivot = PersonParticipantMenuItemFactory(participant=participant, menu_item=menu_item)

        participant_id, pivot_id = participant.id, pivot.id

        participant.delete()

        with self.assertRaises(PersonParticipantMenuItem.DoesNotExist):
            PersonParticipantMenuItem.objects.get(id=pivot_id)