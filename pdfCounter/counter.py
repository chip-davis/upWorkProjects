from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
import time
import tempfile
import re
import glob
import fnmatch
import pandas as pd

def createImages(pdfPath):
    print("loading pages...")
    # Store all the pages of the PDF in a variable
    with tempfile.TemporaryDirectory() as path:
        pages = convert_from_path(pdfPath, 350, output_folder=path, fmt="JPEG", thread_count=2, first_page=1, last_page=5)
    
    # Counter to store images of each page of PDF to image
    image_counter = 1
    
    # Iterate through all the pages stored above
    for page in pages:
        
        filename = f"page_{str(image_counter)}.jpg"
        
        # Save the image of the page in system
        page.save(r'/home/chipdavis/Documents/personalProjects/PDFProj/pages/' + filename, 'JPEG')
    
        # Increment the counter to update filename
        image_counter += 1
        print(f"saving {image_counter}")
    return image_counter

def ocrTextAdjustment(imagePath, image_counter):
    # Variable to get count of total number of pages
    filelimit = image_counter-1
    
    # Creating a text file to write the output
    
    outfile = f"out_text.txt"
    
    f = open(outfile, "a")

    # Iterate from 1 to total number of pages
    for i in range(1, filelimit + 1):
        
        
        filename = f"{imagePath}/page_{str(i)}.jpg"

        print(f"doing {filename}")

        # Recognize the text as string in image using pytesserct
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        
        result = re.sub("(?i)([a-z]+)-\n([a-z]+)", r'\1\2\n', text)
        result = re.sub("(\.*)", "", result)
        result = result.replace("—", " ")
        result = result.replace("-", " ")
        result = re.sub(r'[^\w\s]', '', result)
        # Finally, write the processed text to the file.
        f.write(result)
        f.write("\n=====================\n")
    
        # Close the file after writing all the text.
    f.close()

def processOutText():
    pages = {} # dictionary to store page number and a list containing the page contents
    contents = [] # every line of the page that will get added to the dictionary
    pageNum = 1 # start page off at 1


    with open ('out_text.txt', 'r') as f:
        for line in f:
            if line == "\n": #ignore empty blank lines
                continue
            if "=====" in line: #how we know when a page stops
                pages[pageNum] = contents # add to dictionary for saving
                pageNum += 1
                contents = [] # wipes for next page
                continue            
            contents.append(line) # addes line to list to get added to dictionary
    return pages

def byWord():

    pages = processOutText() # addes line to list to get added to dictionary
    CSV   = []

    for key, value in pages.items():
        lines = [content.strip() for content in value if content.strip() != ""]
        lineNum = 1
        for line in lines:
            words = line.split()
            for wordNum, word in enumerate(words):
                CSV.append(f"{str(key)}, {lineNum}, {wordNum+1}, {word}")
            lineNum+= 1

    return CSV
    
def byLine():
    #returns a CSV with page number and line number and a string of words for every word
    #in the line seperated by commas

    pages = processOutText() 
    CSV   = []

    for key, value in pages.items():
        lines = [content.strip() for content in value if content.strip() != ""]
        lineNum = 1
        for line in lines:
            line = line.split()
            words = ', '
            words = words.join(line) 
            CSV.append(f'{str(key)}, {str(lineNum)}, "{words}"')
            lineNum += 1
    return CSV

def byPage():
    pages, CSV = processOutText()
    allWordsOnPage = ', '
    for key, value in pages.items():
        lines = [content.strip() for content in value if content.strip() != ""]
        allWordsOnPage = allWordsOnPage.join(lines)
        CSV.append(f'{str(key)}, "{allWordsOnPage}"')
    return CSV

def saveCSV(CSV):
    with open("csv.txt", 'w') as f:
        for line in CSV:
            f.write(line + "\n")

def saveDicByWord():
    csv_file = pd.DataFrame(pd.read_csv("csv.txt", sep = ",", names=["page", "line", "wordnum", "word"], index_col = False, skipinitialspace=True))
    csv_file.to_json("dataByWord.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None, indent=4)

def saveDicByLine():
    csv_file = pd.DataFrame(pd.read_csv("csv.txt", sep = ",", names=["page", "linenum", "line"], index_col = False, skipinitialspace=True))
    csv_file.to_json("dataByLine.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None, indent=4)

def saveDicByPage():
    csv_file = pd.DataFrame(pd.read_csv("csv.txt", sep = ",", names=["page", "words"], index_col = False, skipinitialspace=True))
    csv_file.to_json("dataByPage.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None, indent=4)

def main():
    PDF_file = r"/home/chipdavis/Documents/personalProjects/PDFProj/PDFS/andThenThereWereNoneFROCR.pdf"
    imagesPath = r"/home/chipdavis/Documents/personalProjects/PDFProj/pages"
    
    # image_counter = createImages(PDF_file)
    # ocrTextAdjustment(imagesPath, image_counter)
    
    CSV = byWord()
    saveCSV(CSV)
    saveDicByWord()

    # CSV = byPage()
    # saveCSV(CSV)
    # saveDicByPage()
    
    


main()