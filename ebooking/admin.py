from django.contrib import admin

from .models import *

admin.site.register(Host)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(Location)
admin.site.register(Room)
admin.site.register(Book)
admin.site.register(Tag)