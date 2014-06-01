from FeatureExtractor import *
from url_groups import *
import os


for urls in url_groups:
    for product_url in urls:
        #cmd = "get_features.py \"" + product_url  + "\""
        fe = FeatureExtractor(product_url)
        try:
            fe.get_surrouding_details()
        except:
            print "Exception"
        #fe.run()
        title = fe.title
        price = fe.price
        pimgs = fe.product_images
        main_product_image = fe.main_product_image
        to_dump = {'title': title, 'price':price, 'pimg':main_product_image}
        print "################-------------------------------#############"
        print to_dump
        