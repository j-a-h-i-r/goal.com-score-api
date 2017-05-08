'''  To Dos   '''
# create a search function to search for specific team
# to search for specific time
# to seach specific competition
# Change time to BST

import bs4
import requests
from datetime import datetime, timedelta

dateToday = datetime.today()

'''
- goal.com uses date to display live score
- but timezone used is IST. so 0:00 to 0:30 in BD it's a new date.
- But in IST it's still previous date.
- So, check if current time is between 0:00 t0 0:30
- If it is then change date to previous date
'''
if dateToday.hour == 0 and dateToday.minute < 30:
    dateToday -= timedelta(1)

date = dateToday.strftime('%Y-%m-%d')

'''
- preferred league names
- dictionary containing name and id of league given by goal.com
'''
leagueName = ('Premier League', 'Primera División', 'Serie A', 'Bundesliga',
              'Ligue 1', 'UEFA Champions League')
leagueId = {'8': 'Premier League', '7': 'Primera División', '9': 'Bundesliga',
            '13': 'Serie A', '16': 'Ligue 1', '10': 'UEFA Champions League'}

'''
- Many Comp has same Name; There is two Premier League in the website
- I only want EPL, 1st One
- So if I encounter Premier League I need to set its flag as 1
'''
leagueFlag = {'Premier League': 0, 'Primera División': 0, 'Serie A': 0,
              'Bundesliga': 0, 'Ligue 1': 0, 'UEFA Champions League': 0}

'''
- url for live score
- url for match fixture
'''
liveUrl = 'http://goal.com/en-india/live-scores'
fixtureUrl = 'http://goal.com/en-india/fixtures/'


def getLiveMatches():
    '''
    - send scores of live matches
    This will send data for live matches only
    So the data for matches which have finished or have not yet started
        won't be sent
    Goal uses 3 formats to show match status
    1. HH:MM (20:30)    Match not yet started
    2. FT               Match finished
    3. MM'              Match is running at MM minute
    '''

    res = requests.get(liveUrl)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    matchDay = soup.find(
        lambda tag: tag.name == 'section' and
        tag.get('class') == ['matchday'] and tag.get('data-day') == date
        )
    allComp = matchDay.find_all('table', {'class': 'matches'})

    '''
    - matches will be stored in a list where all competition will be in their own list
    - Format:  [ [comp1, (status, Home1, Score, Away1), .... ],
                 [comp2, (status, Home2, Score, Away2), .... ] ]
    '''
    matchList = []

    for allMatch in allComp:
        compList = []

        matches = allMatch.find_all('tbody', {'class': 'match clickable '})
        comp = allMatch.find('span', {'class': 'comp-title'}).string

        if comp not in leagueName:
            # This is out of my preferred league
            continue
        if leagueFlag[comp] == 1:
            # Already got this leagues data. This is duplicate
            continue
        else:
            leagueFlag[comp] = 1

        compList.append(comp)

        for matchData in matches:
            match = matchData.find('tr')

            status = match.find('span').string.split('\n')[1]

            if ':' in status or status == "FT":
                continue

            home = match.find('td', {'class': 'team'})
            away = home.find_next_sibling('td', {'class': 'team'})

            homeTeam = home.find('span').string
            awayTeam = away.find('span').string

            vs = match.find('td', {'class': 'vs'})
            result = vs.find('div').string.split('\n')[1]

            compList.append((status, homeTeam, result, awayTeam))
        matchList.append(compList)

    return matchList


def getFixture(date):
    '''
    - Send Fixtures of matches played/to be played in "date"

    - Fixture will be stored in a list where all competition will be in their own list
    - Format:  [ [comp1, (status, Home1, Away1), .... ],
                 [comp2, (status, Home2, Away2), .... ] ]
    '''
    fixtureList = []

    url = fixtureUrl + date

    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    allComp = soup.find_all('table', {'class': 'match-table '})

    for comp in allComp:

        id = comp.get('data-competition-id')

        if id not in leagueId:
            continue

        compList = []
        compList.append(leagueId[id])

        matches = comp.find_all('tr', {'class': 'clickable '})

        for match in matches:

            status = match.find('td', {'class': 'status'}).string.lstrip('\n')

            home = match.find('td', {'class': 'team'})
            away = home.find_next_sibling('td', {'class': 'team'})

            homeTeam = home.find('span').string
            awayTeam = away.find('span').string

            compList.append((status, homeTeam, awayTeam))

        fixtureList.append(compList)

    return fixtureList


def printMatchInfo(matchInfo):
    for matches in matchInfo:
        print(matches[0])
        print('-' * len(matches[0]))

        if(len(matches) == 1):
            print("No matches!")

        for match in matches[1:]:
            for info in match:
                print(info, end=" ")
            print()
        print()


if __name__ == "__main__":
    matchInfo = getLiveMatches()
    printMatchInfo(matchInfo)

    print("Fixture")
    fixtureInfo = getFixture('2017-05-08')
    printMatchInfo(fixtureInfo)
