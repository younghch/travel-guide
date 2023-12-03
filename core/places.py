import os
import requests

API_URL = 'https://places.googleapis.com/v1/places:searchNearby'
API_KEY = os.environ.get('GCP_PLACES_API_KEY')
REQUIRED_FIELS = ['places.displayName', 'places.googleMapsUri']


class location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


TOURIST_PLACES = [
    'art_gallery',
    'museum',
    'performing_arts_theater',
    'amusement_center',
    'amusement_park',
    'aquarium',
    'casino',
    'convention_center',
    'cultural_center',
    'dog_park',
    'hiking_area',
    'historical_landmark',
    'marina',
    'movie_theater',
    'national_park',
    'park',
    'tourist_attraction',
    'visitor_center',
    'zoo',
]

HEADERS = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': API_KEY,
    'X-Goog-FieldMask': ','.join(REQUIRED_FIELS),
}


def get_nearby_places(location: location, radius=50, language_code='ko'):
    data = {
        'includedTypes': TOURIST_PLACES,
        'maxResultCount': 10,
        'locationRestriction': {
            'circle': {
                'center': {
                    'latitude': location.latitude,
                    'longitude': location.longitude},
                'radius': radius
            }
        },
        'languageCode': language_code,
        'rankPreference': 'POPULARITY',
        'maxResultCount': 10
    }

    res = requests.post(API_URL, json=data, headers=HEADERS)
    return res.json().get('places')

def get_names_of_place(place):
    return place.get('displayName').get('text')