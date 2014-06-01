from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import *   
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.keys import Keys
import math
import datetime
import time
from datetime import date
from datetime import datetime
import re

import BeautifulSoup
from BeautifulSoup import BeautifulSoup, Comment
from htmlops import *
from misc import *

import hashlib

from const import *

import web_interface
#import db_connection
import selenium_extra_ops


def readCssValue(we, attr):
    try:
        attr_v = we.value_of_css_property(attr)
        return attr_v.encode("ascii", "ignore")
    except Exception, e:
        print "!!! Error reading " + attr + " css property of web element "
        print e
        return None


def readWebElementAttr(we, attr):
    try:
        attr_v = we.get_attribute(attr)
        return attr_v
        
    except Exception, e:
        print "!!! Error reading " + attr + " of web element "
        print e
        return None

def getAsciiText(we):
    text = getWebElementText(we)
    if text != None:
        text = text.encode("ascii", "ignore")
    return text
    
def getWebElementText(we):
    try:
        text = we.text
        return text
        
    except Exception, e:
        print "!!! Error reading text of web element "
        print e
        return ""

        
class SeleniumReader:
    def __init__(self, url, page_load_timeout = 0):
        self.driver = webdriver.Firefox()
        
        if page_load_timeout > 0:
            self.driver.set_page_load_timeout(page_load_timeout)
        
        if url:
            self.driver.get(url)
            self.driver.implicitly_wait(10) # set implicit timeout of 10 secs for find element methods
            self.valid_page = 1
        else:
            self.valid_page = 0
        self.verbose = 1;
        
    def moveTo(self, url):
        if url:
            self.driver.get(url)
            self.driver.implicitly_wait(10) # set implicit timeout of 10 secs for find element methods
            self.valid_page = 1
        else:
            self.valid_page = 0
        return self
    
    def isValid(self):
        return self.valid_page
    
    def getDriver(self):
        return self.driver
        
    def getPageSource(self):
        source = self.driver.page_source
        #print element
        return source
        
    def getElementByXPath(self, xpath):
        elements = []
        try :
            elements = self.driver.find_element_by_xpath(xpath)
        except Exception, e:
            if self.verbose:
                print "selection by xpath " + xpath + " failed\n"
                print e
            #return 0
            
        #print element
        return elements

    def getElementsByXPath(self, xpath):
        elements = []
        try :
            elements = self.driver.find_elements_by_xpath(xpath)
        except Exception, e:
            print "selection by xpath " + xpath + " failed\n"
            print e
            #return 0
            
        #print element
        return elements
        
    def getElementsByLinkText(self, link_text):
        elements = []
        try :
            elements = self.driver.find_elements_by_link_text(link_text)
        except Exception, e:
            print "selection by xpath " + xpath + " failed\n"
            print e
            #return 0
            
        #print element
        return elements
        
    def getElementsByCSSSelector(self, css_selector):
        #elements = self.driver.find_elements_by_css_selector(css_selector)
        elements = []
        try:
            elements = self.driver.find_elements_by_css_selector(css_selector)
        except Exception, e:
            print "selection by "+css_selector+ " failed\n"
            print e
            #return 0;
            
        #for e in elements:
        #	print e.text
        #print elements
        return elements
        
    def getElementsByClassName(self, classname):
        elements = []
        try:
            elements = self.driver.find_elements_by_class_name(classname)
        except Exception, e:
            print "selection by class name " + classname + " failed\n"
            print e
            #return 0;
        #for e in elements:
        #	print e.text
        #print elements
        return elements
        
    def getElementsByTagName(self, tagname):
        elements = []
        try:
            elements = self.driver.find_elements_by_tag_name(tagname)
        except Exception, e:
            print "selection by tag name " + tagname + " failed\n"
            print e
            #return 0;
        #for e in elements:
        #	print e.text
        #print elements
        return elements

    def getElementsById(self, id):
        elements = []
        try:
            elements = self.driver.find_elements_by_id(id)
        except Exception, e:
            print "selection by class name " + id + " failed\n"
            print e
            #return 0;
        #for e in elements:
        #	print e.text
        #print elements
        return elements
    
    def isLeaf(self, webEle):
        
        tag = webEle.get_attribute("tagName").encode("ascii", "ignore")
            
        js = "if (arguments[0].childNodes.length) return 1; else return 0;"
        result = self.jsexcute(js, webEle)
        if result[1] != None:
            return result[1]
        else:
            return 0
    
    def getChildren(self, webEle):
        
        tag = webEle.get_attribute("tagName").encode("ascii", "ignore")
            
        js = " return arguments[0].children;"
        result = self.jsexcute(js, webEle)
        if result[1] != None:
            return result[1]
        else:
            return 0
    
    def isRemovableOutgoingElement(self, div, curl):
        
        try:
            if (0 == div.size['width']) or (0 == div.size['height']):
                return False
            
            div_url = div.get_attribute('href')
            if isOutgoingLink(curl, div_url) == True and pointsToAnImage(div_url) == False:
                return True
        except StaleElementReferenceException, e:
            print e
        except Exception, e:
            print e # it may be a remote connection close error
            
            #self.reader.removeElement(div)
            #self.reader.dimElement(div, 0.2)
            #self.hideElement(div)
            #driver.execute_script("arguments[0].style.display='none';", div)
        
        return False
    
    def removeOutgoingElements(self):#, keepPurelyImageItems = True):
        
        driver = self.driver
        curl = driver.current_url
        divs = driver.find_elements_by_tag_name('div')
        
        for div in divs:
            if True == self.isRemovableOutgoingElement(div, curl):
                self.hideElement(div)
        
        divs = driver.find_elements_by_tag_name('a')
        for div in divs:
            if True == self.isRemovableOutgoingElement(div, curl):
                self.hideElement(div)
        
        divs = driver.find_elements_by_tag_name('img')
        for div in divs:
            if True == self.isRemovableOutgoingElement(div, curl):
                self.hideElement(div)
    
    
    # returns [couldDecodeParentNode?, parentNode]
    # valid return values :
    # [1,0] - No parent
    # [1, parentWebElement] 
    # [0] - Could not find parent
    # <body> element is considered root
    def getParentOfWebElement(self, webEle):
        
        tag = webEle.get_attribute("tagName").encode("ascii", "ignore")
        if tag:
            if tag.lower() == "body":
                return [1, None]
            
        js_for_parent_element = "if (arguments[0].parentNode == null) return 0; else return arguments[0].parentNode;"
        result = self.jsexcute(js_for_parent_element, webEle)
        return result
        
    # considers <body> element as root element.
    # does not removes <body> elements
    # otherwise, will remove given element using it parentNode
    #
    def removeElement(self, webEle):
        result = 0
        try:
            tag = webEle.get_attribute("tagName").encode("ascii", "ignore")
            print tag
            if tag:
                if tag.lower() == "body":
                    return [0, None]
            
            js_for_removing_element = "return (elem=arguments[0]).parentNode.removeChild(elem);"
            result = self.jsexcute(js_for_removing_element, webEle)
        except Exception, e:
            print "Error while removing element, possibly because the element is already removed\n"
            
        return result

    def dimElement(self, e, opacity_value):
        if opacity_value < 1:
            js = "arguments[0].style.opacity='0.2'"
        else:
            js = "arguments[0].style.opacity='1'"
        
        self.jsexcute(js, e)
    
    def getOpacity(self, e):
        js = "return arguments[0].style.opacity;"
        re = self.jsexcute(js, e)
        if re[0] == 1:
            return re[1]
        else:
            return 0;
        
    def hideElement(self, e):
        js = "arguments[0].style.display='none';"
        self.jsexcute(js, e)

    def showElement(self, e):
        js = "arguments[0].style.display='block';"
        self.jsexcute(js, e)


    def dimOpacityFromXpath(self, xpaths, opacity_value):
        
        for xpath in xpaths:
            try:
                eles = self.getElementByXPath(xpath)
            except Exception, e:
                print "exception while looking for " + xpath
                print e
            try:
                for e in eles:
                    self.dimElement(js, e, opacity_value)
            except Exception, e:
                print "exception while dimming for " + xpath
                print e

    def hideElementsFromXpath(self, xpaths):
        
        for xpath in xpaths:
            try:
                eles = self.getElementByXPath(xpath)
            except Exception, e:
                print "exception while looking for " + xpath
            try:
                for e in eles:
                    self.hideElement(js, e)
            except Exception, e:
                print "exception while hiding for " + xpath

    def showElementsFromXpath(self, xpaths):
        
        for xpath in xpaths:
            try:
                eles = self.getElementByXPath(xpath)
            except Exception, e:
                print "exception while looking for " + xpath
            try:
                for e in eles:
                    self.showElement(js, e)
            except Exception, e:
                print "exception while hiding for " + xpath

    
    def jsexcute(self, js, webEle):
        
        #self.driver.implicitly_wait(1)
        
        try:
            result = self.driver.execute_script(js, webEle);
            return [1, result];
        except Exception, e:
            print "Error executing Javascript"
            return [0, None];
    
    # does not work as of now
    #
    def getCssSelector(self, webEle):
    
        js = " // start " \
        "	function fullPath(el){" \
        "		var names = [];" \
        "		while (el.parentNode)" \
        "		{" \
        "			if (el.id)" \
        "			{" \
        "				names.unshift('#'+el.id);" \
        "				break;" \
        "			}" \
        "			else" \
        "			{" \
        "				if (el==el.ownerDocument.documentElement) " \
        "				{" \
        "					names.unshift(el.tagName);" \
        "				}" \
        "				else" \
        "				{" \
        "					for (var c=1,e=el;e.previousElementSibling;e=e.previousElementSibling,c++);" \
        "					{" \
        "						names.unshift(el.tagName+\":nth-child(\"+c+\")\");" \
        "					}" \
        "				}" \
        "				el=el.parentNode;" \
        "			}" \
        "		}" \
        "		return names.join(' > ');" \
        "	}" \
        "  ele = arguments[0];	" \
        "  return fullPath(ele); " \
        " // end ";
        
        return self.jsexcute(js, webEle);
        
    
    def adjustCurSymbol(self):
        body_eles = self.getElementsByTagName("body")
        if not body_eles: return
        
        for ele in body_eles:
            oh = ele.get_attribute("outerHTML")
            if not oh: continue
            neat_oh = oh
            replace_lines = []
            replace_lines.append("<span class=\"WebRupee\">`</span>")
            replace_lines.append("<span class=\"WebRupee\"></span>")
            replace_lines.append("<span class=\"WebRupee\"> </span>")
            replace_lines.append("<span class='WebRupee'>`</span>")
            replace_lines.append("<span class='WebRupee'></span>")
            replace_lines.append("<span class='WebRupee'> </span>")
            for rl in replace_lines:
                neat_oh = neat_oh.replace(rl, "INR ")
            
            if neat_oh != oh:
                s = "arguments[0].outerHTML = \""+ re.escape(neat_oh)+"\";"
                self.jsexcute(s, ele)
    
    def deinit(self):
        self.driver.quit()

    def testReader(self):
        print "I am in Selenium Reader";