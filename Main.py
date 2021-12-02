import pandas as pd
import requests
from bs4 import BeautifulSoup
from os.path import exists

class Menu:
    def __init__(self, name):
        self.name = name

    def Selections(self):

        menuChoices = {0:"Exit", 1:"Change source .csv file", 2:"Check current source file", 3: "Search for city/town",
                       4: "Run program(default)"}
        for key, value in menuChoices.items():
            print(str(key) + ". " + value)
        run = True
        while run == True:
            try:
                userChoice = int(input("Please type the corresponding number for the option you want: "))
                break
            except ValueError:
                print("Error: Improper data type, please type a digit answer from 0 to " + str(max(menuChoices.keys())))
        if userChoice not in menuChoices.keys():
            while userChoice not in menuChoices.keys():
                print("Error: Choice does not exist, please type an answer from 0 to " + str(max(menuChoices.keys())))
                userChoice = int(input("Please type the corresponding number for the option you want: "))
        else:
            run == False
            return userChoice

    def fileChange(self):
        userFile = input("Please type the exact name of your .csv file: ")
        if exists(userFile) == False:
            while exists(userFile) == False:
                print("Error: File not found, please check your IDONTYET\Lib folder and try again.")
                userFile = input("Please type the exact name of your .csv file: ")

        if exists(userFile) == True:
            if userFile.endswith(".csv") == False:
                while userFile.endswith(".csv") == False:
                    print("Error: File not correct file format, please try another file.")
                    userFile = input("Please type the exact name of your .csv file: ")
        return userFile

    def checkCurrentFile(self, currentSourceFile):
        print("Current .csv file in use: " + currentSourceFile)

    def quit(self):
        quit()

class Population_Program:
    def __init__(self, name):
        self.name = name

    def townFind(self, listofTownsDF, pos = 0, setting = 1, userTown = ""):
        dataPresent = True
        town = ""
        if setting == 0:
            town = userTown
        else:
            town = listofTownsDF.iloc[pos]['Town']
        url = "https://en.wikipedia.org/wiki/" + town + ",_North_Carolina"
        print(url)
        urlrequest = requests.get(url)
        soup = BeautifulSoup(urlrequest.content, "html.parser")
        all_tables = soup.findAll(class_="toccolours")
        if all_tables:
            dataPresent = True
        else:
            dataPresent = False
        return all_tables, town, dataPresent

    def findData(self, all_tables):
        cells_data = []
        census_data = []
        for row in all_tables:
            body = row.findAll("tbody")
            for cells in body:
                cell = cells.findAll("td")
                cells_data.append(cell)
        census_data = cells_data[0]
        return census_data

    def organizeData(self, census_data):
        year = []
        pops = []
        percents = []
        listofDicts = []
        count = 1
        for x in census_data:
            if count == 1:
                year.append(x.string)
                count += 1
            elif count == 2:
                pops.append(x.string)
                count += 1
            elif count == 3:
                count += 1
            elif count == 4:
                percents.append(x.string)
                count = 1
        return year, pops, percents

    def createFinalDataFrame(self, year, pops, percents):
        listOfDicts = []
        count = 0
        while count < len(pops):
            listOfDicts.append({"Year": year[count], "Population": pops[count], "% Change": percents[count]})
            count += 1
        CensusDF = pd.DataFrame(listOfDicts)
        return CensusDF

currentSourceFile = 'listOfTownsinNC(edited).csv'

Menu = Menu("Menu")
Population_Program = Population_Program("Pop_Program")

userChoice = 0
while userChoice <= 5:
    userChoice = Menu.Selections()

    if userChoice == 0:
        Menu.quit()

    if userChoice == 1:
        currentSourceFile = Menu.fileChange()

    if userChoice == 2:
        Menu.checkCurrentFile(currentSourceFile)

    if userChoice == 3:
        listofTownsDF = pd.read_csv(currentSourceFile)
        userInput = input("Town: ")
        all_tables, town, data_present = Population_Program.townFind(listofTownsDF, setting=0, userTown=userInput)
        data = Population_Program.findData(all_tables)
        year, pops, percents = Population_Program.organizeData(data)
        DF = Population_Program.createFinalDataFrame(year, pops, percents)
        print(DF)

    if userChoice == 4:
        listofTownsDF = pd.read_csv(currentSourceFile)
        count = 0
        while count < len(listofTownsDF):
            all_tables, town, dataPresent = Population_Program.townFind(listofTownsDF, count, setting = 1)
            if dataPresent == False:
                count += 1
                print("Population data unavailable")
                continue
            census_data = Population_Program.findData(all_tables)
            year, pops, percents = Population_Program.organizeData(census_data)
            CensusDF = Population_Program.createFinalDataFrame(year, pops, percents)
            count += 1
            print(town)
            print(CensusDF)





