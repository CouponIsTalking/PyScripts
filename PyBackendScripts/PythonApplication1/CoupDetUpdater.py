from CoupDetParser import *
from CouponWebInf import *

class CoupDetUpdater(object):
    def __init__(self):
        self.cdp = CoupDetParser("", "")
        self.cwi = CouponWebInf()
        pass
    def deinit(self):
        self.cdp.deinit()
        self.cwi.deinit()
        pass
    def set_coupon_info_from_map(self, source, coupon_info_map):
        company_id = coupon_info_map['company_id']
        code = coupon_info_map['code'].encode("ascii","ignore")
        desc = coupon_info_map['desc'].encode("ascii","ignore")
        title = coupon_info_map['title'].encode("ascii","ignore")
        # parse info        
        self.cdp.set_title_and_detail(title, desc)
        exp_date = self.cdp.get_formatted_expiry_date()
        dollar_off = self.cdp.get_dollar_off()
        percent_off = self.cdp.get_percent_off()
        # build update map
        cinfo_to_update = {}
        cinfo_to_update['company_id'] = company_id
        cinfo_to_update['coupon_code'] = code
        cinfo_to_update['coupon_title'] = title
        cinfo_to_update['coupon_detail'] = desc
        cinfo_to_update['coupon_cur_code'] = 'usd'
        cinfo_to_update['coupon_source'] = source
        cinfo_to_update['valid_until_date'] = exp_date
        
        log_only = False
        if dollar_off:
            cinfo_to_update['coupon_worth'] = dollar_off
            cinfo_to_update['coupon_type'] = 'dollar_off'
        elif percent_off:
            cinfo_to_update['coupon_worth'] = percent_off
            cinfo_to_update['coupon_type'] = 'percent_off'
        else:
            log_only = True
        
        if log_only:
            self.cwi.log_coupon_details(cinfo_to_update)
        else:
            self.cwi.update_coupon_details(cinfo_to_update)
    
        
