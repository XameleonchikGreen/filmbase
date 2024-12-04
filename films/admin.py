from django.contrib import admin
from .models import Country, Film, Person, Genre, Group, Conversation, Message, Membership

admin.site.register(Film)
admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Group)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Membership)
