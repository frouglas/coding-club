'''
Created on Jun 20, 2015

@author: frouglas
'''

class game():
    def __init__(self):
        self.homeTm = ""
        self.awayTm = ""

def parseSeason(thisFile):
    thisLine = thisFile.readline()
    gameString = ""
    while thisLine != "":
        if (thisLine[0:2] == "id") & (gameString != ""):
                parseGame(gameString)
            gameString = gameString + thisLine
            thisLine = thisFile.readline()
        
            
            
            
            