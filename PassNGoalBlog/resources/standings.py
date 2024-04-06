from flask_restful import Resource
from PassNGoalBlog.models import League, Season, Team, Standing, db

class LeagueResource(Resource):
    pass

class SeasonResource(Resource):
    pass

class TeamResource(Resource):
    pass

class StandingResource(Resource):
    def get(self, year, league_id):
        season = Season.query.filter_by(league_id=league_id, year=year).first()
        if season:
            standings = Standing.query.filter_by(season_id=season.id).all()
            print(standings)
            return [standing.json() for standing in standings], 200
        else:
            return {'season': 'not found'}, 404
    