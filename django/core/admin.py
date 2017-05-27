"""Administration module."""

from django.contrib import admin

# Register your models here.
from .models import (
    Topic, Space, Event, Account, Comment, ForbiddenEmail, Media, Stat,
    Tag, Vote, EventType
)

admin.site.register(Topic)
admin.site.register(Space)
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Account)
admin.site.register(Comment)
admin.site.register(ForbiddenEmail)
admin.site.register(Media)
admin.site.register(Stat)
admin.site.register(Tag)
admin.site.register(Vote)
