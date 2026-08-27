from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def serialize_features(place):
    return {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [place.lng, place.lat]
        },
        'properties': {
            'title': place.title,
            'placeId': place.id,
            'detailsUrl': reverse('place', args=[place.id])
        }
    }


def index(request):
    places = Place.objects.all()
    context = {
        'places_geojson': {
            'type': 'FeatureCollection',
            'features': [serialize_features(place) for place in places]
        }
    }
    return render(request, 'index.html', context)


def get_place(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    images = place.images.all()
    place_features = {
        'title': place.title,
        'imgs': [request.build_absolute_uri(image.image.url) for image in images],
        'short_description': place.short_description,
        'long_description': place.long_description,
        'coordinates': {
            'lng': place.lng,
            'lat': place.lat,
        },
    }
    return JsonResponse(place_features, json_dumps_params={'ensure_ascii': False, 'indent': 2})
