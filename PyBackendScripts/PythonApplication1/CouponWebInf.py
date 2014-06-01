import json
import urllib
import urllib2

from const import *

class CouponWebInf(object):
    def __init__(self):
        pass
    def deinit(self):
        pass
    def log_coupon_details(self, coupon_info):
        print json.dumps(coupon_info)
        return
    def update_coupon_details(self, coupon_info):
        if 'company_id' not in coupon_info:
            print "Company Id not given"
            return
        if 'coupon_type' not in coupon_info:
            print "Coupon type not given"
            return
        if 'coupon_code' not in coupon_info:
            print "Coupon code not given"
            return
        if 'coupon_worth' not in coupon_info:
            print "Coupon worth not given"
            return
        if 'coupon_cur_code' not in coupon_info:
            print "Coupon currency not given"
            return
        if 'coupon_title' not in coupon_info:
            print "Coupon title not given"
            return
        if 'coupon_detail' not in coupon_info:
            print "Coupon detail not given"
            return
        if 'valid_until_date' not in coupon_info:
            print "Expiry date not given"
            return
        if 'coupon_source' not in coupon_info:
            print "Coupon source not given"
            return
        coupon_info['pcode'] = PYTHON_VERIFICATION_CODE
        
        response_page = ""
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        url =  SITE_NAME + "/coupon_infs/scr_update_coupon_info"
        #data = {'cid' : self.cid, 'pcode':PYTHON_VERIFICATION_CODE, 'store_name':store_name,'cpl':cpl}
        req = urllib2.Request(url, urllib.urlencode(coupon_info), headers)
            
        response_page = ""
        response = None
        try :
            response = urllib2.urlopen(req)
            response_page = response.read()            
        except:
            print self.log_coupon_details(coupon_info);
            
        if response: response.close()
        ret_info = json.loads(response_page)
        print ret_info


