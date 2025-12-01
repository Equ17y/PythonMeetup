from django.db import models


class User(models.Model):
    user_roles = [
        ('organizer', 'Организатор'),
        ('guest', 'Гость'),
        ('speaker', 'Спикер')
    ]

    tg_id = models.IntegerField('ID ТГ')
    username = models.CharField(
        'Username', max_length=255,
        blank=True, null=True
    )
    name = models.CharField('Имя', max_length=255, blank=True, null=True)
    user_role = models.CharField(
        'Роль пользователя',
        max_length=255,
        choices=user_roles,
        default='guest'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.tg_id} - {self.name}'


class Event(models.Model):
    name = models.CharField('Название мероприятия', max_length=255)
    event_date = models.DateField('День мероприятия')
    started_at = models.TimeField('Время начала мероприятия')
    ended_at = models.TimeField('Время окончания мероприятия')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return self.name


class SpeakerTopic(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name='Мероприятие'
    )
    topic = models.CharField('Тема доклада', max_length=255)
    speaker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Спикер',
        limit_choices_to={'user_role': 'speaker'},
    )
    topic_date = models.DateField('День выступления')
    started_at = models.TimeField('Время начала выступления')
    ended_at = models.TimeField('Время окончания выступления')

    class Meta:
        verbose_name = 'Тема спикера'
        verbose_name_plural = 'Темы спикеров'

    def __str__(self):
        return f'{self.topic} - {self.speaker.name}'


class EventSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name='Мероприятие'
    )
    subscribed_at = models.DateTimeField(
        'Дата подписки',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Подписка на мероприятие'
        verbose_name_plural = 'Подписки на мероприятия'
        unique_together = ['user', 'event']

    def __str__(self):
        return f'{self.user.name} - {self.event.name}'
