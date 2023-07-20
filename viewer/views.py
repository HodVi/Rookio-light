import itertools

from django.contrib import messages

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.shortcuts import render, redirect

from viewer.forms import CustomUserCreationForm, RoomForm, TagForm

from viewer.models import Room, PersonOwner, Tag


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


def rooms_overview(request):
    rooms = Room.objects.all()
    # TODO - make a calculations according to the number of registered participants
    # number_of_available_places = None

    return render(request, 'rooms_overview.html', {'rooms': rooms})
                                                   # 'number_of_available_places': number_of_available_places})
