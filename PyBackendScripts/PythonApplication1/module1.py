from GenPriceNotf import *

gpn = GenPriceNotf(job['pid'])
done = gpn.generate_notifications()
result = True if done else False
print result
