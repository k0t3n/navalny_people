from django.db import models
from django.utils import timezone


class PeopleManager(models.Manager):

    def create_person(self, first_name, last_name, bio):
        data = {
            'first_name': first_name,
            'date_register': timezone.now(),
            'last_name': last_name,
            'bio': bio
        }
        person = self.model.objects.create(**data)
        return person