from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import *

admin.site.site_title = 'Sociale Sportschool Beheer'
admin.site.site_header = 'Sociale Sportschool Beheer'
admin.site.site_url = None
admin.site.index_title = 'Overzicht'

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    pass

class InlineSectionAdmin(admin.StackedInline):
    save_on_top = True
    model = Section
    extra = 0
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {"slug": ("title",)}
    inlines = [InlineSectionAdmin]
    list_display = ['position', 'title', 'slug', 'menu']
    list_display_links = ['title']
    list_filter = ['menu']
    # list_editable = ['position']

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_content']
    exclude = ['parameter']

    def get_content(self, obj):
        max = 100
        return (obj.content[:max] + '...') if len(obj.content) > max else obj.content

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['position', 'hyperlink']
    list_display_links = ['hyperlink']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['__str__', 'visibility', 'title', 'page']
    list_filter = ['page']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
