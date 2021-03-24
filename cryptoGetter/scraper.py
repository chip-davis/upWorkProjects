import requests
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import xlsxwriter
import openpyxl
from webbot import Browser
import time

def getSoup(url):
    print(f"Scraping {url}")
    headers =  {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    return soup

def boostVC():
    boostVCHoldings = {}
    cryptoCounter   = {}

    soup = getSoup("https://www.boost.vc/portfolio")

    mainDiv = soup.find('div', {"id":"block-yui_3_17_2_1_1534974512407_13644"})
    div2 = soup.find('div', {"id":"block-yui_3_17_2_1_1539723136853_15889"})
    div3 = soup.find('div', {"id":"block-yui_3_17_2_1_1539817861048_215623"})
    
    for test in mainDiv:
        for div in test.findAll('div', attrs={'class':"summary-title"}):
            cryptoCounter[(div.text.strip())] = 1
    for test in div2:
        for div in test.findAll('div', attrs={'class':"summary-title"}):
            cryptoCounter[(div.text.strip())] = 1
    for test in div3:
        for div in test.findAll('div', attrs={'class':"summary-title"}):
            cryptoCounter[(div.text.strip())] = 1
    
    boostVCHoldings['Boost VC'] = list(cryptoCounter.keys())
    return boostVCHoldings, cryptoCounter
    
def outlierVentures(cryptoCounter):
    finalHoldings = []
    filters  = []
    outlierVenturesHoldings = {}
    soup = getSoup("https://outlierventures.io/portfolio/", )
    lrgfilter = soup.find_all('p', class_="lrg filter")
    holdings  = soup.find_all('p', class_="lrg company")
    for test in lrgfilter:
        try:
            lrg = test.text.strip()
            filters.append(lrg.strip())
        except:
            pass
    for test in holdings:
        try:
            holding = (test.text.strip())
            finalHoldings.append(holding.strip())
        except:
            pass
    zipped = zip(finalHoldings, filters)
    finalHoldings = []
    for item in list(zipped):
        if item[1] == "Convergence Stack":
            finalHoldings.append(item[0])
            if cryptoCounter.get(item[0]):
                cryptoCounter[item[0]] = cryptoCounter.get(item[0]) + 1
            else:
                cryptoCounter[item[0]] = 1
    outlierVenturesHoldings['Outlier Ventures'] = finalHoldings
    return(outlierVenturesHoldings, cryptoCounter)
    
def dcg(cryptoCounter):
    finalHoldings = []
    dcgHoldings  = {} 
    soup = getSoup("https://dcg.co/portfolio/")
    mainDiv = soup.find_all('div', class_='company-info')
    for company in mainDiv:
        name = company.find_all("div", class_="name")
        for crypto in name:
            crypto = (crypto.text.strip())
            result = re.sub('Acquired', '', crypto)
            result = re.sub('ACQUIRED', '', result)
            finalHoldings.append(result.replace("()", ""))

    finalHoldings = set(finalHoldings)
    finalHoldings = list(finalHoldings)

    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)

    dcgHoldings['DCG Holdings'] = finalHoldings
    
    return dcgHoldings, cryptoCounter

def addToCryptoCounter(finalHoldings, cryptoCounter):
    for holding in finalHoldings:
        if cryptoCounter.get(holding):
            cryptoCounter[holding] += 1
        else:
            cryptoCounter[holding] = 1
    return cryptoCounter

def pantera(cryptoCounter):
    finalHoldings = []
    panteraHoldings = {}
    soup = getSoup("https://www.panteracapital.com/portfolio")
    divs = soup.find_all("div", class_="image-slide-title")
    for holding in divs:
        holding = holding.text
        if holding == "0x Protocol":
            holding = "0x"
        finalHoldings.append(holding)

    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    panteraHoldings['Pantera'] = finalHoldings
    
    return panteraHoldings, cryptoCounter

def arringtonxr(cryptoCounter):
    finalHoldings = []
    arringtonxrHoldings = {}

    soup = getSoup("http://arringtonxrpcapital.com/companies/")
    strongs = soup.find_all("strong")
    for strong in strongs:
        holding = strong.text.strip()
        finalHoldings.append(holding)

    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)    
    arringtonxrHoldings['ArringtonXR'] = finalHoldings
    
    return arringtonxrHoldings, cryptoCounter

def coinbase(cryptoCounter):
    finalHoldings = []
    coinbaseHoldings = {}
    soup = getSoup("https://ventures.coinbase.com/")
    holdings = soup.find_all('h4', class_="Typography__Heading4-sc-99jpeg-3")
    for holding in holdings:
        holding = holding.text.strip()
        finalHoldings.append(holding)
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    coinbaseHoldings['Coinbase'] = finalHoldings
    
    return coinbaseHoldings, cryptoCounter

