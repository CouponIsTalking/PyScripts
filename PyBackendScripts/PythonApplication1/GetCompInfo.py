#
# Given a company id, get company info
#
import sys
import urllib
import urllib2
import json

from web_interface import *
from const import *
from SeleniumReader import *

class GetCompInfo(object):
    def __init__(self,cid=0):
        self.cid = cid
        self.info = {'name':'', 'website':''}
    
    def deinit(self):
        pass
    
    def get_approximate_sites(self, site):
        approx_sites = []
        site = site.lower()
        if site.startswith("www."):
            site_without_www = site[4:]
        else:
            site_without_www = site
        
        site_with_www = "www."+site_without_www
        approx_sites = [site_without_www, site_with_www]
        
        site_parts = site_without_www.split(".")
        if len(site_parts)==3:
            site_main_domain = site_parts[1] +"."+site_parts[2]
            approx_sites.append(site_main_domain)
            approx_sites.append("www." + site_main_domain)
        
        return approx_sites
    
    def get_company_info(self, cid):
        self.cid = cid
        response_page = ""
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        url =  SITE_NAME + "/companies/get_cinfo_for_parsing"
        data = {'cid' : self.cid, 'pcode':PYTHON_VERIFICATION_CODE}
        req = urllib2.Request(url, urllib.urlencode(data), headers)
        
        response_page = ""
        response = None
        try :
            response = urllib2.urlopen(req)
            response_page = response.read()            
        except:
            pass
        
        if response: response.close()
        ret_info = json.loads(response_page)
        if ret_info:
            self.info['name'] = ret_info['name'].encode("ascii", "ignore");
            self.info['website'] = ret_info['website'].encode("ascii", "ignore");
        
        return self.info
        
        

