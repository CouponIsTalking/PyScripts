from web_interface import *
from const import *

class GenPriceNotf(object):
    def __init__(self, pid):
        self.pid = pid
        self.wi = WebInterface()
    def deinit(self):
        pass
    
    def generate_notifications(self):
        product_info = self.get_product_info()
        if not product_info:
            print "Product info not found for product-id:" + str(self.pid)
            return False
        
        user_ids = self.get_tracking_users()
        if not user_ids:
            print "No one tracking product-id:" + str(self.pid)
            return True
        
        #user_ids = ""
        #for user in tracking_users:
        #    user_ids = user_ids + "," + str(user['id'])
        notf_info = product_info
        notf_info['users_tracking'] = user_ids
        
        response_page = ""
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        url =  SITE_NAME + "/price_notifications/gen_notifications"
        #data = {'cid' : self.cid, 'pcode':PYTHON_VERIFICATION_CODE, 'store_name':store_name,'cpl':cpl}
        data = notf_info
        data['pcode'] = PYTHON_VERIFICATION_CODE
        print "--Posting data to generate notification--"
        print data
        req = urllib2.Request(url, urllib.urlencode(data), headers)
            
        response_page = ""
        response = None
        try :
            response = urllib2.urlopen(req)
            response_page = response.read()            
        except:
            print "Could not set notifications those tracking product pid : " + str(self.pid)
            
        #print response
        #print response_page
        if response: response.close()
        ret_info = json.loads(response_page)
        print ret_info
        if ("1" == ret_info['s']) or (1 == ret_info['s']):
            return True
        
        print ret_info['m']
        return False
        
        
    def get_tracking_users(self):
        
        response_page = ""
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        url =  SITE_NAME + "/price_notifications/get_tracking_users"
        #data = {'cid' : self.cid, 'pcode':PYTHON_VERIFICATION_CODE, 'store_name':store_name,'cpl':cpl}
        data = {}
        data['pid'] = self.pid
        data['pcode'] = PYTHON_VERIFICATION_CODE
        req = urllib2.Request(url, urllib.urlencode(data), headers)
            
        response_page = ""
        response = None
        try :
            response = urllib2.urlopen(req)
            response_page = response.read()            
        except:
            print "Could not user info for those tracking product pid : " + str(pid)
            
        if response: response.close()
        user_ids = json.loads(response_page) if response_page else "";
        if user_ids: user_ids = user_ids.encode("ascii", "ignore")
        print user_ids
        return user_ids
        
    def get_product_info(self):
        
        response_page = ""
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        url =  SITE_NAME + "/price_notifications/get_product_info"
        #data = {'cid' : self.cid, 'pcode':PYTHON_VERIFICATION_CODE, 'store_name':store_name,'cpl':cpl}
        data = {}
        data['pid'] = self.pid
        data['pcode'] = PYTHON_VERIFICATION_CODE
        req = urllib2.Request(url, urllib.urlencode(data), headers)
            
        response_page = ""
        response = None
        try :
            response = urllib2.urlopen(req)
            response_page = response.read()            
        except:
            print "Could not find product info for pid : " + str(self.pid)
            
        if response: response.close()
        product_info = json.loads(response_page, encoding="ascii") if response_page else None
        product_info_ascii = {}
        #print response_page
        #print product_info
        product_info_ascii = {k.encode("ascii","ignore"): "" if not v else v.encode("ascii","ignore") for k, v in product_info.items()}
        print product_info_ascii
        return product_info_ascii
