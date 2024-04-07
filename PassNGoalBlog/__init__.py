# PassNGoalBlog/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

######################################
########### Database Setup ###########
######################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#####################################
########### Login Configs ###########
#####################################
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login' # The view of log in

from PassNGoalBlog.core.views import core
from PassNGoalBlog.error_pages.handlers import error_pages
from PassNGoalBlog.users.views import users
from PassNGoalBlog.blog_posts.views import blog_posts
from PassNGoalBlog.leagues_stat.views import standings

app.register_blueprint(blog_posts)
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(standings)

##################################
########### Api Setups ###########
##################################
from PassNGoalBlog.resources.league_data import StandingData
from PassNGoalBlog.resources.league_data import TopScorersData
from PassNGoalBlog.resources.league_data import TopAssistData
from PassNGoalBlog.resources.team_data import TeamSquadData
from PassNGoalBlog.resources.team_data import TeamNextFixtures
from PassNGoalBlog.resources.team_data import TeamPastFixtures
from PassNGoalBlog.resources.team_data import TeamCurrentFixture
api = Api(app)
api.add_resource(StandingData, '/leage_standing_data/<int:year>/<int:league_id>')
api.add_resource(TopScorersData, '/top_scorer_data/<int:year>/<int:league_id>')
api.add_resource(TopAssistData, '/top_assist_data/<int:year>/<int:league_id>')
api.add_resource(TeamSquadData, '/team_squad_data/<int:team_id>')
api.add_resource(TeamNextFixtures, '/team_next_fixtures/<int:team_id>/<int:round_num>')
api.add_resource(TeamPastFixtures, '/team_past_fixtures/<int:team_id>/<int:round_num>')
api.add_resource(TeamCurrentFixture, '/team_current_fixture/<int:team_id>')