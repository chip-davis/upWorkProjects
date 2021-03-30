import requests
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import xlsxwriter
import openpyxl
from webbot import Browser
import time
import os

def getSoup(url, verify=True):
    print(f"Scraping {url}")
    headers =  {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    soup = BeautifulSoup(requests.get(url, headers=headers, verify=verify).content, 'html.parser')
    return soup

def addToCryptoCounter(cryptoCounter, finalHoldings):
    finalHoldings = list(set(finalHoldings))
    for holding in finalHoldings:
        if cryptoCounter.get(holding):
            cryptoCounter[holding] += 1
        else:
            cryptoCounter[holding] = 1
    return cryptoCounter, finalHoldings

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

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)

    dcgHoldings['DCG Holdings'] = finalHoldings
    
    return dcgHoldings, cryptoCounter

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

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)    
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
   
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)  
    blockchainCapitalHoldings['Blockchain Capital'] = finalHoldings
    
    return blockchainCapitalHoldings, cryptoCounter

def placeholderVC(cryptoCounter):
    finalHoldings = []
    placeholderVCHoldings = {}
    soup = getSoup("https://www.placeholder.vc/?")
    hrefs = soup.find_all('a', class_="portfolio-link")
    for href in hrefs:
        finalHoldings.append(str((href.get("id").capitalize())))
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
            if link == "theta":
                finalHoldings.append("Thetatoken")
                continue
            finalHoldings.append((link.capitalize()))
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    DHVCholdings['DHVC'] = finalHoldings
    
    return DHVCholdings, cryptoCounter

def craftVentures(cryptoCounter):
    ### I used webbot here because the website had no way of identifying which company was crypto.
    ### there was only a drop down menu to select the crypto class which used JS to change what was displayed.
    ### while it is slower, the program is going to be slow anyway due to the magnitude of the scrapes.
    print("scraping www.craftventures.com")
    finalHoldings = []
    craftVenturesHoldings = {}
    web = Browser(showWindow=False)
    web.go_to("https://www.craftventures.com/portfolio")
    time.sleep(3)
    web.click(xpath='//*[@id="category_2"]/option[4]')
    names = web.find_elements(tag="div", classname="company-name")
    for name in names:
        finalHoldings.append(str(name.text).strip())
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    craftVenturesHoldings['Craft Ventures'] = finalHoldings

    return craftVenturesHoldings, cryptoCounter

def drwvc(cryptoCounter):
    finalHoldings = []
    drwvcHoldings = {}

    soup = getSoup("https://drwvc.com/portfolio/")
    holdings = soup.find_all("p", class_="company__name")
    for holding in holdings:
        finalHoldings.append(holding.text)
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
        cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    mainVCHoldings['Slow VC'] = finalHoldings
    
    return mainVCHoldings, cryptoCounter

def idcap(cryptoCounter):
    ### Again, had to use webbot because the website just wasnt working with BS ###
    print("scraping ldcap.com")
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    yeomanHoldings['Yeoman'] = finalHoldings
    
    return yeomanHoldings, cryptoCounter

def lemniscap(cryptoCounter):
    print("scraping www.lemniscap.com")
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
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    lemniscapHoldings['Lemnis Cap'] = finalHoldings
    
    return lemniscapHoldings, cryptoCounter

