from CoupDetParser import *

cdp = CoupDetParser("", "")
title = "25% Off Tees, Shorts & Swim For Women, Men, Girls & Boys"
detail = "Details: 25% Off tees, shorts & swim for Women, Men, Girls & Boys. In stores and online. Limit 1 code per order. Valid in US & Canada only. Expires on 05/09/2014."
cdp.set_title_and_detail(title, detail)

exp_date = cdp.get_formatted_expiry_date()
dollar_off = cdp.get_dollar_off()
percent_off = cdp.get_percent_off()

print "Expires " + exp_date
if dollar_off:
    print "dollar_off " + dollar_off
if percent_off:
    print "percent_off " + percent_off


