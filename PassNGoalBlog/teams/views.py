from flask import Flask, render_template, url_for, flash, redirect, Blueprint
from PassNGoalBlog.resources.team_data import TeamSquadData 
from PassNGoalBlog.resources.team_data import TeamNextFixtures
from PassNGoalBlog.resources.team_data import TeamPastFixtures 
from PassNGoalBlog.resources.team_data import TeamCurrentFixture 
from PassNGoalBlog.resources.team_data import TeamLeagueInfo
from PassNGoalBlog.resources.team_data import TeamStatistics


teams = Blueprint('teams', __name__)
