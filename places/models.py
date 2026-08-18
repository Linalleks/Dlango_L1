from django.db import models
from django.utils.html import mark_safe


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Короткое описание', blank=True)
    description_long = models.TextField('Длинное описание', blank=True)
    lat = models.FloatField('Широта')
    lng = models.FloatField('Долгота')

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        verbose_name='Место',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField('Изображение', upload_to='images')
    position = models.PositiveIntegerField('Позиция', default=0)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['position']

    def __str__(self):
        return f'{self.position} - {self.place.title}'

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{0}" style="max-height: 200px;" />'.format(self.image.url))
        else:
            return '(No image)'