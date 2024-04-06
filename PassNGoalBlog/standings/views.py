#standings/view.py
from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint
from PassNGoalBlog.resources.football_data import StandingData

standings = Blueprint('standings', __name__)

@standings.route('/league_standing/<int:year>/<int:league_id>')
def show_standing(year, league_id):
    resource = StandingData()
    standing_data = resource.get(year, league_id)
    print(standing_data)
    print(league_id)
    return render_template("league_data.html", standing_data=standing_data, league_id=league_id, year=year)