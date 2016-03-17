import teams
import urllib2
import re
from lxml import html
import requests

# Weight for players with the most minutes.  Nobody after the 7th man matters
P1=1 
P2=.8 
P3=.8
P4=.5
P5=.4
P6=.3
P7=.2

ARBITRARY_CONFERENCE_MULTIPLIER = 1.5

def getSearchableTeamName(team):
    name = team.sportsRefName if team.sportsRefName else team.name
    return name.replace(' St',' State').replace(' ','-').lower()

def computeRanking(bracket):
    for team in bracket:
        computeRankingForTeam(team)

def toValue(text):
    try:
        return float(text)
    except ValueError:
        # not a float, don't care
        return -1

def computeRankingForTeam(team):
    searchableTeamName = getSearchableTeamName(team)
    print searchableTeamName

    # Download the team page and extract the player per-possession conference statistics
    page = requests.get('http://www.sports-reference.com/cbb/schools/'+searchableTeamName+'/2016.html')
    tree = html.fromstring(page.content)
    players = []
    for row in tree.xpath('//div[@id="all_per_poss_conf"]/div/table/tbody/tr'):
        players.append(map(toValue,row.xpath('td/text()')))

    # Download the conference page and locate the item with the conference strength
    conferenceContext = tree.xpath('//p/a/@href')[1]
    page = requests.get('http://www.sports-reference.com'+conferenceContext)
    tree = html.fromstring(page.content)
    confSrsText = tree.xpath('//div/p/text()')[11]

    # Extract first floating point value from the text, which is the strength of the conference
    confSrs = float(re.findall(r'[-+]?\d*\.*\d+',confSrsText)[0])

    # Sort players by minutes played
    players.sort(key=lambda x: x[2], reverse=True)

    # Compute weighted average of players offensive-defensive rating
    team.score = (P1*playerScore(players[0]) +
        P2*playerScore(players[1]) +
        P3*playerScore(players[2]) +
        P4*playerScore(players[3]) +
        P5*playerScore(players[4]) +
        P6*playerScore(players[5]) +
        P7*playerScore(players[6])) / (P1+P2+P3+P4+P5+P6+P7)
    print str(team.score) +" "+ str(confSrs)
    team.score = team.score+confSrs*ARBITRARY_CONFERENCE_MULTIPLIER
    print team.score


def playerScore(player):
    #offensive rating - defensive rating
    return (player[-2]-player[-1])
