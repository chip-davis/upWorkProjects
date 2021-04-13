'''
Author: Diego Arenas
Date: 11/29/2020
Purpose: Script will edit class/index id from .txt file that is for YOLO dataset
'''

#Link below for more info about YOLO Framwork
#Head to Data Collection and Annotation paragraph to understand annotation file
#https://medium.com/analytics-vidhya/everything-you-need-to-know-to-train-your-custom-object-detector-model-using-yolov3-1bf0640b0905

import glob
import os
import sys
from tqdm import tqdm # imports progress bar

classTotal = 0
fileExt = '.txt'
imageFiles= []
ALLOWED_EXTENSIONS = ('.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG')

print("""
+------------------------------------------------------------------------------+
|     __   __ ___   _      ___     ____  _                    ___  ____        |
|     \ \ / // _ \ | |    / _ \   / ___|| |  __ _  ___  ___  |_ _||  _ \       |
|      \ V /| | | || |   | | | | | |    | | / _` |/ __|/ __|  | | | | | |      |
|       | | | |_| || |___| |_| | | |___ | || (_| |\__ \__  \  | | | |_| |      |
|       |_|  \___/ |_____|\___/   \____||_| \__,_||___/|___/ |___||____/       |
|                          _____     _  _  _                                   |
|                         | ____| __| |(_)| |_  ___   _ __                     |
|                         |  _|  / _` || || __|/ _ \ | '__|                    |
|                         | |___| (_| || || |_| (_) || |                       |
|                         |_____|\__,_||_| \__|\___/ |_|                       |
+------------------------------------------------------------------------------+
""")

#print("Total .txt files in ",DirPath, ": {}\n".format(fileCounter))
print("""+------------------------------------------------------------------------------+
|                          YOLO Command Line Interface                         |  
+------------------------------------------------------------------------------+""")

DirPath =input("Enter text files directory: ") # User inputs directory to work on
print("+------------------------------------------------------------------------------+")
print("[Processing] changing directory...")
print("+------------------------------------------------------------------------------+")
os.chdir(DirPath)  # Changes directory that user specified
print ("Current working on directory: %s" % os.getcwd()) # Outputs Current directory
print("+------------------------------------------------------------------------------+")

classesFile = ("classes.txt")# defining classes.txt file. Stores labels of object detector
classes = open(classesFile)# Opens up classses.txt file
line = classes.read()# Reads data from classes.txt as string
classData = line.split("\n")
ids = len(classData)
classes.close()# closes classes.txt file

textFiles = [f for f in os.listdir(DirPath) if f.endswith('.txt')] #opens all files the end with .txt
textFiles.pop(textFiles.index("classes.txt"))

for f in tqdm(textFiles, desc= "Retriving Files",ncols=80):
    with open(f,"r") as fileobj: #opens textFiles
        for data in fileobj: 
            imageFiles.append(f)
            #print(f,"/ " +data) # prints all the .txt files and data

#counts total number of txt files
fileCounter = 0
for cnt in os.listdir(DirPath):
    if cnt.endswith('.txt'):
        fileCounter +=1

print("""+------------------------------------------------------------------------------+
|                          YOLO Command Line Interface                         |  
+------------------------------------------------------------------------------+
+--------------------------------OUTPUT----------------------------------------+""")
print("+------------------------------------------------------------------------------+")
#counts total number of txt files
fileCounter = 0
for cnt in os.listdir(DirPath):
    if cnt.endswith('.txt'):
        fileCounter +=1

#counts total number of line in classes.txt
for i in classData:
    if i:
        classTotal +=1
print("Total classes in dataset:",classTotal, "[Remeber python start to count from 0]")

for i in range(ids):
    print(i,end=" ",)
    #print(i,classData[i], end=' ')
print()
print("+------------------------------------------------------------------------------+")
print("Total # of .txt files",fileCounter)
print("+------------------------------------------------------------------------------+")

NewFolder= input("Enter name of new folder:") # User inputs new folder name
NewDirFolder = os.mkdir(NewFolder) # Creates new folder
print(NewFolder,"folder was created successfully.")# Prints successful message

#newClassID = str(input("Enter new Class ID:")) #user inputs the new number that will replace the old class ID

textFiles.append("classes.txt")

dictOfNumbers = {} #empty dictionary to store the numbers we have already replaced

###STARTING HERE WAS WRITTEN BY ME###
#loop through all the numbers 0->n so we can add them to the dictionary to replace.
for classIDNumber, _ in enumerate(classData): 
    newClassIDNumber = str(input(f"Enter number to replace {classIDNumber}: "))
    dictOfNumbers[str(classIDNumber)] = newClassIDNumber

for f in textFiles:
    with open(f,"r") as fileobj: #opens textFiles
            with open(os.path.join(NewFolder,f), "x") as newfileobj:
                    lines = fileobj.readlines()
                    for line in lines:
                        if (f != "classes.txt"):
                            oldLine = line.split() #turns the line into a list separated by white spaces to fix the case where the first number was a double digit
                            oldClassId = oldLine[0] #grabs the old value so we can replace it
                            new_lines  = dictOfNumbers.get(oldClassId) + " " + ' '.join(map(str, oldLine[1:])) + "\n" #writes the new value
                            newfileobj.writelines(new_lines)
### NO LONGER WRITTEN BY ME ###                  
                            
                    

textFiles.pop(textFiles.index("classes.txt"))# Skips Classes.txt file so i wont edit new value

for f in tqdm(textFiles,desc="Editing Files",ncols=80):
    with open(os.path.join(NewFolder,f),"r") as fileobj: #opens textFiles
        for data in fileobj: 
            imageFiles.append(f)
            #print(f,"/ " +data) # prints all the .txt files and data

print("""+-------------------------------********---------------------------------------+
+-------------------------------*UPDATE*---------------------------------------+
+-------------------------------********---------------------------------------+""")
print("+------------------------------------------------------------------------------+")

#inline print of new ID replacements
#print("New Class ID(s) are:", dictOfNumbers)

#prettier print of classID replacements
print("+----------------------------NEW CLASS IDS----------------------------------+")
for oldID, newID in dictOfNumbers.items():
    print(f"{oldID} ----> {newID}")

print("+------------------------------------------------------------------------------+")
print("Total # of .txt files",fileCounter)
print("""+------------------------------------------------------------------------------+
+------------------------------------------------------------------------------+
|                               TASK COMPLETE                                  |  
+------------------------------------------------------------------------------+""")