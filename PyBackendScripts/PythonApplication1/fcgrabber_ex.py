#
# usage fcgrabber_ex.py sites=coupons.com:retailmenot.com:deals2buy.com,start_comp_id=<start_company_id>,another_setting=<another_setting_val>
#

import sys
from FCGrabber import *
from CoupDetUpdater import *

#fc = FCGrabber( 31 )
#entries = fc.get_fcparser_info()
#rmn_coupons = fc.get_from_retailmenot_dot_com()
#coupons_coupons = fc.get_from_coupons_dot_com()
#print rmn_coupons
#print coupons_coupons
#fc.deinit()
global_settings = {'start_comp_id':30}

if len(sys.argv) >=2 :
    params = sys.argv[1].split(',')
    for param in params:
        vals = param.split('=')
        print vals
        if 'start_comp_id' == vals[0]: 
            global_settings['start_comp_id'] = int(vals[1])
        elif 'sites' == vals[0]:
            sites = vals[1].split(":")
            for s in sites:
                global_settings['enabled_sites']={}
                global_settings['enabled_sites'][s] = True;
        elif 'another_setting' == vals[0]:
            global_settings['another_setting'] = vals[1]			
        

cdu = CoupDetUpdater()

print "Game Begins"

fc = None
i = global_settings['start_comp_id']-1

while i < 140:
    i = i+1
    if fc:
        fc.deinit()
    
    fc = FCGrabber( i ) # 'i' is company id
    
    if (i != global_settings['start_comp_id']): time.sleep(i/3 * 10)
        
    fc.get_fcparser_info()
    rmn_coupons = {}
    coupons_coupons = {}
    deals_to_buy_coupons = {}
    krazycouponlady_coupons = {}
    
    entries = fc.get_fcparser_info() # get foreign coupon parser info
    if not entries:
        #fc.deinit()
        continue
    print ":Entries:"
    print entries
    try:
        if "retailmenot.com" in global_settings['enabled_sites']:
            rmn_coupons = fc.get_from_retailmenot_dot_com()
        #rmn_coupons is hashmap, key is coupon code
        # {'<coupon-code1>' : {'code': xxx1, 'line': yyy1,},
        # {'<coupon-code2>' : {'code': xxx2, 'line': yyy2,} }
        #
        if rmn_coupons:
            for x in rmn_coupons:   #'x' is key, i.e. coupon code
                rmn_coupons[x]['company_id'] = i
                cdu.set_coupon_info_from_map('retailmenot.com', rmn_coupons[x]) 
    except:
        print "Error getting coupons from retailmenot.com"
        pass
    
    print ":Rmn:"
    print rmn_coupons
    
    try:
        if "coupon.com" in global_settings['enabled_sites']:
            coupons_coupons = fc.get_from_coupons_dot_com()
        if coupons_coupons:
            for x in coupons_coupons:
                coupons_coupons[x]['company_id'] = i
                cdu.set_coupon_info_from_map("coupons.com", coupons_coupons[x])
    except:
        print "Error getting coupons from coupons.com"
        pass
    
    print ":Coupons:"
    print coupons_coupons
    
    try:
        if "deals2buy.com" in global_settings['enabled_sites']:
            deals_to_buy_coupons = fc.get_from_deals_to_buy_dot_com()
        if deals_to_buy_coupons:
            for x in deals_to_buy_coupons:
                deals_to_buy_coupons[x]['company_id'] = i
                cdu.set_coupon_info_from_map("deals2buy.com", deals_to_buy_coupons[x])
    except:
        print "Error getting coupons from deals2buy.com"
        pass
    
    print ":Deals2Buy:"
    print deals_to_buy_coupons
    
    try:
        if "krazycouponlady.com" in global_settings['enabled_sites']:
            krazycouponlady_coupons = fc.get_from_coupons_dot_com()
        if krazycouponlady_coupons:
            for x in krazycouponlady_coupons:
                krazycouponlady_coupons[x]['company_id'] = i
                cdu.set_coupon_info_from_map("krazycouponlady.com", krazycouponlady_coupons[x])
    except:
        pass
    
    #fc.deinit()
cdu.deinit()