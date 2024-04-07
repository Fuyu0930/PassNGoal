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

# Get the current team data based on the team id
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

# Get certain numbers of future fixture based on the team id
class TeamNextFixtures(Resource):
    def get(self, team_id, round_num):
        querystring = {"next": round_num, "team": team_id}
        headers = {"X-RapidAPI-Key": api_key,
                   "X-RapidAPI-Host": api_host}
        response = requests.get("https://api-football-v1.p.rapidapi.com/v3/fixtures",
                                headers=headers,
                                params=querystring)
        
        # Parse the json and get the expected result
        data = response.json()
        result = []
        for fixture_data in data["response"]:
            player_json = {
                "fixture_info": {
                    "fixture_id": fixture_data["fixture"]["id"],
                    "referee": fixture_data["fixture"]["referee"],
                    "date": fixture_data["fixture"]["date"],
                    "timezone": fixture_data["fixture"]["timezone"]
                },
                "league_info": {
                    "league_id": fixture_data["league"]["id"],
                    "league": fixture_data["league"]["name"],
                    "league_logo": fixture_data["league"]["logo"]
                },
                "home_team": {
                    "home_id": fixture_data["teams"]["home"]["id"],
                    "home_name": fixture_data["teams"]["home"]["name"],
                    "home_logo": fixture_data["teams"]["home"]["logo"]
                },
                "away_team": {
                     "away_id": fixture_data["teams"]["away"]["id"],
                    "away_name": fixture_data["teams"]["away"]["name"],
                    "away_logo": fixture_data["teams"]["away"]["logo"]
                }
            }
            result.append(player_json)

        return result

# Get certain numbers of past fixture based on the team id
class TeamPastFixtures(Resource):
    def get(self, team_id, round_num):
        querystring = {"last": round_num, "team": team_id}
        headers = {"X-RapidAPI-Key": api_key,
                   "X-RapidAPI-Host": api_host}
        response = requests.get("https://api-football-v1.p.rapidapi.com/v3/fixtures",
                                headers=headers,
                                params=querystring)
        
        # Parse the json and get the expected data
        data = response.json()
        result = []







        return result