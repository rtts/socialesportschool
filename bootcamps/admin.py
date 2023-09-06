from django.shortcuts import render
from django.utils.html import mark_safe
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import *

class CityFilter(admin.SimpleListFilter):
    title = 'stad'
    parameter_name = 'city'

    def lookups(self, request, model_admin):
        bootcamps = Bootcamp.objects.all()
        cities = {}

        for b in bootcamps:
            cities[b.get_city()] = True

        filters = []
        for c in cities:
            filters.append((c, c))

        return filters

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(bootcamp__city=self.value()) | queryset.filter(bootcamp__zorglocatie__city=self.value())
        return queryset

class BootcampCityFilter(CityFilter):
    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(city=self.value()) | queryset.filter(zorglocatie__city=self.value())
        return queryset

@admin.register(ZorgOrganisatie)
class ZorgOrganisatieAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']

@admin.register(Gemeente)
class GemeenteAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']

@admin.register(ZorgLocatie)
class ZorgLocatieAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'city', 'zorgorganisatie']
    list_filter = ['zorgorganisatie']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(Sportschool)
class SportschoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'city']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'get_bootcamp', 'get_city']
    list_filter = [CityFilter, 'bootcamp__sportschool', 'bootcamp__zorglocatie', 'bootcamp']
    actions = ['email_action']

    def get_bootcamp(self, participant):
        return mark_safe('<a href="{}">{}</a>'.format(reverse('admin:bootcamps_bootcamp_change', args=[participant.bootcamp.id]), participant.bootcamp))
    get_bootcamp.short_description = 'Bootcamp'
    get_bootcamp.admin_order_field = 'bootcamp'

    def get_city(self, participant):
        return participant.bootcamp.get_city()
    get_city.short_description = 'Stad'

    def email_action(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect('email/?ids={}'.format(','.join(selected)))
    email_action.short_description = "Email de geselecteerde personen"

    def show_emails(self, request):
        admin_url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        ids = request.GET.get('ids')
        if not ids:
            raise SuspiciousOperation('GET parameter "ids" is missing')
        objects = self.model.objects.filter(id__in=ids.split(','))
        email_addresses = ', '.join([obj.email_spec() for obj in objects if obj.email])

        return render(request, 'admin/show_emails.html', {
            'title': 'Verstuur een email',
            'email_addresses': email_addresses,
            'admin_url': admin_url,
            'opts': self.model._meta,
        })

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'email/$', self.admin_site.admin_view(self.show_emails)),
        ]
        return my_urls + urls

class InlineParticipantAdmin(admin.StackedInline):
    model = Participant
    extra = 0

@admin.register(Bootcamp)
class BootcampAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'start_time', 'deleted', 'places', 'get_city', 'sportschool', 'zorglocatie']
    list_filter = ['deleted', BootcampCityFilter, 'sportschool', 'zorglocatie']
    inlines = [InlineParticipantAdmin]

    def get_city(self, bootcamp):
        return bootcamp.get_city()
    get_city.short_description = 'Stad'

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass
