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


fixtureParser = reqparse.RequestParser()
fixtureParser.add_argument('date')

class FixtureMatches(Resource):
    def get(self):
        args = fixtureParser.parse_args()
        date = args['date']
        fixtureMatchInfo = goal.getFixtureMatches(date)
        return fixtureMatchInfo

api.add_resource(LiveMatches, '/live')
api.add_resource(FixtureMatches, '/fixture')

if __name__ == '__main__':
    app.run(debug=True)