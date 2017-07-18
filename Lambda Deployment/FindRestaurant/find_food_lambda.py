from googleplaces import GooglePlaces, types, lang
import boto3
import json

YOUR_API_KEY = '<insert key here>'  # My private API Key is not provided here for security reasons

google_places = GooglePlaces(YOUR_API_KEY)

def safe_string(str):
    if str != None:
        return str
    else:
        return ''

def lambda_handler(event, context):

    slots = event['currentIntent']['slots']
    location = slots['Location']
    restaurant_type = slots['RestaurantType']

    try:
        query_result = google_places.nearby_search(
            location=location, keyword=restaurant_type,
        radius=20000, types=[types.TYPE_FOOD])
    except:
        return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": 'Sorry I could not find anything with those details. The city you provided seems invalid.'
             }
         }
     }



    response = "I found the following places: "

    if len(query_result.places) < 1:
        return {
            "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Sorry I could not find any restaurants with those details."
            }
        }
    }

    max_places = len(query_result.places)
    char_limit = 640 # Facebook messenger character limit
    

    for place in query_result.places:
        place.get_details()
        # The conditional statement below checks if adding the name of the place and the average rating would exceed character limit
        
        if(len(response) + len(place.name) + len('[ Average Rating: 5 ] ....... ') >= char_limit): # Prevents response from exceeding 640 chars
            return {
                "dialogAction": {                       # Returns response before it becomes too long
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": response
                    }
                }
            }

        response += safe_string(place.name) #+ '(Address: ' + safe_string(place.formatted_address) + ' Phone: ' + safe_string(place.local_phone_number) + ')'

        # Iterates through the reviews and calculates the average rating
        if 'reviews' in list(place.details.keys()):
            sum_ratings = 0
            num_reviews = 0
            for review in place.details['reviews']:
                sum_ratings += review['rating']
                num_reviews += 1
            avg_rating = float(sum_ratings)/float(num_reviews)
            response += '[ Average Rating: {} ] ....... '.format(avg_rating)
        else:
            response += '..........\r'
                
        

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
