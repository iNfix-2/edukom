from django.contrib import admin
from .import models

admin.site.register( models.AboutChild)
admin.site.register( models.Guardian)
admin.site.register( models.Location)
admin.site.register( models.Lesson)

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'date_created')
    list_filter = ('category', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(models.Testimonial)

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'date')
    readonly_fields = ('date',)

@admin.register(models.Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    readonly_fields = ('date_subscribed',)