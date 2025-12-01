from django.contrib import admin
from .models import User, Event, SpeakerTopic, EventSubscription

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'name', 'user_role',)
    list_filter = ('user_role',)
    list_editable = ('user_role',)
    search_fields = ('name', 'tg_id')


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'started_at', 'ended_at',)
    list_filter = ('event_date',)
    search_fields = ('name',)


class SpeakerTopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'speaker', 'event', 'topic_date')
    list_filter = ('event', 'topic_date')
    search_fields = ('topic', 'speaker__name')


class EventSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')
    list_filter = ('event',)
    search_fields = ('user__name', 'event__name')


admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(SpeakerTopic, SpeakerTopicAdmin)
admin.site.register(EventSubscription, EventSubscriptionAdmin)
