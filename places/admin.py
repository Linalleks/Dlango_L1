from django.contrib import admin

from .models import Place, PlaceImage


class ImageInline(admin.TabularInline):
    model = PlaceImage
    raw_id_fields = ['place']
    extra = 1
    verbose_name_plural = 'Фотографии'
    verbose_name = 'Фотография'


class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceImage)
