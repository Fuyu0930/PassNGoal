#models.py
from PassNGoalBlog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone

# Import the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# The User class
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(64), nullable=False, default = 'default_profile.png')
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"Username {self.username}"

# The BlogPost class
class BlogPost(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    date = db.Column(db.DateTime, nullable = False, default = datetime.now(timezone.utc))
    title = db.Column(db.String(140), nullable = False)
    text = db.Column(db.Text, nullable = False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id
    
    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- {self.title}"

# The League class
# class League(db.Model):
#     __tablename__ = 'leagues'
#     id = db.Column(db.Integer, primary_key =True)
#     name = db.Column(db.String(64), nullable = False)
#     country = db.Column(db.String(64), nullable = False)
#     logo = db.Column(db.String(256), nullable = False)
#     flag = db.Column(db.String(256), nullable = False)
#     seasons = db.relationship('Season', backref = 'season', lazy = True)

#     def __init__(self, name, country, logo, flag):
#         self.name = name
#         self.country = country
#         self.logo = logo
#         self.flag = flag
    
#     def json(self):
#         res = {"name": self.name,
#                "country": self.country,
#                "logo": self.logo,
#                "flag": self.flag}
#         return res


# # The Season class
# class Season(db.Model):
#     __tablename__ = 'seasons'
#     id = db.Column(db.Integer, primary_key = True)
#     league_id = db.Column(db.Integer, db.ForeignKey('leagues.id'))
#     year = db.Column(db.Integer)
#     standings = db.relationship('Standing', backref = 'season', lazy = True)

#     def __init__(self, league_id, year):
#         self.league_id = league_id
#         self.year = year
    
#     def json(self):
#         res = {"league_id": self.league_id,
#                "year": self.year}
#         return res

# # The Team class
# class Team(db.Model):
#     __tablename__ = 'teams'
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String)
#     logo = db.Column(db.String)
#     standings = db.relationship('Standing', backref = 'team', lazy = True)

#     def __init__(self, name, logo):
#         self.name = name
#         self.logo = logo
    
#     def json(self):
#         res = {"name": self.name,
#                "logo": self.logo}
#         return res

# #The Standing class
# class Standing(db.Model):
#     __tablename__ = 'standings'
#     id = db.Column(db.Integer, primary_key = True)
#     season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable = False)
#     team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable = False)
#     rank = db.Column(db.Integer)
#     points = db.Column(db.Integer)
#     goals_for = db.Column(db.Integer)
#     goals_against = db.Column(db.Integer)
#     goal_difference = db.Column(db.Integer)
#     form = db.Column(db.String)
#     status = db.Column(db.String)
#     description = db.Column(db.String)

#     def __init__(self, season_id, team_id, rank, points, goals_for, goals_against, goal_difference, form, status, description):
#         self.season_id = season_id
#         self.team_id = team_id
#         self.rank = rank
#         self.points = points
#         self.goals_for = goals_for
#         self.goals_against = goals_against
#         self.goal_difference = goal_difference
#         self.form = form
#         self.status = status
#         self.description = description

#     def json(self):
#         res = {"rank": self.rank, 
#                "team_name": Team.query.filter_by(id=self.team_id).first().name,
#                "team_logo": Team.query.filter_by(id=self.team_id).first().logo,
#                "points": self.points,
#                "goals_for": self.goals_for,
#                "goals_against": self.goals_against,
#                "goal_difference": self.goal_difference,
#                "form": self.form}
#         return res
