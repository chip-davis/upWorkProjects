from tqdm import tqdm
import pdfplumber
import json


def parse(filepath, outdic = True):
    dic = {}
    csv = []

    with pdfplumber.open(filepath) as pdf:
        pages = pdf.pages ## loads all of the pages of the PDF

        try:
            with tqdm(total=len(pages)) as pbar: ## creates the progress bar 
                for pageNum, page in enumerate(pages, start=1):
                    
                    
                    page = pages[pageNum]
                    page = page.crop((0, 0.08 * float(page.height), page.width, page.height)) ## crops the page so that it gets rid of headers
                    page = page.extract_text(x_tolerance=3, y_tolerance=3).split("\n")

                    page = [word.replace('"', '').replace('!', "").replace(',', '').replace("?", "").replace(":", "").replace("''", "") for word in page] ## extracts the text from the whole page then splits it into
                                                                                                                                        ## each line and removes some puncuation
                    for lineNum, line in enumerate(page, start=1):

                        words = line.split() 

                        for wordNum, word in enumerate(words, start=1): ## separates every individual word / line
                            if word.endswith("."): word = word.replace(".", "") ## gets rid of periods
                            if "-" in word:
                                checkValue = checkHypon(word)
                                if checkValue == True:
                                    pass
                                else:
                                    word = word.split("-")
                                    csv.append(f"{pageNum}, {lineNum}, {wordNum}, {word[0]}")
                                    wordNum = wordNum + 1
                                    csv.append(f"{pageNum}, {lineNum}, {wordNum}, {word[1]}")
                            if word: csv.append(f"{pageNum}, {lineNum}, {wordNum}, {word}")
                            
                            
                    pbar.update(1)
                        
        except Exception as ex:
            print(ex)
        return dic if outdic == True else csv
    
def checkHypon(word):
    try:
        check = word[word.find("-") + 1]
        return False
    except IndexError:
        return True
    


def saveDic(dic):
    with open('dump.json', 'w') as f:
        json.dump(dic, f, indent=5)

def saveCSV(csv):
    with open("csv.txt", 'w') as f:
        for line in csv:
            f.write(line + "\n")

def main():
    filepath = r"C:\Users\Chip\Documents\upWorkProjects\PDFcounter\PDFs\therewerenone.pdf"
    #filepath  = r'C:\Users\Chip\Documents\upWorkProjects\PDFcounter\PDFs\andThenThereWereNoneReg.pdf'
    CSV   = parse(filepath, outdic=False)
    saveCSV(CSV)

main()