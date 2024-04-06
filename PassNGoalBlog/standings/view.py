#standings/view.py

from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint
from PassNGoalBlog.resources.standings import StandingResource

standings = Blueprint('standings', __name__)

@standings.route('/standing/<int:year>/<int:league_id>')
def show_standing(year, league_id):
    resource = StandingResource()
    standing_data = resource.get(year, league_id)
    return render_template("standing.html", standing_data=standing_data)