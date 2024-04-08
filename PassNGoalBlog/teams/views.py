from flask import Flask, render_template, url_for, flash, redirect, Blueprint
from PassNGoalBlog.resources.team_data import TeamSquadData 
from PassNGoalBlog.resources.team_data import TeamNextFixtures
from PassNGoalBlog.resources.team_data import TeamPastFixtures 
from PassNGoalBlog.resources.team_data import TeamCurrentFixture 
from PassNGoalBlog.resources.team_data import TeamLeagueInfo
from PassNGoalBlog.resources.team_data import TeamStatistics


teams = Blueprint('teams', __name__)
@teams.route('/team_overview/<int:year>/<int:team_id>/')
def team_overview(year, team_id):
    team_league_resource = TeamLeagueInfo()
    team_statistics_resource = TeamStatistics()

    team_league_data = team_league_resource.get(year, team_id, 0)
    league_id = team_league_data["league_id"]

    team_overview_data = team_statistics_resource.get(year, team_id, league_id)

    league_data = team_overview_data["league"]
    team_data = team_overview_data["team"]
    form = team_overview_data["form"]
    played_fixtures = team_overview_data["fixtures"]["played"]
    win_fixtures = team_overview_data["fixtures"]["wins"]
    draw_fixtures = team_overview_data["fixtures"]["draws"]
    lose_fixtures = team_overview_data["fixtures"]["loses"]
    goals_for = team_overview_data["goals"]["for"]
    goals_against = team_overview_data["goals"]["against"]

    return render_template("team_overview.html", 
                           team_overview_data=team_overview_data,
                           league_data=league_data,
                           team_data=team_data,
                           form=form,
                           played_fixtures=played_fixtures,
                           win_fixtures=win_fixtures,
                           draw_fixtures=draw_fixtures,
                           lose_fixtures=lose_fixtures,
                           goals_for=goals_for,
                           goals_against=goals_against)

@teams.route('/team_squad/<int:team_id>')
def team_squad(team_id):
    pass


@teams.route('/team_fixture/<int:team_id>')
def team_fixtures(team_id):
    pass