import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re

# Function Definitions
def generateUrls():
    baseUrl = "https://en.as.com/resultados/futbol/inglaterra/2017_2018/jornada/regular_a_"
    allGameWeeks = list()

    for i in range(1, 32):
        allGameWeeks.append(baseUrl + str(i))
    return allGameWeeks

def scrapeFixtureWeek(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Home Team Name
    homeTeam = scrapeTeamNames(soup, {"class": "equipo-local"})
    awayTeam = scrapeTeamNames(soup, {"class": "equipo-visitante"})
    scores = scrapeScore(soup)
    dates = scrapeDates(soup)

    allGames = pd.DataFrame()

    allGames = (
        allGames.assign(homeTeam = homeTeam)
            .assign(awayTeam = awayTeam)
            .assign(score = scores)
            .assign(date = dates)
            # .assign(awayTeamScore = awayScore)
    )
    return allGames


def scrapeTeamNames(soup, attrs = {}):
    teamRaw = soup.find_all("div", attrs = attrs)
    teamRaw = list(map(lambda x: x.find_all("span", attrs = {"class", "nombre-equipo"}), teamRaw))
    teamName = list(map(lambda x: str(x).replace('[<span class="nombre-equipo" itemprop="name">', ""), teamRaw))
    teamName = list(map(lambda x: str(x).replace("</span>]", ""), teamName))
    return teamName


def scrapeScore(soup):
    scoresRaw = soup.find_all("a", attrs = {"class" : "resultado"})
    scores = list(map(lambda x: x.string, scoresRaw))
    return scores

def scrapeDates(soup):
    datesRaw = soup.find_all("li", attrs = {"class" : "cont-fecha"})
    datesRaw = list(map(lambda x: x.find_all('span', attrs = {"class" : "fecha"}), datesRaw))
    datesRaw = list(map(lambda x: str(x).replace('[<span class="fecha">', ""), datesRaw))
    dates = list(map(lambda x: str(x).replace("</span>]", ""), datesRaw))
    return dates

# Main
def main():
    gameWeeks = generateUrls()
    totalSeason = pd.DataFrame()

    for week in gameWeeks:
        weekData = scrapeFixtureWeek(week)
        totalSeason = totalSeason.append(weekData)
        pass

    totalSeason = totalSeason.reset_index()
    return totalSeason

rawData = main()
rawData = (
    rawData.assign(score = rawData.score.str.replace("\s", ""))
)
rawData.to_csv("dataLake/rawZone/rawData.csv")

data = (
    rawData.drop("index", 1)
    .assign(homeScore = rawData.score.str.split("-").str.get(0))
    .assign(awayScore = rawData.score.str.split("-").str.get(1))
    .drop("score", 1)
    .query('homeScore != "Aplaz."')
    .assign(gameData = rawData.date.str.split(" ").str.get(0))
    .assign(gameTime = rawData.date.str.split(" ").str.get(1))
    .assign(gameData = data.gameData.str.replace("^[A-z]*-", ""))
    .drop("date", 1)
)
data.to_csv("dataLake/trustedZone/premierLeagueResults.csv")

# Testing Aggregations
goalsPerTeam = (
    data.assign(homeScore = pd.to_numeric(data.homeScore))
    .assign(awayScore = pd.to_numeric(data.awayScore))
    .groupby('homeTeam')
    .agg({"homeScore": sum, "awayScore" : sum})
)

data.to_csv("dataLake/trustedZone/goalsPerTeam.csv")
