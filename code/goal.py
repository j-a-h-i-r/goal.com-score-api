import live

LIVE_URL = 'http://goal.com/en-in/live-scores'

def getLiveMatches():
    liveMatchInfo = live.getLiveMatches(LIVE_URL)
    return liveMatchInfo