from SeleniumReader import *
from misc import *
from tag_classifier import *
from web_interface import *
import urllib2

class site_diver:
    
    def __init__(self, url):
        self.url = url
        self.wi = WebInterface()
        self.links = {}
        self.links_page_properties = {}
        self.tag_list_separator = "!@#$$#@!"
        self.reader = SeleniumReader(url)
        self.tags = Tags();
    
    def moveTo(self, url):
        self.url = url
        self.reader.moveTo(url)
        self.links = {}
        self.links_page_properties = {}
        
    
    def getNewLinksThisLevel(self, parent_name_list):
        # get all a links 
        # filter from tag classifier
        # find new links by diff-in with links_one_level_up
        # remaining links are links at this level
            
        if not parent_name_list:
            parent_link_names = []
        else:
            parent_link_names = parent_name_list.split(self.tag_list_separator)
        
        divs = self.reader.getElementsByTagName('a')
        new_links = {}
        for div in divs:
            text = getAsciiText(div)
            
            if not text:
                continue
            
            #if word in exclude_dict:
            if self.tags.isExclusionType(text) == 1:
                #print s + " excluded\n"
                continue
            
            # if not an apparel type or promo type, then continue
            if not(self.tags.isApparelType(text) == 1 or self.tags.isPromoType(text)):
                #print firstword + " excluded\n"
                continue
            
            if parent_link_names:
                present_in_parents = 0
                for pln in parent_link_names:
                    if pln == text:
                        present_in_parents = 1
                        break
                if present_in_parents:
                    continue
            
            div_url = readWebElementAttr(div, 'href')
            if not div_url:
                continue
            
            if haveDifferentBaseSite(self.url, div_url) == True or pointsToAnImage(div_url) == True:
                continue
            
            if div_url:
                new_links[text] = div_url
            
        
        return new_links
        
    
        
    def dfs_to_get_new_links(self, level, parent_name_path):
        
        if level >= 2:
            return
        
        moved = False
        if parent_name_path:
            eles = self.reader.getElementsByLinkText(parent_name_path.split(self.tag_list_separator)[-1])
            for e in eles:
                e_link = readWebElementAttr(e, 'href')
                if e_link and (e_link == self.links[parent_name_path]):
                    e.click()
                    #self.reader.moveTo(AddHTTP(e_link))
                    moved = True
        
        new_links = self.getNewLinksThisLevel(parent_name_path)
        
        #parent_level_name = str(level)
        #level_name = str(level+1)
        #if level_name not in link_this_level:
        #    link_this_leval[level_name] = {}
        
        new_paths = []
        for new_link_name in new_links:
            new_link_url = new_links[new_link_name]
            if parent_name_path:
                new_path = parent_name_path + self.tag_list_separator + new_link_name
            else:
                new_path = new_link_name
            new_paths.append(new_path)
            self.links[new_path] = new_link_url
            
        for path in new_paths:
            self.dfs_to_get_new_links(level+1, path)
        
        if moved:
            self.reader.getDriver().back();
        
        return    
    
    def get_links_page_properties(self):
        for link_path in self.links:
            url = self.links[link_path]
            self.reader.moveTo(url)
            is_product_listing_page = self.isProductListingPage()
            self.links_page_properties[link_path] = not(not(is_product_listing_page))
        
    def run(self):
        self.dfs_to_get_new_links(0,"")
        self.get_links_page_properties()
    
    
    def isProductListingPage(self):
        
        product_list = self.getProductsListed()
        return product_list
        
    # Creates different bins based on (width, height) pair of images
    # Sort all images on the page in different bins
    # Pick the bin that has at least 8 images of height >=90 and width >= 90
    # returns list of those image el
    def doesElementHasProductsListed(self, ele):
        
        threshold = 8
        divs = ele.find_elements_by_tag_name("img")
        ge = {}
        
        product_divs = []
        max = 0
        for div in divs:
            if div.size['width'] < 90:
                continue
            if div.size['height'] < 90:
                continue
                
            w = div.size['width']
            h = div.size['height']
            
            if w not in ge:
                ge[w] = {}
            if h not in ge[w]:
                ge[w][h] = []
                
            ge[w][h].append(div)
            bin_size = len(ge[w][h])
            if  bin_size> max and bin_size >= threshold:
                max = bin_size
                product_divs = ge[w][h]
        
        ret_val = [0, []]
        if max >= threshold:
            ret_val[0] = 1
            ret_val[1] = product_divs
        
        return ret_val
                
             
    
    def getProductsListed(self):
        
        ret_val = self.doesElementHasProductsListed(self.reader.getDriver())
        
        if ret_val[0] == 0:
            return []
        else:
            len = len(ret_val[1])
            pEle = ret_val[1][ int (len/2) ]
            parent_re = self.reader.getParentOfWebElement(pEle)
            while parent_re[0] == 1:
                pEle = parent_re[1]
                ret_val_temp = self.doesElementHasProductsListed(pEle)
                if ret_val_temp[0] > 0:
                    product_list = ret_val_temp[1]
                    return product_list;
                    
                parent_re = self.reader.getParentOfWebElement(pEle)
        
        return []
                

                
    
    
## test site diver
##
def test_site_diver():
    urls = []
    urls.append("www.express.com")
    urls.append("www.nordstrom.com")
    urls.append("www.anthropologie.com")
    sd = None
    for url in urls:
        if not sd:
            sd = site_diver(AddHTTP(url))
        else:
            sd.moveTo(url)
        sd.run()
    return

test_site_diver()