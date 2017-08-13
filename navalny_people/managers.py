from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class PeopleManager(BaseUserManager):

    def create_person(self, first_name, last_name, email=None, uid=None,
                      social_type=None, story=None, password=None):
        data = {
            'email': email,
            'uid': uid,
            'social_type': social_type,
            'first_name': first_name,
            'date_register': timezone.now(),
            'last_name': last_name,
            'password': password
        }
        data.update({'story': story}) if story is not None else False
        person = self.model.objects.create(**data)
        if password:
            person.set_password(password)
        else:
            person.set_unusable_password()
        person.save(update_fields=['password'])
        return person

    def create_superuser(self, email, first_name, last_name, password):
        person = self.create_person(email=email, first_name=first_name,
                                    last_name=last_name, password=password)
        person.is_superuser = True
        person.set_password(password)
        person.save(update_fields=['is_superuser', 'password'])
        return person
