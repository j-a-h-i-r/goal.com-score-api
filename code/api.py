from flask import Flask
from flask_restful import Resource, Api

import goal

app = Flask(__name__)
api = Api(app)

class LiveMatches(Resource):
    def get(self):
        liveMatchInfo = goal.getLiveMatches()
        return liveMatchInfo

api.add_resource(LiveMatches, '/live')

if __name__ == '__main__':
    app.run(debug=True)