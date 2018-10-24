'''
Class for creating a quote-scraping web crawler within a scrapy project
'''

import scrapy
import pandas as pd


class QuotesSpider(scrapy.Spider):
    name = "utility"


    def start_requests(self):
        #Pull in external data for URLs
        urls = list(pd.read_csv("../../Rate_URLs.csv")['Utility Domain URL'].unique())

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
        Method for parsing the page content that the spider finds.

        It is expected that typically the parse method will be passed to the 
        callback parameter of a scrapy.Request() object (e.g. see the 
        start_requests method above)
        '''

        #page is the text data scraped from the webpage being parsed
        #Pull the "www...." portion of the URL for value of page
        page = response.url.split("/")[-1]
        filename = f'../../Pages/{self.name}-{page}.html'
        
        #Write the page contents text to file for later use
        with open(filename, 'wb') as f: 
            #Want to track the URL that generated the file
            #f.write(f"URL: {response.url}\n\n")
            f.write(response.body)
        
        #Keep track of what we've crawled in memory
        self.log(f'Saved file {filename}')