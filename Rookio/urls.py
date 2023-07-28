"""
URL configuration for Rookio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from viewer import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add_room/', views.add_room, name='add_room'),
    path('rooms_overview/', views.rooms_overview, name='rooms_overview'),

    path('my_rooms/', views.my_rooms, name='my_rooms'),
    path('my_rooms/<int:room_id>/edit_room', views.edit_room, name='edit_room'),
    path('room_detail/<int:room_id>/', views.room_detail, name='room_detail'),

    path('room_detail/<int:room_id>/show_items', views.show_items, name='show_items'),
    path('room_detail/<int:room_id>/add_item', views.add_item, name='add_item'),
    path('room_detail/<int:room_id>/edit_item', views.edit_item, name='edit_item'),

    path('room_detail/<int:room_id>/items/<int:item_id>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('room_detail/<int:room_id>/items/<int:item_id>/delete/', views.delete_menu_item, name='delete_menu_item'),

    # detail of the room from "Rooms Overview"
    path('room_detail_with_items/<int:room_id>/', views.room_detail_with_items, name='room_detail_with_items'),
]

# my note - enable Django to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
