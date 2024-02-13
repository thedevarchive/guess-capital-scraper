from bs4 import BeautifulSoup
import requests

class CountryScraper: 
    #initialise CountryScraper
    def __init__(self):
        #get url of website
        self.url = "https://www.scrapethissite.com/pages/simple/"
        self.result = requests.get(self.url).text
        self.doc = BeautifulSoup(self.result, "html.parser")
        #get all divs with class "row"
        self.rows = self.doc.find("div", id="page").find("div", class_="container").find_all("div", class_="row")
        self.countries = {}

    def getCountries(self): 
        for row in self.rows: 
            try: 
                countryRows = row.find_all("div", class_="country")
                #each row class contains more than one div 
                #with the "country" class
                for country in countryRows: 
                    #find h3's text and strip it 
                    #text has excessive whitespace
                    countryName = country.find("h3").text.strip()
                    capital = country.find("div", class_="country-info").find("span").text.strip()
                    #put 
                    self.countries[countryName] = { "capital": capital }
            except: 
                pass
        
        return self.countries