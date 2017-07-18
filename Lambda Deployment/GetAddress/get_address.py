from googleplaces import GooglePlaces, types, lang
import boto3
import json

YOUR_API_KEY = '<insert key here>'  # My private API Key is not provided here for security reasons

google_places = GooglePlaces(YOUR_API_KEY)

def lambda_handler(event, context):
    slots = event['currentIntent']['slots']
    location = slots['Location']
    restaurant_name = slots['RestaurantName']

    try:
        query_result = google_places.nearby_search(
            location=location, keyword=restaurant_name,
            radius=20000, types=[types.TYPE_FOOD])
    except:
        return {  # If an error occurs it is probably because the user provided an invalid city.
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                "contentType": "PlainText",
                "content": "Sorry I could not find anything with those details. The city you provided seems invalid."
            }
        }
    }

    response = "I found the following places: "

    char_limit = 640

    if len(query_result.places) == 0:   # If the search returned no results

        return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Sorry I could not find any results for that place."
            }
        }
    }
    else:
        for place in query_result.places:
            place.get_details()
            if(len(response) + len(place.name) + len("Address: {}".format(place.address)) + 5 >= 640): # Checks character limit (+5 for spaces and periods)
                return {                    # If the character limit is about to be exceeded, returns accummulated response
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled",
                        "message": {
                            "contentType": "PlainText",
                            "content": response
                        }
                    }
                }
            response += place.name + " "
            response += "Address: {}".format(place.address) + "...."

    return {  # If the character has not been exceeded and all places have been explored, return response
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": response
            }
        }
    }
