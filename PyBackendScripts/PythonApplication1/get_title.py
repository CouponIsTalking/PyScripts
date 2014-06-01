from selenium import webdriver
import sys
import json
import urllib2
import lxml.html
            
url = sys.argv[1]
title = ""
use_selenium = False
use_lxml = False

try :
    req = urllib2.Request(url, None, {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
    response = urllib2.urlopen(req)
    response_page = response.read()
    if response: response.close()
    t = lxml.html.fromstring(response_page)
    title = t.find(".//title").text
    if not title:
        title_start = response_page.index("<title>")
        title_end = response_page.index("</title>")
        if title_start and title_end:
            title = title[title_start+7:title_end].strip()
except :
    a = 1
    
if not title and (use_lxml):
    try:
        t = lxml.html.parse(url)
        title = t.find(".//title").text
    except:
        a = 1

if (not title) and (use_selenium == True):
    driver = webdriver.Firefox()
    driver.get(url)
    title = driver.title

if title:
    print json.dumps({'title': title})


