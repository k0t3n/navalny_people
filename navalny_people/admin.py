from django.contrib import admin
from navalny_people.models import Person


class PersonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)