def gumi(cryptoCounter):
    finalHoldings = []
    gumiCryptosHoldings = {}

    soup = getSoup("https://www.gumi-cryptos.com/")
    div  = soup.find('div', class_="filtr-container")
    hrefs = div.find_all("a")
    for href in hrefs:
        link = str(href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.org\/*)*(\.com*\/*e*n*\/*h*o*m*e*)*(\.io\/*)*(\.jp\/*)*(\.xyz\/*)*(\.network\/*)*(\.finance\/*\#*\/*)*(\.exchange\/*)*", "", link)
        finalHoldings.append(link.capitalize())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    gumiCryptosHoldings["Gumi Crypto"] = finalHoldings
    
    return gumiCryptosHoldings, cryptoCounter

def hardYaka(cryptoCounter):
    finalHoldings = []
    hardYakaHoldings = {}

    soup = getSoup("https://hardyaka.com/investments/")
    div  = soup.find("div", class_="content-container")
    hrefs = div.find_all("a")
    for href in hrefs:
        link = (href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.net\/*)*(\.com*\/*e*n*\/*w*e*l*c*o*m*e*a*b*o*u*t*\-*u*s*\.*h*t*m*l*\#*i*n*d*e*x*\/*)*(corporate\.)*(\.it\/*)*(\.app\/*)*(\.io\/*)*(\.org\/*)*(\.money\/*)*(\.is\/*)*(\.social\/*)*(\.engineering\/*)*(\.financial\/*)*(\.br\/*)*(\.tech\/*)*(\.us\/*)*(\.mx\/*)*", "", link)
        link = re.sub("(\/)*(corp\.)*", "", link)
        finalHoldings.append(link.capitalize())
        
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    hardYakaHoldings['Hard Yaka Holdings'] = finalHoldings

    return hardYakaHoldings, cryptoCounter

def milestone(cryptoCounter):
    finalHoldings = []
    milestoneHoldings = {}

    soup = getSoup("http://milestonevc.com/project/qukuai/")
    holdings = soup.find_all("p")
    for holding in holdings:
        holding = (holding.text.strip())
        if holding:
            finalHoldings.append(holding)
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    milestoneHoldings["Milestone Holdings"] = finalHoldings
    
    return milestoneHoldings, cryptoCounter

def socialCapital(cryptoCounter):
    finalHoldings = []
    socialCapitalHoldings = {}

    soup = getSoup("https://www.socialcapital.com/portfolio")
    divs = soup.find_all("div")
    for div in divs:
        if div.get("class") == ["Portfolio-name-0-2-82"]:
            holding = div.text.strip()
            finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    socialCapitalHoldings['Social Capital'] = finalHoldings
    
    return socialCapitalHoldings, cryptoCounter

def abstractVC(cryptoCounter):
    finalHoldings = []
    abstractVCHoldings = {}

    soup = getSoup("https://www.abstractvc.com/companies")
    div = soup.find('div', class_="MuiGrid-root MuiGrid-container MuiGrid-align-items-xs-center MuiGrid-justify-xs-center")
    images = div.find_all("img")
    for image in images:
        holding = str((image.get("alt")))
        finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    abstractVCHoldings['Abstract VC'] = finalHoldings

    return abstractVCHoldings, cryptoCounter

def signalVC(cryptoCounter):
    ### WEBSITE REQUIRED JS USING WEBBOT ###
    print("scraping https://signal.vc")
    finalHoldings    = []
    signalVCHoldings = {}
    
    web = Browser(showWindow=False)
    web.go_to("https://signal.vc/")
    hrefs = web.find_elements(tag="a")
    
    for href in hrefs:
        link = str((href.get_attribute("href")))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.com\/*)*(\.network\/*)*(\.finance\/*)*(\.io\/*e*n*\/*)*(\.org\/*)*", "", link)
        link = re.sub("\.", " ", link)
        link = link.replace("/", "")
        if link == "fetch ai":
            link = "Fetch.AI"
            finalHoldings.append(link)
            continue
        if not link.startswith("mailto"):
            finalHoldings.append(link.capitalize())


    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    signalVCHoldings['Signal VC'] = finalHoldings
    
    return signalVCHoldings, cryptoCounter

def notation(cryptoCounter):
    finalHoldings = []
    notationVCHoldings = {}
    soup = getSoup("https://notation.vc/companies/")
    
    #I use regex to get a partial class name match.
    #All of the class names in the HTML that corresponded to crypto were slightly different.
    #But, they all had blockchain in there somewhere so this grabs all of them and ignores the
    #other companies.

    divs = soup.find_all("div", attrs={'class' : re.compile(".*blockchain.*")})
    
    for div in divs:
        holding = div.find("span", class_="company-name")
        holding = (holding.text)
        finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    notationVCHoldings['Notation VC'] = finalHoldings
    
    return notationVCHoldings, cryptoCounter

def metaVerse(cryptoCounter):
    finalHoldings = []
    metaVerseVenturesHoldings = {}
    
    soup = getSoup("https://metaverseventures.co/?ref=block123#investments")
    holdings = soup.find_all("h3")
    for holding in holdings:
        finalHoldings.append(str(holding.text))

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    metaVerseVenturesHoldings['MetaVerse Ventures'] = finalHoldings

    return metaVerseVenturesHoldings, cryptoCounter

def nirvanaCapital(cryptoCounter):
    finalHoldings = []
    nirvanaCapitalHoldings = {}

    soup = getSoup("http://nirvana.capital/")
    holdings = soup.find_all("figcaption", class_="wp-caption-text")

    for holding in holdings:
        holding = (str(holding.text).strip())
        if holding == "Zen Protocol":
            holding = "Zenprotocol"
            finalHoldings.append(holding)
            continue
        finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    nirvanaCapitalHoldings['Nirvana Capital'] = finalHoldings

    return nirvanaCapitalHoldings, cryptoCounter

def binanceLabs(cryptoCounter):
    finalHoldings = []
    binanceLabsHoldings = {}

    soup = getSoup("https://labs.binance.com/")
    headings = soup.find_all("h4")
    for heading in headings:
        href = heading.find("a")
        finalHoldings.append(str(href.text).strip())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    binanceLabsHoldings['Binance Labs'] = finalHoldings
       
    return binanceLabsHoldings, cryptoCounter

def castleIsland(cryptoCounter):
    finalHoldings = []
    castleIslandHoldings = {}

    soup = getSoup("https://www.castleisland.vc/portfolio")
    hrefs = soup.find_all("a")
    for href in hrefs:
        link = str((href.get("href")))
        
        if not link.startswith(("index", "/", "mailto", "https://onthebrink")):
            
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            link = re.sub("(\.com\/*)*(\.casa\/*)*(\.io\/*.*)*(\.id\/*)*", "", link)
            holding = link.strip().capitalize()
            finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    castleIslandHoldings['Castle Island'] = finalHoldings
    
    return castleIslandHoldings, cryptoCounter

def consensys(cryptoCounter):
    finalHoldings = []
    consensysLabsHoldings = {}

    soup = getSoup("https://mesh.xyz/portfolio/")
    headings = soup.find_all("h5")
    for heading in headings:
        holding = str(heading.text).strip()
        finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    consensysLabsHoldings['Consensys Labs'] = finalHoldings
    
    return consensysLabsHoldings, cryptoCounter

def ecf(cryptoCounter):
    finalHoldings = []
    ecfHoldings   = {}

    soup = getSoup("https://ecf.network/")
    headings = soup.find_all("h5")
    for heading in headings:
        finalHoldings.append(str(heading.text).capitalize())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    ecfHoldings['Etherem Community Fund'] = finalHoldings
   
    return ecfHoldings, cryptoCounter

def a16z(cryptoCounter):
    finalHoldings = []
    a16zHoldings  = {}

    soup = getSoup("https://a16z.com/portfolio/#crypto")
    divs = soup.find_all('div', attrs={"class":re.compile(".*crypto.*")})

    for div in divs:
        try:
            href = div.find('a')
            link = str(href.get("href"))
            if not link.startswith(("https://a16z", "https://twitter", "https://info.a16z","https://https://portfoliojobs", "/", "#")):
                link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
                link = re.sub("(\.com*\/*)*(\.org\/*e*n*\-*U*S*\/*)*(\.finance\/*)*(\.net\/*)*(\.exchange\/*)*(\.ai\/*)*(\.network\/*)*(\.capital\/*)*(\.io\/*)*(\/)*", "", link)
                holding = link.capitalize().strip()
                finalHoldings.append(holding)
        except:
            pass
  
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    a16zHoldings['A16z'] = finalHoldings
    
    return a16zHoldings, cryptoCounter

def fabricVC(cryptoCounter):
    finalHoldings = []
    fabricVCHoldings = {}

    soup = getSoup("https://www.fabric.vc/")
    #div = soup.find("div", class_="sqs-block-content")
    hrefs = soup.find_all("a")
    for href in hrefs:
        link = str(href.get("href"))
        if not link.startswith(("/", "https://www.fabric", "https://medium", "#", "https://twitter", "https://www.linkedin", "https://youtu.be", "https://player.fm",
                                "https://techcrunch", "https://www.eventbrite", "https://blog", "https://tbtc", "https://www.youtube", "https://open.spotify",
                                "https://www.ft", "https://cbhack", "https://human", "https://innovator", "http://cogx", "mailto", "https://www.facebook",
                                "https://www.coindesk", "https://centrifuge", "https://blockchainconvergence", "https://www.thimble", "https://www.devcon",
                                "https://www.dld", "https://www.etherealsummit", "https://dappcon", "https://instant", "https://podcasts",
                                "https://blockchainventuresummit", "http://www.thimble", "https://devcon", "https://fabricvc", "http://eepurl")) and link != "None":
            
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            link = re.sub("(\.com*\/*)*(\.org\/*e*n*\-*U*S*\/*)*(\.finance\/*)*(\.net\/*)*(\.exchange\/*)*(\.ai\/*)*(\.network\/*)*(\.capital\/*)*(\.io\/*)*(\/)*(\.us\/*)*(\.casa\/*)*(\.xyz\/*)*(\.im)*", "", link)
            holding = link.capitalize().strip()
            finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    fabricVCHoldings['Fabric VC'] = finalHoldings
    
    return fabricVCHoldings, cryptoCounter

def eightDCapital(cryptoCounter):
    finalHoldings = []
    eightDCapitalHoldings = {}

    soup = getSoup("http://www.8dcapital.com/portfolio.html")
    table = soup.find("tbody")
    for tr in table.find_all("tr"):
        td = tr.find("td")
        holding = td.text
        finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    eightDCapitalHoldings['8D Capital'] = finalHoldings

    return eightDCapitalHoldings, cryptoCounter

def blockchainff(cryptoCounter):
    finalHoldings = []
    blockchainffHoldings = {}

    links = []

    soup = getSoup("https://blockchainff.com/")
    div = soup.find("div", class_="elementor-container elementor-column-gap-default")
    hrefs = soup.find_all("a")
    for href in hrefs:
        link = str(href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        if not link.startswith(("blockchainff", "investment", "linkedin", "twitter", "#", "pbs", "t.co", "facebook", "//pinterest")):
            links.append(link)
    links = list(set(links))
    for link in links:
        link = re.sub("(\.com*\/*)*(\.org\/*e*n*\-*U*S*\/*)*(\.finance\/*)*(\.net\/*)*(\.exchange\/*)*(\.ai\/*)*(\.network\/*)*(\.capital\/*)*(\.io\/*)*(\/)*(\.us\/*)*(\.casa\/*)*(\.xyz\/*)*(\.im)*", "", link)
        link = re.sub("(\.vc)*(app)*(\.nyc)*(home)*(\.ie)*(\.wine)*(\.biz)*(\.in)*(\.my)*(\.cc)*(\.r\w)*(\.one)*(\.ca)*(sosvportfolio)*", "", link)
        finalHoldings.append(link.capitalize())
        

    cryptoCouter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    blockchainffHoldings['Blockchainff Holdings'] = finalHoldings

    return blockchainffHoldings, cryptoCounter

def fundamentalLabs(cryptoCounter):
    ###SITE REQUIRED JS ###
    ###Some of the ones that are grabbed where the ALT tag is only 3 letters, do not look good but
    ###its the best I can do as the images are not links.
    print("scraping https://www.fundamentallabs.com")
    finalHoldings = []
    fundamentalHoldings  = {}
    banned = ("Logo", "home image", "banner-1")

    web = Browser(showWindow=False)
    web.go_to("https://www.fundamentallabs.com/#/")
    web.click(xpath='//*[@id="portfolio"]/div[2]')
    images = web.find_elements(tag="img")
    for img in images:
        img = str(img.get_attribute("alt"))
        if img not in banned:
            holding = re.sub("(\.)*(\d*)*(\W)*", "", img)
            if holding == "":
                continue
            finalHoldings.append(holding.strip().capitalize())
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    fundamentalHoldings['Fundamental Labs'] = finalHoldings
    
    return fundamentalHoldings, cryptoCounter

def chainfund(cryptoCounter):
    finalHoldings = []
    chainfundHoldings = {}

    web   = Browser(showWindow=False)
    web.go_to("http://chainfund.capital/")
    hrefs = web.find_elements(tag="a")
    for href in hrefs:
        link = str(href.get_attribute("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        if not link.startswith(("chainfund", "medium", "youtu", "forbes", "advfn", "businessinsider", "finance.yahoo")):
            link = re.sub("(\.com\/*i*n*d*e*x*\/*)*(\.io\/*)*", "", link)
            if link != "None":
                finalHoldings.append(link.capitalize())

    finalHoldings.append("Good Money")
    finalHoldings.append("Abra")

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    chainfundHoldings['Chain Fund'] = finalHoldings

    return chainfundHoldings, cryptoCounter

def unionCapital(cryptoCounter):
    finalHoldings = []
    unionCapitalHoldings = {}

    soup      = getSoup("https://www.usv.com/companies/")
    companies = soup.find_all("div", class_="m__list-row__title")
    for company in companies:
        holding = str(company.text.strip())
        finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    unionCapitalHoldings['Union Capital'] = finalHoldings

    return unionCapitalHoldings, cryptoCounter

def sequoiaCap(cryptoCounter):
    finalHoldings = []
    sequoiaCapHoldings = {}

    soup = getSoup("https://www.sequoiacap.com/companies/")
    companies = soup.find_all('div', class_="_name")
    for company in companies:
        holding = str(company.text.strip())
        finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    sequoiaCapHoldings['Sequoia Capital'] = finalHoldings
    
    return sequoiaCapHoldings, cryptoCounter

def gv(cryptoCounter):
    finalHoldings = []
    gvHoldings    = {}

    soup = getSoup("https://www.gv.com/portfolio/")
    holdings = soup.find_all("a", attrs={"data-name" : True})
    for holding in holdings:
        holding = str(holding.get("data-name")).strip()
        finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    gvHoldings['GV Holdings'] = finalHoldings
    
    return gvHoldings, cryptoCounter

def collaborativeFund(cryptoCounter):
    finalHoldings =  []
    collaborativeFundHoldings = {}
    banned = ['eepurlcgCbcz', 'feeds.feedburnercollabfund', 'twittercollabfund']
    soup = getSoup("https://www.collaborativefund.com/investments/")
    main = soup.find_all("main")
    hrefs = soup.find_all('a')
    for href in hrefs:
        link = str(href.get("href"))
        if not link.startswith("/"):
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            link = re.sub("(\.com*\/*)*(\.org\/*e*n*\-*U*S*\/*)*(\.finance\/*)*(\.net\/*)*(\.exchange\/*)*(\.ai\/*)*(\.network\/*)*(\.capital\/*)*(\.io\/*)*(\/)*(\.us\/*)*(\.casa\/*)*(\.xyz\/*)*(\.im)*", "", link)
            if link not in banned and link != "None":
                finalHoldings.append(link.capitalize())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    collaborativeFundHoldings['Collaborative Fund'] = finalHoldings

    return collaborativeFundHoldings, cryptoCounter

def freesvc(cryptoCounter):
    print("Scraping freesvc.com")

    finalHoldings = []
    freesvcHoldings = {}
    banned = ["freesvc", "itunes.applecnappfrees-clubid1106515579?mt=8", "a.app.qqosimple.jsp?pkgname=com.freesvc.club", "beian.miit.gov.cn", "beian.miit.gov"]

    web = Browser(showWindow=False)
    web.go_to("https://www.freesvc.com/company")
    hrefs = web.find_elements(tag="a")
    
    for href in hrefs:
        link = str(href.get_attribute("href"))
        if not link.startswith(("mailto")):
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            link = re.sub("(\.com*\/*)*(\.org\/*e*n*\-*U*S*\/*)*(\.finance\/*)*(\.net\/*)*(\.exchange\/*)*(\.ai\/*)*(\.network\/*)*(\.capital\/*)*(\.io\/*)*(\/)*(\.us\/*)*(\.casa\/*)*(\.xyz\/*)*(\.im)*(\/*\.*index\.html)*(\/*hshcweb\/beijing\.html)*(\/*Index.aspx)*(\/*download_app\/)*(\/*home/index)*(\.cn\/*)*(\.*zh\/*)*(\/zh-hans\/*)*(\/*shanghai)*(#)*", "", link)
            if link not in banned:
                finalHoldings.append(link.capitalize())
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    freesvcHoldings['Free SVC'] = finalHoldings

    return freesvcHoldings, cryptoCounter

def generalCatalyst(cryptoCounter):
    finalHoldings = []
    generalCatalystHoldings = {}
    banned = ['generalcatalyst.comgcamplified', 'generalcatalyst.comgcamplified', 'generalcatalyst.comterms-of-use', 'generalcatalyst.comprivacy-policy', 'generalcatalyst.comdisclaimer']

    soup = getSoup("https://www.generalcatalyst.com/")
    hrefs = soup.find_all('a')
    for href in hrefs:
        link = (href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        
        if not link.startswith(("/", "#", "mailto", "jobs", "twitter", "facebook", "linkedin")):
            link = re.sub("generalcatalyst\.com\/portfolio\/", "", link)
            link = link.replace("/", "")
            if link not  in banned:
                finalHoldings.append(link.capitalize())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    generalCatalystHoldings['General Catalyst'] = finalHoldings

    return generalCatalystHoldings, cryptoCounter

def preAngel(cryptoCounter):
    finalHoldings = []
    preAngelHoldings = {}
    soup = getSoup("http://pre-angel.com/portfolios/")
    holdings = soup.find_all('h4')
    for holding in holdings:
        holding = str(holding.text.strip())
        holding = re.sub("\(.*\)", "", holding)
        for char in holding:
            #makes sure that only fully english words are getting added
            #this does create duplicates but finalHoldings gets converted to a set
            #and back to a list in addToCryptoCounter so its not that big of a deal
            #as the list isnt that long anyway

            if ord(char.lower()) not in range(97, 123):
                continue
            finalHoldings.append(holding)
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    preAngelHoldings['Pre Angel'] = finalHoldings

    return preAngelHoldings, cryptoCounter

def collider(cryptoCounter):
    finalHoldings = []
    colliderHoldings = {}

    soup = getSoup("https://www.collider.vc/")
    divs = soup.find_all('div', class_="_2TxBB _3TiYw")
    for div in divs:
        href = div.find('a')
        link = str(href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        if not link.startswith("collider"):
            link = re.sub("(\.io\/*)*(\.mw\/*)*(\.com\/*)*(\.fi\/*)*", "", link)
            link = link.replace("-", " ")
            finalHoldings.append(link.capitalize())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    colliderHoldings['Collider'] = finalHoldings

    return colliderHoldings, cryptoCounter

def colliderLabs(crytpoCounter):
    finalHoldings = []
    colliderLabsHoldings = {}

    soup = getSoup("https://www.collider.vc/collider-labs")
    main = soup.find("section", attrs={"id":"comp-kgdz7dnb"})
    spans = main.find_all("span", attrs={"style" : "color:#000000"})
    
    for span in spans:
        description = str(span.text)
        description = re.sub("(develops.*)*(is.*)*", "", description)
        if description != "\u200b":
            finalHoldings.append(description.strip())

    cryptoCounter, finalHoldings = addToCryptoCounter(crytpoCounter, finalHoldings)
    colliderLabsHoldings['Collider Labs'] = finalHoldings

    return colliderLabsHoldings, cryptoCounter

def framework(cryptoCounter):
    finalHoldings = []
    frameworkHoldings = {}

    soup = getSoup("https://framework.ventures/")
    holdings = soup.find_all("div", attrs={"class":"Home__PortfolioImageLabel-sc-1aigozo-13 fPKzYY"})
    
    for holding in holdings:
        finalHoldings.append(str(holding.text).strip())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    frameworkHoldings['Framework'] = finalHoldings

    return frameworkHoldings, cryptoCounter

def maven(cryptoCounter):
    finalHoldings = []
    mavenHoldings = {}
    banned = ['Maven 11', "Contact", "Legal", "Subscribe to our publications"]
    soup = getSoup("https://www.maven11.com/portfolio")
    holdings = soup.find_all('h4')
    for holding in holdings:
        holding = holding.text
        if holding not in banned:
            finalHoldings.append(holding)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    mavenHoldings['Maven11'] = finalHoldings

    return mavenHoldings, cryptoCounter

def digistrats(cryptoCounter):
    finalHoldings = []
    digistratsHoldings = {}

    soup = getSoup("https://digistrats.com/")
    images = soup.find_all("img")
    for img in images:
        holding = str(img.get("alt"))
        if holding != "None":
            finalHoldings.append(holding)
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    digistratsHoldings['Digistrat'] = finalHoldings

    return digistratsHoldings, cryptoCounter

def sparkdigital(cryptoCounter):
    finalHoldings = []
    sparkdigitalHoldings = {}

    soup = getSoup("http://www.sparkdigitalcapital.com/#portfolio_sec", False)
    section = soup.find('section', attrs={"id" : 'portfolio_sec'})
    hrefs = section.find_all("a")
    for href in hrefs:
        link = str(href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.exchange\/*#*\/*)*(\.com*\/*)*(\.pro\/*)*(\.xyz\/*)*(\.org\/*)*(\.network\/*)*(\.io\/*)*(\.finance\/*)*(\.one\/*)*(\.trade\/*)*", "", link)
        finalHoldings.append(link.capitalize())
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    sparkdigitalHoldings['Spark Digital'] = finalHoldings

    return sparkdigitalHoldings, cryptoCounter

def rarestone(cryptoCounter):
    finalHoldings = []
    rarestoneHoldings = {}

    soup = getSoup('https://rarestone.capital/capital/')
    hrefs = soup.find_all('a', attrs={"class":"logo col-4 lg-col-3 px2 sm-px4 sm-px5 sm-my2 my1 lg-my3"})

    for href in hrefs:
        link = str(href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.exchange\/*#*\/*)*(\.com*\/*)*(\.pro\/*)*(\.xyz\/*)*(\.org\/*)*(\.network\/*)*(\.io\/*)*(\.finance\/*)*(\.one\/*)*(\.trade\/*)*(\.dev\/*#*\/*)*(\.im\/*)*", "", link)
        finalHoldings.append(link.capitalize())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    rarestoneHoldings['Rarestone'] = finalHoldings

    return rarestoneHoldings, cryptoCounter

def bitscale(cryptoCounter):
    finalHoldings = []
    bitscaleHoldings = {}

    soup = getSoup("https://bitscale.capital/#projects")
    section = soup.find('section', id="projects")
    hrefs = section.find_all('a')
    for href in hrefs:
        link = str(href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.exchange\/*#*\/*)*(\.com*\/*)*(\.pro\/*)*(\.xyz\/*)*(\.org\/*)*(\.network\/*)*(\.io\/*)*(\.finance\/*)*(\.one\/*)*(\.trade\/*)*(\.dev\/*#*\/*)*(\.im\/*)*(\.fi\/*)*(\.games\/*)*(\.net\/*)*", "", link)
        finalHoldings.append(link.capitalize())
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    bitscaleHoldings['Bitscale'] = finalHoldings

    return bitscaleHoldings, cryptoCounter 

def divVC(cryptoCounter):
    finalHoldings = []
    divVCHoldings = {}

    soup = getSoup("https://www.div.vc/")
    div  = soup.find("div", class_="portfolio-big-container")
    hrefs = div.find_all("a")
    for href in hrefs:
        finalHoldings.append(href.text)

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    divVCHoldings['DIV VC'] = finalHoldings

    return divVCHoldings, cryptoCounter
    
def mondayCapital(cryptoCounter):
    finalHoldings = []
    mondayCapitalHoldings = {}

    soup = getSoup('https://www.monday.capital/our-startups')
    hrefs = soup.find_all("a")
    for href in hrefs:
        link = str(href.get("href"))
        if not link.startswith(("/")):
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            link = re.sub("(\.exchange\/*#*\/*)*(\.com*\/*)*(\.pro\/*)*(\.xyz\/*)*(\.org\/*)*(\.network\/*)*(\.io\/*)*(\.finance\/*)*(\.one\/*)*(\.trade\/*)*(\.dev\/*#*\/*)*(\.im\/*)*(\.fi\/*)*(\.games\/*)*(\.net\/*)*(\.app\/*)*", "", link)
            finalHoldings.append(link.capitalize())
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    mondayCapitalHoldings['Monday Capital'] = finalHoldings
 
    return mondayCapitalHoldings, cryptoCounter

def ideocolab(cryptoCounter):
    finalHoldings = []
    ideocolabHoldings = {}

    soup = getSoup('https://www.ideocolab.com/ventures/')
    hrefs = soup.find_all("a", class_="ventures__portfolio-item")
    for href in hrefs:
        link = str(href.get("href"))
        
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.exchange\/*#*\/*)*(\.com*\/*)*(\.pro\/*)*(\.xyz\/*)*(\.org\/*)*(\.network\/*)*(\.io\/*)*(\.finance\/*)*(\.one\/*)*(\.trade\/*)*(\.dev\/*#*\/*)*(\.im\/*)*(\.fi\/*)*(\.games\/*)*(\.net\/*)*(\.app\/*)*(\.us\/*)*", "", link)
        link = re.sub("(medium@)*(PBC)*", "", link)
        finalHoldings.append(link.capitalize())


    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    ideocolabHoldings['Ideoco Labs'] = finalHoldings

    return ideocolabHoldings, cryptoCounter

def mihVC(cryptoCounter):
    finalHoldings = []
    mihHoldings   = {}
    
    soup = getSoup("https://www.mih.vc/portfolio/")
    portfolio = soup.find("div", id="portfolio")
    holdings = portfolio.find_all('p')
    for holding in holdings:
        finalHoldings.append(holding.text)
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    mihHoldings['MIH VC'] = finalHoldings
    
    return mihHoldings, cryptoCounter

def elevenEleven(cryptoCounter):
    finalHoldings = []
    elevenElevenHoldings = {}
    banned = ['Partnering With The Best Entrepreneurial Minds', 'Portfolio', 'ABOUT THE STARTUPS WE INVEST IN', 'We invest in early stage technology startups run by the best entrepreneurial minds in the world.',
              'Why startups partner with us?', 'Our Investment Size and Stages Of Investment', 'Apply To Be One Of Our Startups', 'If you meet the above criteria, we would love to partner with you and work along with you to help you grow to the next level.',
              'OUR PORTFOLIO', 'We are proud of our entrepreneurs who are building great companies!', 'BLOCKCHAIN COMPANIES IN OUR PORTFOLIO', 'ADVANCED TECHNOLOGY STARTUPS IN OUR PORTFOLIO']


    soup = getSoup("http://11-11ventures.com/portfolio/")
    divs = soup.find_all('div', class_="dslc-text-module-content")
    for div in divs:
        desc = div.find("p")
        if desc:
            desc = str(desc.text)
            desc = re.sub("(is.*)*(was*)*(provides.*)*(founded.*)*", "", desc)
            if desc not in banned:
                finalHoldings.append(desc)
   
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    elevenElevenHoldings['11-11 Venutres'] = finalHoldings
    
    return elevenElevenHoldings, cryptoCounter

def coinfund(cryptoCounter):
    finalHoldings = []
    coinfundHoldings = {}

    soup = getSoup("https://www.coinfund.io/portfolio")
    divs = soup.find_all("div", class_="intrinsic")
    for div in divs:
        href = div.find("a")
        link = str(href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("(\.community\/*)*(\.exchange\/*#*\/*)*(\.com*\/*)*(\.pro\/*)*(\.xyz\/*)*(\.org\/*)*(\.network\/*)*(\.io\/*)*(\.finance\/*)*(\.one\/*)*(\.trade\/*)*(\.dev\/*#*\/*)*(\.im\/*)*(\.fi\/*)*(\.games\/*)*(\.net\/*)*(\.app\/*)*(\.info\/*)*(\.ai\/*)*", "", link)
        finalHoldings.append(link.capitalize())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    coinfundHoldings['Coin Fund'] = finalHoldings

    return coinfundHoldings, cryptoCounter

def unicorn(cryptoCounter):
    finalHoldings = []
    unicornHoldings = {}

    soup = getSoup("https://www.unicorn.vc/portfolio")
    hrefs = soup.find_all("a", class_="w-inline-block")
    for href in hrefs:
        link = str(href.get('href'))
        if not link.startswith("/"):
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            link = re.sub("(\.bank/*)*(\.exchange\/*#*\/*)*(\.com*\/*)*(\.pro\/*)*(\.xyz\/*)*(\.org\/*)*(\.network\/*)*(\.io\/*)*(\.finance\/*)*(\.one\/*)*(\.trade\/*)*(\.dev\/*#*\/*)*(\.im\/*)*(\.fi\/*)*(\.games\/*)*(\.net\/*)*(\.app\/*)*(\.info\/*)*(\.ai\/*)*(\.chat\/*)*", "", link)
            link = re.sub("http;//", "", link)
            finalHoldings.append(link.capitalize())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    unicornHoldings['Unicorn VC'] = finalHoldings

    return unicornHoldings, cryptoCounter

def longhash(cryptoCounter):
    finalHoldings = []
    longHashHoldings = {}
    banned = ['None','longhash.com/','mailchi.mp/longhash/sign-up-for-longhash-ventures-newsletter', 'twitter.com/longhashhatch', 'eventbrite.com/o/longhash-singapore-17480892639', "linkedin.com/company/longhashventures",
              'longhashventures.com/filecoin', 'forms.gle/kqGeAQ14t3LVnFKe9', 'access-sg.org/']
    
    soup = getSoup("https://www.longhashventures.com/")
    hrefs = soup.find_all("a")
    
    for href in hrefs:
        link = str(href.get("href"))
        
        if not link.startswith("/"):
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            
            if link not in banned:
                link = re.sub("(\.bank/*)*(\.exchange\/*#*\/*)*(\.com*\/*.*)*(\.pro\/*)*(\.xyz\/*)*(\.org\/*.*)*(\.network\/*)*(\.io\/*)*(\.finance\/*)*(\.one\/*)*(\.trade\/*)*(\.dev\/*#*\/*)*(\.im\/*)*(\.fi\/*)*(\.games\/*)*(\.net\/*)*(\.app\/*)*(\.info\/*)*(\.ai\/*)*(\.chat\/*)*(\.gov.*)*(\.vc.*)*(\.nus.*)*", "", link)
                finalHoldings.append(link.capitalize())
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    longHashHoldings['Long Hash'] = finalHoldings

    return longHashHoldings, cryptoCounter

def consensus(cryptoCounter):
    finalHoldings = []
    consensusHoldings = {}

    soup = getSoup("https://www.consensus-capital.com/#portfolio")
    holdings = soup.find_all("div", class_='text-block')
    
    for holding in holdings:
        finalHoldings.append(holding.text)
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    consensusHoldings['Consensus Capital'] = finalHoldings

    return consensusHoldings, cryptoCounter

def trgc(cryptoCounter):
    finalHoldings = []
    trgcHoldings  = {}
    banned        = ['TRGC', ""]

    soup = getSoup("https://trgc.io/")
    images = soup.find_all("img")
    
    for img in images:
        link = str(img.get("alt"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        if link not in banned:
            link = re.sub("(\.bank/*)*(\.exchange\/*#*\/*)*(\.com*\/*.*)*(\.pro\/*)*(\.xyz\/*)*(\.org\/*.*)*(\.network\/*)*(\.io\/*)*(\.finance\/*)*(\.one\/*)*(\.trade\/*)*(\.dev\/*#*\/*)*(\.im\/*)*(\.fi\/*)*(\.games\/*)*(\.net\/*)*(\.app\/*)*(\.info\/*)*(\.ai\/*)*(\.chat\/*)*(\.gov.*)*(\.vc.*)*(\.nus.*)*", "", link)
            finalHoldings.append(link.capitalize())
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    trgcHoldings['TRGC'] = finalHoldings

    return trgcHoldings, cryptoCounter

def brilliance(cryptoCounter):
    finalHoldings      = []
    brillianceHoldings = {}
    banned             = ['../svg/map.svg', '../svg/logo.svg', '../svg/hamburger.svg']

    soup = getSoup("https://brillianceventures.com/portfolio/portfolio.html")
    images = soup.find_all("img")
    for img in images:
        holding = str(img.get("src"))
        holding = re.sub("(img\/)*(-s)*(\.png)*(-m-01)*", "", holding)
        if holding not in banned:
            finalHoldings.append(holding.capitalize())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    brillianceHoldings['Brilliance Venutres'] = finalHoldings

    return brillianceHoldings, cryptoCounter

def blockGround(cryptoCounter):
    finalHoldings = []
    blockGroundHoldings = {}

    soup = getSoup('https://blockgroundcapital.com/portfolio/')
    hrefs = soup.find_all("a")
    for href in hrefs:
        link = str(href.get('href'))
        if not link.startswith("https://blockgroundcapital.com/"):
            link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
            link = re.sub("(\.bank/*)*(\.exchange\/*#*\/*)*(\.com*\/*.*)*(\.pro\/*)*(\.xyz\/*)*(\.org\/*.*)*(\.network\/*)*(\.io\/*)*(\.finance\/*)*(\.one\/*)*(\.trade\/*)*(\.dev\/*#*\/*)*(\.im\/*)*(\.fi\/*)*(\.games\/*)*(\.net\/*)*(\.app\/*)*(\.info\/*)*(\.ai\/*)*(\.chat\/*)*(\.gov.*)*(\.vc.*)*(\.nus.*)*", "", link)
            finalHoldings.append(link.capitalize())

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    blockGroundHoldings['Block Ground'] = finalHoldings

    return blockGroundHoldings, cryptoCounter

def moonchain(cryptoCounter):
    finalHoldings = []
    moonchainHoldings = {}

    soup = getSoup("https://moonchain.capital/")
    holdings = soup.find_all("div", class_="title")
    
    finalHoldings = [holding.text.strip() for holding in holdings]
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    moonchainHoldings['Moonchain'] = finalHoldings

    return moonchainHoldings, cryptoCounter

def woodstock(cryptoCounter):
    finalHoldings = []
    woodstockHoldings = {}

    soup = getSoup("https://woodstockfund.com/#portfolio")
    hrefs = soup.find_all('a', class_='portlink')
    
    for href in hrefs:
        link = str(href.get("href"))
        link = re.sub('^(?:https?:\/\/)?(?:www\.)?', '', link)
        link = re.sub("\..*", "", link)
        finalHoldings.append(link.capitalize())
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    woodstockHoldings['Woodstock Fund'] = finalHoldings

    return woodstockHoldings, cryptoCounter

def blockwall(cryptoCounter):
    finalHoldings = []
    blockwallHoldings = {}

    soup = getSoup("https://www.blockwall.capital/")
    holdings = soup.find_all('span', style="color:rgb(229, 243, 251)")
    
    for holding in holdings:
        finalHoldings.append(holding.text)
    finalHoldings.append("Dusk Network")
    
    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    blockwallHoldings['Blockwall'] = finalHoldings

    return blockwallHoldings, cryptoCounter

def bitfury(cryptoCounter):
    finalHoldings = []
    bitFuryHoldings = {}

    soup = getSoup("https://bitfury.com/bitfury-capital")
    holdings = soup.find_all("h2")
    finalHoldings = [holding.text.strip() for holding in holdings[1:]]

    cryptoCounter, finalHoldings = addToCryptoCounter(cryptoCounter, finalHoldings)
    bitFuryHoldings['Bit Fury'] = finalHoldings

    return bitFuryHoldings, cryptoCounter

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

    # gbicHoldings, cryptoCounter = gbic(cryptoCounter)
    # allHoldings.append(gbicHoldings)

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

    gumiCryptosHoldings, cryptoCounter = gumi(cryptoCounter)
    allHoldings.append(gumiCryptosHoldings)

    hardYakaHoldings, cryptoCounter = hardYaka(cryptoCounter)
    allHoldings.append(hardYakaHoldings)

    milestoneHoldings, cryptoCounter = milestone(cryptoCounter)
    allHoldings.append(milestoneHoldings)
    

    socialCapitalHoldings, cryptoCounter = socialCapital(cryptoCounter)
    allHoldings.append(socialCapitalHoldings)

    abstractVCHoldings, cryptoCounter = abstractVC(cryptoCounter)
    allHoldings.append(abstractVCHoldings)

    signalVCHoldings, cryptoCounter = signalVC(cryptoCounter)
    allHoldings.append(signalVCHoldings)

    notationVCHoldings, cryptoCounter = notation(cryptoCounter)
    allHoldings.append(notationVCHoldings)

    metaverseventuresHoldings, cryptoCounter = metaVerse(cryptoCounter)
    allHoldings.append(metaverseventuresHoldings)

    nirvanaCapitalHoldings, cryptoCounter = nirvanaCapital(cryptoCounter)
    allHoldings.append(nirvanaCapitalHoldings)

    binanceLabsHoldings, cryptoCounter = binanceLabs(cryptoCounter)
    allHoldings.append(binanceLabsHoldings)

    castleIslandHoldings, cryptoCounter = castleIsland(cryptoCounter)
    allHoldings.append(castleIslandHoldings)

    consensysLabsHoldings, cryptoCounter = consensys(cryptoCounter)
    allHoldings.append(consensysLabsHoldings)

    ecfHoldings, cryptoCounter = ecf(cryptoCounter)
    allHoldings.append(ecfHoldings)

    a16zHoldings, cryptoCounter = a16z(cryptoCounter)
    allHoldings.append(a16zHoldings)

    fabricVCHoldings, cryptoCounter = fabricVC(cryptoCounter)
    allHoldings.append(fabricVCHoldings)

    eightDCapitalHoldings, cryptoCounter = eightDCapital(cryptoCounter)
    allHoldings.append(eightDCapitalHoldings)

    blockchainffHoldings, cryptoCounter = blockchainff(cryptoCounter)
    allHoldings.append(blockchainffHoldings)

    chainfundHoldings, cryptoCounter = chainfund(cryptoCounter)
    allHoldings.append(chainfundHoldings)
    

    fundamentalHoldings, cryptoCounter = fundamentalLabs(cryptoCounter)
    allHoldings.append(fundamentalHoldings)

    idCapHoldings, cryptoCounter = idcap(cryptoCounter)
    allHoldings.append(idCapHoldings)

    craftVenturesHoldings, cryptoCounter = craftVentures(cryptoCounter)
    allHoldings.append(craftVenturesHoldings)

    unionHoldings, cryptoCounter = unionCapital(cryptoCounter)
    allHoldings.append(unionHoldings)

    sequoiaCapHoldings, cryptoCounter = sequoiaCap(cryptoCounter)
    allHoldings.append(sequoiaCapHoldings)

    gvHoldings, cryptoCounter = gv(cryptoCounter)
    allHoldings.append(gvHoldings)

    collaborativeFundHoldings, cryptoCounter = collaborativeFund(cryptoCounter)
    allHoldings.append(collaborativeFundHoldings)

    freesvcHoldings, cryptoCounter = freesvc(cryptoCounter)
    allHoldings.append(freesvcHoldings)

    generalCatalystHoldings, cryptoCounter = generalCatalyst(cryptoCounter)
    allHoldings.append(generalCatalystHoldings)

    preAngelHoldings, cryptoCounter = preAngel(cryptoCounter)
    allHoldings.append(preAngelHoldings)
    
    colliderHoldings, cryptoCounter = collider(cryptoCounter)
    allHoldings.append(colliderHoldings)

    colliderLabsHoldings, cryptoCounter = colliderLabs(cryptoCounter)
    allHoldings.append(colliderLabsHoldings)

    frameworkHoldings, cryptoCounter = framework(cryptoCounter)
    allHoldings.append(frameworkHoldings)

    mavenHoldings, cryptoCounter = maven(cryptoCounter)
    allHoldings.append(mavenHoldings)

    digistratsHoldings, cryptoCounter = digistrats(cryptoCounter)
    allHoldings.append(digistratsHoldings)

    sparkdigitalHoldings, cryptoCounter = sparkdigital(cryptoCounter)
    allHoldings.append(sparkdigitalHoldings)

    rarestoneHoldings, cryptoCounter = rarestone(cryptoCounter)
    allHoldings.append(rarestoneHoldings)

    bitscaleHoldings, cryptoCounter = bitscale(cryptoCounter)
    allHoldings.append(bitscaleHoldings)

    divVCHoldings, cryptoCounter = divVC(cryptoCounter)
    allHoldings.append(divVCHoldings)

    mondayCapitalHoldings, cryptoCounter = mondayCapital(cryptoCounter)
    allHoldings.append(mondayCapitalHoldings)

    ideocolabHoldings, cryptoCounter = ideocolab(cryptoCounter)
    allHoldings.append(ideocolabHoldings)

    mihVCHoldings, cryptoCounter = mihVC(cryptoCounter)
    allHoldings.append(mihVCHoldings)

    elevenElevenHoldings, cryptoCounter = elevenEleven(cryptoCounter)
    allHoldings.append(elevenElevenHoldings)

    coinfundHoldings, cryptoCounter = coinfund(cryptoCounter)
    allHoldings.append(coinfundHoldings)

    unicornHoldings, cryptoCounter = unicorn(cryptoCounter)
    allHoldings.append(unicornHoldings)

    longHashHoldings, cryptoCounter = longhash(cryptoCounter)
    allHoldings.append(longHashHoldings)

    consensusHoldings, cryptoCounter = consensus(cryptoCounter)
    allHoldings.append(consensusHoldings)

    trgcHoldings, cryptoCounter = trgc(cryptoCounter)
    allHoldings.append(trgcHoldings)

    brillianceHoldings, cryptoCounter = brilliance(cryptoCounter)
    allHoldings.append(brillianceHoldings)

    blockGroundHoldings, cryptoCounter = blockGround(cryptoCounter)
    allHoldings.append(blockGroundHoldings)

    moonchainHoldings, cryptoCounter = moonchain(cryptoCounter)
    allHoldings.append(moonchainHoldings)

    woodstockHoldings, cryptoCounter = woodstock(cryptoCounter)
    allHoldings.append(woodstockHoldings)

    blockwallHoldings, cryptoCounter = blockwall(cryptoCounter)
    allHoldings.append(blockwallHoldings)

    bitfuryHoldings, cryptoCounter = bitfury(cryptoCounter)
    allHoldings.append(bitfuryHoldings)

    os.chdir(r"C:\Users\Chip\Documents\upWorkProjects\justinScraping")
    with open ('dump.txt', 'w') as f:
        f.write(json.dumps(allHoldings))

    keys = []
    for i,j in enumerate (allHoldings):
        keys.append((j.keys()))
    convertToExcel(cryptoCounter, allHoldings, keys)

def convertToExcel(cryptoCounter, allHoldings, keys):
    print("Converting to excel!")
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
    print("DONE!")
    
main()