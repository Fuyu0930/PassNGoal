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
        
        if response:
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
        return {"response": "not found"}, 404

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
            fixture_json = {
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
            result.append(fixture_json)

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
        
        if response:
            # Parse the json and get the expected data
            data = response.json()
            result = []
            for fixture_data in data["response"]:
                fixture_json = {
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
                    },
                    "halftime_score": {
                        "home": fixture_data["score"]["halftime"]["home"],
                        "away": fixture_data["score"]["halftime"]["away"]
                    },
                    "fulltime_score": {
                        "home": fixture_data["goals"]["home"],
                        "away": fixture_data["goals"]["away"]
                    }
                }
                result.append(fixture_json)

            return result
        
        return {"response": "not found"}, 404

# Get team's current fixture (live)
class TeamCurrentFixture(Resource):
    def get(self, team_id):
        querystring = {"live": "all", "team": team_id}
        headers = {"X-RapidAPI-Key": api_key,
                   "X-RapidAPI-Host": api_host}
        response = requests.get("https://api-football-v1.p.rapidapi.com/v3/fixtures", headers=headers, params=querystring)
        if response:
            data = response.json()
            if data["results"] == 0:
                return False, {"response": "no current fixture"}
            
            fixture_data = data["response"]

            result = {
                "fixture_info" : {
                    "id": fixture_data["fixture"]["id"],
                    "referee": fixture_data["fixture"]["referee"],
                    "date": fixture_data["fixture"]["date"]
                },
                "fixture_status": {
                    "long": fixture_data["fixture"]["status"]["long"],
                    "elapsed": fixture_data["fixture"]["status"]["elapsed"]
                },
                "league_info": {
                    "id": fixture_data["league"]["id"],
                    "name": fixture_data["league"]["name"],
                    "country": fixture_data["league"]["country"],
                    "logo": fixture_data["league"]["logo"],
                    "round": fixture_data["league"]["round"]
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
                },
                "goals": {
                    "home": fixture_data["goals"]["home"],
                    "away": fixture_data["goals"]["away"]
                },
                "events": fixture_data["events"]
            }
            return True, result
            
        return {"response": "not found"}, 404

# Get team's league based on season
class TeamLeagueInfo(Resource):
    def get(self, year, team_id, is_current):
        # If it is current, then get current league's id
        if is_current == 1:
            querystring = {"team": team_id, "current": "true", "type": "league"}
        else:
            querystring = {"team": team_id, "season": year, "type": "league"}

        # Get the response
        headers = {"X-RapidAPI-Key": api_key,
                   "X-RapidAPI-Host": api_host}
        response = requests.get("https://api-football-v1.p.rapidapi.com/v3/leagues", headers=headers, params=querystring)

        if response:
            data = response.json()
            if len(data["response"]) == 0:
                return {"response": "no league found"}, 204
            
            league_data = data["response"][0]
            result = {
                "league_id": league_data["league"]["id"],
                "league_name": league_data["league"]["name"],
                "league_logo": league_data["league"]["logo"],
                "league_country": league_data["country"]["name"],
                "league_flag": league_data["country"]["flag"],
                "season": league_data["seasons"][0]["year"]
            }

            return result

        return {"response": "not found"}, 404

class TeamStatistics(Resource):
    def get(self, year, team_id, league_id):
        querystring = {"league": league_id, "season": year, "team": team_id}
        headers = {"X-RapidAPI-Key": api_key,
                   "X-RapidAPI-Host": api_host}
        response = requests.get("https://api-football-v1.p.rapidapi.com/v3/teams/statistics", headers=headers, params=querystring)

        if response:
            data = response.json()
            return data["response"]
        
        return {"response": "not found"}, 404
