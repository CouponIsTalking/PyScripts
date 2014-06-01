#
# Grab pages of companies from foreign coupon stores
#
import sys
import urllib
import urllib2
import json

from web_interface import *
from const import *
from SeleniumReader import *
from GetCompInfo import *

class FCPLinks(object):
    def __init__(self,cid=0):
        self.gci = GetCompInfo()
        self.wi = WebInterface()
        self.reader = SeleniumReader("")
        self.reader.getDriver().maximize_window()
        self.cid = cid
        self.cinfo = {'name':'', 'website':''}
        self.fcp_info = {}
        
        # set configuration
        self.enabled_sites = []
        
        # things specific to individual deals or coupons site
        self.dealstobuy_links = {}
        
    def deinit(self):
        self.reader.deinit()
    
    def reinit(self, cid):
        self.gci = GetCompInfo()
        self.wi = WebInterface()
        #self.reader.moveTo("about:blank")
        #self.reader.deinit()
        #self.reader = SeleniumReader("")
        #self.reader.getDriver().maximize_window()
        self.cid = cid
        self.cinfo = {'name':'', 'website':''}
        self.fcp_info = {}
        
        # set configuration
        self.enabled_sites = []
        
        # things specific to individual deals or coupons site
        #self.dealstobuy_links = {} # dont reinit this, this is persistent info
        
    def set_cid(self, cid):
        self.cid = cid
    
    def set_enabled_sites(self, sites):
        self.enabled_sites = []
        for site in sites:
            if "deals2buy.com" == site:
                self.get_preprocess_for_dealstobuy()
            self.enabled_sites.append(site)
        
        return
    
    def get_fcp_coupons_dot_com_link(self):
        if (not self.cinfo['name']) or (not self.cinfo['website']):
            return ""
        self.reader.moveTo("http://www.coupons.com/coupon-codes")
        q_eles = self.reader.getElementsById('query')
        if not q_eles:
            return ""
        
        name = self.cinfo['name'].replace("WWW1.","www.").replace("www1.", "www.")
        if name.startswith('http://'):
            name = name[7:]
        elif name.startswith('https://'):
            name = name[8:]
        else:
            pass
        
        parts = name.split('.')
        if parts[-1] == 'com':
            name = parts[-2]
        
        q_eles[0].send_keys(name)
        time.sleep(2)
        drop_down_menu_eles = self.reader.getElementsByClassName('tt-dropdown-menu')
        if not drop_down_menu_eles:
            return ""
        
        try:
            li_eles = drop_down_menu_eles[0].find_elements_by_tag_name('li')
        except:
            return ""
        
        if not li_eles:
            return ""
        try:
            li_eles[0].click()
        except:
            return ""
        
        return self.reader.getDriver().current_url


    def get_fcp_retailmenot_dot_com_link(self):
        if (not self.cinfo['name']) or (not self.cinfo['website']):
            return ""
        self.reader.moveTo("http://www.retailmenot.com")
        q_eles = self.reader.getElementsById('query')
        if not q_eles:
            return ""
        
        web = self.cinfo['website'].replace("WWW1.","www.").replace("www1.", "www.")
        if web.startswith('http://'):
            web = web[7:]
        elif web.startswith('https://'):
            web = web[8:]
        else:
            pass
        
        q_eles[0].click()
        q_eles[0].send_keys(web)
        time.sleep(2)
        form_re = self.reader.getParentOfWebElement(q_eles[0])
        if form_re[0] and form_re[1]:
            form = form_re[1]
            try:
                btn = form.find_element_by_tag_name('button')
                clicked = btn.click() if btn else 0
                return self.reader.getDriver().current_url
            except:
                pass
        
        return ""
        
    def get_preprocess_for_dealstobuy(self):
        if not self.dealstobuy_links:
            self.reader.moveTo("http://www.deals2buy.com/stores")
            uls = self.reader.getElementsByClassName("store-list")
            for ul in uls:
                lis = ul.find_elements_by_tag_name("li")
                text = getAsciiText(lis[0])
                text = text.lower() if text else text
                link_ele = lis[0].find_element_by_tag_name("a")
                link = readWebElementAttr(link_ele, 'href')
                link = link.lower() if link else link
                if link and text:
                    self.dealstobuy_links[text] = link.encode("ascii", "ignore")
        
    def get_fcp_dealstobuy_dot_com_link(self):
        if (not self.cinfo['website']):
            return ""
        website = self.cinfo['website']
        
        if self.dealstobuy_links:
            sites = self.gci.get_approximate_sites(website)
        
        for site in sites:
            if site in self.dealstobuy_links:
                return self.dealstobuy_links[site]
        return ""
    
    def get_fcp_slickdeals_dot_net_link(self):
        pass
    def get_fcp_dealsofamerica_dot_com_link(self):
        pass
        
    def init_fcplink_retrv(self, cid=0):
        l_gci = GetCompInfo()
        if not cid:
            cid = self.cid
        
        cinfo = l_gci.get_company_info(cid)
        self.cinfo = cinfo
        self.fcp_info[cid] = {'retailmenot.com':'','coupons.com':'','dealshark.com':'','deals2buy.com':''}
        for a_site in self.enabled_sites:
            if "retailmenot.com" == a_site:
                self.fcp_info[cid]['retailmenot.com'] = self.get_fcp_retailmenot_dot_com_link()
            elif "coupons.com" == a_site:
                self.fcp_info[cid]['coupons.com'] = self.get_fcp_coupons_dot_com_link()
            elif "deals2buy.com" == a_site:
                self.fcp_info[cid]['deals2buy.com'] = self.get_fcp_dealstobuy_dot_com_link()
    
    def update_fcplink(self):
        cid = self.cid
        for store_name in self.fcp_info[cid]:
            cpl = self.fcp_info[cid][store_name]
            if not cpl:
                continue
            response_page = ""
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = { 'User-Agent' : user_agent }
            url =  SITE_NAME + "/fcparser_infos/update_fcp_info"
            data = {'cid' : self.cid, 'pcode':PYTHON_VERIFICATION_CODE, 'store_name':store_name,'cpl':cpl}
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
            print ret_info
        
        return True