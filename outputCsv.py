import teams
import csv
from teams import Team

def outputCsv(bracket):
    with open('bracket.csv','wb') as csvfile:
        bracketWriter = csv.writer(csvfile, delimiter=',')
        printRound(bracket, bracketWriter)


def printRound(bracket, writer):
    if len(bracket) > 1:
        nextRound = []
        regionSize = len(bracket)/4
        for i in range(len(bracket)/2):
            winningTeam = winner(bracket[i*2],bracket[i*2+1])
            nextRound.append(winningTeam)
        writer.writerow(map(lambda team: team.name, nextRound))
        printRound(nextRound, writer)

def winner(team1,team2):
    return team1 if team1.score > team2.score else team2
