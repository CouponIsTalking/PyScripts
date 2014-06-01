#
# Grab coupons given coupon page link for 
# companies on foreign stores, for e.g. given link of MACYS
# on retailmenot.com and coupons.com, grab MACYS coupons
#
import sys
import urllib
import urllib2
import json

from web_interface import *
from const import *
from SeleniumReader import *

class FCGrabber(object):
    def __init__(self,cid=0):
        self.wi = WebInterface()
        self.reader = SeleniumReader("")
        self.cid = cid
        self.fcp_entries = None
    
    def deinit(self):
        self.reader.deinit()
    
    def set_cid(self, cid):
        self.cid = cid
    
    def get_from_krazy_coupon_lady(self):
        ###
        return {}
    
    def get_from_deals_to_buy_dot_com(self):
        # maximize window
        self.reader.getDriver().maximize_window()
        
        if "deals2buy.com" in self.fcp_entries:
            coupon_page = self.fcp_entries["deals2buy.com"]
            self.reader.moveTo(coupon_page)
        
        # get list of tabs
        lis = self.reader.getElementsByClassName("tab")
        if not lis:
            return None
        
        coupon_tab_found = False
        i = 0
        while i < len(lis):
            li_tab_text = getAsciiText(lis[i])
            if li_tab_text.lower().find("coupons") >= 0:
                lis[i].click()
                coupon_tab_found = True
                break
            i=i+1
        
        if not coupon_tab_found:
            return None
        # find the "Coupons" tab and click on that
        #li_tab_text = getAsciiText(lis[1])
        #if li_tab_text.lower().find("coupons") == -1:
        #    return None
        #else:
        #    lis[1].click()
        
        # find the coupon table now
        webeles = self.reader.getElementsByClassName("coupons-table")
        
        if not webeles:
            print "Coupon table not found"
            return None
        
        # find all coupon rows in coupon table
        coupon_lists = webeles[0].find_elements_by_tag_name("tr")
        if not coupon_lists:
            print "Coupon lists not found"
            return None
        
        coupons = {}
        next_line_index = 0
        total_coupon_lines = len(coupon_lists)
        title=""
        desc=""
        code=""
        while next_line_index < total_coupon_lines:
            next_line_index = next_line_index + 1
            code = 0
            desc = ""
            title = ""
            # find coupon-code class element in the row
            try:
                innerHTML = readWebElementAttr(coupon_lists[next_line_index-1],'innerHTML')
                if "coupon-code" in innerHTML:
                    code_ele = coupon_lists[next_line_index-1].find_element_by_class_name("coupon-code")
                    if code_ele:
                        code = getAsciiText(code_ele)
            except:
                print "error while looking for element with class name 'coupon-code'"
            
            # if code not found, then continue onto next row
            if not code:
                continue
            
            # otherwise find the coupon line and expiry date
            tds = 0
            try:
                tds = coupon_lists[next_line_index-1].find_elements_by_tag_name("td")
            except:
                print "error while looking for 'td' elements inside a 'tr' elements"
            
            if tds:
                title = getAsciiText(tds[0])
                exp_date = getAsciiText(tds[3])
                desc = title + " Expires " + exp_date
                if title and desc and code:
                   coupons[code] = {'title':title, 'desc':desc, 'code':code}
        
        #delete coupon list
        del coupon_lists[:]
        #return coupons map
        return coupons
        
    def get_from_coupons_dot_com(self):
        if "coupons.com" in self.fcp_entries:
            self.reader.moveTo(self.fcp_entries['coupons.com'])
        
        webeles = self.reader.getElementsByClassName('new-pods')
        if not webeles:
            return None        
        
        coupons = {}
        driver = self.reader.getDriver()
        coupon_btns = webeles[0].find_elements_by_class_name('btn-block')
        if not coupon_btns:
            return None
        
        next_btn_index = 0
        title = ""
        desc = ""
        code = ""                
        while next_btn_index < len(coupon_btns):
            btn = coupon_btns[next_btn_index]
            btn_text = btn.text.encode("ascii","ignore")
            if "Get Code" != btn_text:
                next_btn_index = next_btn_index + 1
                continue
            
            btn.find_element_by_tag_name('a').click()
            time.sleep(3);
            # get handle to new window to grab coupon info
            new_window_handle = driver.window_handles[1]
            driver.switch_to_window(new_window_handle)
            try:
                iframe = driver.find_element_by_class_name('mfp-iframe')
                driver.switch_to_frame(iframe)
                code_ele = driver.find_element_by_class_name('offer-code-b')
                desc_ele = driver.find_element_by_class_name('offer-details-b-code')
                title_ele = driver.find_element_by_class_name('offer-info-b')
                # get text
                code = code_ele.text if code_ele else ""
                desc = desc_ele.text if desc_ele else ""
                title = title_ele.text if title_ele else ""
                if title and desc and code:
                    coupons[code] = {'title':title, 'desc':desc, 'code':code}
                
                driver.switch_to_default_content()
            except:
                pass
            
            # close all windows
            i=1
            while i < len(driver.window_handles):
                driver.switch_to_window(driver.window_handles[i])
                driver.close()
                i=i+1
            
            # go to the main window
            driver.switch_to_window(driver.window_handles[0])
            driver.back()
            try:
                del webeles[:]
                del coupon_btns[:]
                webeles = self.reader.getElementsByClassName('new-pods')
                coupon_btns = webeles[0].find_elements_by_class_name('btn-block')
            except:
                print "Exception while grabbing new-pods and btn-block"
                break
            next_btn_index = next_btn_index + 1
                
        del coupon_btns[:]
        return coupons
        
    def get_from_retailmenot_dot_com(self):
        
        if "retailmenot.com" not in self.fcp_entries:
            return None
        self.reader.moveTo(self.fcp_entries['retailmenot.com'])
        webeles = self.reader.getElementsByClassName('popular')
        if not webeles:
            return None
        coupons = {}
        div_webeles = webeles[0].find_elements_by_tag_name('div')
        del webeles[:]
                
        for webele in div_webeles:
            data_type_val = readWebElementAttr(webele, 'data-type')
            if 'code' == data_type_val:
                title = ""
                desc = ""
                code = ""
                try:
                    title_ele = webele.find_element_by_tag_name('h3')
                    title = title_ele.text if title_ele else ""
                    desc_ele = webele.find_element_by_class_name('description-wrapper')
                    desc = desc_ele.text if desc_ele else ""
                    code_ele = webele.find_element_by_class_name('code-text')
                    code = code_ele.text if code_ele else ""
                except:
                    pass
                
                if title and desc and code:
                    coupons[code] = {'title':title, 'desc':desc, 'code':code}
        
        del div_webeles[:]
        return coupons
    
    def get_fcparser_info(self):
        response_page = ""
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        url =  SITE_NAME + "/fcparser_infos/get_fcp_info"
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
        else: return False
        fcp_info = json.loads(response_page)
        entries = {}
        for entry in fcp_info:
            coupon_page_link = entry['FcparserInfo']['coupon_page_link'].encode("ascii", "ignore");
            coupon_store = entry['FcparserInfo']['store_name'].encode("ascii", "ignore");
            entries[coupon_store] = coupon_page_link
        
        self.fcp_entries = entries
        return entries
        
        

