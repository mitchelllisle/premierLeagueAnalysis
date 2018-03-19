def generateUrls():
    baseUrl = "https://en.as.com/resultados/futbol/inglaterra/2017_2018/jornada/regular_a_"
    allGameWeeks = list()

    for i in range(1, 39):
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
            .assign(dates = dates)
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
    datesRaw = soup.find_all("span", attrs = {"class" : "fecha"})
    dates = list(map(lambda x: x.string, datesRaw))
    return dates
