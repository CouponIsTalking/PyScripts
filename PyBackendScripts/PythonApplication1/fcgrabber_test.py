from FCGrabber import *

fcg = FCGrabber(0)
fcg.fcp_entries={}
fcg.fcp_entries['deals2buy.com']="http://www.deals2buy.com/stores/24hourfitness.com/deals"
#fcg.fcp_entries['deals2buy.com']="http://www.deals2buy.com/stores/oakleyvault.com/deals"
coupons=fcg.get_from_deals_to_buy_dot_com()
print coupons
fcg.deinit()