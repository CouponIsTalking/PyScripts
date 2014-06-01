from web_interface import *
import const
from FeatureExtractor import *

class PriceCheck(object):
    def __init__(self):
        self.wi = WebInterface()
        self.fe = FeatureExtractor("")
        self.price = ''
        self.purl = ''
        self.pid = 0
        self.modeset = 'accurate'
    
    def set_new_mode(self, new_modeset):
        self.modeset = new_modeset
    
    def reinit(self, purl, pid):
        self.purl = purl
        self.pid = pid
    
    def deinit(self):
        self.fe.deinit()
    
    def call_wi_to_update_price(self):
        if self.price:
            self.wi.price_update(self.pid, self.price)
        
    def get_price(self):
        self.fe.reinit(self.purl)
        self.fe.set_mode(self.modeset)#'accurate')
        self.fe.run()
        self.price = self.fe.price
        self.sale_price = self.fe.sale_price
        self.regular_price = self.fe.regular_price
        self.was_price = self.fe.was_price
    
    def single_run(self):
        products = self.wi.get_prod_list_for_price_update()
        if not products:
            print "No more products to check price for."
            return
        for prod in products:
            if 'Product' in prod:
                purl = prod['Product']['purl']
                pid = prod['Product']['id']
                print "Getting new price for : " + purl
                print "Pid : " + pid
                self.reinit(purl, pid)
                self.get_price()
                print "New price :" + str(self.price)
                self.call_wi_to_update_price()
                print "---"
    
    def run(self):
        while True:
            self.single_run()
            print "...zzz...5 mins...zzz..."
            time.sleep(300)
    
            
    