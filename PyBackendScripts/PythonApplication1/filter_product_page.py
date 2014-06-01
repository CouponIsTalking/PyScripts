import sys
import urllib
import urllib2
import urlparse
import const
from const import *

import BeautifulSoup
from BeautifulSoup import BeautifulSoup, Comment

import misc
from misc import *
import htmlops
from htmlops import *
from tag_classifier import *

import SeleniumReader
from SeleniumReader import *
from PriceDecoder import *
import random

import lxml.html
from lxml.html import etree


class ProductListingPage:
    def __init__(self, url_or_reader):
        
        if isinstance(url_or_reader, str):
            self.listing_url = url_or_reader
            self.reader = SeleniumReader(self.listing_url);
            
        elif isinstance(url_or_reader, SeleniumReader):
            self.reader = url_or_reader
            self.listing_url = self.reader.getDriver().current_url
        else:
            print "~~~~~~~~~ Bad param to constructor ~~~~~~~~~~~~~"
            return
            
        self.product_div = 0
        self.product_img_src = ""
        self.product_tag = ""
        self.tag_dict = Tags()
    
    def moveTo(url):
        self.product_div = 0
        self.reader.moveTo(url)
        self.listing_url = url
        
    
    def isShareItem(self, div):
        
        #sharewords = ['fblike', 'twitter', 'social', 'share', 'email', 'pinterest', 'instagram', 'pinit', 'facebook']
        sharewords = ['fblike', 'twitter', 'email', 'pinterest', 'instagram', 'pinit', 'facebook']
            
        innerhtml = readWebElementAttr(div, 'innerHTML')
        if innerhtml and ("</" not in innerhtml):
            outerhtml = readWebElementAttr(div, 'outerHTML').lower()
            words = html_to_words(outerhtml)
            for w in sharewords:
                if (w in words):
                    return True
            
        classname = readWebElementAttr(div, 'class')
        idname = readWebElementAttr(div, 'id')
            
        if classname:
            classname = classname.encode("ascii", "ignore")
        if idname:
            idname = idname.encode("ascii", "ignore")
            
        if classname:
            classname = classname.lower()
            for w in sharewords:
                if w in classname:
                    return True
            
        if idname:
            idname = idname.lower()
            for w in sharewords:
                if w in idname:
                    return False
            
        return False
    
    
    def getShareItems(self):
        
        driver = self.reader.getDriver()
        divs = driver.find_elements_by_tag_name("div")
        sharedivs = []
        for div in divs:
            shareitem = self.isShareItem(div)
            if shareitem:
                sharedivs.append(div)
        
        return sharedivs
        
    
        
    def thingsBelowReviewDivs(self, review_divs):
        
        driver = self.reader.getDriver()
        divs = driver.find_elements_by_tag_name("div")
        
        belowReviewDiv = []
        y1Min = 10000000
        
        if not review_divs:
            return belowReviewDiv
            
        for r in review_divs:
            y1 = r.location['y'];
            if y1 < y1Min:
                y1Min = y1
        
        
        for r in divs:
            y1 = r.location['y'];
            if y1 > y1Min:
                belowReviewDiv.append(r)
                
        
        #for div in belowReviewDiv:
            #self.reader.removeElement(div)
            #self.reader.dimElement(div, 0.2)
        #	self.reader.hideElement(div)
            
        return belowReviewDiv
        

    def detectReviews(self, product_div):
        
        review_divs = self.sizeBasedReviewDetection(product_div)
        #if not review_divs:
        #	review_divs = self.findReviewUsingLiguisticHints()

        # if couldn't find any,
        # then do a text based analysis
        # basically looking for lines (>=4 words (subject, verb, adjective, expressive emotion)) leaf elements with i, me, my, myself words in it
        if not review_divs:
            review_divs = self.findReviewUsingLiguisticHints(product_div)

        #for div in review_divs:
            #self.reader.removeElement(div)
            #self.reader.dimElement(div, 0.2)
        #	self.reader.hideElement(div)
        
        return review_divs
            
    def sizeBasedReviewDetection(self, product_div):
    
        driver = self.reader.getDriver()
        divs = driver.find_elements_by_tag_name("div")
        
        # find a div that does not contain product div 
        # and is of size 4 times greater than product div
        product_div_area = product_div.size['width'] * product_div.size['height']
        product_div_x1 = product_div.location['x']
        product_div_x2 = product_div_x1 + product_div.size['width']
        product_div_y1 = product_div.location['y']
        product_div_y2 = product_div_y1 + product_div.size['height']
        
        review_divs = []
        max = 0
        for div in divs:
            
            try:
                if False == div.is_displayed():
                    continue
            except Exception, e:
                print "Element not found when checking if it is displayed, assuming element not displayed and skipping\n"
                continue
                
            x1 = div.location['x']
            y1 = div.location['y']
            x2 = x1 + div.size['width']
            y2 = y1 + div.size['height']
            
            if product_div_area * 4 > (x2-x1)*(y2-y1):
                #print "area less then threshold\n"
                continue
            
            if product_div_x1 >= x1 and product_div_x2 <= x2 and product_div_y1 >= y1 and product_div_y2 <= y2:
                #print "product div not completely outside\n"
                continue
            
            #if h > w:	# we are looking for a rectangle with height < width type of shape
            #	continue
            
            # what is this div ? of size greater than 4 times image div
            # and completely outside of it
            # lets do some more checking
            # ensure that this falls below the product image
            if y1 < product_div_y2:
                #print "product div not above\n"
                continue
            
            # now I am getting supicious, 
            # but it may contain product details :(
            # look for children, should have at least 4 children
            # that are x1 and x2 aligned
            
            # Ok, this is TODO 
            print "appending " + str(div) + "\n"
            review_divs.append(div)
        
        
        return review_divs


    def findReviewUsingLiguisticHints(self, product_div):
    
        driver = self.reader.getDriver()
        
        product_div_area = product_div.size['width'] * product_div.size['height']
        product_div_x1 = product_div.location['x']
        product_div_x2 = product_div_x1 + product_div.size['width']
        product_div_y1 = product_div.location['y']
        product_div_y2 = product_div_y1 + product_div.size['height']
        
        html = driver.page_source
        html = removeCommentsAndJS(html)
        tree1 = lxml.html.fromstring(driver.page_source)
        etree1 = etree.ElementTree(tree1)
        
        review_divs = []
        reviewXPaths = []
        reviewtextslen = []
        childList = []
        childList.append(tree1)
        i = 0
        first_largest_len = 0
        second_largest_len = 0
        f_xpath = ''
        s_xpath = ''
        
        while i < len(childList):
            
            nextChild = childList[i]
            nextChildsChildren = list(nextChild)
            if nextChildsChildren:
                for ncc in nextChildsChildren:
                    childList.append(ncc)
            else:
                text = nextChild.text_content()
                if text:
                    text = text.encode("ascii", "ignore")
                    text = text.lower()
                    spaceCount = text.count(' ')
                    if spaceCount >= 3:
                        text = text.replace('.', ' ')
                        text = text.replace('$', ' ')
                        text = text.replace('!', ' ')
                        text = text.replace(',', ' ')
                        text = text.replace('?', ' ')
                        text = text.replace('\n', ' ')
                        
                        hasreview = False
                        if not hasreview:
                            hasreview = " i " in text
                        if not hasreview:
                            hasreview = " me " in text
                        if not hasreview:
                            hasreview = " my " in text
                        if not hasreview:
                            hasreview = " myself " in text
                        if not hasreview:
                            hasreview = " we " in text
                        
                        if hasreview:
                            xpath = etree1.getpath(nextChild)
                            reviewXPaths.append([xpath, len(text)])
                            
                            # keep track of xpaths of first 2 largest review elements
                            if len(text) >= first_largest_len:
                                second_largest_len = first_largest_len
                                first_largest_len = len(text)
                                s_xpath = f_xpath
                                f_xpath = xpath
                            
                            elif second_largest_len < len(text) and len(text) < first_largest_len:
                                second_largest_len = len(text)
                                s_xpath = xpath
                                    
                                
                            
                
            i = i +1
                
        
        #print reviewXPaths
        
        maxid = 0
        maxclass = 0
        maxid_name = ''
        maxclass_name = ''
        
        idMap = {}
        for (r, l) in reviewXPaths:
            rid = r + "/@id"
            ids = etree1.xpath(rid)
            for id in ids:
                if id in idMap:
                    idMap[id] = idMap[id]+1
                else:
                    idMap[id] = 1
        
        
        for e in idMap:
            if idMap[e] > maxid:
                maxid = idMap[e]
                maxid_name = e
                    
        
        
        classMap = {}
        for (r, l) in reviewXPaths:
            rclass = r + "/@class"
            classes = etree1.xpath(rclass)
            for aclass in classes:
                if aclass in classMap:
                    classMap[aclass] = classMap[aclass] + 1
                else:
                    classMap[aclass] = 1
        
        
        for e in classMap:
            if classMap[e] > maxclass:
                maxclass = classMap[e]
                maxclass_name = e
        
        #if maxid == 0 and maxclass == 0
        #	return []
            
        haha_i_found_yous = []
        if maxid > maxclass and maxid_name:
            haha_i_found_yous = driver.find_elements_by_id(maxid_name)
        elif maxid < maxclass and maxclass_name:
            haha_i_found_yous = driver.find_elements_by_class_name(maxclass_name)
        else:
            return [] # couldnt find anything
        
        if not haha_i_found_yous:
            return [] # couldnt find anything below product img
        
        # filter elements above or at product img level
        elements_below_product_div = []
        for e in haha_i_found_yous:
            y1 = e.location['y']
            y2 = e.location['y'] + e.size['height']
            if not (y2 > product_div_y2):
                continue
            else:
                elements_below_product_div.append(e)
        
        haha_i_found_yous = elements_below_product_div
        
        if not haha_i_found_yous:
            return [] # couldnt find anything below product img
        
        
        # now recurse up to find the nearest encompassing rectangle
        #
        x =[]
        y =[]
        for e in haha_i_found_yous:
            x.append(e.location['x'])
            x.append(e.location['x'] + e.size['width'])
            y.append(e.location['y'])
            y.append(e.location['y'] + e.size['height'])

        x.sort()
        y.sort()
        x1 = x[0]
        x2 = x[len(x)-1] 
        y1 = y[0]
        y2 = y[len(y)-1]
        
        review_divs = []
        crappy_element = None
        pEle = haha_i_found_yous[0]
        while True:
            px1 = pEle.location['x']
            px2 = pEle.location['x'] + pEle.size['width']
            py1 = pEle.location['y']
            py2 = pEle.location['y'] + pEle.size['height']
            
            print px1, px2, py1, py2
            
            # if the element-being-considered is not location below product image,then break
            if not (py2 > product_div_y2):
                break
            
            # does rectangle given by x1, x2 ,y1, y2 fall within px1, px2, py1, py2
            if px1 <= x1 and x2 <= px2 and py1 <= y1 and y2 <= py2:
                crappy_element = pEle
                break
            tag = pEle.get_attribute('tag')
            if tag:
                if tag.lower() == 'body':
                    break
            re = self.reader.getParentOfWebElement(pEle)
            if re[0] == 1 and re[1] != None:
                pEle = re[1]
            else:
                break
        
        if crappy_element is not None:
            review_divs.append(crappy_element)
        else:
            for an_element in haha_i_found_yous:
                review_divs.append(an_element)
        
