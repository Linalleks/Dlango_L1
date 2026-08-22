import json
from io import BytesIO

import requests
from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand

from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Загружает JSON по указанному URL и сохраняет данные в базу'

    def add_arguments(self, parser):
        parser.add_argument('file_url', help='URL на JSON для загрузки')

    def handle(self, *args, **options):
        file_url = options['file_url']

        try:
            response = requests.get(file_url)
            response.raise_for_status()
            place_properties = response.json()

            place, created = Place.objects.get_or_create(
                title=place_properties['title'],
                lat=place_properties['coordinates']['lat'],
                lng=place_properties['coordinates']['lng'],
                defaults={
                    "title": place_properties['title'],
                    "description_short": place_properties['description_short'],
                    "description_long": place_properties['description_long'],
                    "lat": place_properties['coordinates']['lat'],
                    "lng": place_properties['coordinates']['lng'],
                }
            )
            if created:
                print(f'Добавлено новое место: "{place}"')
                imgs_urls = place_properties['imgs']
                for num, img_url in enumerate(imgs_urls, start=1):
                    response = requests.get(img_url)
                    response.raise_for_status()
                    img_name = img_url.split('/')[-1]
                    image = BytesIO(response.content)
                    place_image = PlaceImage(place=place, position=num)
                    place_image.image.save(img_name, image)
                    print(f'Добавлено фото "{img_name}"')
                print(f'Всего добавлено {num} фото для нового места "{place}"')
            else:
                print(f'Место "{place}" уже существует')

        except requests.exceptions.RequestException as e:
            print(f'Ошибка при запросе к URL: {e}')
        except json.JSONDecodeError as e:
            print(f'Не удалось распарсить JSON: {e}')
        except Exception as e:
            print(f'Неожиданная ошибка: {e}')
        except MultipleObjectsReturned:
            print(f"Найдено несколько объектов для {place_properties}.")
