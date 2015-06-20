fuckThis = 0

import urllib.request, urllib.error
import pickle
import os.path
import math
from datetime import *
from parseClasses import *

if sys == "Windows":
    leadSlug = "H:/gDrive"
else:
    leadSlug = "/Users/frouglas/Google Drive"
    
blockquoted = 0
isTweet = 0
redirects = {}
deads = []
manualRecode = {}

logFile = datetime.today().strftime("%m%d_%H%M")
logFile = leadSlug + "/penn/dishness/dishParse/runLogs/" + logFile + ".txt"
log = open(logFile, 'w')

output = "initializing..."
print(output)
log.write(output + "\n")

# defaults to the range containing the first month of the archive and the last full month

posts = {}
dateRange = rangeSet()

startMonth = dateRange[0][0:2]
startYear = dateRange[0][2:4]

endMonth = dateRange[1][0:2]
endYear = dateRange[1][2:4]

output = "Parsing from " + startMonth + startYear + " to " + endMonth + endYear
print(output)
log.write(output + "\n")
i = 1
runID = 0
monthID = 1
contBool = 1
archiveID = 1
activeMonth = startMonth
activeYear = startYear
yearParse = 0
monthPosts = 9999
totalParsed = 0
totalPosts = 0
prevTime = datetime.now()
noTitle = 1

# controls when the run stops
runBool = 1
linkIndices = leadFile + "/penn/dishness/dishParse/tools/linkIndices.index"
        

if os.path.exists(linkIndices):
    f = open(linkIndices, 'rb')
    linkIndex = pickle.load(f)
    redirects = linkIndex[0]
    deads = linkIndex[1]
    manualRecode = linkIndex[2]

while runBool == 1:
    newURL = "http://dish.andrewsullivan.com/20" + activeYear + "/" + activeMonth + "/page/" + str(i) + "/"  
    runID += 1
    try:
#        output = "trying URL " + newURL + " ..."
#        print(output)
#        log.write(output + "\n")
        f = urllib.request.urlopen(newURL)
        refF = f  
        readError = 0
    except urllib.error.URLError:
        output = "Unable to load URL " + newURL
        print(output)
        log.write(output + "\n")
        break
    yearParse += 1
    breakLoop = 0
    while(breakLoop == 0):
        line = str(f.readline())
        headerStart = int(line.find("class=\"title-wrap"))
        menu = int(line.find("archive-dropdown"))
        htmlTag = int(line.find("</html>"))
        if headerStart != -1:
            store = 1
            line = str(f.readline())
            if int(line.find("class=\"post-title")) != -1:
                noTitle = 0
            line = str(f.readline())
            headerStart = int(line.find(">"))+1
            x = post()
            x.id = activeMonth + activeYear + "." + str(monthID)
#            if monthID == 155:
#                booyah = 1
#            output = "        Parsing post " + str(monthID) + "..."
#            print(output)
#            log.write(output + "\n")
            headerEnd = int(line.find("</a",headerStart))
            titleStr = line[headerStart:headerEnd]
            lowerCTD = titleStr.find(" ctd")
            upperCTD = titleStr.find(" Ctd")
            linkStart = line.find("href=")+6
            linkEnd = line.find("\"",linkStart)
            if ((lowerCTD != -1) | (upperCTD!=-1)):
                x.ctd = 1
                locCTD = max(lowerCTD,upperCTD)
                if titleStr[locCTD-1] == ",":
                    locCTD -= 1
                titleStr = titleStr[0:locCTD]
            urlVal = line[linkStart:linkEnd]
            x.url = urlVal
            if noTitle == 0:
                x.title = titleStr
                currLine = str(f.readline())
            else:
                x.title = "UNTITLED"
                currLine = line
            while(currLine.find(".post-m") == -1):
                if currLine.find("class=\"the-time") != -1:
                    dateLoc = currLine.find("the-time")+18
                    dateEnd = currLine.find("<",dateLoc)
                    currLine = currLine[dateLoc:dateEnd]
                    fullTime = datetime.strptime(currLine, "%b %d %Y @ %I:%M%p")
                    fullTime = fullTime.replace(tzinfo=EST())
                    x.timeStamp = fullTime
                elif currLine.find("\"entry-con") != -1:
                    currLine = str(f.readline())
                    while currLine.find("/.entry") == -1:
                        if store == 0:
                            break
                        parseMedia(currLine, x)
                        currLine = str(f.readline())
                if store == 0:
                    break
                currLine = str(f.readline())
            while x.timeStamp in posts:
                x.timeStamp = x.timeStamp+timedelta(seconds=1)
            posts[x.timeStamp] = x
            noTitle = 1
            monthID += 1
            if ((monthID != 1) & (monthID % 25 == 1) & (runID != 1)) | (monthID - 1 == monthPosts):
                breakLoop = 1
        elif ((runID == 1) & (menu != -1)):
            menuCt = 1
            while (menuCt != -1):
                menuRef = int(line.find("andrewsullivan.com/20"))
                while menuRef == -1:
                    line = str(f.readline())
                    menuRef = int(line.find("andrewsullivan.com/20"))
                keyYear = line[menuRef + 21:menuRef + 23]
                keyMonth = line[menuRef + 24:menuRef + 26]
                menuRef = line.find("(")
                menuRefEnd = line.find(")")
                keyVal = int(line[menuRef+1:menuRefEnd])
                keyRef = keyMonth + keyYear
                if (menuCt == 1):
                    archList = {keyRef:keyVal}
                else:
                    archList[keyRef] = keyVal
                if (keyYear == "01") & (keyMonth == "01"):
                    menuCt = -1
                else:
                    menuCt += 1
                    line = str(f.readline())
                if (((int(keyYear) > int(startYear)) | ((int(keyMonth) >= int(startMonth)) & (int(keyYear) == int(startYear)))) & ((int(keyYear)<int(endYear)) | ((int(keyMonth)<=int(endMonth)) & (int(keyYear)<=int(endYear))))):
                    totalPosts += keyVal 
            monthKey = activeMonth + activeYear
            monthPosts = archList[monthKey]
        elif (htmlTag != -1):
            breakLoop = 1
    i += 1
