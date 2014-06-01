from GenPriceNotf import *
import time

i=367;
while i < 400:
    i=i+1
    gpn = GenPriceNotf(i)
    prd_info = gpn.generate_notifications()
    print prd_info
    #time.sleep(2);    
