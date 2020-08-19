from flask import Flask
from flask_restful import Resource, Api, reqparse

import goal
import util

app = Flask(__name__)
api = Api(app)

class LiveMatches(Resource):
    def get(self):
        liveMatchInfo = goal.getLiveMatches()
        return liveMatchInfo


class FixtureMatches(Resource):
    fixtureParser = reqparse.RequestParser()
    fixtureParser.add_argument('date')

    def get(self):
        date = self.getQueryDate()
        fixtureMatchInfo = goal.getFixtureMatches(date)
        return fixtureMatchInfo

    def getQueryDate(self):
        args = FixtureMatches.fixtureParser.parse_args()
        date = args['date']
        return date

class Competitions(Resource):
    competitionParser = reqparse.RequestParser()
    competitionParser.add_argument('competition_type', required=True, default='all',
                    help='Pass either `all` or `popular` as competition type'
    )

    def get(self):
        competitionType = self.getCompetitionType()
        competitions = goal.getCompetitions(competitionType)
        return competitions
    
    def getCompetitionType(self):
        args = Competitions.competitionParser.parse_args()
        competitionType = args['competition_type']
        return competitionType


api.add_resource(LiveMatches, '/live')
api.add_resource(FixtureMatches, '/fixture')
api.add_resource(Competitions, '/competition')

if __name__ == '__main__':
    app.run(debug=True)