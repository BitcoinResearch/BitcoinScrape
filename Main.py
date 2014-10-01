#PYTHON 2.7
#MODULES REQUIRED: mechanize, lxml, urllib2, csv, BeautifulSoup, datetime.

import mechanize, lxml.html             #mechanize used for user agents
from lxml.html import parse             #lxml used for finding XPaths
from random import randrange
from urllib2 import HTTPError
import csv
import sys
import XPaths as xpath                  #XPaths.py


months = {'01':"Jan", '02':"Feb", '03':"Mar", '04':"Apr", '05':"May",
          '06':"Jun", '07':"Jul", '08':"Aug", '09':"Sep", '10':"Oct", '11':"Nov", '12':"Dec"}


searchTerm = "bitcoin"             #term you wish to search.
domainRoot = "coindesk.com"        #site you wish to search. Leave empty quotes: "" if you don't want to narrow it
chooseMinDate = ["01","04","2013"] #use UK Format
chooseMaxDate = ["31","03","2014"]
sleepSecs = 5                      #seconds to sleep after a Google page worth of scraping. Can also use decimals: 0.5

searchRoot = "https://www.google.co.uk/search?q=site%3A"
postAttribs = "&safe=off&espv=2&biw=1594&bih=1029&source=lnt&tbs=cdr%3A1"
googlePage = "&start="

#user agents. find more at http://www.useragentstring.com/pages/useragentstring.php
userAgents = [#"Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",                                                               broken
              "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330",
              "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
              #"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0",
              #"Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
              #"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52",
              #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",        broken
              "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
              #"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
              "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
              #"Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1",                                         broken
              #"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
              #"Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
              #"Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",                                            broken
              "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
              #"Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US)",                                                                     broken
              "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4325)",
              "Mozilla/4.0 (compatible; MSIE 6.0b; Windows NT 5.0; .NET CLR 1.1.4322)"]

lastURLs = []
firstCSV = []

global brokenHTTP
global brokenHTTPDetails

