from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        ENGINEER = 'engineer', 'Инженер'
        SUPERVISOR = 'supervisor', 'Супервайзер'

    role = models.CharField(
        'Роль',
        max_length=20,
        choices=Roles.choices,
        default=Roles.ENGINEER,
    )
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    city = models.CharField('Город', max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_engineer(self):
        return self.role == self.Roles.ENGINEER

    @property
    def is_supervisor(self):
        return self.role == self.Roles.SUPERVISOR


class City(models.Model):
    """Город или населённый пункт."""
    name = models.CharField('Название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def __str__(self):
        return self.name


class Object(models.Model):
    """Дом / отель / кафе / объект обслуживания."""
    
    # Основная информация об объекте
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="building_objects", verbose_name='Город')
    name = models.CharField('Название объекта', max_length=150)
    address = models.CharField('Адрес', max_length=255)
    
    # Контактная информация
    apartment_number = models.CharField('Номер квартиры/помещения', max_length=20, blank=True, null=True)
    contact_phone = models.CharField('Контактный телефон', max_length=20, blank=True, null=True)
    
    # Описание клиента
    client_portrait = models.TextField('Описание портрета клиента', blank=True, null=True, 
                                      help_text="Например: мужчина 40 лет, безработный")
    
    # Используемые услуги (multiple choice)
    SERVICES_CHOICES = [
        ('internet', 'Интернет'),
        ('tv', 'Цифровое ТВ'),
        ('video_surveillance', 'Видеонаблюдение'),
        ('internet_nanny', 'Интернет-няня'),
        ('smart_home', 'Умный дом'),
        ('telephony', 'Телефония'),
    ]
    
    services_used = models.JSONField(
        'Чем пользуется', 
        blank=True, 
        null=True,
        help_text="Выберите используемые услуги"
    )
    
    # Оценка текущего провайдера
    SATISFACTION_CHOICES = [
        (1, '1 - Очень неудовлетворен'),
        (2, '2 - Неудовлетворен'),
        (3, '3 - Нейтрален'),
        (4, '4 - Удовлетворен'),
        (5, '5 - Очень удовлетворен'),
    ]
    
    current_provider_rating = models.IntegerField(
        'Оценка текущего провайдера',
        choices=SATISFACTION_CHOICES,
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Интерес к услугам
    INTEREST_SERVICES_CHOICES = [
        ('internet', 'Интернет'),
        ('tv', 'Цифровое ТВ'),
        ('video_surveillance', 'Видеонаблюдение'),
        ('internet_nanny', 'Интернет-няня'),
        ('smart_home', 'Умный дом'),
        ('telephony', 'Телефония'),
        ('additional_services', 'Дополнительные услуги'),
    ]
    
    interested_services = models.JSONField(
        'Интерес к услугам',
        blank=True,
        null=True,
        help_text="Какие услуги интересуют клиента"
    )
    
    # Удобное время для связи
    CONTACT_TIME_CHOICES = [
        ('morning', 'Утро (9:00-12:00)'),
        ('lunch', 'Обед (12:00-15:00)'),
        ('evening', 'Вечер (15:00-18:00)'),
        ('late_evening', 'Поздний вечер (18:00-21:00)'),
        ('weekend', 'Выходные дни'),
        ('any', 'Любое время'),
    ]
    
    convenient_contact_time = models.CharField(
        'Удобное время для связи',
        max_length=20,
        choices=CONTACT_TIME_CHOICES,
        blank=True,
        null=True
    )
    
    # Ценовые ожидания
    desired_price = models.PositiveIntegerField(
        'Желаемая цена за интернет',
        blank=True,
        null=True,
        help_text="Рублей в месяц"
    )
    
    # Дополнительная информация
    notes = models.TextField('Примечание', blank=True, null=True,
                           help_text="Произвольный комментарий инженера")
    
    # Геолокация
    latitude = models.FloatField('Широта', null=True, blank=True)
    longitude = models.FloatField('Долгота', null=True, blank=True)
    
    # Технические поля
    created_at = models.DateTimeField('Дата создания')
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='Кем создано'
    )
    
    # Статус клиента
    CLIENT_STATUS_CHOICES = [
        ('new', 'Новый клиент'),
        ('potential', 'Потенциальный клиент'),
        ('existing', 'Существующий клиент'),
        ('refused', 'Отказался'),
        ('callback', 'Нужен перезвон'),
    ]
    
    status = models.CharField(
        'Статус клиента',
        max_length=20,
        choices=CLIENT_STATUS_CHOICES,
        default='new'
    )
    
    # Дата следующего контакта
    next_contact_date = models.DateField('Дата следующего контакта', blank=True, null=True)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['-created_at']

    def __str__(self):
        address_info = f", кв. {self.apartment_number}" if self.apartment_number else ""
        return f"{self.name}{address_info} ({self.city})"
    
    def get_services_used_display(self):
        """Возвращает читаемый список используемых услуг"""
        if not self.services_used:
            return "Не указано"
        display_names = dict(self.SERVICES_CHOICES)
        return ", ".join([display_names.get(service, service) for service in self.services_used])
    
    def get_interested_services_display(self):
        """Возвращает читаемый список интересующих услуг"""
        if not self.interested_services:
            return "Не указано"
        display_names = dict(self.INTEREST_SERVICES_CHOICES)
        return ", ".join([display_names.get(service, service) for service in self.interested_services])
    
    @property
    def has_call_back(self):
        """Проверяет, требуется ли обратный звонок"""
        return self.status == 'callback' and self.next_contact_date is not None


class ClientProfile(models.Model):
    """Информация о клиенте."""
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="clients", verbose_name='Объект')
    apartment_number = models.CharField('№ квартиры', max_length=20, null=True, blank=True)
    name = models.CharField('ФИО', max_length=100, null=True, blank=True)
    description = models.TextField('Описание', blank=True, help_text="Портрет клиента, например: мужчина 40 лет, безработный")
    contact_phone = models.CharField('Телефон', max_length=20, null=True, blank=True)
    current_provider = models.CharField('Текущий провайдер', max_length=100, blank=True)
    satisfaction_level = models.IntegerField(
        'Уровень удовлетворенности',
        choices=[(i, str(i)) for i in range(1, 6)],
        null=True,
        blank=True,
        help_text="Оценка текущего провайдера (1-5)"
    )
    interested_services = models.CharField('Интересующие услуги', max_length=255, blank=True, help_text="Какие услуги интересуют")
    fair_price = models.CharField('Справедливая цена', max_length=50, blank=True)
    preferred_contact_time = models.CharField('Удобное время для связи', max_length=100, blank=True)
    notes = models.TextField('Заметки', blank=True)
    last_updated = models.DateTimeField('Последнее обновление', auto_now=True)

    class Meta:
        verbose_name = 'Профиль клиента'
        verbose_name_plural = 'Профили клиентов'
        ordering = ['-last_updated']

    def __str__(self):
        return f"{self.name or 'Без имени'} ({self.object})"


