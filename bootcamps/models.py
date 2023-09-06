from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class ZorgOrganisatie(models.Model):
    name = models.CharField('naam', max_length=255)
    logo = models.ImageField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Gemeente(models.Model):
    name = models.CharField('naam', max_length=255)
    logo = models.ImageField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Gemeenten'

class BaseOrg(models.Model):
    name = models.CharField('naam', max_length=255)
    logo = models.ImageField(blank=True)
    photo = models.ImageField('foto', blank=True)
    website = models.CharField(max_length=255, blank=True)
    street = models.CharField('straatnaam', max_length=255, blank=True)
    number = models.CharField('huisnummer', max_length=255, blank=True)
    zipcode = models.CharField('postcode', max_length=255, blank=True)
    city = models.CharField('plaatsnaam', max_length=255, blank=True)

    # Ensure correct name of Den Bosch City
    def save(self, *args, **kwargs):
        if self.city.lower() == 'den bosch':
            self.city = '’s-Hertogenbosch'
        if self.city.lower() == '\'s-hertogenbosch':
            self.city = '’s-Hertogenbosch'
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_logo(self):
        return self.logo

    class Meta:
        ordering = ['name']
        abstract = True

class ZorgLocatie(BaseOrg):
    zorgorganisatie = models.ForeignKey('ZorgOrganisatie', verbose_name='Moederorganisatie', help_text='(indien van toepassing)', blank=True, null=True, on_delete=models.CASCADE)
    sportscholen = models.ManyToManyField('Sportschool', verbose_name='Samenwerking met', help_text='Selecter hier de sportclubs waarmee deze zorglocatie samenwerkt', related_name='zorglocaties', blank=True)
    users = models.ManyToManyField(User, verbose_name='Gebruikers', help_text='Geef hier de accounts op die deze zorglocatie mogen beheren', blank=True, related_name='zorglocaties')

    def get_logo(self):
        if self.logo:
            return self.logo
        elif self.zorgorganisatie:
            return self.zorgorganisatie.logo
ZorgLocatie._meta.get_field('photo').verbose_name = 'foto gebouw'

class Sportschool(BaseOrg):
    users = models.ManyToManyField(User, verbose_name='Gebruikers', help_text='Geef hier de account op die deze sportschool mogen beheren', blank=True, related_name='sportscholen')

    def get_logo(self):
        if self.logo:
            return self.logo

    class Meta(BaseOrg.Meta):
        verbose_name_plural = 'sportscholen'
Sportschool._meta.get_field('photo').verbose_name = 'foto trainer'

# class Samenwerking(models.Model):
#     zorglocatie = models.ForeignKey('ZorgLocatie')
#     sportschool = models.ForeignKey('Sportschool')

#     class Meta:
#         verbose_name_plural = 'Samenwerkingen'

class Price(models.Model):
    product = models.PositiveIntegerField(unique=True, choices=[
        (1, 'ZorgLocatie'),
        (2, 'Sportschool'),
        ])
    description = models.CharField('omschrijving', help_text='Deze omschrijving komt op de factuur', max_length=255, blank=True)
    amount = models.DecimalField('bedrag', max_digits=6, decimal_places=2)

    def __str__(self):
        if self.description:
            return self.description
        else:
            return 'Jaarbedrag van €{} voor een {}'.format(self.amount, self.get_product_display())

    class Meta:
        verbose_name = 'Prijs'
        verbose_name_plural = 'Prijzen'
        ordering = ['product']

class Invoice(models.Model):
    identifier = models.CharField('factuurkenmerk', max_length=255)
    date = models.DateField('factuurdatum')
    description = models.CharField('omschrijving', max_length=255, blank=True)
    amount = models.DecimalField('factuurbedrag', max_digits=6, decimal_places=2)
    zorglocatie = models.ForeignKey('ZorgLocatie', blank=True, null=True, on_delete=models.CASCADE)
    sportschool = models.ForeignKey('Sportschool', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('invoice', args=[self.pk])

    def __str__(self):
        return 'Factuur van €{} met kenmerk {}'.format(self.amount, self.identifier)

    class Meta:
        verbose_name = 'Factuur'
        verbose_name_plural = 'Facturen'
        ordering = ['date']

class Trainer(models.Model):
    name = models.CharField('naam v.d. trainer', max_length=255)
    photo = models.ImageField('foto', max_length=255)

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField('naam', max_length=255)
    email = models.EmailField('emailadres')
    bootcamp = models.ForeignKey('Bootcamp', related_name='participants', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def email_spec(self):
        if not self.email:
            return None
        if self.name:
            return '{} <{}>'.format(self.name, self.email)
        else:
            return self.email

    class Meta:
        verbose_name = 'Deelnemer'
        verbose_name_plural = 'Deelnemers'

class Bootcamp(models.Model):
    deleted = models.BooleanField('verwijderd', default=False)
    date = models.DateField('datum')
    start_time = models.TimeField('begintijd', blank=True, null=True)
    end_time = models.TimeField('eindtijd', blank=True, null=True)
    places = models.PositiveIntegerField('beschikbare plaatsen', default=10)
    info = RichTextField('extra informatie', blank=True)

    street = models.CharField('straatnaam', max_length=255, blank=True, help_text='Dit is optioneel. Standaard gebruikt de agenda het adres van de zorglocatie')
    number = models.CharField('huisnummer', max_length=255, blank=True, help_text='Dit is optioneel. Standaard gebruikt de agenda het adres van de zorglocatie')
    zipcode = models.CharField('postcode', max_length=255, blank=True, help_text='Dit is optioneel. Standaard gebruikt de agenda het adres van de zorglocatie')
    city = models.CharField('plaatsnaam', max_length=255, blank=True, help_text='Dit is optioneel. Standaard gebruikt de agenda het adres van de zorglocatie')

    sportschool = models.ForeignKey('Sportschool', blank=True, null=True, on_delete=models.CASCADE)
    zorglocatie = models.ForeignKey('ZorgLocatie', blank=True, null=True, on_delete=models.CASCADE)
    trainer = models.ForeignKey('Trainer', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Ensure correct name of Den Bosch City
    def save(self, *args, **kwargs):
        if self.city.lower() == 'den bosch':
            self.city = '’s-Hertogenbosch'
        if self.city.lower() == '\'s-hertogenbosch':
            self.city = '’s-Hertogenbosch'
        return super().save(*args, **kwargs)

    def __str__(self):
        return 'Bootcamp op {}'.format(self.date)

    def get_city(self):
        return self.city if self.city else self.zorglocatie.city if self.zorglocatie else ''

    def get_location(self):
        street = self.street if self.street else self.zorglocatie.street if self.zorglocatie else ''
        number = self.number if self.number else self.zorglocatie.number if self.zorglocatie else ''
        zipcode = self.zipcode if self.zipcode else self.zorglocatie.zipcode if self.zorglocatie else ''
        city = self.city if self.city else self.zorglocatie.city if self.zorglocatie else ''
        return '{} {}, {} {}'.format(street, number, zipcode, city).lstrip().rstrip().lstrip(',').rstrip(',')

    class Meta:
        ordering = ['date', 'start_time']