#Write data to a CSV file path. Will override existing data. Use for a first time write.
def csv_writer(data, path):
    with open(path, 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            print("line: ",line)
            writer.writerows(line)

#Append data to an existing CSV file. Won't override existing data. Use with an existing CSV file.
def csv_append(data, path):
    with open(path, 'ab') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            [x[0].encode('utf-8') for x in line]
            print("line: ",line)
            writer.writerows(line)


if __name__ == "__main__":
    print "Starting main"

    killMe = False

    googlePageNum = 480
    #create the Google URL including the minimum and maximum dates
    minimumDate = "%2Ccd_min%3A"+chooseMinDate[0]+"%2F"+chooseMinDate[1]+"%2F"+chooseMinDate[2]+""
    maximumDate = "%2Ccd_max%3A"+chooseMaxDate[0]+"%2F"+chooseMaxDate[1]+"%2F"+chooseMaxDate[2]+""
    minDate = chooseMinDate[0] + chooseMinDate[1] + chooseMinDate[2]
    maxDate = chooseMaxDate[0] + chooseMaxDate[1] + chooseMaxDate[2]
    #create the filename, including searchTerm, and date range
    filename = (domainRoot+"_"+searchTerm+"_"+minDate+"-"+maxDate+"test7.csv")

    #add field headers to .csv file
    csvData = [("type"+"^"+"title"+"^"+"description"+"^"+"siteURL"+"^"+
                "sections"+"^"+"tags"+"^"+"publishedTime"+"^"+"modifiedTime").split("^")] #CSV field names
    print("csv: ", csvData)

    firstCSV.append(csvData)
    csv_writer(firstCSV, filename)  #send to CSV function

    #Enter loop which is continuously scraping data
    while killMe is False:
        #next 4 lines randomly choose a user agent to pose as the browser
        index = randrange(0, (len(userAgents)), 2)
        br = mechanize.Browser()
        br.addheaders = [('User-agent', userAgents[index])]
        br.set_handle_robots(False)

        #create final URL, including the page number on the end
        finalURL = searchRoot+domainRoot+"+"+searchTerm+postAttribs+minimumDate+maximumDate+googlePage+str(googlePageNum)

        print finalURL
        print "googlePageNum: ", googlePageNum
        print "USER AGENT: ", userAgents[index]
        #open URL, save response
        response = br.open(finalURL)
        #retrieve html
        html = response.read().lower()
        #convert to lxml html document
        doc = lxml.html.document_fromstring(html)

        allURLs = []
        #for every element found in html class='r': (every URL found on this Google search page)
        for element in doc.xpath("//h3[@class='r']/a"):
            #find the href element within class='r' and save it to thisURL
            thisURL = str(element.get('href'))
            print "rawURL: ",thisURL
            print "domainRoot: ", domainRoot

            #clean up the url by splitting "/url?q=" off the start of it
            #this creates an array thisURL = ["/url?q=", "www.coindesk.com/somethingsomething"]
            thisURL = thisURL.split("/url?q=")
            #if successfully splitted, then go into if statement and pop the extra string from the array
            if len(thisURL) > 1:
                print "about to pop... ", thisURL
                thisURL.pop(0)
            thisURL = thisURL[0]  #convert thisURL from an array back to a String

            #if thisURL string ends in "&sa", split again.
            thisURL = thisURL.split("&sa")
            #if there was a split, go into if statement and pop the extra string from the array
            if len(thisURL) > 1:
                thisURL.pop(1)
            thisURL = thisURL[0] #convert from an array back into a String
            print(thisURL)       #URL should now be clean and ready to use...

            #...but sometimes Google adds extra gobbledegoop to the url
            #if the url starts with a google URL, split it. If it doesn't it's going to ignore all this extraURL stuff.
            extraURL = thisURL.split("http://www.google.co.uk/url?url=")
            print "extraURLraw: ",extraURL
            if len(extraURL) > 1:               #if the URL has been split, pop the extra string from the URL
                extraURL.pop(0)
            print "extraURL: ",extraURL

            #if the url ALSO ends with "&rct", split it again
            extraURL = extraURL[0].split("&rct")
            print "extraURL2raw: ", extraURL
            if len(extraURL) > 1:
                extraURL.pop(1)     #pop off the end

            print "Finished URL: ", extraURL

            extraURL = extraURL[0]      #convert off the end
            allURLs.append(extraURL)    #append the URL to allURLs list

        print(allURLs)             #print allURLs

        #check all allURL's aren't the same as the previous page..
        #..this ends the program if we're collecting duplicate URLs (happens around page 51)
        if allURLs == lastURLs:
            print(lastURLs)
            print "KILLED"
            killMe = True
        lastURLs = allURLs  #if they're not the same, update lastURLs.

        #next 4 lines randomly choose a new user agent to pose as the browser
        index = randrange(0, (len(userAgents)), 2)
        br = mechanize.Browser()
        br.addheaders = [('User-agent', userAgents[index])]
        br.set_handle_robots(False)
        print "USER AGENT: ", userAgents[index]

        finalCSV = []

        #for each URL in the allURLs list
        for url in range (len(allURLs)):
            brokenHTTP = False
            articleBody = []
            allArticles = []
            sectionString = ''
            tagString = ''

            #make sure the URL still exists / the website hasn't blocked us
            try:
                response = br.open(allURLs[url])
            except HTTPError, e:
                print "HTTP Error code: ", e.code
                print "HTTP Error msg: ", e.msg
                brokenHTTP = True                                   #brokenHTTP is True if it's broken
                brokenHTTPDetails = str(e.code)+ " " + str(e.msg)

            #if it isn't broken, continue into if statement:
            if brokenHTTP is False:

                html = response.read().lower()
                doc = lxml.html.document_fromstring(html)

                #retrieve locale information from our findLocale function in XPaths.py
                locale = xpath.findLocale(doc)
                print "locale: ", locale
                locale = locale.encode("utf-8")

                #retrieve page type
                type = xpath.findType(doc)
                print "type: ", type
                if type == "" or type == None:  #if no 'type' found, save it was 'unknown'
                    type = "unknown"
                type = type.encode("utf-8")

                #retrieve page title
                title = xpath.findTitle(doc)
                print "title: ", title
                title = title.encode("utf-8")

                #retrieve page description
                description = xpath.findDescription(doc)
                print "description: ", description
                description = description.encode("utf-8")

                #retrieve site URL
                siteURL = xpath.findSiteURL(doc)
                print "articleURL: ", siteURL
                if siteURL == '':               #if it doesn't exist, use the URL we retrieved from Google.
                    siteURL = allURLs[url]
                siteURL = siteURL.encode("utf-8")

                #retrieve publisher
                publisher = xpath.findPublisher(doc)
                print "publisher: ", publisher
                publisher = publisher.encode("utf-8")

                #retrieve page sections
                sections = xpath.findSections(doc)
                print "section: ", sections

                #retrieve published time
                publishedTime = xpath.findPublishedTime(doc)
                print "publishedTime: ", publishedTime
                publishedTime = publishedTime.encode("utf-8")

                #retrieve modified time
                modifiedTime = xpath.findModifiedTime(doc)
                print "modifiedTime: ", modifiedTime
                modifiedTime = modifiedTime.encode("utf-8")

                #retrieve page tags
                tags = xpath.findTags(doc)
                print "tags: ", tags

                #ONLY WORKS FOR COINDESK. Retrieve article body, line by line
                for el in doc.xpath("//div[@class='single-content']/p"):
                    paragraph = el.text_content()
                    articleBody.append(paragraph)
                print len(articleBody)
                thisArticle = ''
                #Append each line onto to each other to create full article body
                for x in range (len(articleBody)):
                    thisArticle.encode('utf-8', errors='strict')
                    thisArticle = thisArticle + articleBody[x]
                thisArticle.encode('utf-8')

                #append all section strings returned into a single string
                for index in range (len(sections)):
                    sectionString = sectionString + "(" + sections[index] + ")"
                #append all tag strings returned into a single string
                for index in range (len(tags)):
                    tagString = tagString + "(" + tags[index] + ")"

                #print the data we're about to add to the CSV. Apart from article text.
                print type, title, description, siteURL, sectionString, tagString, publishedTime, modifiedTime

                #note that we're not adding ALL the retrieved information such as locale, feel free to add if you need it.                                                                                                       #'''thisArticle currently ommitted due to ascii errors'''
                csvData = [(type+"^"+title+"^"+description+"^"+siteURL+"^"+sectionString+"^"+tagString+"^"+publishedTime+"^"+modifiedTime+"" '''+"^"+thisArticle''' ).split("^")]

                #attempting to remove encoding errors
                try:
                    [x[0].decode('utf-8') for x in csvData]
                except UnicodeDecodeError:
                    raise
                except UnicodeEncodeError:
                    raise

                print("csv: ", csvData)
                finalCSV.append(csvData)    #append all web page data to a final list

            #else if the URL was broken, make a record of the URL error we got and add it to the csv:
            else:
                csvDataError = [("broken"+"^"+"ERROR"+"^"+brokenHTTPDetails+"^"+allURLs[url]).split("^")]
                print("csv error: ", csvDataError)
                finalCSV.append(csvDataError)

        #append all article information to our CSV file:
        try:
            csv_append(finalCSV, filename)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

        #increment to the next Google page, repeat.
        googlePageNum = googlePageNum + 10






    '''
    global finalNextMaxDate
    finalNextMaxDate = {}
    datesStartList = []
    datesEndList = []
    finalMinDate = {'day':chooseMinDate[0], 'month':chooseMinDate[1], 'year':chooseMinDate[2]}
    finalMaxDate = {'day':chooseMaxDate[0], 'month':chooseMaxDate[1], 'year':chooseMaxDate[2]}
    datesEndList.append(finalMinDate)

    #chooseMinDate = ["01","04","2013"]
    #chooseMaxDate = ["31","03","2014"]
    #x = 0
    #y = 0

    while finalNextMaxDate != finalMaxDate:
        #nextMaxDate = [datesList[x]['day'],datesList[x]['month'],datesList[x]['year']]

        altMinDate = datesEndList[y]['day'] +"/"+ months.get(str(datesEndList[y]['month'])) +"/"+ datesEndList[y]['year']
        #altMaxDate = chooseMaxDate[0] +"/"+ months.get(str(chooseMinDate[1])) +"/"+ chooseMaxDate[2]
        print "ALTMINDATE: ",altMinDate
        dt = datetime.strptime(altMinDate, '%d/%b/%Y')
        start = dt - timedelta(days = dt.weekday())
        print("start: ", start)
        end = start + timedelta(days = 6)
        end2 = start + timedelta(days = 7)

        endDate = str(end).split("-")
        endDate[2] = endDate[2].strip(" 00:00:00")
        print endDate
        endDateItem = {'day':endDate[2], 'month':endDate[1], 'year':endDate[0]}
        datesStartList.append(endDateItem)

        endDate = str(end2).split("-")
        endDate[2] = endDate[2].strip(" 00:00:00")
        print endDate
        endDateItem = {'day':endDate[2], 'month':endDate[1], 'year':endDate[0]}
        datesEndList.append(endDateItem)

        print datesStartList
        print datesEndList
        finalNextMaxDate = endDateItem
        y = y + 1
    '''
    #print datesList
    #thisMinimumDate = "%2Ccd_min%3A"+datesList[x]['day']+"%2F"+datesList[x]['month']+"%2F"+datesList[x]['year']+""
    #thisMaximumDate = "%2Ccd_max%3A"+datesList[x+1]['day']+"%2F"+datesList[x+1]['month']+"%2F"+datesList[x+1]['year']+""


