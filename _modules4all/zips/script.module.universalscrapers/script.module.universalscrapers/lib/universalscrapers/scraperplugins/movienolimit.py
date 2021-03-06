import requests
import urlparse
import re
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class movienolimit(Scraper):
    domains = ['movienolimit.to']
    name = "MovieNoLimit"
    sources = []

    def __init__(self):
        self.base_link = 'https://movienolimit.to'


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        
            start_url = '%s/search?query=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print 'scraperchk - scrape_movie - start_url:  ' + start_url                                  
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            #print html           
            match = re.compile('class="movie-item view-tenth".+?href="(.+?)">.+?alt="(.+?)" />.+?data-title="Quality">(.+?)<',re.DOTALL).findall(html)  
            for item_url1,name,qual in match:
                #print item_url1
                item_url = self.base_link+item_url1
                qual=qual.replace('&nbsp;','')
                #print 'scraperchk - scrape_movie - name: '+name
                #print 'scraperchk - scrape_movie - item_url: '+item_url
                if clean_title(search_id).lower() == clean_title(name).lower():                                                                        
                    #print 'scraperchk - scrape_movie - Send this URL: ' + item_url                             
                    self.get_source(item_url,title,year,start_time,qual)                                      
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 


    def get_source(self,item_url,title,year,start_time,qual):
        try:
            #print 'PASSEDURL >>>>>>'+item_url
            count = 0
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content
            Endlinks = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(OPEN)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for link in Endlinks:
                #print 'scraperchk - scrape_movie - link: '+str(link)        
                count+=1
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                self.sources.append({'source':host, 'quality':qual, 'scraper':self.name, 'url':link, 'direct':False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]