#    output = "    " + str(monthID - 1) + ""
#    print(output)
#    log.write(output + "\n")
    if math.ceil(monthPosts/25) == i - 1:
        totalParsed += (monthID - 1)
        totalPosts -= (monthID - 1)
        currTime = datetime.now()
        timeelapsed = currTime - prevTime
        elapsed = timeelapsed.total_seconds()
        prevTime = currTime
        currTimeStr = currTime.strftime("%H:%M")
        timeLeft = elapsed * totalPosts / (monthID - 1)
        hrElapsed = str(int(elapsed / 3600))
        minElapsed = str(int((elapsed - int(hrElapsed) * 3600)/60))
        if len(minElapsed) == 1:
            minElapsed = "0" + minElapsed
        secElapsed = str(int((elapsed - int(hrElapsed) * 3600 - int(minElapsed) * 60)))
        if len(secElapsed) == 1:
            secElapsed = "0" + secElapsed
        hrLeft = str(int(timeLeft / 3600))
        minLeft = str(int((timeLeft - int(hrLeft) * 3600)/60))
        if len(minLeft) == 1:
            minLeft = "0" + minLeft
        secLeft = str(int((timeLeft - int(hrLeft) * 3600 - int(minLeft) * 60)))
        if len(secLeft) == 1:
            secLeft = "0" + secLeft
        output = "    " + currTimeStr + ", Finished " + monthKey + " (" + str(monthPosts) + "/" + str(monthID-1) + "), " + str(totalParsed) + " parsed, " + str(totalPosts) + " remaining, time elapsed, " + hrElapsed + ":" + minElapsed + ":" + secElapsed + ", est. remaining: " + hrLeft + ":" + minLeft + ":" + secLeft
        print(output)
        log.write(output + "\n")
        log.close()
        log = open(logFile, 'a')
        monthID =  1
        saveFile = leadSlug + "/penn/dishness/dishParse/20" + activeYear + "/dishData" + activeYear + activeMonth + ".posts"
        if (activeMonth == endMonth) & (activeYear == endYear):
            runBool = 0
        elif activeMonth == "12":
            activeYear = int(activeYear) + 1
            activeYear = str(activeYear)
            if len(activeYear) == 1:
                activeYear = "0" + activeYear
            activeMonth = "01"
        else:
            activeMonth = int(activeMonth) + 1
            activeMonth = str(activeMonth)
            if len(activeMonth) == 1:
                activeMonth = "0" + activeMonth
        i = 1
        monthKey = activeMonth + activeYear
        monthPosts = archList[monthKey]
        with open(saveFile, 'wb') as fNew:
            pickle.dump(posts, fNew)
        linkIndex = [redirects, deads, manualRecode]
        with open(linkIndices, 'wb') as fNew:
            pickle.dump(linkIndex, fNew)
        posts = {}
output = "Parsing complete from " + startMonth + startYear + " to " + endMonth + endYear + ", Total Posts Parsed = " + str(totalParsed)
print(output)
log.write(output + "\n")
log.close()