import requests
import bs4
import pprint
import datetime
from urllib.parse import urljoin
from typing_extensions import Literal

pp = pprint.PrettyPrinter()

BASE_URL = 'https://www.goal.com'
ALL_COMPETITION_URL = 'https://www.goal.com/en-in/all-competitions'
POPULAR_COMPETITION_URL = 'https://www.goal.com/en-in/competitions'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
}

def filterCompetitionTag(tag):
    return tag.has_attr('href') and tag.get('href') == '/en-in/all-competitions'


def getPopularCompetitions(goalHomeUrl=POPULAR_COMPETITION_URL, baseUrl=BASE_URL):
    res = requests.get(goalHomeUrl, headers=HEADERS)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    competitionSoupList = soup.find_all('a', class_='widget-competitions-popular__competition')

    competitions = list()
    for competitionSoup in competitionSoupList:
        competitionTitle = competitionSoup.text.strip()
        competitionUrlFragement = competitionSoup.get('href')
        competitionUrl = urljoin(baseUrl, competitionUrlFragement)
        competitions.append({
            'title': competitionTitle,
            'url': competitionUrl
        })
    competitionInfo = dict()
    competitionInfo = {
        'meta': {
            'description': 'List of the popular competitions'
        },
        'competitions': competitions
    }
    return competitionInfo

def getAllCompetitions(allCompetitionUrl = ALL_COMPETITION_URL, baseUrl = BASE_URL):
    res = requests.get(allCompetitionUrl, headers=HEADERS)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    
    competitionWidgetSoup = soup.find('div', class_='widget-competitions-list-of-all')
    groupSoupList = competitionWidgetSoup.find_all('div', class_='widget-competitions-list-of-all__group')

    groups = list()
    for groupSoup in groupSoupList:
        groupTitle = groupSoup.text.strip()
        competitionSoupList = groupSoup.findNextSibling().find_all('li')
        competitions = list()
        for competitionSoup in competitionSoupList:
            competitionTitle = competitionSoup.find(class_='widget-competitions-list-of-all__label').text
            competitionUrlRelativeUrl = competitionSoup.find(class_='widget-competitions-list-of-all__competition').get('href')
            competitionUrl = urljoin(baseUrl, competitionUrlRelativeUrl)
            competitions.append({
                'title': competitionTitle,
                'url': competitionUrl
            })
        groups.append({
            'group': groupTitle,
            'competitions': competitions
        })
    
    competitionInfo = dict()
    competitionInfo = {
        'meta': {
            'description': 'List of all competitions grouped by region/country'
        },
        'groups': groups
    }
    return competitionInfo


def getCompetitions(competitionType: Literal['popular', 'all']):
    competition = list()
    if competitionType == 'popular':
        competition = getPopularCompetitions()
    elif competitionType == 'all':
        competition = getAllCompetitions()
    return competition


if __name__ == '__main__':
    pass