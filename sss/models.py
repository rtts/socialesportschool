from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from numberedmodel.models import NumberedModel
from embed_video.fields import EmbedVideoField
from bootcamps.models import *

class Upload(models.Model):
    file = models.FileField('Bestand')

    def __str__(self):
        return self.file.url

    class Meta:
        ordering = ['file']

class Page(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    title = models.CharField('titel', max_length=255)
    slug = models.SlugField('URL', blank=True, unique=True, help_text='het gedeelte achter www.socialesportschool.nl')
    external_url = models.URLField('externe URL', blank=True)
    menu = models.BooleanField('zichtbaar in het menu', default=True)
    image = models.ImageField('afbeelding (desktop)', blank=True, help_text='Deze afbeelding wordt de banner van deze pagina')
    mobile_image = models.ImageField('afbeelding (mobiel)', blank=True, help_text='Deze afbeelding wordt de banner van deze pagina op de smalste layout. Als je hier géén afbeelding kiest, dan wordt de afbeelding desktop gebruikt, maar wel verkleind tot een breedte van 800 pixels.')

    def __str__(self):
        return '{}. {}'.format(self.position, self.title)

    def get_absolute_url(self):
        if self.slug:
            return reverse('page', args=[self.slug])
        else:
            return '/'

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Pagina’s'
        ordering = ['position']

class Config(models.Model):
    TYPES = [
        (1, 'Footer links'),
        (2, 'Footer midden'),
        (3, 'Footer rechts'),
        (10, 'Registratie aanmeldpagina'),
        (11, 'Registratie bedankt'),
        (12, 'Registratie email onderwerp'),
        (13, 'Registratie email inhoud'),
        (14, 'Registratie activatie bedankt'),
        (15, 'Registratie activatie mislukt'),
        (20, 'Inlogpagina'),
        (21, 'Uitgelogd pagina'),
        (30, 'Wachtwoord vergeten pagina'),
        (31, 'Wachtwoord vergeten bedankt'),
        (32, 'Wachtwoord vergeten nieuw wachtwoord'),
        (33, 'Wachtwoord vergeten klaar'),
        (34, 'Algemene Voorwaarden'),
        (40, 'Nieuwe zorglocatie opgeven'),
        (41, 'Nieuwe sportclub opgeven'),
        (42, 'Melding over algemene voorwaarden'),
        (49, 'Infotekst voordat deelnemers zich aanmelden'),
        (50, 'Bedankt aanmelden deelnemer'),
        (60, 'Email na aanmelden deelnemer (onderwerp)'),
        (61, 'Email na aanmelden deelnemer (inhoud)'),
    ]

    parameter = models.PositiveIntegerField(choices=TYPES, unique=True)
    content = models.TextField('inhoud')

    def __str__(self):
        return "{}. {}".format(self.parameter, self.get_parameter_display())

    class Meta:
        verbose_name = 'Configuratieparameter'
        ordering = ['parameter']

class SocialMedia(NumberedModel):
    position = models.PositiveIntegerField('positie', blank=True)
    image = models.ImageField('afbeelding')
    hyperlink = models.URLField()

    class Meta:
        verbose_name_plural = 'Social Media'
        ordering = ['position']

class Section(NumberedModel):
    visibility = [
        (1, 'Altijd zichtbaar'),
        (2, 'Niet op smartphone'),
        (3, 'Onzichtbaar'),
    ]
    colors = [
        (1, 'Wit'),
        (2, 'Blauw'),
        (3, 'Blauw-Wit'),
    ]
    types = [
        (1, 'Normaal'),
        (2, 'Agenda smal'),
        (3, 'Agenda breed'),
        (4, 'Partners'),
    ]
    page = models.ForeignKey(Page, verbose_name='pagina', related_name='sections', on_delete=models.CASCADE)
    position = models.PositiveIntegerField('positie', blank=True)
    visibility = models.PositiveIntegerField('zichtbaarheid', default=1, choices=visibility)
    type = models.PositiveIntegerField('soort sectie', default=1, choices=types)
    partners_sport = models.ManyToManyField(Sportschool, blank=True)
    partners_locatie = models.ManyToManyField(ZorgLocatie, blank=True)
    partners_zorg = models.ManyToManyField(ZorgOrganisatie, blank=True)
    partners_gemeenten = models.ManyToManyField(Gemeente, blank=True)
    color = models.PositiveIntegerField('kleur', default=1, choices=colors)
    title = models.CharField('titel', max_length=255, blank=True)
    contents = RichTextField('inhoud', blank=True)
    image = models.ImageField('afbeelding', blank=True)
    video = EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')
    button = models.CharField('button', max_length=255, blank=True)
    hyperlink = models.CharField(max_length=255, blank=True)

    def number_with_respect_to(self):
        return self.page.sections.all()

    def __str__(self):
        return 'Sectie: #{} {}'.format(self.position, self.title)

    class Meta:
        verbose_name = 'sectie'
        ordering = ['position']
