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



    response = ""

    if len(query_result.places) == 0:

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

    elif len(query_result.places) == 1:

        for place in query_result.places: # This iteration wil only occur once since there is one item in the list
            place.get_details()
            reviews_string = "Here is what people had to say about {} : ".format(place.name)
            response += "I found {0} in {1}.".format(place.name, location)
            sum_ratings = 0
            num_reviews = 0
            if (place.details['reviews']):
                for review in place.details['reviews']: # Will iterate through all reviews and and calculate the average
                    sum_ratings += review['rating']
                    num_reviews += 1
                    new_review = "Review {0}: {1} ..... ".format(num_reviews, review['text'])
                    
                    if(len(reviews_string) + len(response) + len(new_review) + 45 >= 640): # If there is a risk of exceeding limit return the response
                        avg_rating = float(sum_ratings) / float(num_reviews)
                        response += ' {0} received an average rating of: {1} out of 5 '.format(place.name, avg_rating)
                        response += reviews_string
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
                    reviews_string += "Review {0}: {1} ..... ".format(num_reviews, review['text'])
            
                avg_rating = sum_ratings / num_reviews
            response += ' {0} received an average rating of: {1} out of 5'.format(place.name, avg_rating)
            response += reviews_string # Adds the text of all of the reviews to the response
    else:
        response += "I found the following results for {} : ".format(restaurant_name)
        exact_match = False
        for place in query_result.places: # This iteration will occur multiple times since the list has multiple items
            if(place.name == restaurant_name): # If there is an exact match
                exact_match = True
                place.get_details()
                sum_ratings = 0
                num_reviews = 0
                reviews_string = "Here is what people had to say about {} : ".format(place.name)
                if(place.details['reviews']):
                    for review in place.details['reviews']:
                        sum_ratings += review['rating']
                        num_reviews += 1
                        new_review = "Review {0}: {1} ..... ".format(num_reviews, review['text'])
                        if(len(reviews_string) + len(response) + len(new_review) + 20 >= 640): # If there is a risk of exceeding limit return the response
                            avg_rating = float(sum_ratings) / float(num_reviews)
                            response += ' {0} received an average rating of: {1} out of 5 '.format(place.name, avg_rating)
                            response += reviews_string
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
                        reviews_string += new_review
                    avg_rating = sum_ratings / num_reviews
                    response += ' {0} which received an average rating of {1} out of 5. '.format(place.name, avg_rating)
                    response += reviews_string
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
            elif(not exact_match): # If the current place is not an exact match
                place.get_details()
                sum_ratings = 0
                num_reviews = 0
                if(place.details['reviews']):
                    for review in place.details['reviews']:
                        sum_ratings += review['rating']
                        num_reviews += 1
                    avg_rating = float(sum_ratings) / float(num_reviews)
                    if(len(response) + len(' {0} (average rating : {1} out of 5) ..... '.format(place.name, avg_rating)) >= 640):
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
                    response += ' {0} (average rating : {1} out of 5) ..... '.format(place.name, avg_rating)

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

