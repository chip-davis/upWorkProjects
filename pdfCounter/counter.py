from tqdm import tqdm
import pdfplumber
import json
import csv
import pandas as pd

def byWord(filepath):
    csv = []

    with pdfplumber.open(filepath) as pdf:
        pages = pdf.pages ## loads all of the pages of the PDF
        wordNum = 1
        hyponatedWord = ''
        try:
            with tqdm(total=len(pages)) as pbar: ## creates the progress bar 
                for pageNum, page in enumerate(pages):
                    
                    
                    page = pages[pageNum]
                    page = page.crop((0, 0.08 * float(page.height), page.width, page.height)).extract_text(x_tolerance=3, y_tolerance=3).split("\n") ## crops the page so that it gets rid of headers

                    page = [word.replace('"', '').replace('!', "").replace(',', '').replace("?", "").replace(":", "").replace("''", "").strip() for word in page] ## extracts the text from the whole page then splits it into
                                                                                                                                        ## each line and removes some puncuation
                    for lineNum, line in enumerate(page, start = 1):

                        words = line.split() 
                        
                        for word in  words: ## separates every individual word / line
                            if word.endswith("."): word = word.replace(".", "") ## gets rid of periods

                            if hyponatedWord:
                                word = hyponatedWord.replace("-", "") + word
                                hyponatedWord = ''

                            if "-" in word:
                                checkValue = checkHypon(word)
                                if checkValue == True:
                                    hyponatedWord = word
                                    continue
                
                                word = word.split("-")
                                csv.append(f"{str(pageNum + 1)}, {lineNum}, {wordNum}, {word[0]}")
                                wordNum = wordNum + 1
                                csv.append(f"{str(pageNum + 1)}, {lineNum}, {wordNum}, {word[1]}")
                                wordNum += 1
                                continue
                            if word: csv.append(f"{str(pageNum + 1)}, {lineNum}, {wordNum}, {word}")
                            wordNum += 1
                        wordNum = 1
                    pbar.update(1)
                        
        except Exception as ex:
            print(ex)
        return csv

def byLine(filepath):
    csv = []
    listOfWords = []
    with pdfplumber.open(filepath) as pdf:
        pages = pdf.pages ## loads all of the pages of the PDF
        wordNum = 1
        hyponatedWord = ''
        try:
            with tqdm(total=len(pages)) as pbar: ## creates the progress bar 
                for pageNum, page in enumerate(pages):
                    page = pages[pageNum]
                    page = page.crop((0, 0.08 * float(page.height), page.width, page.height)).extract_text(x_tolerance=3, y_tolerance=3).split("\n") ## crops the page so that it gets rid of headers

                    page = [word.replace('"', '').replace('!', "").replace(',', '').replace("?", "").replace(":", "").replace("''", "").strip() for word in page] ## extracts the text from the whole page then splits it into
                                                                                                                                        ## each line and removes some puncuation
                    for lineNum, line in enumerate(page, start = 1):

                        words = line.split() 
                        
                        for word in  words: ## separates every individual word / line
                            if word.endswith("."): word = word.replace(".", "") ## gets rid of periods

                            if hyponatedWord:
                                word = hyponatedWord.replace("-", "") + word
                                hyponatedWord = ''

                            if "-" in word:
                                checkValue = checkHypon(word)
                                if checkValue == True:
                                    hyponatedWord = word
                                    continue
                
                                word = word.split("-")
                                listOfWords.append(word[0])
                                listOfWords.append(word[1])
                                continue

                            if word: 
                                listOfWords.append(word)
                        # converts the list of individual words back into a single string seperated by commas
                        stringOfWords = ", "
                        stringOfWords = stringOfWords.join(listOfWords)
                        listOfWords = []

                        csv.append(f'{str(pageNum + 1)}, {lineNum}, "{stringOfWords}"')
                    
                    pbar.update(1)
                        
        except Exception as ex:
            print(ex)
        return csv

def byPage(filepath):
    csv = []
    allWordsOnPage = ', '
    with pdfplumber.open(filepath) as pdf:
        pages = pdf.pages ## loads all of the pages of the PDF
        wordNum = 1
        try:
            with tqdm(total=len(pages)) as pbar: ## creates the progress bar 
                for pageNum, page in enumerate(pages):
                    page = pages[pageNum]
                    page = page.crop((0, 0.08 * float(page.height), page.width, page.height)).extract_text(x_tolerance=3, y_tolerance=3).split("\n") ## crops the page so that it gets rid of headers

                    page = [word.replace('"', '').replace('!', "").replace(',', '').replace("?", "").replace(":", "").replace("''", "").strip() for word in page] ## extracts the text from the whole page then splits it into
                                                                                                                                        ## each line and removes some puncuation
                    allWordsOnPage = allWordsOnPage.join(page)

                    csv.append(f'{str(pageNum + 1)}, "{allWordsOnPage}"')
                    
                    allWordsOnPage = ', '

                    pbar.update(1)
                        
        except Exception as ex:
            print(ex)
        return csv

def checkHypon(word):
    #returns false if its just an instance like "and then--there were none"
    #returns true  if its a hypen connecting a word to the next line
    try:
        check = word[word.find("-") + 1]
        return False
    except IndexError:
        return True
    
def saveDicByWord():
    
    csv_file = pd.DataFrame(pd.read_csv("csv.txt", sep = ",", names=["page", "line", "wordnum", "word"], index_col = False, skipinitialspace=True))
    csv_file.to_json("dataByWord.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None, indent=4)

def saveDicByLine():
    csv_file = pd.DataFrame(pd.read_csv("csv.txt", sep = ",", names=["page", "linenum", "line"], index_col = False, skipinitialspace=True))
    csv_file.to_json("dataByLine.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None, indent=4)

def saveDicByPage():
    csv_file = pd.DataFrame(pd.read_csv("csv.txt", sep = ",", names=["page", "words"], index_col = False, skipinitialspace=True))
    csv_file.to_json("dataByPage.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None, indent=4)

def saveCSV(data):
    with open("csv.txt", 'w') as f:
        for line in data:
            f.write(line + "\n")
            

def main():
    filepath = str(input("Please enter the filepath of the pdf: "))
    option   = int(input("Please enter a '1' for byWord, a '2' for byLine, or a '3' for byPage: "))
    
    if option == 1:
        CSV = byWord(filepath)
        saveCSV(CSV)
        saveDicByWord()
        return
    if option == 2:
        CSV = byLine(filepath)
        saveCSV(CSV)
        saveDicByLine()
        return
    if option == 3:
        CSV = byPage(filepath)
        saveCSV(CSV)
        saveDicByPage()
        return
    else:
        print("You inputted an incorect option. Exiting")
        return
    
main()