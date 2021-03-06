from django.contrib import admin  # noqa

# Register your models here.
from .models import (IncomingEmail, EditedEmail, ArchiveEmail,
                     Edition, Subscriber, Attachment)


@admin.register(ArchiveEmail)
class ArchiveEmailAdmin(admin.ModelAdmin):
    list_display = ['filename']


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['email', 'original_filename']


@admin.register(IncomingEmail)
class IncomingEmailAdmin(admin.ModelAdmin):
    list_display = ['date', 'sender', 'subject', 'used']


@admin.register(EditedEmail)
class EditedEmailAdmin(admin.ModelAdmin):
    list_display = ['edition', 'sender', 'subject']


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ['date_created', 'subject', 'sent', 'date_sent']


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
