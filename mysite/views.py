from django.shortcuts import render
from django.templatetags.static import static

from places.models import Place, PlaceImage


def serialize_place(place):
    images = place.images.all()
    return {
        'title': place.title,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'lat': place.lat,
        'lng': place.lng,
        'images': [serialize_image(image) for image in images],
    }


def serialize_features(place):
    # images = place.images.all()
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [place.lng, place.lat]
        },
        "properties": {
            "title": place.title,
            "placeId": place.id,
            "detailsUrl": static('/places/moscow_legends.json')
        }
    }


def serialize_image(image):
    return {
        'position': image.position,
        'image': image.image,
    }


def index(request):
    places = Place.objects.all()
    context = {
        'places_geojson': {
            "type": "FeatureCollection",
            "features": [serialize_features(place) for place in places]
            #     {
            #         "type": "Feature",
            #         "geometry": {
            #             "type": "Point",
            #             "coordinates": [37.62, 55.793676]
            #         },
            #         "properties": {
            #             "title": "«Легенды Москвы",
            #             "placeId": "moscow_legends",
            #             "detailsUrl": static('/places/moscow_legends.json')
            #         }
            #     },
            #     {
            #         "type": "Feature",
            #         "geometry": {
            #             "type": "Point",
            #             "coordinates": [37.64, 55.753676]
            #         },
            #         "properties": {
            #             "title": "Крыши24.рф",
            #             "placeId": "roofs24",
            #             "detailsUrl": static('/places/roofs24.json')
            #         }
            #     }
            # ]
        }
    }

    return render(request, 'index.html', context)
