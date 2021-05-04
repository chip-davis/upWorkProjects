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
from dearpygui.core import *
from dearpygui.simple import *


def createImages(pdfPath, tempPath, imagesPath):
    log_info("loading pages...")
    # Store all the pages of the PDF in a variable
    path = tempPath
        
    pages = convert_from_path(pdfPath, 350, output_folder=os.path.normpath(path), fmt="JPEG", thread_count=2, first_page=1, last_page=5, poppler_path=r"C:\Users\Chip\Poppler\poppler-0.68.0\bin")
    
    # Counter to store images of each page of PDF to image
    image_counter = 1
    
    # Iterate through all the pages stored above
    for page in pages:
        
        pageFolder = imagesPath

        filename = f"page_{str(image_counter)}.jpg"
        
        # Save the image of the page in system
        page.save(f"{pageFolder}\\{filename}", 'JPEG')
    
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

        log_info(f"doing {filename}")

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
    with open("csv.txt", 'w', encoding='utf-8') as f:
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

def generatePages():
    PDF_file = get_value("file_path")
    imagesPath = get_value("pages")
    tempPath = get_value("directory")

    image_counter = createImages(PDF_file, tempPath, imagesPath)
    ocrTextAdjustment(imagesPath, image_counter)

def generateJson():  
    CSV = byWord()
    saveCSV(CSV)
    saveDicByWord()

    # CSV = byPage()
    # saveCSV(CSV)
    # saveDicByPage()
    
    
def theme_callback(sender, data):
    set_theme(sender)

def file_picker(sender, data):
    open_file_dialog(callback=apply_selected_file, extensions=".pdf,.*")

def directory_picker(sender, data):
    select_directory_dialog(callback=apply_selected_directory)

def page_directory_picker(sender, data):
    select_directory_dialog(callback=apply_selected_page_directory)

def apply_selected_file(sender, data):
    log_debug(data)
    directory = data[0]
    file = data[1]
    
    set_value("file", file)
    set_value("file_path", f"{directory}\\{file}")

def apply_selected_directory(sender, data):
    directory = data[0]
    folder = data[1]
    set_value("directory", f"{directory}\\{folder}")

def apply_selected_page_directory(sender, data):
    directory = data[0]
    folder = data[1]
    set_value("pages", f"{directory}\\{folder}")

show_logger()

with window("Main Window"):
    
    add_button("PDF Selector", callback=file_picker) 
    add_spacing(count=3)

    add_button("Temp folder selector", callback=directory_picker)
    add_spacing(count=3)

    add_button("Page directory picker", callback=page_directory_picker)
    add_spacing(count=3)
    
    add_text("File: ")
    add_same_line()
    add_label_text("##file", source="file", color=[255, 0, 0])
    
    add_text("File Path: ")
    add_same_line()
    add_label_text("##filepath", source="file_path", color=[255, 0, 0])
    
    add_text("Temp Directory: ")
    add_same_line()
    add_label_text("##filedir", source="directory", color=[255, 0, 0])


    add_text("Page Directory: ")
    add_same_line()
    add_label_text("##pagedir", source="pages", color=[255, 0, 0])

    add_spacing(count=10)
    add_button("Generate Text File", callback=generatePages)

    
    add_spacing(count=10)
    add_combo("Combo##widget", items=["By word", "By line", "By page"])
    add_spacing(count=5)
    add_button("Generate JSON", callback = generateJson)





    add_menu_bar("MenuBar")
    add_menu("Themes")
    add_menu_item("Dark", callback=theme_callback)
    add_menu_item("Light", callback=theme_callback)
    add_menu_item("Classic", callback=theme_callback)
    add_menu_item("Dark 2", callback=theme_callback)
    add_menu_item("Grey", callback=theme_callback)
    add_menu_item("Dark Grey", callback=theme_callback)
    add_menu_item("Cherry", callback=theme_callback)
    add_menu_item("Purple", callback=theme_callback)
    add_menu_item("Gold", callback=theme_callback)
    add_menu_item("Red", callback=theme_callback)
    end()

    add_menu("Tools")
    add_menu_item("Show Logger", callback=show_logger)
    end()




start_dearpygui(primary_window="Main Window")
