from django.urls import path
from . import views

app_name = "films"
urlpatterns = [
    path('', views.film_list, name='home'),
    path('countries/', views.country_list, name='country_list'),
    path('countries/<int:id>/', views.country_detail, name='country_detail'),
    path('countries/create/', views.country_create, name='country_create'),
    path('countries/<int:id>/update/',
         views.country_update, name='country_update'),
    path('countries/<int:id>/delete/',
         views.country_delete, name='country_delete'),
    path('countries/autocomplete/',
         views.CountryAutocomplete.as_view(), name='country_autocomplete'),

    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:id>/', views.genre_detail, name='genre_detail'),
    path('genres/create/', views.genre_create, name='genre_create'),
    path('genres/<int:id>/update/',
         views.genre_update, name='genre_update'),
    path('genres/<int:id>/delete/',
         views.genre_delete, name='genre_delete'),

    path('films/', views.film_list, name='film_list'),
    path('films/<int:id>/', views.film_detail, name='film_detail'),
    path('films/create/', views.film_create, name='film_create'),
    path('films/<int:id>/update/',
         views.film_update, name='film_update'),
    path('film/<int:id>/delete/',
         views.film_delete, name='film_delete'),

    path('people/', views.person_list, name='person_list'),
    path('people/<int:id>/', views.person_detail, name='person_detail'),
    path('people/create/', views.person_create, name='person_create'),
    path('people/<int:id>/update/',
         views.person_update, name='person_update'),
    path('people/<int:id>/delete/',
         views.person_delete, name='person_delete'),
    path('people/autocomplete/',
         views.PersonAutocomplete.as_view(), name='person_autocomplete'),

    path('films/<int:id>/group_create',
         views.group_create, name='group_create'),
    path('films/<int:id>/group_detail',
         views.group_detail, name='group_detail'),
    path('films/<int:id>/group_delete',
         views.group_delete, name='group_delete'),
    path('films/<int:id>/group_detail/group_wait',
         views.group_wait, name='group_wait'),
    path('films/<int:group_id>/group_detail/group_add_user/<int:member_id>',
         views.group_add_user, name='group_add_user'),
    path('films/<int:group_id>/group_detail/group_reject_user/<int:member_id>',
         views.group_reject_user, name='group_reject_user'),
    path('films/<int:group_id>/group_detail/group_delete_user/<int:member_id>',
         views.group_delete_user, name='group_delete_user'),
    path('films/<int:group_id>/group_detail/group_new_admin/<int:member_id>',
         views.group_new_admin, name='group_new_admin'),
    path('films/<int:group_id>/group_detail/group_delete_admin/<int:member_id>',
         views.group_delete_admin, name='group_delete_admin'),

    path('films/<int:id>/group_detail/conversation_create',
         views.conversation_create, name='conversation_create'),
    path('films/<int:id>/group_detail/conversation_detail',
         views.conversation_detail, name='conversation_detail'),
    path('films/<int:id>/group_detail/conversation_update',
         views.conversation_update, name='conversation_update'),
    path('films/<int:id>/group_detail/conversation_close',
         views.conversation_close, name='conversation_close'),
    path('films/<int:id>/group_detail/conversation_open',
         views.conversation_open, name='conversation_open'),
    path('films/<int:id>/group_detail/conversation_delete',
         views.conversation_delete, name='conversation_delete'),

    path('films/<int:conv_id>/group_detail/conversation_detail/message_create',
         views.message_create, name='message_create'),
    path('films/<int:id>/group_detail/conversation_detail/message_update',
         views.message_update, name='message_update'),
    path('films/<int:id>/group_detail/conversation_detail/message_delete',
         views.message_delete, name='message_delete'),
]
