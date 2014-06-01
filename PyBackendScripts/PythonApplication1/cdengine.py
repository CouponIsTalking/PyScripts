import urllib2
from urlparse import urlparse
from web_interface import *
from const import *
from BeautifulSoup import *
from htmlops import *
from misc import *

class Cdengine:
    def __init__(self):
        self.wi = WebInterface()
        
    
    def get_surfers(self):
        page_content = self.wi.get_a_webpage(AB_SITE_NAME + "/surfers/index")
        page_content = removeCommentsAndJS(page_content)
        soup = BeautifulSoup(page_content)
        divs = soup.findAll('div', attrs={'class':'tag'})
        for div in divs:
            url = AddHTTP(div.text.encode("ascii","ignore").strip())
            self.extract(url)
        
    def isConjectiveWord(self, word):
        
        conj_adverbs = """ accordingly,    furthermore,    moreover,       similarly,
        also,           hence,          namely,         still,
        anyway,         however,        nevertheless,   then,
        besides,        incidentally,   next,           thereafter,
        certainly,      indeed,         nonetheless,    therefore,
        consequently,   instead,        now,            thus,
        finally,        likewise,       otherwise,      undoubtedly,
        further,        meanwhile,"""
        
        coord_conj = """and,but,or,nor,for,yet,so,as,between,among,"""
        
        if ( (word +",") in conj_adverbs + coord_conj):
            return True
        else:
            return False
        
    def isNewsArticle(self, heading, link):
        heading = heading.lower()
        link = link.lower()
        heading_words = clean_text(heading.replace("\r"," ")).split(" ")
        words = 0;
        for hw in heading_words:
            if self.isConjectiveWord(hw):
                continue
            if len(hw) > 2:
                words = words +1
        
        if words > 4:
            return True
            
    def combine_url(self, base_url, next_url):
        if next_url.startswith("/") or next_url.startswith("#"):
            return base_url + next_url
        else:
            return next_url
    
    def classify_link_text(self, link_text, link_url):
        rv={}
        rv['isnews'] = self.isNewsArticle(link_text, link_url)
        return rv
        
    def extract(self, url):
        page = self.wi.get_a_webpage(url)
        page = removeCommentsAndJS(page)
        soup = BeautifulSoup(page)
        adivs = soup.findAll('a', href=True)
        for adiv in adivs:
            link_url = self.combine_url(url, adiv.attrMap['href'].encode("ascii", "ignore"))
            link_text = adiv.text.encode("ascii","ignore").strip()
            rv = self.classify_link_text(link_text, link_url)
            if rv['isnews'] == True:
                news = {}
                news['title'] = link_text
                news['link'] = link_url
                news['desc'] = 'SharedByUser'
                news['topic1'] = 0
                news['state'] = 1
                news['type'] = 'news'
                print news
                print "---"
                self.wi.add_news(news)
    
    def run(self):
        self.get_surfers()
    


def test_cd_engine():
    cde = Cdengine()
    cde.run()

test_cd_engine()