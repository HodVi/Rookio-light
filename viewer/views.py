import itertools

from django.contrib import messages

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render, redirect, get_object_or_404

from viewer.forms import CustomUserCreationForm, RoomForm, TagForm, MenuItemForm

from viewer.models import Room, PersonOwner, Tag, MenuItem


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful.')
            return render(request, "welcome.html")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('welcome')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"form": form})


def logout_view(request):
    username = request.user.username
    auth_logout(request)
    messages.success(request, f'{username}, you have been logged out.')
    return redirect('welcome')


def welcome(request):
    return render(request, "welcome.html")


# TODO ak existuje tag tak umozni odoslat formular ALE priradi existujuci tag k novovytvaranej roomke

# TODO BUG, ASI uz fixnute otestovat moznosti a ci sa nezmenila fukcionalita inych validacii tagov -
#  zmazanim tag fieldov napr zo stredu a naslednym pridanim,
#  vzniknu duplikaty Tag nameov a potom data z jedneho z duplikatov nezapise do DB
@login_required
def add_room(request):
    if request.method == 'POST':
        room_form = RoomForm(request.POST)
        # total_tags = int(request.POST.get('total-tags', 0))

        tag_names = [value for key, value in request.POST.items() if key.startswith('tag-')]

        # check if it has any duplicates by comparing its length with the length of its set
        if len(tag_names) != len(set(tag_names)):
            messages.error(request, 'Tag names must be unique.')
            return render(request, 'add_room.html', {'room_form': room_form, 'tag_names': tag_names})

        tag_forms = [TagForm({'name': tag_name}) for tag_name in tag_names]

        all_forms_valid = room_form.is_valid() and all(tag_form.is_valid() for tag_form in tag_forms)

        if all_forms_valid:
            new_room = room_form.save(commit=False)
            person_owner, created = PersonOwner.objects.get_or_create(user_person_owner=request.user, defaults={
                'permission': PersonOwner.PERMISSION_CHOICES[0][0]})
            if created:
                person_owner.permission = PersonOwner.PERMISSION_CHOICES[0][0]
                person_owner.save()
            new_room.save()  # First save the room !!
            new_room.owners.add(person_owner)  # Then add the owner

            for tag_form in tag_forms:
                tag, created = Tag.objects.get_or_create(name=tag_form.cleaned_data['name'])
                new_room.tags.add(tag)  # Add the tag to the room

            messages.success(request, "Room created successfully!")
            return redirect('welcome')  # TODO redirect to "Show Rooms" page
        else:
            # iterate over all fields in all forms (the room form and all tag forms) in a single loop
            # each TagForm instance in the tag_forms list is passed as a separate argument
            for field in itertools.chain(room_form, *tag_forms):
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            return render(request, 'add_room.html', {'room_form': room_form, 'tag_names': tag_names})
    else:
        room_form = RoomForm()
        tag_names = ['']
    return render(request, 'add_room.html', {'room_form': room_form, 'tag_names': tag_names})


@login_required
def my_rooms(request):
    try:
        person_owner = PersonOwner.objects.get(user_person_owner=request.user)
        my_rooms_list = Room.objects.filter(owners__permission=PersonOwner.PERMISSION_CHOICES[0][0],
                                            owners=person_owner)

        return render(request, 'my_rooms.html', {'rooms': my_rooms_list})
    except PersonOwner.DoesNotExist:
        # messages.info(request, f"{request.user.username}, you have not yet created any room.")

        return render(request, 'my_rooms.html')


def rooms_overview(request):
    rooms = Room.objects.all()
    # TODO - make a calculations according to the number of registered participants
    # number_of_available_places = None

    return render(request, 'rooms_overview.html', {'rooms': rooms})
                                                   # 'number_of_available_places': number_of_available_places})


@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    return render(request, 'room_detail.html', {'room': room})


@login_required
def show_items(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    return render(request, 'show_items.html', {'room': room})
    # return render(request, 'edit_item.html', {'room': room})


@login_required
def add_item(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.room = room
            item.save()
            return redirect('show_items', room_id=room_id)
    else:
        form = MenuItemForm()

    return render(request, 'add_item.html', {'room': room, 'form': form})


@login_required
def edit_item(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    items = room.menu_items.all()

    return render(request, 'edit_item.html', {'room': room, 'items': items})


@login_required
def edit_menu_item(request, room_id, item_id):
    room = get_object_or_404(Room, id=room_id)
    item = get_object_or_404(MenuItem, room__id=room_id, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('edit_item', room_id=room_id)
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'edit_menu_item.html', {'form': form, 'room': room})


@login_required
def delete_menu_item(request, room_id, item_id):
    room = get_object_or_404(Room, id=room_id)
    item = get_object_or_404(MenuItem, room__id=room_id, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('edit_item', room_id=room_id)
    return render(request, 'delete_menu_item.html', {'item': item, 'room': room})
