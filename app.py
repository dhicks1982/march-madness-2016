import readInTeams
import computePercentages
import outputCsv
from teams import Team

def main():
    teams = readInTeams.getTeams()
    computePercentages.computeRanking(teams)
    outputCsv.outputCsv(teams)

main()