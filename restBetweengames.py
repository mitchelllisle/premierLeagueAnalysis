import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

url = "https://www.fctables.com/england/premier-league/schedule/"

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# Get status of game, one of ['Finished', 'Postponded', 'Not Started']
statusOfGamesRaw = soup.find_all("div", attrs = {"class": "status_name"})
statusOfGames = list(map(lambda x: x.string, statusOfGamesRaw))

# Get home team
homeTeamRaw = soup.find_all("span", attrs = {"class": "home"})
homeTeam = list(map(lambda x: x.string, homeTeamRaw))
# Get Home Score
homeScoreRaw = soup.find_all("span", attrs = {"class": "score text-center"})
homeScore = list(map(lambda x: x.find_all("span")[0].string, homeScoreRaw))

# Get away team
awayTeamRaw = soup.find_all("span", attrs = {"class": "home"})
awayTeam = list(map(lambda x: x.string, awayTeamRaw))
# Get away team score
awayScoreRaw = soup.find_all("span", attrs = {"class": "score text-center"})
awayScore = list(map(lambda x: x.find_all("span")[2].string, awayScoreRaw))

allGames = pd.DataFrame()

allGames = (
    allGames.assign(status = statusOfGames)
        .assign(homeTeam = homeTeam)
        .assign(awayTeam = awayTeam)
        .assign(homeTeamScore = homeScore)
        .assign(awayTeamScore = awayScore)
)

totalGoalsByTeam = (
    allGames.groupby(homeTeam)['homeTeamScore']
    .agg(['sum'])
)
