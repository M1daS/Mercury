'''
Created on Jul 8, 2017

@author: micha
'''

'''
Created on Mar 27, 2017

@author: michael sands
'''
from bs4 import BeautifulSoup
import feedparser
import csv
import re 
from bs4 import BeautifulSoup


#Function to fetch the rss feed and return the parsed RSS
def parseRSS( rss_url ):
    return feedparser.parse( rss_url ) 
    
# Function grabs the rss feed headlines (titles) and returns them as a list
def getTagInfo (rss_url, key, type):
    link = []
    title = []
    summary = []
    titlelist = []
    linklist = []
    
    feed = parseRSS( rss_url )

    for newsitem in feed['items']:
        title.append(newsitem['title'])
        #summary.append(BeautifulSoup(newsitem['summary'], 'html.parser') )#'lxml').text Beautifulsoup.text cleans the html tags from the text
        link.append(newsitem['link'])
  
        
    for i in range(len(link)):
        titlelist.append(title[i])
        linklist.append(link[i])

    if type == 'title':
        return titlelist
    elif type == 'link':
        return linklist


 
fulltitlelist = []
fulllinklist = []
# List of RSS feeds that we will fetch and combine



def start_rss(out_path):
    print('Initializing RSS')
    newsurls = {
        'MW_TopStories':  'http://feeds.marketwatch.com/marketwatch/topstories/',
        'MW_Breaking': 'http://feeds.marketwatch.com/marketwatch/bulletins',
        'CNN_TopStories':'http://rss.cnn.com/rss/cnn_topstories.rss',
        'CNN_World':'http://rss.cnn.com/rss/cnn_world.rss',

    }
    # Iterate over the urls to retrieve data and append the master arrays with the retrieved data
    for key,url in newsurls.items():
        fulltitlelist.extend( getTagInfo (url, key, 'title'))
        fulllinklist.extend( getTagInfo (url, key, 'link'))



    return (fulltitlelist, fulllinklist)
    #return a list that alternates title and then link so it can be looped in one statement in
    #the newsrss html file to insert title and link and summary images in seperate column on same row.
    #also get the source of the document











#WRITE TO FILE

    # myfile = open(out_path,'wt')
    # writer = csv.writer(myfile, delimiter=',', quotechar='"')
    # for i in range(len(fulltitlelist)):
    #     try:
    #         writer.writerow([fulltitlelist[i] + '  ' +fulllinklist[i]])
    #         myfile.flush() 
    #     except(UnicodeEncodeError):
    #         writer.writerow('')
    
    # myfile.close() 



#SEARCH HEADLINE FOR KEYWORD
    # headline_overview = [] 
    # length = len(fulltitlelist)
    # for i in range(length):
    #     headline_overview.append(fulltitlelist[i])
 
    # #ticker specefific analysis

    # # def search_headlines(ticker):
    # #     for i in range(len(headline_overview)):   
    # #         if ticker in headline_overview[i]:
    # #             print('yes ', i)
    # #             print(headline_overview[i])      
    # # search_headlines('Tesla')
    # # #SEND KEYWORD IN as ticker