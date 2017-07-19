# SuperRestaurantBot
Chatbot that finds restaurants and reviews. Created for the 2017 AWS Chatbot Challenge.

This chatbot was created using AWS Lex and AWS Lambda and is designed to function as a Facebook Messenger application.
The Super Restaurant Bot is capable to finding restaurants based on the food preference that the user specifies in any
valid location and can also find reviews for specific restaurants. This application is now public and can be found on Facebook at: https://www.facebook.com/superrestaurantbot/ .

## What is in this repository:
- bot_definition.json - a JSON configuration file that describes the slots, intents, sample-utterances, and other details regarding the
AWS Lex components of the bot.
- Lambda Deployment - folder that contains the files necessary for creating lambda deployment packages for the lambda functions that
fulfill each intent. This folder contains the following sub-directories/zip files:
  - FindRestaurant - contains the deployment package for the Lambda function that fulfills the FindRestaurant intent:
      - The code for the lambda function is located in the find_food_lambda.py file.
  - GetReviews - contains the deployment package for the Lambda function that fulfils the GetReviews intent:
      - The code for the lambda function is located in the get_reviews.py file.
  - GetAddress - contains the deployment package for the Lambda function that fulfills the GetAddress intent:
      - The code for the lambda function is located in the get_address.py file.
  - HelloRestaurantBot.zip - package for simple Lambda function that responds to a greeting.
  - HelpRestaurantBot.zip - package for simple Lambda function that responds to a help request.
      
## Chatbot Design
This chatbot contains three primary intents and two other intents that are just used for conversation. The three primary intents are:
- FindRestaurant - finds restaurants and their average ratings given the type of food preferred and the location as inputs.
- GetReviews - gets reviews for a specific restaurant in a specific location.
- GetAddress - finds the addresses of the restaurants in a particular city returned by a search result.

The chatbot also contains an intent that responds to a greeting such as "Hello" and the Lex built-in HelpIntent. 

Libraries/APIs used:
- Python-Google-Places - a python wrapper for the Google Places API. The repository can be found here: https://github.com/slimkrazy/python-google-places
- boto3 - standard AWS library for python.
- python's json library - used for dealing with JSON input and output.

## Testing Instructions for AWS Chatbot Challenge:
If you are here as a judge for the AWS Chatbot Challenge, this application is now public. The Facebook page can be found at: https://www.facebook.com/superrestaurantbot/
Here is how to test this bot:
- If you want to find a restaurant type something such as "Find a restaurant" and then the bot will prompt you for a city and the type of food
you would prefer. If the city does not exist, an exception is triggered and the bot will tell you that no places were found and perhaps the city was
invalid. The bot should return a list of search results for that query.
- If you want to get the reviews for a restaurant type "Get reviews" or something such as "get reviews for <Restaurant Name>" and follow a similar process as in the 
previous intent.
- The GetAddress intent also follows a similar process.


