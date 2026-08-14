from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Короткое описание', blank=True)
    description_long = models.TextField('Длинное описание', blank=True)
    # image = models.ImageField('Изображение', upload_to='images', null=True, blank=True)
    lat = models.FloatField('Широта')
    lng = models.FloatField('Долгота')

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title
