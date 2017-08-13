from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class PeopleManager(BaseUserManager):

    def create_person(self, email, first_name, last_name, bio, password):
        data = {
            'email': email,
            'first_name': first_name,
            'date_register': timezone.now(),
            'last_name': last_name,
        }
        data.update({'bio': bio}) if bio is not None else False
        person = self.model.objects.create(**data)
        if password:
            person.set_password(password)
        else:
            person.set_unusable_password()
        person.save(update_fields=['password'])
        return person

    def create_superuser(self, email, first_name, last_name, password):
        person = self.create_person(email, first_name, last_name, None, password)
        person.is_superuser = True
        person.set_password(password)
        person.save(update_fields=['is_superuser', 'password'])
        return person
