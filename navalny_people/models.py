from django.db import models


class Person(models.Model):
    """
    Модель карточки человека
    """

    photo = models.ImageField(verbose_name='фото')  # Ещё не работал с аплоадом фоток

    first_name = models.CharField(
        max_length=20,
        verbose_name='имя',
    )

    last_name = models.CharField(
        max_length=30,
        verbose_name='фамилия')

    date_birth = models.DateField(
        verbose_name='дата рождения',
    )

    city = models.TextField(
        max_length=40,
        verbose_name='город'
    )
    # TODO придумать способ для выбора городов (через селекты)

    EDUCATION_TYPES = (
        ('HIGH', 'Высшее'),
        ('SECONDARY', 'Среднее'),
        ('BASIC', 'Основное'),
    )

    education = models.CharField(
        max_length=40,
        choices=EDUCATION_TYPES,
        verbose_name='образование'
    )

    profession = models.CharField(
        max_length=40,
        verbose_name='профессия',
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
        verbose_name='проверен модераторами'
    )

    def create_person(self):
        # TODO
        pass

    def get_full_name(self):
        return '%s %s'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'персону '
        verbose_name_plural = 'персоны'
