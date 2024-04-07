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

class TeamSquadData(Resource):
    def get(self, team_id):
        querystring = {"team": team_id}
        headers = {"X-RapidAPI-Key": api_key,
                   "X-RapidAPI-Host": api_host}
        response = requests.get("https://api-football-v1.p.rapidapi.com/v3/players/squads", 
                                headers=headers, 
                                params=querystring)
        
        # Parse the json and get the expected result
        data = response.json()
        result = {"Goalkeeper": [],
                  "Defender": [],
                  "Midfielder": [],
                  "Attacker":[]}
        players = data["response"][0]["players"]

        # Sort the player based on their position
        for player in players:
            player_json = {
                "id": player["id"],
                "name": player["name"],
                "age": player["age"],
                "number": player["number"],
                "photo": player["photo"]
            }
            result[player["position"]].append(player_json)

        return result