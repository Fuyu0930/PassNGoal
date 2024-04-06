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
######## Set up own API ########
#################################

# Get the standingData based on league and year
class StandingData(Resource):
    def get(self, year, league_id):
        querystring = {'season': str(year), 'league': str(league_id)}
        headers = {"X-RapidAPI-Key": api_key,
                   "X-RapidAPI-Host": api_host}
        response = requests.get("https://api-football-v1.p.rapidapi.com/v3/standings", headers=headers, params=querystring)

        # Parse the json and get the result
        data = response.json()
        extracted_data = [
            {
                "rank": item["rank"],
                "team": item["team"]["name"],
                "team_logo": item["team"]["logo"],
                "points": item["points"],
                "goals_for": item["all"]["goals"]["for"],
                "goals_against": item["all"]["goals"]["against"],
                "goal_difference": item["goalsDiff"],
                "form": item["form"]
            }
            for league_data in data["response"]
            for standings_group in league_data["league"]["standings"]
            for item in standings_group
        ]

        return extracted_data

class TopScorersData(Resource):
    def get(year, league_id):
        querystring = {'season': str(year), 'league': str(league_id)}
        headers = {"X-RapidAPI-Key": api_key,
                   "X-RapidAPI-Host": api_host}
        response = requests.get("https://api-football-v1.p.rapidapi.com/v3/players/topscorers", headers=headers, params=querystring)

        # Parse the json and get the result
        data = response.json()
        extracted_data = [
            {
                "player_id": player_data["player"]["id"],
                "firstname": player_data["player"]["firstname"],
                "lastname": player_data["player"]["lastname"],
                "photo": player_data["player"]["photo"],
                "team_id": player_data["statistics"]["team"]["id"],
                "team_logo": player_data["statistics"]["team"]["logo"],
                "appearences": player_data["statistics"]["games"]["appearances"],
                "goals": player_data["statistics"]["goals"]["total"],
                "penalty": player_data["statistics"]["penalty"]["scored"]
            }
            for player_data in data["response"]
        ]

        return extracted_data