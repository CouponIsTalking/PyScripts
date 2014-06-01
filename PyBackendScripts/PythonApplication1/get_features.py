#usage
# get_features.py "<product-url>" <mode>
# <mode> can be fast or accurate
#

from FeatureExtractor import *
from misc import *
import sys
import json

product_url = sys.argv[1]
fe = FeatureExtractor(product_url)
if len(sys.argv) >=3:
    fe.set_mode(sys.argv[2])
else:
    fe.set_mode('fast')

title = ""
price = ""
sale_price = ""
regular_price = ""
was_price = ""
pimg = ""
#try:
if 1:
    fe.run()
    title = fe.title
    price = fe.price
    sale_price = fe.sale_price
    regular_price = fe.regular_price
    was_price = fe.was_price
    pimgs = fe.product_images
    main_product_image = fe.main_product_image
try:
    a=1
except:
    a = 1

fe.deinit()

to_dump = {'title': title, 'price':price, 'sale_price': sale_price, 'regular_price': regular_price, 'was_price': was_price, 'pimg':main_product_image}
i = 0
for pimg in pimgs:
    i+=1
    key = 'pimg'+str(i)
    to_dump[key] = pimg

print json.dumps(to_dump)