from django.db import models
from django.utils import timezone


class PeopleManager(models.Manager):

    def create_person(self, first_name, last_name, bio):
        data = {
            'first_name': first_name,
            'date_register': timezone.now(),
            'last_name': last_name,
        }
        data.update({'bio': bio}) if bio is not None else False
        person = self.model.objects.create(**data)
        return person

    def create_superuser(self, first_name, last_name):
        person = self.create_person(first_name, last_name, None)
        person.is_superuser = True
        person.save(update_fields=['is_superuser'])
        return person