class Visit(models.Model):
    """Визит инженера к клиенту."""
    engineer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visits", verbose_name='Инженер')
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="visits", verbose_name='Клиент')
    date = models.DateTimeField('Дата визита', auto_now_add=True)
    comment = models.TextField('Комментарий', blank=True)
    gps_lat = models.FloatField('Широта', null=True, blank=True)
    gps_lng = models.FloatField('Долгота', null=True, blank=True)
    is_synced = models.BooleanField('Синхронизировано', default=True, help_text="Синхронизировано ли с сервером")

    class Meta:
        verbose_name = 'Визит'
        verbose_name_plural = 'Визиты'
        ordering = ['-date']

    def __str__(self):
        return f"Визит {self.engineer} → {self.client}"


class ServiceInterest(models.Model):
    """Интерес клиента к конкретным услугам."""
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="services", verbose_name='Клиент')
    service_name = models.CharField('Название услуги', max_length=100)
    interested = models.BooleanField('Заинтересован', default=False)

    class Meta:
        verbose_name = 'Интерес к услуге'
        verbose_name_plural = 'Интересы к услугам'
        ordering = ['client', 'service_name']
        unique_together = ['client', 'service_name']

    def __str__(self):
        return f"{self.client.name}: {self.service_name} ({'интересен' if self.interested else 'нет'})"