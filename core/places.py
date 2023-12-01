import os
import requests

API_URL = 'https://places.googleapis.com/v1/places:searchNearby'
API_KEY = os.environ.get('GCP_PLACES_API_KEY')
REQUIRED_FIELS = ['places.displayName', 'places.formattedAddress']
LANUGAGE_CODE = 'ko'
RADIUS = 1000.0


class location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


test_location = location(37.5734003, 126.9772253)

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

data = {
    'includedTypes': TOURIST_PLACES,
    'maxResultCount': 10,
    'locationRestriction': {
        'circle': {
            'center': {
                'latitude': test_location.latitude,
                'longitude': test_location.longitude},
            'radius': RADIUS
        }
    },
    'languageCode': LANUGAGE_CODE,
    'rankPreference': 'POPULARITY',
    'maxResultCount': 20
}

headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': API_KEY,
    'X-Goog-FieldMask': '*'
}

res = requests.post(API_URL, json=data, headers=headers)
print(res.text)
