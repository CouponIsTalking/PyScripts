from web_interface import *
from const import *
import time

class SendPriceNotf(object):
    def __init__(self):
        self.wi=WebInterface();
        self.send_notification_page = SITE_NAME + "/price_notifications/send_next_notification"
        
    def deinit(self):
        pass
    def send_next_notification(self):
        url = self.send_notification_page
        response_page = self.wi.get_selfpage(url)
        return response_page
    
    def send_notifications(self):
        while True:
            response_page = self.send_next_notification()
            if not response_page:
                print "Bad response : "
                print "LIKELY PROBLEM WITH NETWORK."
                break
            ret_info = json.loads(response_page)
            if not ret_info:
                return False
            elif 1 == int(ret_info['nomore']):
                print "No more notifications to be sent. Waiting for 2 minutes before re-check"
                time.sleep(120)
            elif 0 == int(ret_info['s']):
                print "We're not out of notifications, but no new notification sent."
                print "POSSIBLY A PROBLEM IF PERSISTS."
                print "MESSAGE : " + ret_info['m']
                time.sleep(5)
                break
            elif 1 == int(ret_info['s']):
                print "A new notification sent"
                # play nice
                time.sleep(5)
            
    

