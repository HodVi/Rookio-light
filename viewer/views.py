
from django.contrib import messages

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.shortcuts import render, redirect

from viewer.forms import CustomUserCreationForm, RoomForm

from viewer.models import Room, PersonOwner


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


@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            new_room = form.save(commit=False)
            # PersonOwner object for the current user, or create a new one if it doesn't exist.
            person_owner, created = PersonOwner.objects.get_or_create(user=request.user, defaults={
                # 'permission': PersonOwner.PERMISSION1ADMIN})
                # person_owner.permission = 'PERMISSION1ADMIN'
                'permission': PersonOwner.PERMISSION_CHOICES[0][0]})
            if created:
                # If the PersonOwner object was newly created, set the permission level.
                # person_owner.permission = PersonOwner.PERMISSION1ADMIN
                # person_owner.permission = 'PERMISSION1ADMIN'
                person_owner.permission = PersonOwner.PERMISSION_CHOICES[0][0]
                person_owner.save()
            new_room.person_owner = person_owner
            new_room.save()

            return redirect('welcome')  # TODO redirect to "Show Rooms" page
    else:
        form = RoomForm()
    return render(request, 'add_room.html', {'form': form})


def rooms_overview(request):
    rooms = Room.objects.all()
    return render(request, 'rooms_overview.html', {'rooms': rooms})