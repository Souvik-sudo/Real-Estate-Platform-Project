# from django.contrib import admin

# # Register your models here.
from django.contrib import admin
from .models import CustomUser, Property, Image, ContactForm

class ImageInline(admin.StackedInline):
    model = Image
    extra = 1  # Number of extra forms to display

class PropertyAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('title', 'price', 'bedrooms', 'bathrooms', 'area', 'city', 'state', 'zip_code', 'owner')
    search_fields = ('title', 'city', 'state', 'zip_code')
    list_filter = ('city', 'state', 'created_at', 'updated_at')

admin.site.register(Property, PropertyAdmin)
admin.site.register(CustomUser)
admin.site.register(ContactForm)