from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

class parseLink(HTMLParser):
    def tag_handle(self,tag,att):
        if tag == 'a':
            for(key,value) in att:
                if key == 'href':
                    newURL = parse.urljoin(self.baseUrl,value)
                    self.links = self.links + [newUrl]


    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]

    def spider(url,word,maxPages):
        pagestoVisit = [url]
        numberVisited = 0
        foundWord = False
        while numberVisited < maxPages and pagestoVisit !=[] and not foundWord:
            numberVisited = numberVisited +1
            url = pagestoVisit[0]
            pagestoVisit = pagestoVisit[1:]
            try:
                print(numberVisited, "Visiting:", url)
                parser = parseLink()
                data, links = parser.getLinks(url)
                if data.find(word)>-1:
                    foundWord = True
                    pagestoVisit = pagestoVisit + links
                    print("Sucess")
            except:
                print("Failed")
        if foundWord:
            print("The word",word,"was found at", url)
        else:
            print("Word not found")
