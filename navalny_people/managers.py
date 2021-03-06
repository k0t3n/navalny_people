from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class PeopleManager(BaseUserManager):

    def create_person(self, first_name, last_name, photo=None, email=None, uid=None,
                      social_type=None, story=None, password=None):
        data = {
            'photo': photo,
            'email': email,
            'uid': uid,
            'social_type': self.model.VK
            if social_type is None else social_type,
            'first_name': first_name,
            'date_register': timezone.now(),
            'last_name': last_name,
            'password': password,
        }
        data.update({'story': story}) if story is not None else False
        person = self.model.objects.create(**data)
        if password:
            person.set_password(password)
        else:
            person.set_unusable_password()
        person.save(update_fields=['password'])
        return person

    def create_superuser(self, uid, first_name, last_name, password):
        person = self.create_person(uid=uid, first_name=first_name,
                                    last_name=last_name, password=password)
        person.is_superuser = True
        person.set_password(password)
        person.save(update_fields=['is_superuser', 'password'])
        return person
