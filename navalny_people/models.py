from django.db import models


class Person(models.Model):
    """
    Модель карточки человека
    """

    photo = models.ImageField(
        upload_to='image/',
        default='image/default.jpg',
        verbose_name='фото',
    )

    first_name = models.CharField(
        max_length=20,
        verbose_name='имя',
    )

    last_name = models.CharField(
        max_length=30,
        verbose_name='фамилия')

    city = models.CharField(
        max_length=40,
        verbose_name='город'
    )
    # TODO придумать способ для выбора городов (через селекты)

    bio = models.TextField(
        max_length=10000,
        verbose_name='биография'
    )

    donated_money = models.DecimalField(
        max_digits=1000000,
        decimal_places=0,
        default=0,
        verbose_name='пожертвованных средств'
    )

    verified = models.BooleanField(
        default=False,
        verbose_name='верифицирован'
    )
    moderated = models.BooleanField(
        default=False,
        verbose_name='Проверен'
    )

    def create_person(self):
        # TODO
        pass

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'человек'
        verbose_name_plural = 'люди'
