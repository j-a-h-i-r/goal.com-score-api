import requests
import bs4
import pprint
import datetime

pp = pprint.PrettyPrinter()

def extractionCompetitionTitleFromCompetitionSoup(competitionSoup):
    competitionTitleTag = competitionSoup.find('a', class_='competition-title')
    competitionTitle = competitionTitleTag.text
    competitionTitle = competitionTitle.strip()
    return competitionTitle

def extractCompetitionUrlFromCompetitionSoup(competitionSoup):
    competitionUrlTag = competitionSoup.find('a', class_='competition-title')
    competitionUrl = competitionUrlTag['href']
    return competitionUrl

def extractMatchSoupsFromCompetitionSoup(competitionSoup):
    matchTagList = competitionSoup.find_all('div', class_='match-row')
    return matchTagList
    
def extractMatchInfo(matchSoup):
    matchInfo = dict()
    matchStateSoup = matchSoup.find('span', class_='match-row__state')
    matchState = matchStateSoup.text if matchStateSoup else None
    matchTimeSoup = matchSoup.find('span', class_='match-row__date')
    matchTime = matchTimeSoup.text
    matchInfo['state'] = matchState
    matchInfo['time'] = matchTime
    
    homeTeamSoup = matchSoup.find('td', class_='match-row__team-home')
    homeTeamTitle = homeTeamSoup.text.strip()
    homeTeamUrl = homeTeamSoup.find('a', class_='match-row__link')['href']
    
    awayTeamSoup = matchSoup.find('td', class_='match-row__team-away')
    awayTeamTitle = awayTeamSoup.text.strip()
    awayTeamUrl = awayTeamSoup.find('a', class_='match-row__link')['href']
    
    scoreSoup = matchSoup.find_all('b', class_='match-row__goals')
    if scoreSoup:
        homeScore = scoreSoup[0].text
        awayScore = scoreSoup[1].text
        matchInfo['score'] = {
            'home': homeScore,
            'away': awayScore
        }
    
    matchInfo['teams'] = dict()
    matchInfo['teams']['home'] = {
        'title': homeTeamTitle,
        'url': homeTeamUrl
    }
    matchInfo['teams']['away'] = {
        'title': awayTeamTitle,
        'url': awayTeamUrl
    }
    return matchInfo

def getCurrentTime():
    currentDateTime = datetime.datetime.now()
    formattedDateTime = currentDateTime.strftime('%Y-%m-%d %H:%M')
    return formattedDateTime

def getFixtureMatches(fixtureUrl):
    res = requests.get(fixtureUrl)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    
    fixtureInfo = dict()
    competitions = list()

    competitionSoupList = soup.find_all('div', class_='competition-matches')
    for competitionSoup in competitionSoupList:
        competitionTitle = extractionCompetitionTitleFromCompetitionSoup(competitionSoup)
        competitionUrl = extractCompetitionUrlFromCompetitionSoup(competitionSoup)
        matchSoupList = extractMatchSoupsFromCompetitionSoup(competitionSoup)
        
        matchInfoList = list()
        for matchSoup in matchSoupList:
            matchInfo = extractMatchInfo(matchSoup)
            matchInfoList.append(matchInfo)
        competitionInfo = dict()
        competitionInfo = {
            'title': competitionTitle,
            'url': competitionUrl,
            'matches': matchInfoList
        }
        competitions.append(competitionInfo)
        print(pp.pprint(competitionInfo))
    fixtureInfo = {
        'now': getCurrentTime(),
        'url': fixtureUrl,
        'competitions': competitions
    }
    return fixtureInfo

if __name__ == "__main__":
    ROOT_FIXTURE_URL = 'https://www.goal.com/en-in/fixtures/'
    todayDate = datetime.datetime.now().strftime('%Y-%m-%d')
    fixtureUrl = ROOT_FIXTURE_URL + todayDate
    liveMatches = getFixtureMatches(ROOT_FIXTURE_URL)