def fenBushCapital(cryptoCounter):
    finalHoldings = []
    fenbushcapitalHoldings = {}
    soup = getSoup("https://www.fenbushicapital.vc/index_en.html")
    forbidden = ['Dr. Feng Xiao General Partner', 'Bo ShenGeneral Partner', 'Vitalik ButerinAdvisor','Remington OngPartner']
    holdings = soup.find_all('h4')
    for holding in holdings:
        holding = holding.text
        if holding not in forbidden:
            if holding == "51signing.com":
                holding = "51signing"
            finalHoldings.append(holding)
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    fenbushcapitalHoldings['Fenbushi'] = finalHoldings
    
    return fenbushcapitalHoldings, cryptoCounter

def hashedVC(cryptoCounter):
    finalHoldings = []
    hashedHoldings = {}
    soup = getSoup("https://www.hashed.com/portfolio")
    section = soup.find("section", class_="portfolioGroup-module__portfolio-group___vWCPb")
    holdings = section.find_all("button")
    
    for holding in holdings:
        holding = holding.text.strip()
        finalHoldings.append(holding)
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    hashedHoldings['Hashed VC'] = finalHoldings
    
    return hashedHoldings, cryptoCounter

def continueCapital(cryptoCounter):
    finalHoldings = []
    continueCapitalHoldings = {}
    soup = getSoup("https://continue.capital/portfolio/")
    div = soup.find('div', class_="wpb_column vc_column_container vc_col-sm-12")
    hrefs = div.find_all('a')
    for href in hrefs:
        href = str(href)
        result = re.sub(r'<a href="https://w*\.*',"", href)
        result = re.sub(r'\.\w*.*', "", result)
        holding = re.sub('</a>', "", result)
        holding = re.sub('<a href="http://', "", holding)
        holding = holding.capitalize()
        finalHoldings.append(holding.strip())
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    continueCapitalHoldings['Continue Capital'] = finalHoldings

    return continueCapitalHoldings, cryptoCounter

def cmeGroup(cryptoCounter):
    soup = getSoup("https://www.cmegroup.com/cme-ventures.html?o")
    hrefs = (soup.find_all("a"))
    finalHoldings = []
    cmeHoldings = {}
    for href in hrefs:
        link = (href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', str(link))
        link = re.sub('\.com*/*', '', str(link))
        link = str(link)
        if not link.endswith(('.html', '.pdf', "/", "form", "cmegroup", "CMEGroup", "cme-group", "insights")) and not link.startswith("#") and link != 'None':
            finalHoldings.append((link.capitalize().replace(".", " ")))
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    cmeHoldings['CME Group'] = finalHoldings
    
    return cmeHoldings, cryptoCounter

def breyerCapital(cryptoCounter):
    finalHoldings = []
    breyerCapitalHoldings =  {}
    soup = getSoup("https://breyercapital.com/portfolio/#crypto")
    divs = soup.find_all("div")
    #gets starting location for all of their cryptos by the ID Blockchain
    for index, div in enumerate (divs):
        if (div.get("id")) == "Blockchain":
            startDivIndex = index
            break
    #finds the next index of the ID that comes after it.
    #the sight could change which is why it isn't hardcoded.
    #currently the next one is Media but that could change. So this ensures
    #it will always work.
    for index, div in enumerate(divs):
        if div.get("id"):
            if index > startDivIndex:
                endIndex = index
                break
    for i in range(startDivIndex, endIndex):
        holding = divs[i].find("strong")
        if holding:
            finalHoldings.append((holding.text))
    #gets rid of duplicates
    finalHoldings = list(set(finalHoldings))
   
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    breyerCapitalHoldings['Breyer Capital'] = finalHoldings
   
    return breyerCapitalHoldings, cryptoCounter

def dcp(cryptoCounter):
    finalHoldings = []
    dcpHoldings   = {}
    soup = getSoup("https://www.dcp.capital/portfolio")
    hrefs = (soup.find_all("a"))
    for href in hrefs:
        link = (href.get("href"))
        link = str(link)
        link = re.sub('https*://w*w*w*\.*', '', link)
        link = re.sub('\.com*/*', '', link)
        link = re.sub('(.org)*(.io)*(.finance)*(.network)*(.app)*(.exchange)*(.tech)*', '', link)
        
        if not link.endswith(("/", "team", "portfolio", "research", "jobs", "home", "/portfo")):
            link = (link.capitalize())
            if link == "Alpha.tryshowtime": link = "Show Time"
            finalHoldings.append(link)
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    dcpHoldings['Dragonfly Capital'] = finalHoldings
    
    return dcpHoldings, cryptoCounter

def blockchain(cryptoCounter):
    finalHoldings             = []
    blockchainCapitalHoldings = {}
    soup = getSoup("https://blockchain.capital/portfolio/")
    hrefs = (soup.find_all("a"))
    for href in hrefs:
        
        link = (href.get("href"))
        link = str(link)
        
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub('\.com*/*', '', link)
        link = re.sub('(.org)*(.io)*(.finance)*(.network)*(.app)*(.exchange)*(.tech)*(\/)*(.gg)*(\/en)*(\-US)*(#)*(about)*(\/es)*', '', link)
        if not link.startswith(("blockchain", "app", "jobs", "#", "mailto", "subscribe", "141", "facebook", "twitter")) and link != "":
            finalHoldings.append((link.capitalize()))
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)  
    blockchainCapitalHoldings['Blockchain Capital'] = finalHoldings
    
    return blockchainCapitalHoldings, cryptoCounter