#		if f_xpath and s_xpath:
#			
#			i = 0
#			xpath1_len = len(f_xpath)
#			xpath2_len = len(s_xpath)
#			
#			while i < xpath1_len and i < xpath2_len:
#				if f_xpath[i] != s_xpath[i]:
#					xpath = f_xpath[:i]
#					break
#				i = i+1
#			
#			if xpath:
#				reviewXPaths = [xpath]
            
#		i = 0
#		review_divs = []
#		while i < len(reviewXPaths):
#			rd = reader.getElementsByXPath(reviewXPaths[i])
#			if rd:
#				review_divs = review_divs + rd
#			i = i +1
#		
        print reviewXPaths
        
        return review_divs
        
    
    def removeElementsAtWrongSideOfProduct(self, product_div, removeSideOnes, removeAboveProductDiv, removeBelowProductDiv):
        # driver should be already maximized for this part to work properly
        # because it utilizes window width and height
        #
        driver = self.reader.getDriver()
        divs = driver.find_elements_by_tag_name("div")
        shouldRemove = [0] * len(divs)
        window_size = driver.get_window_size()
        window_width = window_size['width']
        window_height = window_size['height']
        
        # find a div that does not contain product div 
        # and is of size 4 times greater than product div
        product_div_area = product_div.size['width'] * product_div.size['height']
        product_div_x1 = product_div.location['x']
        product_div_x2 = product_div_x1 + product_div.size['width']
        product_div_y1 = product_div.location['y']
        product_div_y2 = product_div_y1 + product_div.size['height']
        
        
        left_of_product = product_div_x1
        right_of_product = window_width - product_div_x2
        if (left_of_product <= right_of_product):
            remove_in = 'left'
        else:
            remove_in = 'right'
        
        
        side_divs = []
        i = -1
        for div in divs:
            i = i +1
            try:
                if False == div.is_displayed():
                    continue
            except Exception, e:
                print "Element not found when checking if it is displayed, assuming element not displayed and skipping\n"
                continue
                
            x1 = div.location['x']
            y1 = div.location['y']
            x2 = x1 + div.size['width']
            y2 = y1 + div.size['height']
            
            if div.size['width'] == 0 or div.size['height'] == 0:
                continue
            
            if removeSideOnes and ((remove_in == 'left' and x2 <= product_div_x1) or (remove_in == 'right' and product_div_x2 <= x1)):
                #side_divs.append(div)
                shouldRemove[i] = 1
            elif removeAboveProductDiv and (y2 <= product_div_y1):
                #side_divs.append(div)
                shouldRemove[i] = 1
            elif removeBelowProductDiv and (y1 >= product_div_y2):
                shouldRemove[i] = 1
        
        i =-1
        for div in divs:
            i = i+1
            if shouldRemove[i] == 1:
                self.reader.hideElement(div)
        
        
        #return side_divs
        return
    
    
    def getElementsBelowProduct(self, product_div):
        # driver should be already maximized for this part to work properly
        # because it utilizes window width and height
        #
        driver = self.reader.getDriver()
        divs = driver.find_elements_by_tag_name("div")
        window_size = driver.get_window_size()
        window_width = window_size['width']
        window_height = window_size['height']
        
        # find a div that does not contain product div 
        # and is of size 4 times greater than product div
        product_div_area = product_div.size['width'] * product_div.size['height']
        product_div_x1 = product_div.location['x']
        product_div_x2 = product_div_x1 + product_div.size['width']
        product_div_y1 = product_div.location['y']
        product_div_y2 = product_div_y1 + product_div.size['height']
        
        
        below_product_divs = []
        for div in divs:
            
            try:
                if False == div.is_displayed():
                    continue
            except Exception, e:
                print "Element not found when checking if it is displayed, assuming element not displayed and skipping\n"
                continue
                
            x1 = div.location['x']
            y1 = div.location['y']
            x2 = x1 + div.size['width']
            y2 = y1 + div.size['height']
            
            if div.size['width'] == 0 or div.size['height'] == 0:
                continue
            
            if product_div_y2 <= y1:
                below_product_divs.append(div)
        
        return below_product_divs
    
    
    def hideElementsBelowElement(self, ref_webele):
        
        dir = {'left' : 0, 'right': 0, 'top':0, 'bottom' : 0}
        self.hideElementsWithGivenDirections(ref_webele, dir)
    
    
    def hideElementsWithGivenDirs(self, ref_webele, dir):
        # driver should be already maximized for this part to work properly
        # because it utilizes window width and height
        #
        driver = self.reader.getDriver()
        divs = driver.find_elements_by_tag_name("div")
        window_size = driver.get_window_size()
        window_width = window_size['width']
        window_height = window_size['height']
        
        # find a div that does not contain product div 
        # and is of size 4 times greater than product div
        ref_webele_area = ref_webele.size['width'] * ref_webele.size['height']
        ref_webele_x1 = ref_webele.location['x']
        ref_webele_x2 = ref_webele_x1 + ref_webele.size['width']
        ref_webele_y1 = ref_webele.location['y']
        ref_webele_y2 = ref_webele_y1 + ref_webele.size['height']
        ref_webele_outer_html = readWebElementAttr(ref_webele, 'outerHTML')
        
        hide_below = hide_top = hide_left = hide_right = 0
        if ('below' in dir) and (dir['below']):
            hide_below = 1
        if ('top' in dir) and (dir['top']):
            hide_top = 1
        if ('left' in dir) and (dir['left']):
            hide_left = 1
        if ('right' in dir) and (dir['right']):
            hide_right = 1
        
        divs_to_hide = []
        for div in divs:
            
            hideable = False
            
            try:
                if False == div.is_displayed():
                    continue
            except Exception, e:
                print "Element not found when checking if it is displayed, assuming element not displayed and skipping\n"
                continue
                
            div_outer_html = readWebElementAttr(div, 'outerHTML')
            if div_outer_html in ref_webele_outer_html:
                continue
            
            x1 = div.location['x']
            y1 = div.location['y']
            x2 = x1 + div.size['width']
            y2 = y1 + div.size['height']
            
            if div.size['width'] == 0 or div.size['height'] == 0:
                continue
            
            if hide_below and (ref_webele_y2 <= y1):
                #below_ref_webele.append(div)
                #self.reader.hideElement(div)
                hideable = True
            
            if hide_top and (y2 <= ref_webele_y1):
                #below_ref_webele.append(div)
                #self.reader.hideElement(div)
                hideable = True
            
            if hide_left and (x2 <= ref_webele_x1 and y1 >= ref_webele_y1 and y2 <= ref_webele_y2):
                #below_ref_webele.append(div)
                #self.reader.hideElement(div)
                hideable = True
            
            if hide_right and (ref_webele_x2 <= x1 and y1 >= ref_webele_y1 and y2 <= ref_webele_y2):
                #below_ref_webele.append(div)
                #self.reader.hideElement(div)
                hideable = True
            
            if hideable:
                divs_to_hide.append(div)
            
        for div in divs_to_hide:
            self.reader.hideElement(div)
        
        return divs_to_hide
    
    
    def hideElementsOutsideElement(self, webele):
        
        if not webele:
            return []
        
        # driver should be already maximized for this part to work properly
        # because it utilizes window width and height
        #
        driver = self.reader.getDriver()
        divs = driver.find_elements_by_tag_name("div")
        shouldRemove = [0] * len(divs)
        
        window_size = driver.get_window_size()
        window_width = window_size['width']
        window_height = window_size['height']
        # find a div that does not contain product div 
        # and is of size 4 times greater than product div
        webele_x1 = webele.location['x']
        webele_x2 = webele_x1 + webele.size['width']
        webele_y1 = webele.location['y']
        webele_y2 = webele_y1 + webele.size['height']
        
        
        outside_divs = []
        i = -1
        for div in divs:
            i = i+1
            try:
                if False == div.is_displayed():
                    continue
            except Exception, e:
                print "Element not found when checking if it is displayed, assuming element not displayed and skipping\n"
                continue
                
            x1 = div.location['x']
            y1 = div.location['y']
            x2 = x1 + div.size['width']
            y2 = y1 + div.size['height']
            
            if div.size['width'] == 0 or div.size['height'] == 0:
                continue
            if (y1 >= 1.5*window_height):
                shouldRemove[i] = 1
            elif (x2 <= webele_x1) or (webele_x2 <= x1) or (y2 <= webele_y1) or (webele_y2 <= y1):
                #self.reader.hideElement(div)
                #outside_divs.append(div)
                 shouldRemove[i] = 1
        
        i = -1
        for div in divs:
            i = i+1
            if shouldRemove[i] == 1:
                self.reader.hideElement(div)
        
        return
        #return outside_divs
    
    
    def getOuterElementOfProduct(self, product_div):
        
        PD = PriceDecoder("", "")
        
        remove_sides = {'left' :0, 'right' : 0, 'top' : 0, 'below' : 0}
        
        driver = self.reader.getDriver()
        
        # find a div that does not contain product div 
        # and is of size 4 times greater than product div
        product_div_area = product_div.size['width'] * product_div.size['height']
        product_div_width = product_div.size['width']
        product_div_height = product_div.size['height']
        product_div_text = getAsciiText(product_div)
        if not product_div_text:
            product_div_text = ""
        product_div_text = nicely_clean_text(product_div_text)
        product_div_words = nicely_clean_word_list(product_div_text)
        product_div_words_len = len(product_div_words)
        
        outer_ele = None
        webele = product_div
        while True:
            re = self.reader.getParentOfWebElement(webele)
            if re and re[0]:
                webele = re[1]
            else:
                break
            
            div_width = webele.size['width']
            div_height = webele.size['height']
            
            if div_width == 0 or div_height == 0:
                continue
            
            webele_text = getAsciiText(webele)
            if not webele_text:
                webele_text = ""
            webele_text = nicely_clean_text(webele_text)
            webele_text_lower = webele_text.lower()
            webele_words = nicely_clean_word_list(webele_text)
            
            PD.reset(webele_text, "")
            text_is_with_price = PD.textHasPriceInIt()
            
            # is a product name appears in it
            if not self.tag_dict.isProductType(webele_text):
                continue
                
            #if (webele_text is not None) and (textHasPrice(webele_text)):
            #if (webele_text is not None) and (textHasDollarPrice(webele_text)):
            if (webele_text is not None) and (text_is_with_price):
                outer_ele = webele
                price_position = PD.getPricePosition()
                if price_position and (price_position > 10):
                    remove_sides['left'] = remove_sides['right'] = remove_sides['top'] = remove_sides['below'] = 1
                else:
                    remove_sides['left'] = remove_sides['right'] = remove_sides['below'] = 1
                break
            
            if (div_width > 1.2*product_div_width):
                if len(webele_words) > product_div_words_len + 10:
                    remove_sides['below'] = 1
                    outer_ele = webele
                    break        
                #if ("size" in webele_text_lower):
                #    size_present = 1
                #if ("qty" in webele_text_lower) or ("quantity" in webele_text_lower):
                #    qty_present = 1
            
            
            #if (div_width > 1.5*product_div_width):
            #    if len(webele_text) > len(product_div_text) + 10:
            #        remove_sides['left'] = remove_sides['right'] = remove_sides['below'] = 1
            #        outer_ele = webele
            #        break
        
        return {'outer_ele' : outer_ele, 'removable_sides' : remove_sides}
    
    def isSimilarProductDiv(self, div):
        
        div_text = getAsciiText(div)
        if not div_text:
            return False
        
        possible = False    
        div_text = clean_text(div_text).lower()
        div_words = [w for w in re.split('\W', div_text) if w]
        if len(div_words) == 2:
            if div_text.startswith("try this"):
                possible = True
            elif div_text.startswith("related items") :
                possible = True
            elif div_text.startswith("related products") :
                possible = True
            elif div_text.startswith("similar products") :
                possible = True
            elif div_text.startswith("similar items") :
                possible = True
                
        elif len(div_words) >= 3:
            if (div_words[0] == 'we') or (div_words[0] == 'customer') or (div_words[0] == 'customers') or (div_words[0] == 'people') or (div_text.startswith("guest")) or (div_text.startswith("you may")) or (div_text.startswith("you might")) or (div_text.startswith("you will")):
                i = 0
                while i < len(div_words) - 1:
                    i = i+1
                    if div_words[i] == "also":
                        next_word = div_words[i+1]
                        if next_word.startswith('love') or next_word.startswith('like') or next_word.startswith('bought') or next_word.startswith('shop') or next_word.startswith('buy') or next_word.startswith('view'):
                            possible = True
                        else:
                            return False
                    
        if div_text.startswith("frequently bought together") :
            possible = True
        elif div_text.startswith("our stylist love") :
            possible = True
        elif div_text.startswith("our stylist like") :
            possible = True
        elif div_text.startswith("our stylist recommend") :
            possible = True
        elif div_text.startswith("our recommendation") :
            possible = True
        else:
            div_width = div.size['width']
            div_height = div.size['height']
            if div_width and div_height and div_width <= 300 and (div_width *5 <= div_height):
                possible = True
        
        is_similar_item_div = False
        if possible:
            all_images_same_size = False
            
            images = div.find_elements_by_tag_name('img')
            image_wnhs = {}
            if images:
                for image in images:
                    image_wnhs[str(image.size['width']) + "_" + str(image.size['height'])] = 1
                if len(image_wnhs) == 1:
                    all_images_same_size = True
            if all_images_same_size:
                canvases = div.find_elements_by_tag_name('canvas')    
                if not canvases:
                    is_similar_item_div = True
        
        if is_similar_item_div:
            return True
        else:    
            return False
    
    
    def clean_distracting_divs(self):
        
        driver = self.reader.getDriver()
        divs = driver.find_elements_by_tag_name("div")
        #main_x1 = main_element.location['x']
        #main_y1 = main_element.location['y']
        #main_x2 = main_x1 + main_element.size['width']
        #main_y2 = main_y1 + main_element.size['height']
        distracting_divs = []
        
        for div in divs:
            try:
                if False == div.is_displayed():
                    continue
                
                div_w = div.size['width']
                div_h = div.size['height']
                if (0 == div_w) or (0 == div_h):
                    continue
                
                div_x1 = div.location['x']
                div_x2 = div_x1 + div_w
                div_y1 = div.location['y']
                div_y2 = div_y1 + div_h
                
                #if do_rectangles_intersect(div_x1, div_x2, div_y1, div_y2, main_x1, main_x2, main_y1, main_y2):
                #    continue
                
            except Exception, e:
                print "Element not found when checking if it is displayed, assuming element not displayed and skipping\n"
                continue
            
            if self.isSimilarProductDiv(div):# or self.isShareItem(div): ## gotta improve discovery of shareitem
                self.reader.hideElement(div)

        return
        
    def clearProductImgDiv(self):
        self.product_div = None
    
    def getProductImgDiv(self, banned_pimg_srces):
        
        # return the product div if already calculated
        if self.product_div:
            return self.product_div
        
        product_img_src = ""
            
        driver = self.reader.getDriver()
        divs = driver.find_elements_by_tag_name("img")
        ge = {}
        product_div = []
        max = 0
        for div in divs:
            
            displayed = True
            try:
                displayed = div.is_displayed()
            except StaleElementReferenceException, e:
                displayed = False
            
            if False == displayed:
                continue
            
            w = div.size['width']
            h = div.size['height']
            
            if w < 90 or h < 90:
                continue
            
            # we expect product image to be out there in the front, it shouldn't have y start after 500px.
            if div.location['y'] < 0 or div.location['y'] > 500: 
                continue
                            
            #if h < w:	# we are looking for a rectangle with height > width type of shape
            #	continue
            # if img src is banned then continue
            img_src = readWebElementAttr(div, 'src')
            if img_src in banned_pimg_srces:
                continue
            
            if w not in ge:
                ge[w] = {}
            if h not in ge[w]:
                ge[w][h] = []
                
            area = w*h
            ge[w][h].append([div, area])
            bin_size = len(ge[w][h])
            
            if  area> max:
                max = area
                product_div = div
                product_img_src = img_src
        
        # look for divs with background - image
        if not product_div:
            divs = driver.find_elements_by_tag_name("div")
            ge = {}
            product_div = []
            max = 0
            for div in divs:
                if False == div.is_displayed():
                    continue
                w = div.size['width']
                h = div.size['height']
                
                if w < 90 or h < 90:
                    continue
                
                bg_img_prop_val = readCssValue(div, 'background-image')
                bg_img_src = create_full_path_from_bgimage_prop(bg_img_prop_val, driver.current_url) if (bg_img_prop_val and ('none' != bg_img_prop_val)) else ""
                
                if not pointsToAnImage(bg_img_src):
                    continue
                
                # we expect product image to be out there in the front, it shouldn't have y start after 500px.
                if div.location['y'] < 0 or div.location['y'] > 500: 
                    continue
                            
                if bg_img_src in banned_pimg_srces:
                    continue
                
                if w not in ge:
                    ge[w] = {}
                if h not in ge[w]:
                    ge[w][h] = []
                
                area = w*h
                ge[w][h].append([div, area])
                bin_size = len(ge[w][h])
                
                if  area> max:
                    max = area
                    product_div = div   
                    product_img_src = bg_img_src
                    
        
        self.product_div = product_div	
        self.product_img_src = product_img_src
        self.product_tag = product_div.tag_name
        return product_div
                
    
    # Following 2 routines doesElementHasProductsListed and getProductsListed should move to site diver
    
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
     
    
    def getProductsListed():
        
        re = self.doesElementHasProductsListed(self, self.reader.getDriver())
        
        if re[0] == 0:
            return []
        else:
            pEle = re[1][0]
            parent_re = self.reader.getParentOfWebElement(pEle)
            while parent_re[0] == 1:
                pEle = parent_re[1]
                re = self.doesElementHasProductsListed(self, pEle)
                if re[0] > 0:
                    product_list = re[1]
                    return product_list;
                    
                parent_re = self.reader.getParentOfWebElement(self, pEle)
                
                
    
    def hideDistractingImages():
        
        driver = self.reader()
        divs = driver.find_elements_by_tag_name("img")
        for div in divs:
            div.get
        
    def removeHiddenDivs(self):
        
        driver = self.reader.getDriver()
        divs = driver.find_elements_by_tag_name('div')
        
        removeList = []
        
        for div in divs:
            if False == div.is_displayed():
                removeList.append(div)
                
        #self.removeElements(removeList)
        
        
    def removeOutgoingElements(self):
        self.reader.removeOutgoingElements()
         
                
    def recurseUpForHoldingContainer(self, div, conditions):
    
        driver = self.reader.getDriver()
        
        text = div.text.encode("ascii", "ignore")
        wordList = re.sub("[^\w]", " ",  mystr).split()
        conditions['words'] = len(wordList)
        
        if textHasPrice(text):
            conditions['price'] = 1
        
        hrefAttr = div.get_attribute('href')
        outLink = False
        if hrefAttr:
            if isOutgoingLink(driver.current_url, hrefAttr) == True:
                conditions['outgoingLinks'] = conditions['outgoingLinks'] + 1
        
        conditions['imageCount'] = len(div.find_elements_by_tag_name('img'))
        
        # check if div can not qualify by recursing up
        qualifies = True
        if conditions['words'] > 10:
            qualifies = False
            
        if conditions['outgoingLinks'] > 1:
            qualifies = False
            
        if conditions['imageCount'] > 1:
            qualifies = False
        
        if not qualifies:
            return False
        
        # check if parent qualify
        parentDiv = getParentOfWebElement(reader, div)
        re = recurseUpForHoldingContainer(self, parentDiv, conditions)
        if re:
            return re
        
        # if you came here, means the div can not qualify by going up, so 
        # check if the div itself qualifies
        if conditions['words'] < 10 and conditions['outgoingLinks'] == 1 and conditions['imageCount'] == 1:
            return div
        
        return False
        
        
    
    def findRelatedImageContainers(self):
        
        driver = self.reader.getDriver()
        imgs = driver.find_elements_by_tag_name('img')
        
        imgsOutgoingLinkHolders = []
        outgoingImgs = []
        
        print len(imgs)
        
        i = -1
        for img in imgs:
            i = i + 1
            parentWithOutgoingLink = None
            
            pImg = img
            re = [1, pImg]
            
            while True:
                print re
                if re[0] == 0:
                    parentWithOutgoingLink = None
                    break
                if re[0] == 1 and re[1] is None:
                    parentWithOutgoingLink = None
                    break
                    
                pImg = re[1]
                
                href = pImg.get_attribute('href')
                print href
                if href:
                    outgoingLink = isOutgoingLink(driver.current_url, href)
                    if outgoingLink:
                        print "-------------------matched--------------------------------"
                        parentWithOutgoingLink = pImg
                    else:
                        parentWithOutgoingLink = None
                    break
                
                if parentWithOutgoingLink:
                    imgsOutgoingLinkHolders.append(parentWithOutgoingLink)
                    outgoingImgs.append(imgs[i])
                    
                re = self.reader.getParentOfWebElement(pImg)
        
            
        imgs = outgoingImgs
        print imgs
        
        imgBySize = {}
        imgByX = {}
        imgByY = {}
        imgsSizeAndXAligned = {} 
        imgsSizeAndYAligned = {} 
        
        i = -1
        for img in imgs:
            i = i + 1
            size = img.size['width'] +'_'+img.size['height']
            if size in imgBySize:
                imgBySize[size].append(i)
            else:
                imgBySize[size] = []
                imgBySize[size].append(i)
            
            x = img.location['x']
            if x in imgByX:
                imgByX[x].append(i)
            else:
                imgByX[x] = []
                imgByX[x].append(i)
                
            y = img.location['y']
            if y in imgByY:
                imgByY[y].append(i)
            else:
                imgByY[y] = []
                imgByY[y].append(i)
                
            size_and_x = img.size['width'] +'_'+img.size['height'] + '_' + x
            size_and_y = img.size['width'] +'_'+img.size['height'] + '_' + y
            
            if size_and_x in imgsSizeAndXAligned:
                imgsSizeAndXAligned[size_and_x].append(i)
            
            if size_and_y in imgsSizeAndYAligned:
                imgsSizeAndYAligned[size_and_y].append(i)
            
        # for images in imgsSizeAndXAligned
        # find nearest common enclosing rectangle or nearest common ancestors
        
        NCAs = []
        
        for size_and_x in imgsSizeAndXAligned:
            imgList = imgsSizeAndXAligned[size_and_x]
            lenImgList = len(imgList)
            
            if lenImgList == 1:
                NCAs.append(imgs[imgsSizeAndXAligned[0]])
            
            if lenImgList > 1:
                p1 = imgs[imgsSizeAndXAligned[0]]
                p2 = imgs[imgsSizeAndXAligned[1]]
                p = 0	
                
                while True:
                    
                    innerhtml1 = p1.get_attribute('innerHTML')
                    innerhtml2 = p2.get_attribute('innerHTML')
                    if not innerhtml1:
                        break
                    if not innerhtml2:
                        break
                    if innerhtml1 == innerhtml2:
                        imagesInP = p.find_elements_by_tag_name('img')
                        if len(imagesInP) <= lenImgList:
                            NCAs.append(p1)
                        
                        break
                    
                    # if not empty innerhtmls that are not equal
                    
                    # we can do the following because both elements must be at the same level
                    # when they first start tracing to parents
                    # this is an assumption which should hold true and will hold true
                    re = self.reader.getParentOfWebElement(p1)
                    if re[0] == 1 and re[1] is not None:
                        p1 = re[1]
                    else:
                        break
                    
                    re = self.reader.getParentOfWebElement(p2)
                    if re[0] == 1 and re[1] is not None:
                        p2 = re[1]
                    else:
                        break
                    
            
        for size_and_y in imgsSizeAndYAligned:
            imgList = imgsSizeAndYAligned[size_and_y]
            lenImgList = len(imgList)
            
            if lenImgList == 1:
                NCAs.append(imgs[imgsSizeAndYAligned[0]])
            
            if lenImgList > 1:
                p1 = imgs[imgsSizeAndYAligned[0]]
                p2 = imgs[imgsSizeAndYAligned[1]]
                p = 0	
                
                while True:
                    
                    innerhtml1 = p1.get_attribute('innerHTML')
                    innerhtml2 = p2.get_attribute('innerHTML')
                    if not innerhtml1:
                        break
                    if not innerhtml2:
                        break
                    if innerhtml1 == innerhtml2:
                        imagesInP = p.find_elements_by_tag_name('img')
                        if len(imagesInP) <= lenImgList:
                            NCAs.append(p1)
                        
                        break
                    
                    # if not empty innerhtmls that are not equal
                    
                    # we can do the following because both elements must be at the same level
                    # when they first start tracing to parents
                    # this is an assumption which should hold true and will hold true
                    re = self.reader.getParentOfWebElement(p1)
                    if re[0] == 1 and re[1] !=0:
                        p1 = re[1]
                    else:
                        break
                    
                    re = self.reader.getParentOfWebElement(p2)
                    if re[0] == 1 and re[1] !=0:
                        p2 = re[1]
                    else:
                        break
                    
        
        for e in NCAs:
            driver.dimElement(e)
        
    
    def binSimilarTextCSSElements():
        
        
        driver = reader.getDriver()
        
        
            
            
    def pluckRelatedImages():
        
        re = self.doesElementHasProductsListed(self, self.reader.getDriver())
        
        if re[0] == 0:
            return []
        else:
            pEle = re[1][0]
            parent_re = self.reader.getParentOfWebElement(pEle)
            while parent_re[0] == 1:
                pEle = parent_re[1]
                re = self.doesElementHasProductsListed(self, pEle)
                if re[0] > 0:
                    product_list = re[1]
                    return product_list;
                    
                parent_re = self.reader.getParentOfWebElement(self, pEle)
        
        
    def removeElements(self, e_list):
        
        for e in e_list:
            self.reader.removeElement(e)
    
    def hideElements(self, e_list):
        
        for e in e_list:
            self.reader.hideElement(e)
    
    def getVisibleDivs(self):

        driver = self.reader.getDriver()
        
        divs = driver.find_elements_by_tag_name("div")
        visibleDivs = []
        
        for div in divs:
            if div.is_displayed() == True:
                o = self.reader.getOpacity(div)
                if o <= 0.2:
                    continue
                else:
                    visibleDivs.append(div)
            
        return visibleDivs
        
    def leafsYSorted(self, divs):
        
        driver = self.reader.getDriver()
        
        #divs = driver.find_elements_by_tag_name("div")
        leafDivs = []
        yMap = {}
        ys = []
        for div in divs:
            if self.reader.isLeaf(div) == 1:
                leafDivs.append(div)
                y = div.location['y']
                if y not in yMap:
                    yMap[y] = []
                yMap[y].append(div)
                ys.append(y)
                if div.text:
                    print div.text.encode("ascii", "ignore")
        
        return None
                
        
        ySortedDivs = {}
        
        ys = sorted(ys)
        unique_ys = []
        
        prev_y = ys[0]
        unique_ys.append(ys[0])
        i = 1
        while i < len(ys):
            if prev_y != ys[i]:
                unique_ys.append(ys[i])
                prev_y = ys[i]
            i = i +1
        
        i = 0
        stacked_divs = []
        while i < len(unique_ys):
            for ey in yMap[unique_ys[i]]:
                if ey.text:
                    s = ey.text.encode("ascii","ignore")
                    stacked_divs.append([unique_ys[i], ey])
            i = i +1
        #print ys
        #print yMap
        return stacked_divs
        #return yMap
        #return leafdivs
        
    def sortByDistanceFromProduct(self, product_div):
        
        driver = self.reader.getDriver()
        
        
        # find a div that does not contain product div 
        # and is of size 4 times greater than product div
        pdiv_area = product_div.size['width'] * product_div.size['height']
        pdiv_x1 = product_div.location['x']
        pdiv_x2 = product_div_x1 + product_div.size['width']
        pdiv_y1 = product_div.location['y']
        pdiv_y2 = product_div_y1 + product_div.size['height']
        
        
        for div in divs:
            
                
            o = reader.getOpacity(div)
            if o <= 0.2:
                continue
            
                x1 = div.location['x']
                y1 = div.location['y']
                x2 = x1 + div.size['width']
                y2 = y1 + div.size['height']
                
                dist = 1000000
                
                
                if x1 >= pdiv_x2 and (not ((y2 <= pdiv_y1) or (y1 >= pdiv_y2))):
                    dist = x1 - pdiv_x2
                elif x2 <= pdiv_x1 and (not ((y2 <= pdiv_y1) or (y1 >= pdiv_y2))):
                    dist = pdiv_x1 - x2
                elif y2 <= pdiv_y1 and (not ((x2 <= pdiv_x1) or (x1 >= pdiv_x2))):
                    dist = pdiv_y1 - y2
                elif y1 >= pdiv_y2 and (not ((x2 <= pdiv_x1) or (x1 >= pdiv_x2))):
                    dist = pdiv_y2 - y1
                #else:
                #	minX = min(x1-
                    
    
    def decodeDetails(self, stacked_divs, product_div):
    
        driver = self.reader.getDriver()
        
        
        # find a div that does not contain product div 
        # and is of size 4 times greater than product div
        pdiv_area = product_div.size['width'] * product_div.size['height']
        pdiv_x1 = product_div.location['x']
        pdiv_x2 = product_div_x1 + product_div.size['width']
        pdiv_y1 = product_div.location['y']
        pdiv_y2 = product_div_y1 + product_div.size['height']
    
        
        # title should come before the price
        # look for price to for title bound
        
        #for y_div in stacked_divs:
        #	if y_t
        
    def test():
        #p = ProductListingPage("http://shop.nordstrom.com/s/burberry-london-woven-silk-tie/3189709?origin=fashionresultspreview")
        p = ProductListingPage(sys.argv[1])
        review_divs = p.findReviewUsingLiguisticHints()
        exit()
        p.removeHiddenDivs()
        p.removeOutgoingElements()
        #p.findRelatedImageContainers()
        product_div = p.getProductImgDiv({})
        review_divs = p.detectReviews(product_div)
        belowReviewDivs = p.thingsBelowReviewDivs(review_divs)
        p.hideElements(review_divs)
        p.hideElements(belowReviewDivs)
        divs = p.getVisibleDivs()
        stacked_divs = p.leafsYSorted(divs)
        print stacked_divs