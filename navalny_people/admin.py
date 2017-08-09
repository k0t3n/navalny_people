from django.contrib import admin

from .models import *

admin.site.site_header = 'Проект Навальный.Люди'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('verified', 'moderated',)
    list_display = (Person.get_full_name, 'donated_money', 'verified',
                    'moderated',)
