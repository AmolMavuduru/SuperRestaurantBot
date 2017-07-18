from googleplaces import GooglePlaces, types, lang
import boto3
import json

YOUR_API_KEY = '<insert key here>'

google_places = GooglePlaces(YOUR_API_KEY)

def lambda_handler(event, context):

    slots = event['currentIntent']['slots']
    location = slots['Location']
    restaurant_type = slots['RestaurantType']


    query_result = google_places.nearby_search(
            location=location, keyword=restaurant_type,
        radius=20000, types=[types.TYPE_FOOD])

    response = "I found the following places: "
    for place in query_result.places:
        response = response + place.name + ", "

    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": response
            }
        }
    }
