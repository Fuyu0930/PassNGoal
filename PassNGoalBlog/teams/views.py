import datetime
from flask import Flask, render_template, url_for, flash, redirect, Blueprint
from PassNGoalBlog.resources.team_data import TeamSquadData 
from PassNGoalBlog.resources.team_data import TeamNextFixtures
from PassNGoalBlog.resources.team_data import TeamPastFixtures 
from PassNGoalBlog.resources.team_data import TeamCurrentFixture 
from PassNGoalBlog.resources.team_data import TeamLeagueInfo
from PassNGoalBlog.resources.team_data import TeamStatistics
from PassNGoalBlog.resources.league_data import StandingData, TopScorersData, TopAssistData

teams = Blueprint('teams', __name__)
today = datetime.date.today()

def find_target_team(data, target):
    index = None
    
    for i, team_data in enumerate(data):
        if team_data["team_id"] == target:
            index = i
            break

    if index == 0:
        return data[:3]
    elif index == len(data) - 1:
        return data[-3:]
    else:
        return data[index-1:index+2]

@teams.route('/team_overview/<int:year>/<int:team_id>/<int:is_current>')
def team_overview(year, team_id, is_current):
    team_league_resource = TeamLeagueInfo()
    team_statistics_resource = TeamStatistics()
    standing_data_resource = StandingData()

    if is_current == 1:
        year = int(today.year) - 1
        team_league_data = team_league_resource.get(year, team_id, 1)
    else:
        team_league_data = team_league_resource.get(year, team_id, 0)

    league_id = team_league_data["league_id"]

    # Get the standing with the target team
    league_standing_data = standing_data_resource.get(year, league_id)
    team_standing = find_target_team(league_standing_data, team_id)

    # Get the team statistics
    team_overview_data = team_statistics_resource.get(year, team_id, league_id)

    league_data = team_overview_data["league"]
    team_data = team_overview_data["team"]

    # Get the recent form
    form = team_overview_data["form"][-5:]
    recent_form = {"win": 0, "draw": 0, "loss": 0}

    for match in form:
        if match == "W":
            recent_form["win"] += 1
        elif match == "D":
            recent_form["draw"] += 1
        else:
            recent_form["loss"] += 1
    
    played_fixtures = team_overview_data["fixtures"]["played"]
    win_fixtures = team_overview_data["fixtures"]["wins"]
    draw_fixtures = team_overview_data["fixtures"]["draws"]
    loss_fixtures = team_overview_data["fixtures"]["loses"]
    goals_for = team_overview_data["goals"]["for"]
    goals_against = team_overview_data["goals"]["against"]

    return render_template("team_overview.html", 
                           team_overview_data=team_overview_data,
                           league_data=league_data,
                           team_data=team_data,
                           recent_form=recent_form,
                           played_fixtures=played_fixtures,
                           win_fixtures=win_fixtures,
                           draw_fixtures=draw_fixtures,
                           loss_fixtures=loss_fixtures,
                           goals_for=goals_for,
                           goals_against=goals_against,
                           team_standing=team_standing)


@teams.route('/team_squad/<int:team_id>')
def team_squad(team_id):
    team_squad_resource = TeamSquadData()
    team_squad_info = team_squad_resource.get(team_id)
    team_data = team_squad_info["team_data"]
    goalkeeper_info = team_squad_info["Goalkeeper"]
    defender_info = team_squad_info["Defender"]
    midfielder_info = team_squad_info["Midfielder"]
    attacker_info = team_squad_info["Attacker"]

    return render_template("team_squad.html",
                           team_data=team_data,
                           goalkeeper_info=goalkeeper_info,
                           defender_info=defender_info,
                           midfielder_info=midfielder_info,
                           attacker_info=attacker_info)


@teams.route('/team_fixture/<int:team_id>')
def team_fixtures(team_id):
    next_fixture_resource = TeamNextFixtures()
    past_fixture_resource = TeamPastFixtures()
    team_squad_resource = TeamSquadData()

    next_fixture_data = next_fixture_resource.get(team_id, 3)
    past_fixture_data = past_fixture_resource.get(team_id, 12)
    team_squad_data = team_squad_resource.get(team_id)

    team_data = team_squad_data["team_data"]

    return render_template("team_fixture.html",
                           team_data=team_data,
                           next_fixture_data=next_fixture_data,
                           past_fixture_data=past_fixture_data)