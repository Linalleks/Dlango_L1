from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from django.contrib import admin

from .models import Place, PlaceImage


class ImageInline(SortableTabularInline):
    model = PlaceImage
    raw_id_fields = ['place']
    list_display = ['image_preview']
    readonly_fields = ['image_preview']
    fields = ["image", "image_preview"]
    extra = 1
    verbose_name_plural = 'Фотографии'
    verbose_name = 'Фотография'


class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]


class PlaceImageAdmin(admin.ModelAdmin):
    raw_id_fields = ['place']


admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceImage, PlaceImageAdmin)
