import live
import fixture
import competitions

import util

LIVE_URL = 'http://goal.com/en-in/live-scores'
FIXTURE_URL = 'https://www.goal.com/en-in/fixtures/'

def getLiveMatches():
    liveMatchInfo = live.getLiveMatches(LIVE_URL)
    return liveMatchInfo


def getFixtureMatches(fixtureDate = ''):
    if not fixtureDate:
        fixtureDate = util.getTodayDateString()
    fixtureUrl = FIXTURE_URL + fixtureDate
    fixtureMatches = fixture.getFixtureMatches(fixtureUrl)
    return fixtureMatches

def getCompetitions(competitionType):
    allCompetitions = competitions.getCompetitions(competitionType)
    return allCompetitions
