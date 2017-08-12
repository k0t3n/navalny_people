from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

from navalny_people.managers import PeopleManager
from navalny_people.utils import upload_to


class Person(AbstractBaseUser, PermissionsMixin):
    """
    Модель карточки человека
    """
    VK, FB = 0, 1
    SOCIAL_TYPE = (
        (VK, 'VKontakte'),
        (FB, 'FaceBook')
    )
    photo = ProcessedImageField(
        upload_to=upload_to,
        format='JPEG',
        default='image/default.jpg',
        verbose_name='фото',
    )
    preview = ImageSpecField(
        format='JPEG',
        options={'quality': 80},
        source='photo',
        processors=[ResizeToFill(300, 300)]
    )
    first_name = models.CharField(
        max_length=20,
        verbose_name='имя',
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='фамилия',
    )
    email = models.EmailField(
        unique=True,
        verbose_name='E-mail'
    )
    social_type = models.PositiveSmallIntegerField(
        default=VK,
        choices=SOCIAL_TYPE,
        verbose_name='тип социальной сети'
    )
    location = models.ForeignKey(
        'geodata.GeoCoding',
        related_name='person_geodata',
        verbose_name='геодата пользователя',
        blank=True, null=True
    )
    profession = models.CharField(
        max_length=30,
        blank=True, null=True,
        verbose_name='профессия'
    )
    story = models.TextField(
        verbose_name='биография'
    )
    donated_money = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        default=0,
        verbose_name='пожертвованных средств'
    )
    date_register = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата регистрации'
    )
    verified = models.BooleanField(
        default=False,
        verbose_name='верифицирован'
    )
    moderated = models.BooleanField(
        default=False,
        verbose_name='Проверен'
    )

    REQUIRED_FIELDS = ['last_name', 'first_name']
    USERNAME_FIELD = 'email'

    objects = PeopleManager()

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

    def get_short_name(self):
        return f'{self.first_name, self.last_name[0]}'

    def __str__(self):
        return self.get_short_name()

    class Meta:
        verbose_name = 'человек'
        verbose_name_plural = 'люди'
