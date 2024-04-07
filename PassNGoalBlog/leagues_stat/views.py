#standings/view.py
from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint
from PassNGoalBlog.resources.league_data import StandingData, TopScorersData, TopAssistData

standings = Blueprint('standings', __name__)

@standings.route('/league_standing/<int:year>/<int:league_id>')
def show_standing(year, league_id):
    standing_resource = StandingData()
    top_scorer_resource = TopScorersData()
    top_assist_resource = TopAssistData()

    standing_data = standing_resource.get(year, league_id)
    top_scorer_data = top_scorer_resource.get(year, league_id)
    top_assist_data = top_assist_resource.get(year, league_id)
    return render_template("league_data.html", 
                           standing_data=standing_data, 
                           top_scorer_data=top_scorer_data,
                           top_assist_data=top_assist_data,
                           league_id=league_id, 
                           year=year)