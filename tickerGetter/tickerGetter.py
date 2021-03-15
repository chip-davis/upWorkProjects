import requests
import json
import yahoo_fin.stock_info as si
import re
from bs4 import BeautifulSoup
class getTickers():

    @staticmethod
    def getSoup(url):
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        return soup

    @staticmethod
    def getTicker(companyName):
        url        = (f"http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={companyName}&region=1&lang=en")
        r          = requests.get(url)
        tickerDict = json.loads(r.text)
        ticker     = ''
        tickerDict = (tickerDict.get("ResultSet").get("Result"))
        
        try:
            ticker = (tickerDict[0].get('symbol'))
        except:
            pass
        if ticker: return ticker

    @staticmethod
    def getWikiTicker(companynameUrl):
        tickers = []
        soup = getTickers.getSoup(f"https://en.wikipedia.org/{companynameUrl}")
        table = soup.find('table', class_="infobox vcard")
        try:
            for tr in table.find_all('tr'):
                tds = tr.find_all("td")
                for td in tds:
                    for ul in td.find_all("ul"):
                        for li in ul.find_all('li'):
                            for ahref in li.find_all('a', {'href' : "external text"}):
                                tickers.append(ahref.text)
                                print(tickers)
        except:
            print(f"oops{companynameUrl}")
        return tickers

    @staticmethod
    def getspGlobal100():
    
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/S%26P_Global_100")
        companies = []
        tickers   = []

        #all of the companies names where in a unordered list element on WIKI
        for ul in soup.find_all("ul"):
            companies.append(ul)
        
        #gets rid of extra tags we dont need
        companies = companies[1]
        
        for company in companies:
            company=str(company)
            result = re.search('"/wiki/\w*"', company)
            try:
                ticker = getTickers.getWikiTicker(result.group().replace('"', ""))
                tickers.append(ticker)
            except:
                pass
            
        print(tickers)
        print(len(tickers))

    @staticmethod
    def getBBCGlobal30():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/BBC_Global_30")
        tables = soup.find_all('table')
        tickers = []
        for table in tables:
            ths = table.find_all("th")
            headings = [th.text.strip() for th in ths]
            
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if not tds:
                continue
            ticker = [str(td).strip() for td in tds[2]]
            ticker = ticker[2]
            ticker = ticker[ticker.find(">"):]
            ticker = ticker[1:ticker.find("<")]
            tickers.append(ticker)

        return(tickers)

    @staticmethod
    def getDJG50():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/Dow_Jones_Global_Titans_50")
        tables = soup.find_all("table")
        ourTable = soup.find_all("table", class_='wikitable sortable')
        tickers = []
        for row in ourTable[0].findAll('tr'):
            tds = row.find_all('td')
            if not tds:
                continue
            ticker = [str(td).strip() for td in tds]
            ticker = (ticker[2])
            ticker = (ticker[ticker.find('w">'):])
            ticker = (ticker[3:ticker.find('<')])
            tickers.append(ticker)
        return tickers

    @staticmethod
    def getFTSE100():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/FTSE_100_Index")

        tickers = []
        tables = soup.find_all("table")
        
        ourTable = soup.find_all("table", id='constituents')
        
        for row in ourTable[0].findAll("tr"):
            tds = row.find_all("td")
            ticker = [str(td).strip() for td in tds]
            if ticker:
                ticker = ticker[1]
            ticker = str(ticker)
            ticker = ticker.replace("<td>", "").replace("</td>", "")
            if ticker: tickers.append(ticker)
        return(tickers)

    @staticmethod
    def getNikkei225():
        soup =  getTickers.getSoup("https://en.wikipedia.org/wiki/Nikkei_225")
        tickers = []

        uls = soup.find_all("ul")
        lis = []
        for ul in uls:
            for li in ul.findAll("li"):
                if li.find('ul'):
                    break
                lis.append(li)
        for li in lis:
            li = (li.text.encode("utf-8"))
            li = (li.decode('utf-8'))
            if "TYO" in li:
                li = (li[li.find(":"):])
                li = li[1:-1].strip()
                tickers.append(li)
        return(tickers)
    
    @staticmethod
    def getOmxNordic40():
        soup    = getTickers.getSoup("https://en.wikipedia.org/wiki/OMX_Nordic_40")
        tickers = []
        tables = soup.find_all("table")
        ourTable = soup.find_all("table", class_='wikitable sortable')

        for row in ourTable[0].findAll('tr'):
            tds = row.find_all('td')
            if not tds:
                continue
            tds = tds[3]
            tds = str(tds)
            tds = tds[tds.find('w"'):]
            tds = tds.replace('w">', "").replace("</a>", "").replace("</td>", "")
            if tds:
                tickers.append(tds.strip())
        return(tickers)
    
    @staticmethod
    def getDAX30():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/DAX")
        tickers = []
        tables = soup.find_all("table")
        
        ourTable = soup.find_all("table", id='constituents')
        
        for row in ourTable[0].findAll("tr"):
            tds = row.find_all("td")
            ticker = [str(td).strip() for td in tds]
            if ticker:
                ticker = ticker[3]
            ticker = str(ticker)
            ticker = ticker[ticker.find('w"'):ticker.find("</a>")].replace('w"', "").replace(">", "")
            if ticker: tickers.append((ticker))
        return(tickers)
    
    @staticmethod
    def getEuroNext100():
        pages = 3
        count = 1
        bannedWords = ["€", "🇫🇷", "🇳🇱", "🇵🇹", "🇧🇪", "🇱🇺", "🇨🇭", "Fr.15.4bn"]
        finalTickers = []
        while count <= pages:
            soup = getTickers.getSoup(f"https://www.dividendmax.com/market-index-constituents/euronext-100?page={count}")
            table = soup.find("table", class_="mdc-data-table__table")
        

            for row in table.findAll('tr'):
                tds = row.find_all('td')
                tickers = [str(td).strip() for td in tds]
                for ticker in tickers:
                    ticker= str(ticker)
                    ticker = ticker[ticker.find('">'):]
                    ticker = ticker[2:ticker.find('<')]
                    
                    if "€" not in ticker and "🇫🇷" not in ticker and "🇳🇱" not in ticker and "🇵🇹" not in ticker and "🇧🇪" not in ticker and '🇱🇺' not in ticker and "Fr.15.4bn" not in ticker and  '🇨🇭' not in ticker and ticker:
                        ticker = ticker.strip()
                        finalTickers.append(ticker)
            count +=1
        return finalTickers

    @staticmethod
    def getSP500():
        tickers = (si.tickers_sp500())
        return tickers

    @staticmethod
    def getDOWJonesIndustrial():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#Components")
        tickers = []
        table = soup.find_all("table", id="constituents")
        for row in table[0].findAll('tr'):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            try:
                tickers.append((ticker[0].split(">")[6]).replace("</a", ""))
            except:
                pass
        return tickers
    
    @staticmethod
    def getDOWJonesTransportation():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/Dow_Jones_Transportation_Average")
        tickers = []
        table = soup.find_all("table", class_="wikitable sortable")
        for row in table[0].findAll("tr"):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            ticker = ticker[0].split(",")
            try:
                ticker = ((ticker[0].replace("<td>", "").replace("</td>", "").replace("[", "")).strip())
                if ticker != ']': tickers.append(ticker)
            except:
                pass
        return tickers

    @staticmethod
    def getDOWJonesUtility():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/Dow_Jones_Utility_Average")
        tickers = []
        table = soup.find_all("table", class_='wikitable sortable')
        for row in table[0].findAll('tr'):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            ticker = ticker[0].split(",")
            try:
                ticker = ticker[0].replace("<td>", "").replace("</td>", "").replace("[", "").strip()
                if ticker != ']': tickers.append(ticker)
            except:
                pass
        return tickers

    @staticmethod
    def getSP400():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/List_of_S%26P_400_companies")
        tickers =[]
        table = soup.find_all("table", id="constituents")
        for row in table[0].find_all("tr"):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            try:
                ticker = ((ticker[0].split(">"))[6]).replace("</a", "")
                tickers.append(ticker)
            except:
                pass
        return(tickers)
    
    @staticmethod
    def getNasdaq100():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/Nasdaq-100#Components")
        tickers =[]
        table = soup.find_all("table", id="constituents")
        for row in table[0].find_all("tr"):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            try:
                ticker = ((ticker[0].split(">"))[5]).replace("</td", "")
                tickers.append(ticker)
            except:
                pass
        return tickers
    
    @staticmethod
    def getSP100():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/S%26P_100#Components")
        tickers = []
        table = soup.find_all("table", id="constituents")
        for row in table[0].find_all('tr'):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            try:
                ticker = (ticker[0].split(">")[1]).replace("</td", "").strip()
                tickers.append(ticker)
            except:
                pass
        return tickers

    @staticmethod
    def getRussel1000():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/Russell_1000_Index")
        tickers = []
        table = soup.find_all("table", class_="wikitable sortable")
        for row in table[0].find_all('tr'):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            try:
                ticker = (ticker[0].split(">")[5]).replace("</td", "").strip()
                tickers.append(ticker)
            except:
                pass
        return tickers

    @staticmethod
    def getRussel2000():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/Russell_2000_Index")
        tickers = []
        table = soup.find_all("table", class_="wikitable")
        for row in table[0].find_all('tr'):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            try:
                tickers.append(ticker[0].split("<td>")[2].replace("</td>]", "").strip())
            except:
                pass
        print(tickers)

    @staticmethod
    def getPHLXSemiconductor():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/PHLX_Semiconductor_Sector")
        tickers = []
        uls = soup.find_all("ul")
        tickers = []
        
        for ul in uls[0]:
            try:
                li = str(ul)
                length = len(li)
                li = (li[length-10:].replace("</li>", "").replace(",", "").strip())
                if li: tickers.append(li)
            except:
                pass
        return tickers
        
    @staticmethod
    def getPHLXGoldSilver():
        manualReplacements = {"AuRico Gold Inc" : "AUQ", "Coeur Mining, Inc" : "Couer Mining", "Compañia de Mínas Buenaventura" :"BVN",
                              "Freeport-McMoRan Copper ; Gold" : "FCX",  "IAMGOLD Corp" : "IAG", "McEwen Mining Inc" : "MUX",
                              "Wheaton Precious Metals Corporation" : "WPM", "Pan American Silver Corp" : "PAAS", "Silver Standard Resources" : "SSRM",
                              "Harmony Gold Mining Company Limited" : "HMY", "Tanzanian Royalty Exploration Corp" : "TRX"}
            
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/Philadelphia_Gold_and_Silver_Index")
        tickers = []
        table = soup.find_all("table", class_="wikitable sortable")
        for row in table[0].find_all('tr'):
            tds = [row.find_all('td')]
            company = [str(td).strip() for td in tds]
           
            try:
                company = (company[0].split(">")[2]).replace("</td", "").replace("</a", "").replace(".", "").replace("&amp", "").replace("Inc", "").strip()
                if company: 
                    if manualReplacements.get(company):
                        company = (manualReplacements.get(company))
                    tickers.append(getTickers.getTicker(company))
            except:
                pass
        
        return tickers

    @staticmethod
    def getNYSEAMEX():
        manualReplacements = {"American Shared Hospital Srvcs":"AMS", "Avino Silver Gold":"ASM","Blonder Tongue Labs":"BDR","Can Fite Biopharma ADR":"CANF",
                              "Cornerstone Strategic Return":"CRF","Delaware Minnesota II":"VMM", "Delaware Florida":"VFL","Dreyfus Municipalome":"DMF",
                              "ETV California MBF":"EVM","ETV California MIT":"CEV", "ETV Limited Duration":"EVV", "ETV MBF":"EIM","ETV New York MBF":"EMC",
                              "ETV New York MIT":"EVY", "Ellsworth Convertible Growth":"ECF","Enservco Co":"ENSV", "Flanigans Enterprises ":"BDL",
                              "Grupo Simec ADR":"SIM","HMG Courtland Properties":"HMG", "ome Opponvesco Advantage II":"VKI","Neuberger Brtunity Realty":"NRREX",
                              "InfuSystems" : "INFU", "Invesco Advantage II" : "VKI", "Neuberger Berman Hi-Yield":"NHS","Sanchez Midstream":"SNMP",
                              "Western Copper Gold":"WRN","WF ome Opportunities":"EAD","WF Multi Sector ome":"ERC","ome Opportunity Realty":"IOR"}
                              
        url = "http://www.investing.com/indices/nyse-market-composite-components"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
        table = soup.find_all("table", id="cr1")
        companies = []
        tickers   = []
        bad       = []
        for row in table[0].findAll('tr'):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            try:
                ticker = str(ticker)
                result = re.search(r'">\w*\s*\w*.?\w*\W*\w*</a>', ticker)
                companies.append((result.group().replace('">', "").replace("</a>", "").replace("Corp", "").replace("Inc", "")))
            except:
                pass
        for company in companies:
            if manualReplacements.get(company):
                company = manualReplacements.get(company)
            tickers.append(getTickers.getTicker(company))
        return (tickers)
        
    @staticmethod
    def getNYSEArcaMajor():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/NYSE_Arca_Major_Market_Index")
        tickers = []
        table = soup.find_all("table", class_="wikitable sortable")
        for row in table[0].find_all('tr'):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            try:
                tickers.append(ticker[0].split("<td>")[1].replace("</td>,","").strip())
            except:
                pass
        return (tickers)

    @staticmethod
    def getNYSEArcaOil():
        soup = getTickers.getSoup("https://en.wikipedia.org/wiki/Amex_Oil_Index")
        tickers = []
        table = soup.find_all("table", class_="wikitable")
        for row in table[0].find_all('tr'):
            tds = [row.find_all('td')]
            ticker = [str(td).strip() for td in tds]
            try:
                tickers.append(ticker[0].split("<td>")[2].replace("</td>]", "").strip())
            except:
                pass
        return(tickers)


getTickers.getspGlobal100()
