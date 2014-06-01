from CoupDetUpdater import *
# coupon update example
cdu = CoupDetUpdater()
coupon_info = {'SUMMER': {'code': u'SUMMER', 'desc': u'Details: 25% Off tees, shorts & swim for Women, Men, Girls & Boys. In stores and online. Limit 1 code per order. Valid in US & Canada only. Expires on 05/09/2014.', 'title': u'25% Off Tees, Shorts & Swim For Women, Men, Girls & Boys'}}
coupon_info['SUMMER']['company_id'] = 21;
cdu.set_coupon_info_from_map('retailmenot.com', coupon_info['SUMMER']) 
cdu.deinit()