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
from PassNGoalBlog.standings.views import standings

app.register_blueprint(blog_posts)
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(standings)

##################################
########### Api Setups ###########
##################################
from PassNGoalBlog.resources.football_data import StandingData
api = Api(app)
api.add_resource(StandingData, '/leage_standing_data/<int:year>/<int:league_id>')