def placeholderVC(cryptoCounter):
    finalHoldings = []
    placeholderVCHoldings = {}
    soup = getSoup("https://www.placeholder.vc/?")
    hrefs = soup.find_all('a', class_="portfolio-link")
    for href in hrefs:
        finalHoldings.append(str((href.get("id").capitalize())))
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    placeholderVCHoldings['Placeholder VC'] = finalHoldings
    
    return placeholderVCHoldings, cryptoCounter

def intializedVC(cryptoCounter):
    ### THIS HAS A TON THAT ARE NOT CRYPTOS ###
    finalHoldings = []
    intializedVCHoldings = {}
    soup = getSoup("https://initialized.com/startups/")
    hrefs = soup.find_all('a')
    for href in hrefs:
        link = (href.get("href"))
        link = str(link)
        
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.com*\/*)*(\.ai\/)*(\.io\/)*(\.org\/)*(\.so\/)*(\.me\/)*(\.app\/)*(\.gg\/)*(\.net\/)*(\.capital\/)*(\.work\/)*(\.nyc\/)*(\.auto\/)*(\.it\/)*(\.io\/)*", "", link)
        if not link.startswith(("/", "blog", "jobs", "merch", "java", "/who", "/how", "twitter", "instagram")) and link != "":
            if link.endswith((".nyc", ".app", ".fyi/")):
                index = len(link)
                link = link[:index-4]
                link.replace(".", "")
            finalHoldings.append(link.capitalize())
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    intializedVCHoldings['Initalized VC'] = finalHoldings
    
    return intializedVCHoldings, cryptoCounter

def lsvp(cryptoCounter):
    finalHoldings = []
    lsvpHoldings  = {}

    soup = getSoup("https://lsvp.com/portfolio/#Commerce&Emerging&FinTech&Big%20Data/Analytics")
    holdings = soup.find_all("li")
    for holding in holdings:
        holding = str((holding.get("id")))
        if not holding.startswith("menu") and holding != "None":
            finalHoldings.append(holding)
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    lsvpHoldings["Lightspeed Holdings"] = finalHoldings
    
    return lsvpHoldings, cryptoCounter

def dhvc(cryptoCounter):
    finalHoldings = []
    DHVCholdings  = {}

    soup = getSoup("https://www.dh.vc/")
    divs = soup.find_all('div', id="pro-gallery-container")

    for div in divs[-1]:
        hrefs = div.find_all('a')
        for href in hrefs:
            link = (href.get("href"))
            link = str(link)
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            link = re.sub("(\.com*\/*)*(\.ai\/)*(\.io\/)*(\.org\/)*(\.foundation\/)*(\.me\/)*(\.app\/)*(\.finance\/)*(\.net\/)*(\.capital\/)*(\.network\/)*(\.tv\/)*(\.auto\/)*(\.it\/)*(\.io\/)*", "", link)
            finalHoldings.append((link.capitalize()))
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    DHVCholdings['DHVC'] = finalHoldings
    
    return DHVCholdings, cryptoCounter

def craftVentures(cryptoCounter):
    ### I used webbot here because the website had no way of identifying which company was crypto.
    ### there was only a drop down menu to select the crypto class which used JS to change what was displayed.
    ### while it is slower, the program is going to be slow anyway due to the magnitude of the scrapes.
    finalHoldings = []
    craftVenturesHoldings = {}
    web = Browser(showWindow=False)
    web.go_to("https://www.craftventures.com/portfolio")
    time.sleep(3)
    web.click(xpath='//*[@id="category_2"]/option[4]')
    names = web.find_elements(tag="div", classname="company-name")
    for name in names:
        finalHoldings.append(str(name.text).strip())
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    craftVenturesHoldings['Craft Ventures'] = finalHoldings

    return craftVenturesHoldings, cryptoCounter

def drwvc(cryptoCounter):
    finalHoldings = []
    drwvcHoldings = {}

    soup = getSoup("https://drwvc.com/portfolio/")
    holdings = soup.find_all("p", class_="company__name")
    for holding in holdings:
        finalHoldings.append(holding.text)
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    drwvcHoldings['DRWVC'] = finalHoldings
    
    return drwvcHoldings, cryptoCounter

def compound(cryptoCounter):
    finalHoldings = []
    compoundVCholdings = {}

    soup = getSoup("https://compound.vc/portfolio")
    sections = soup.find_all("section")
    for section in sections:
        h4 = section.find("h4")
        try:
            if h4.text == "Blockchain":
                hrefs = section.find_all("a")
                for href in hrefs:
                    link = (href.get("href"))
                    link = str(link)
                    link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
                    link = re.sub("(\.com*\/*)*(\.ai\/)*(\.io\/)*(\.org\/)*(\.casa\/)*(\.me\/)*(\.finance\/)*(\.gg\/)*(\.net\/)*(\.capital\/)*(\.work\/)*(\.nyc\/)*(\.auto\/)*(\.com/blockchain.html)*(\.io\/)*", "", link)
                    link = re.sub("blockchain.html", '', link)
                    finalHoldings.append((link.capitalize()))
        except Exception as ec:
            pass
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    compoundVCholdings['Compound VC'] = finalHoldings
    
    return compoundVCholdings, cryptoCounter

def fundersClub(cryptoCounter):
    finalHoldings = []
    fundersClubHoldings = {}

    soup = getSoup("https://fundersclub.com/portfolio/?filters=Financial%20Technology")

    divs = soup.find_all('div', class_="partnership-card")
    hrefs = divs[1].find_all('a')
    for href in hrefs:
        try:
            finalHoldings.append(str(href.contents[0]).strip())
        except:
            pass

    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    fundersClubHoldings['Funders Club'] = finalHoldings
    
    return fundersClubHoldings, cryptoCounter

def futurePerfect(cryptoCounter):
    finalHoldings = []
    futurePerfectVenturesHoldings = {}

    soup = getSoup("https://futureperfectventures.com/#_Portfolio")
    try:
        div = soup.find('div', id="fusion-recent-works-1")
        hrefs = div.find_all("a")
        for href in hrefs:
            try:
                holding = (str(href.contents[0]).strip())
                if holding not in ["zoechan", "Permalink", "Jalak Jobanputra"]:
                    holding = re.sub("(\(acquired by BitGo\))*(\(acquired Harbor\))*(\(acquired by Blockchains LLC\))*", "", holding)
                    finalHoldings.append(holding.strip())
            except:
                pass
        cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
        futurePerfectVenturesHoldings['Future Perfect'] = finalHoldings
    except Exception as ex:
        print("There was an error with future perfect.")
    
    return futurePerfectVenturesHoldings, cryptoCounter

def rre(cryptoCounter):
    finalHoldings = []
    rreHoldings   = {}

    soup = getSoup("https://rre.com/industries/blockchain")
    holdings = soup.find_all('div', class_="portfolio-hoverlabel")
    for holding in holdings:
        finalHoldings.append(str(holding.text).strip())
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    rreHoldings['RRE Holdings'] = finalHoldings
    
    return rreHoldings, cryptoCounter

def kryptonite(cryptoCounter):
    tempHoldings  = []
    finalHoldings = []
    kryptoniteHoldings = {}
    banned = ['KR1 PLC\xa0(KR1:AQSE)', "(including partial and full exits)", "2020", "INVESTMENTS", "2016", "team@kr1.io", "SINGULARDTV", "2018", "2017", "TO BE ANNOUNCED", 
              "KR1 PLC\xa0(KR1:AQSE)\xa0| 4th Floor, Queen Victoria House, 41-43 Victoria Street, Douglas, Isle of Man, IM12LF | team@kr1.io", "2019", "ACALA 2ND ROUND",
              "2021"]
    
    soup = getSoup("https://www.kryptonite1.co/investments")
    holdings = soup.find_all("span")
    for holding in holdings:
        tempHoldings.append(holding.text)
    tempHoldings = list(set(tempHoldings))
    for holding in tempHoldings:
        holding = holding.strip()
        if holding not in banned and holding != "":
            holding = re.sub("\(FOLLOW-ON\)", "", holding)
            finalHoldings.append(holding.capitalize())
    finalHoldings = list(set(finalHoldings))

    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    kryptoniteHoldings['Kryptonite1 Holdings'] = finalHoldings
    
    return kryptoniteHoldings, cryptoCounter

def blockVC(cryptoCounter):
    finalHoldings = []
    blockVCHoldings = {}

    soup = getSoup("https://www.blockvc.com/portfolio-en.html")
    div  = soup.find("div", class_="noLoady_down")
    hrefs = div.find_all('a')
    for href in hrefs:
        link = (href.get("href"))
        link = str(link)
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.com\/*\#*\/*)*(.io\/*)*(\.network\/)*(\.org\/*)*(\.im\/en\/index.html)*(\.net)*(\.co\/)*(\.cc\/*)*(\.global\/)*(\.plus\/*)*(\.foundation\/)*(\.info\/)*", "", link)
        finalHoldings.append(link.capitalize())
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    blockVCHoldings["Block VC"] = finalHoldings
    
    return blockVCHoldings, cryptoCounter

def btc(cryptoCounter):
    finalHoldings = []
    btcHoldings   = {}

    soup = getSoup("https://b.tc/about")
    div  = soup.find("div", class_="collection-list-2 w-dyn-items w-row")
    hrefs = div.find_all("a")
    for href in hrefs:
        link = str((href.get("href")))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub('(\/conference)*(\.com\/*)*(\.management\/)*', "", link)
        finalHoldings.append(link.capitalize())
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    btcHoldings['B.TC Holdings'] = finalHoldings
    
    return btcHoldings, cryptoCounter

def gbic(cryptoCounter):
    finalHoldings = []
    gbicHoldings  = {}

    soup = getSoup("https://gbic.io/portfolio")
    hrefs = soup.find_all("a")
    for href in hrefs:
        try:
            link = href.get("href")
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            link = re.sub("(\.com*\/*)*(\.ai\/)*(\.io\/)*(\.org\/)*(\.network\/)*(\.cloud\/)*(\.finance\/)*(\.eco\/)*(\.net\/)*(\.capital\/)*(\.work\/)*(\.foundation\/\?lang\=en)*(\.auto\/)*(\.com/blockchain.html)*(\.io\/)*", "", link)
            if not link.startswith(("/", "twitter", "medium", "linkedin")):
                finalHoldings.append(link.capitalize())
        except:
            pass
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    gbicHoldings['GBIC Holdings'] = finalHoldings

    return gbicHoldings, cryptoCounter

def svkCrypto(cryptoCounter):
    finalHoldings = []
    svkCryptoHoldings = {}

    soup = getSoup("https://www.svkcrypto.com/")
    hrefs  = soup.find_all("a")
    for href in hrefs:
        try:
            link = href.get("href")
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            
            if not link.startswith(("#", "svk", "docs", "twitter", "linkedin", "youtube", "audioboom", "t.me", "mailto", "uk.linkedin", "youtu.be", "block.one", "eos.io")):
                link = re.sub("(\.com\/*)*(wp\.)*(\.io\/*)*(\.games\/*)*(\.gg\/*)*(app\.)*", "", link)
                finalHoldings.append(link.capitalize())
        except:
            pass
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    svkCryptoHoldings['SVK Crypto'] = finalHoldings
    
    return svkCryptoHoldings, cryptoCounter

def multiCoin(cryptoCounter):
    finalHoldings = []
    multiCoinCapitalHoldings = {}

    soup = getSoup("https://multicoin.capital/portfolio/")
    hrefs  = soup.find_all("a")
    for href in hrefs:
        try:
            link = href.get("href")
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            if not link.startswith(("/", "github", "jobs", "twitter", "multicoin", "mailto")):
                link = re.sub("(\.com\/*)*(\.co\/*)*(\.org\/*e*n*-*u*s*\/*)*(\.io\/*)*(\.network\/*)*(\.fi\/*)*(\.us\/*)*", "", link)
                finalHoldings.append(link.capitalize())
        except:
            pass

    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    multiCoinCapitalHoldings['MultiCoin Capital'] = finalHoldings
    
    return multiCoinCapitalHoldings, cryptoCounter

def inBlockChain(cryptoCounter):
    finalHoldings = []
    inblockchainHoldings = {}
    banned = ['Specialty', "About", "Portfolio"]
    soup = getSoup("https://www.inblockchain.com/")
    hrefs = soup.find_all("a")
    for href in hrefs:
        holding = (str(href.text))
        if holding not in banned:
            finalHoldings.append(holding)

    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    inblockchainHoldings['Inblockchain Holdings'] = finalHoldings
    
    return inblockchainHoldings, cryptoCounter

def threshold(cryptoCounter):
    finalHoldings = []
    thresholdVCHoldings = {}

    soup = getSoup("https://threshold.vc/companies")
    h3   = soup.find_all("h3")
    for heading in h3:
        holding = heading.find("a")
        holding = holding.text
        holding = re.sub("(\(NASDAQ: LVGO\))*(\(NASDAQ: SFT\))*(\(Foundation Medical\))*(\(Sisense\))*", "", holding)
        finalHoldings.append(holding.strip())

    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    thresholdVCHoldings['Threshold VC'] = finalHoldings
    
    return thresholdVCHoldings, cryptoCounter

def bixin(cryptoCounter):
    finalHoldings = []
    bixinVCHoldings = {}

    soup = getSoup("http://bixincapital.com/")
    portfolio = soup.find('div', id="portfolio")
    hrefs = portfolio.find_all('a')
    for href in hrefs:
        link = str(href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.com\/*)*(\.org\/*)*", "", link)
        finalHoldings.append(link.capitalize())
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    bixinVCHoldings['Bixin VC'] = finalHoldings
    
    return bixinVCHoldings, cryptoCounter

def winklevoss(cryptoCounter):
    finalHoldings      = []
    winklevossHoldings = {}

    soup = getSoup("https://winklevosscapital.com/portfolio/?category=crypto-blockchain")
    div = soup.find('div', class_="portfolio-feed")
    headings = div.find_all('h2')
    for holding in headings:
        finalHoldings.append(str(holding.text))
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    winklevossHoldings['Winklevoss'] = finalHoldings
    
    return winklevossHoldings, cryptoCounter

def signum(cryptoCounter):
    finalHoldings   = []
    signumHoldings = {}

    soup = getSoup("https://www.signum.capital/")
    divs = soup.find_all("div", class_="swiper-slide")
    for div in divs:
        holding = div.find("img")
        holding = holding.get("alt")
        finalHoldings.append(str(holding))

    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    signumHoldings['Signum Holdings'] = finalHoldings

    return signumHoldings, cryptoCounter

def sora(cryptoCounter):
    finalHoldings = []
    soraHoldings  = {}

    soup = getSoup("http://www.sora.vc/?")
    container = soup.find("div", class_="container")
    spans = container.find_all("span")
    for span in spans:
        finalHoldings.append(str(span.text))

    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    soraHoldings['Sora Holdings'] = finalHoldings
    
    return soraHoldings, cryptoCounter

def mainVC(cryptoCounter):
    finalHoldings  = []
    mainVCHoldings = {}

    soup = getSoup("http://main.slow.co/about/")
    headings = soup.find_all('h4')
    for index, heading in enumerate(headings):
        if heading.text == "Crypto":
            cryptoIndex = index
    paragraphs = soup.find_all("p")
    holdings = (paragraphs[cryptoIndex+1])
    p = re.compile(">\w*</a>")
    result = p.findall(str(holdings))
    for holding in result:
        holding = re.sub("(>)*(<\/a>)*", "", holding)
        finalHoldings.append(holding)
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    mainVCHoldings['Slow VC'] = finalHoldings
    
    return mainVCHoldings, cryptoCounter

def idcap(cryptoCounter):
    ### Again, had to use webbot because the website just wasnt working with BS ###
    finalHoldings = []
    idCapHoldings = {}
    replacements = {"BTC":"Bitcoin", "ETH":"Ethereum", "OMG":"OMG Network", "BTM" :"Bytom", "LRC" : "Loopring", "GXS" : "GXChain"}
    web = Browser(showWindow=False)
    web.go_to("http://ldcap.com/")
    holdings = web.find_elements(tag="span")
    for holding in holdings:
        holding = holding.text
        if replacements.get(holding):
            finalHoldings.append(replacements.get(holding))
            continue
        finalHoldings.append(holding)
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    idCapHoldings['ID Cap'] = finalHoldings
    
    return idCapHoldings, cryptoCounter

def versionOne(cryptoCounter):
    finalHoldings      = []
    versionOneHoldings = {}
    links = []
    soup = getSoup("https://versionone.vc/our-portfolio/")
    lis = soup.find_all("li", {"class" : "portfolio__list-item", "data-is-exited" : "false"})
    for li in lis:
        href = li.find("a")
        links.append(str(href.get("href")))
    for link in links:
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.com*\/*\#*\/*e*n*\/*)*(\.support\/*)*(\.io\/*)*(\.org\/*)*(\.dev\/*)*(network\.)*", "", link)
        finalHoldings.append(link.capitalize())
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    versionOneHoldings['Version One VC'] = finalHoldings
    
    return versionOneHoldings, cryptoCounter

def yeoman(cryptoCounter):
    finalHoldings = []
    yeomanHoldings = {}

    soup = getSoup("https://www.yeomans.capital/")
    div = soup.find('div', class_="s-mh s-repeatable")
    hrefs = div.find_all("a")
    for href in hrefs:
        link = str(href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.org\/*)*(\.network\/*)*(\.com\/*e*n*\/*)*(\.mw\/*)*(\.one\/*)*", "", link)
        finalHoldings.append(link.capitalize())
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    yeomanHoldings['Yeoman'] = finalHoldings
    
    return yeomanHoldings, cryptoCounter

def lemniscap(cryptoCounter):
    finalHoldings = []
    lemniscapHoldings = {}
    banned = ["website ➞", "DISCLAIMER", "PRIVACY", "ABOUT", "PORTFOLIO", "JOBS", "CONTACT"]
    web = Browser(showWindow=False)
    web.go_to("https://lemniscap.com/portfolio")
    
    count = 1
    descriptions = []
    while count < 40:
        description = web.find_elements(xpath=f"/html/body/div/div[3]/div/div[{count}]/span")
        for desc in description:
            if desc.text != "" and desc.text not in banned:
                descriptions.append(desc.text)
                
        count += 1
    for description in descriptions:
        description = re.sub("(is.*)*(provides.*\n*.*)*(enables.*)*(operates.*)*(anonymou.* )*(aims.*)*", "", description)
        if description == "Anonymous payment channels for instant, cheap and private payments. BOLT eliminates lag time and high transaction fees — while offering strong privacy protections. BOLT ":
            description = "Bolt"
            finalHoldings.append(description)
            continue
        finalHoldings.append(description.strip())
    
    cryptoCounter = addToCryptoCounter(finalHoldings, cryptoCounter)
    lemniscapHoldings['Lemnis Cap'] = finalHoldings
    
    return lemniscapHoldings, cryptoCounter



def main():
    allHoldings = []

    boostVCHoldings, cryptoCounter         = boostVC()
    allHoldings.append(boostVCHoldings)
    
    outlierVenturesHoldings, cryptoCounter = outlierVentures(cryptoCounter)
    allHoldings.append(outlierVenturesHoldings)

    dcgHoldings, cryptoCounter            = dcg(cryptoCounter)
    allHoldings.append(dcgHoldings)
   
    panteraHoldings, cryptoCounter         = pantera(cryptoCounter)
    allHoldings.append(panteraHoldings)
    
    arringtonxrHoldings, cryptoCounter     = arringtonxr(cryptoCounter)
    allHoldings.append(arringtonxrHoldings)
 
    coinbaseHoldings, cryptoCounter          = coinbase(cryptoCounter)
    allHoldings.append(coinbaseHoldings)
    
    fenbushcapitalHoldings, cryptoCounter    = fenBushCapital(cryptoCounter)
    allHoldings.append(fenbushcapitalHoldings)

    hashedHoldings, cryptoCounter             = hashedVC(cryptoCounter)
    allHoldings.append(hashedHoldings)
      
    continueCapitalHoldings, cryptoCounter    = continueCapital(cryptoCounter)
    allHoldings.append(continueCapitalHoldings)

    cmeHoldings, cryptoCounter      = cmeGroup(cryptoCounter)
    allHoldings.append(cmeHoldings)
    
    breyerCapitalHoldings, cryptoCounter = breyerCapital(cryptoCounter)
    allHoldings.append(breyerCapitalHoldings)
    
    dcpCapitalHoldings, cryptoCounter = dcp(cryptoCounter)
    allHoldings.append(dcpCapitalHoldings)
    
    blockchainCapitalHoldings, cryptoCounter = blockchain(cryptoCounter)
    allHoldings.append(blockchainCapitalHoldings)
    
    placeholderVCHoldings, cryptoCounter = placeholderVC(cryptoCounter)
    allHoldings.append(placeholderVCHoldings)

    intializedVCHoldings, cryptoCounter = intializedVC(cryptoCounter)
    allHoldings.append(intializedVCHoldings)
    
    lsvpHoldings, cryptoCounter = lsvp(cryptoCounter)
    allHoldings.append(lsvpHoldings)

    DHVCholdings, cryptoCounter = dhvc(cryptoCounter)
    allHoldings.append(DHVCholdings)
    
    drwvcHoldings, cryptoCounter = drwvc(cryptoCounter)
    allHoldings.append(drwvcHoldings)
    
    compoundVCholdings, cryptoCounter = compound(cryptoCounter)
    allHoldings.append(compoundVCholdings)
    
    fundersClubHoldings, cryptoCounter = fundersClub(cryptoCounter)
    allHoldings.append(fundersClubHoldings)
    
    futurePerfectVenturesHoldings, cryptoCounter = futurePerfect(cryptoCounter)
    allHoldings.append(futurePerfectVenturesHoldings)
    

    rreHoldings, cryptoCounter = rre(cryptoCounter)
    allHoldings.append(rreHoldings)

    kryptoniteHoldings, cryptoCounter = kryptonite(cryptoCounter)
    allHoldings.append(kryptoniteHoldings)
    
    blockVCHoldings, cryptoCounter = blockVC(cryptoCounter)
    allHoldings.append(blockVCHoldings)
    
    btcHoldings, cryptoCounter = btc(cryptoCounter)
    allHoldings.append(btcHoldings)

    gbicHoldings, cryptoCounter = gbic(cryptoCounter)
    allHoldings.append(gbicHoldings)

    svkCryptoHoldings, cryptoCounter = svkCrypto(cryptoCounter)
    allHoldings.append(svkCryptoHoldings)

    multiCoinCapitalHoldings, cryptoCounter = multiCoin(cryptoCounter)
    allHoldings.append(multiCoinCapitalHoldings)

    inblockchainHoldings, cryptoCounter = inBlockChain(cryptoCounter)
    allHoldings.append(inblockchainHoldings)

    thresholdVCHoldings, cryptoCounter = threshold(cryptoCounter)
    allHoldings.append(thresholdVCHoldings)

    bixinVCHoldings, cryptoCounter = bixin(cryptoCounter)
    allHoldings.append(bixinVCHoldings)

    winklevossHoldings, cryptoCounter = winklevoss(cryptoCounter)
    allHoldings.append(winklevossHoldings)

    signumHoldings, cryptoCounter = signum(cryptoCounter)
    allHoldings.append(signumHoldings)

    soraHoldings, cryptoCounter = sora(cryptoCounter)
    allHoldings.append(soraHoldings)

    mainSlowHoldings, cryptoCounter = mainVC(cryptoCounter)
    allHoldings.append(mainSlowHoldings)

    versionOneHoldings, cryptoCounter = versionOne(cryptoCounter)
    allHoldings.append(versionOneHoldings)

    yeomanHoldings, cryptoCounter = yeoman(cryptoCounter)
    allHoldings.append(yeomanHoldings)

    lemniscapHoldings, cryptoCounter = lemniscap(cryptoCounter)
    allHoldings.append(lemniscapHoldings)


    idCapHoldings, cryptoCounter = idcap(cryptoCounter)
    allHoldings.append(idCapHoldings)

    craftVenturesHoldings, cryptoCounter = craftVentures(cryptoCounter)
    allHoldings.append(craftVenturesHoldings)

    print(cryptoCounter)

    keys = []
    for i,j in enumerate (allHoldings):
        keys.append((j.keys()))
        
        
    
    convertToExcel(cryptoCounter, allHoldings, keys)

def convertToExcel(cryptoCounter, allHoldings, keys):
    wb = xlsxwriter.Workbook('cryptos.xlsx')
    ws = wb.add_worksheet("Outlined Rows")
    ws.set_column('A:A', 20)
    ws.write('A1', "Crypto")
    ws.write('B1', "Counter")
    cell_format = wb.add_format()
    cell_format.set_bold()
    aCount  = 2
    bCount = 2 
    for key, value in cryptoCounter.items():
        cryptoCol = 'A' + str(aCount)
        countCol = 'B' + str(bCount)
        ws.write(cryptoCol, key)
        ws.write(countCol, value)
        for i in keys:
            for j in i:
                for k, l in enumerate(allHoldings):
                    try:
                        if key in allHoldings[k].get(j):
                            aCount = aCount + 1
                            bCount = bCount + 1
                            cryptoCol = 'A' + str(aCount)
                            ws.write(cryptoCol, j, cell_format)
                            ws.set_row(aCount - 1, None , None, {'level':1, 'hidden':True,'collapsed':True})
                    except:
                        pass
        aCount += 1
        bCount += 1
    wb.close()
    
main()