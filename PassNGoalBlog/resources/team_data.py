from flask_restful import Resource
import requests
import json

##########################################
######## Get the api_key and host ########
##########################################
file_path = '/Users/william/Desktop/PassNGoal/PassNGoalBlog/resources/headers.json'
with open(file_path, 'r') as file:
    headers = json.load(file)
api_key = headers["X-RapidAPI-Key"]
api_host = headers["X-RapidAPI-Host"]


#################################
######## Set up team API ########
#################################

