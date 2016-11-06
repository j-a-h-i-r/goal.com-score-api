'''  To Dos   '''

# create a search function to search for specific team
# to search for specific time
# to seach specific competition
# Change time to Bangladesh Time
# Create GUI


import bs4, requests
import lxml
from datetime import datetime, timedelta
from tkinter import *

dateToday = datetime.today()
###
## goal.com uses date to display live score
## but timezone used is IST. so 0:00 to 0:30 in Bangladesh it's a new date.
## But in IST it's still previous date.
## So, check if current time is between 0:00 t0 0:30
## If it is then   change date   to    previous date
###

if dateToday.hour == 0 and dateToday.minute <30:
    dateToday -= timedelta(1)    # get date of previous day

date = dateToday.strftime('%Y-%m-%d')

# league name to display information
# goal.com used an ID to identify leagues;
# so the dictionary will dereference the ID to league name
leagueName = ('Premier League', 'Primera División', 'Serie A','Bundesliga','Ligue 1','UEFA Champions League')
leagueId = {'8':'Premier League', '7':'Primera División', '9':'Bundesliga', '13':'Serie A', '16':'Ligue 1', '10':'UEFA Champions League'}

# Many Comp has same Name; There is two Premier League.
# I only want EPL, 1st One
# So if I encounter Premier League I need to set its flag as 1
# This way I can get EPL, which is my target
leagueFlag = {'Premier League':0, 'Primera División':0,'Serie A':0, 'Bundesliga':0,'Ligue 1':0, 'UEFA Champions League':0}

# URL of the pages to scan
liveUrl = 'http://goal.com/en-india/live-scores'
fixtureUrl = 'http://goal.com/en-india/fixtures/'


def getMatches():
    '''This function parses the score page and gets current score
    and returns a list of team name and score '''
    
    res = requests.get(liveUrl)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    matchDay=soup.find(lambda tag: tag.name=='section' and tag.get('class')==['matchday'] and tag.get('data-day')==date)
    allComp = matchDay.find_all('table', {'class':'matches'})

    matchList = []
    i=0
    
    for allMatch in allComp:
        matches = allMatch.find_all('tbody', {'class':'match clickable '})
        comp = allMatch.find('span', {'class':'comp-title'}).string

        if comp not in leagueName:
            continue
        if leagueFlag[comp] == 1:
            continue
        else:
            leagueFlag[comp] = 1
        
        matchList.append([comp])
        
        for table in matches:
            row = table.find('tr')

            status = row.find('span').string.split('\n')[1]

            home = row.find('td', {'class':'team'})
            away = home.find_next_sibling('td', {'class':'team'})

            homeTeam = home.find('span').string
            awayTeam = away.find('span').string

            vs = row.find('td', {'class':'vs'})
            result = vs.find('div').string.split('\n')[1]

            matchList[i].append((status,homeTeam,result,awayTeam))
        i += 1
    return matchList

def getFixture(date):
    '''This function will scan the fixture page to get fixtures of 
    matches to be played in the selected leagues '''

    i = 0

    l = []

    url = fixtureUrl + date

    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    allComp = soup.find_all('table', {'class':'match-table '})

    for comp in allComp:

        id = comp.get('data-competition-id')

        if id not in leagueId:
            continue

        l.append([leagueId[id]])

        matches = comp.find_all('tr', {'class':'clickable '})

        for match in matches:

            status = match.find('td', {'class':'status'}).string.lstrip('\n')

            home = match.find('td', {'class':'team'})
            away = home.find_next_sibling('td', {'class':'team'})

            homeTeam = home.find('span').string
            awayTeam = away.find('span').string

            #print(status+'\t'+ homeTeam + '\t' + awayTeam )

            l[i].append((status, homeTeam, awayTeam))

        i += 1

    return l


def printMatch():
    '''This function prints score of the matches'''
    
    for matches in matchInfo:
        print(matches[0])
        print('-'*len(matches[0]))
        for match in matches[1:]:
            print(match[0], match[1],match[2],match[3])
        print()

matchInfo = getMatches()

printMatch()

f = getFixture('2015-09-22')

#print(f)
# getting fixtures is still in process
