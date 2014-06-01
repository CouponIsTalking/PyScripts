from url_groups import *
from misc import *
from web_interface import *
from SeleniumReader import *
import lxml.html
from lxml import etree
from StringIO import StringIO

class GetRelatedProds:
    
    def print_related_prods_links(self):
        for link in self.full_links:
            print link
        
    def __init__(self, input, method):
        self.wi = WebInterface()
        if method == 'page_url':
            self.move_to_url(input)
        
        self.tool = 'urllib2'
        self.reader = None
    
    def set_tool(self, new_tool):
        if new_tool == 'urllib2' or new_tool == 'selenium':
            self.tool = new_tool
            return True
        else:
            return False
        
    def move_to_url (self, url):
        self.initvars()
        self.page_url = AddHTTP(url)
        if 'urllib2' == self.tool:
            self.page = self.wi.get_a_webpage(self.page_url)
        elif 'selenium' == self.tool:
            self.reader = SeleniumReader(self.page_url) if self.reader is None else self.reader.moveTo(self.page_url)
            self.page = self.reader.getPageSource()
        
        self.et = etree.parse(StringIO(self.page), etree.HTMLParser())   
    
    def initvars(self):    
        self.page = self.page_url = ""
        self.et = None
        self.related_links = self.full_links = []
    
    def deinit(self):
        self.page = self.page_url = ""
        self.et = None
        self.related_links = self.full_links = []
        if self.reader:
            self.reader.deinit()                 
        
    def update_related_prods_in_db(self):
        retval = self.wi.update_get_prod_detail_jobs(self.full_links);
        return retval
    
    def extract_related_prods(self):
        if self.tool == 'urllib2':
            self.extract_related_prods_urllib2()
        elif self.tool == 'selenium':
            self.extract_related_prods_selenium()
        
        return self.full_links
    
    def extract_related_prods_selenium(self):
            
        et = self.et
        self.related_links = []
        
        image_elements = self.reader.getElementsByTagName('img')
        
        for image in image_elements:
            ele = image
            link = self.get_prod_info_by_web_element(ele)
            if link: 
                self.related_links.append(link)
        
        return self.process_related_links(self.related_links)
    
    def extract_related_prods_urllib2(self):
            
        et = self.et
        self.related_links = []
        
        images = et.xpath("//img")
        for image in images:
            ele = image
            link = self.get_prod_info_by_lxml_element(ele)
            if link: 
                self.related_links.append(link)
        
        return self.process_related_links(self.related_links)
    
    def process_related_links(self, related_links):
        
        related_links = self.related_links
        
        l = len(related_links)
        full_links = []
        i = 0
        while i<l:
            if "javascript" in related_links[i]:
                pass
            elif related_links[i].startswith("#"):
                pass
            elif related_links[i] == "/":
                pass
            elif related_links[i] == self.page_url:
                pass
            else:
                full_links.append(get_full_path(related_links[i], self.page_url))
            i+=1
        
        self.full_links = list(set(full_links)) if full_links else []
        
        return full_links
    
    def get_prod_info_by_web_element(self, ele):
        
        et = self.et
        price_found = False
        info_found = False
        link = ""
        
        while True:
            
#            try:
#                if len(ele.find_elements_by_tag_name('img')) > 1:
#                    print "more than 1 images"
#                    break
#            except Exception, e:
#                print "exception figuring out number of images"
#                break
            
            link = readWebElementAttr(ele, 'href') if not link else link
            
            text = getAsciiText(ele)
            text = nicely_clean_text(text)
            words = nicely_clean_word_list(text)
            if len(words) > 15:
                break
            
            price_found = True if (text and textHasDollarPrice(text)) else price_found
            
            if link and price_found:
                info_found = True
                break
            
            ele = self.reader.getParentOfWebElement(ele)
            if ele is None:
                break
            
            
        return link if info_found else ""
        
    
    def get_prod_info_by_lxml_element(self, ele):
        
        et = self.et
        price_found = False
        info_found = False
        link = ""
        
        img_src = et.xpath(et.getpath(ele) + "/@src")
        if img_src:
            img_src = img_src[0]
        else:
            return ""
        
        if img_src == "http://s7d5.scene7.com/is/image/adidasgroup/V13315_01":
            a = 1
        
        while True:
            #descendant-or-self
            xpath = et.getpath(ele)
            all_images = ele.xpath(xpath+"/descendant-or-self::img")
            
            #print all_images
            if len(all_images) != 1:
                pass #break
            
            if not link:
                if ele.attrib.get("href"):
                    link = ele.attrib.get("href").strip()
            
            text = etree.tostring(ele, encoding="utf-8", method="text")
            text = nicely_clean_text(text)
            words = nicely_clean_word_list(text)
            if len(words) > 15:
                break
            
            #print text
            #print "--------"
            if text and textHasDollarPrice(text):
                #print text
                price_found = True
            
            
            if link and price_found:
                info_found = True
                break
            
            ele = ele.getparent()
            if ele is None:
                break
            
            #print ele.findall("img")
            #total_images_in_this_div = len(ele.findall("img"))
            #print str(total_images_in_this_div)
            #if total_images_in_this_div != 1:
            #    break
        
        if info_found:
            return link
        else:
            return ""

