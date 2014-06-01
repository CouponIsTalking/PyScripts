import re
import datetime

class CoupDetParser(object):
    def __init__(self, title, detail):
        self.coupon_detail = detail.lower()
        self.coupon_title = title.lower()
        self.date_re = {}
        self.date_re['expire_on'] = re.compile("(?:(expire|expires|end|ends))[ ](on )?[\d]+[/][\d]+[/][\d]+")
        self.date_re['expire_today'] = re.compile('(expire|expires|end|ends)[ ](on )?today')
        self.date_re['expire_tom'] = re.compile('(expire|expires|end|ends)[ ](on )?tomorrow')
        self.date_re['pure_date'] = re.compile("[\d]+[/][\d]+[/][\d]+")
        self.percent_off_re = []
        self.percent_off_re.append(re.compile("[\d]+[%] off"))
        self.dollar_off_re = []   
        self.dollar_off_re.append(re.compile("[\d]+[$] off"))
        self.dollar_off_re.append(re.compile("[$][\d]+ off"))
        self.digits_re = re.compile("[\d]+")
        
        return
    def deinit(self):
        self.date_re.clear()
        del self.dollar_off_re[:]
        del self.percent_off_re[:]
        return
    
    def set_title_and_detail(self, title, detail):
        self.set_title(title)
        self.set_detail(detail)
        return
    
    def set_detail(self, detail):
        self.coupon_detail = detail.lower()
        return
    
    def set_title(self, title):
        self.coupon_title = title.lower()
        return
    
    def get_dollar_off(self):
        doff = 0
        for x in self.dollar_off_re:
            m = x.search(self.coupon_title)
            if m:
                doff = self.digits_re.search(m.group(0)).group(0)
                break
        if doff:
            return doff
        
        for x in self.dollar_off_re:
            m = x.search(self.coupon_title)
            if m:
                doff = self.digits_re.search(m.group(0)).group(0)
                break
        
        return doff
    
    def get_percent_off(self):
        poff = 0
        for x in self.percent_off_re:
            m = x.search(self.coupon_detail)
            if m:
                poff = self.digits_re.search(m.group(0)).group(0)
                break
        if poff:
            return poff
        
        for x in self.percent_off_re:
            m = x.search(self.coupon_detail)
            if m:
                poff = self.digits_re.search(m.group(0)).group(0)
                break
        
        return poff
    
    def get_formatted_expiry_date(self):
        d = self.get_expiry_date()
        if not d:
            return ""
        else:
            return d.strftime("%Y-%m-%d")
    
    def get_expiry_date(self):
        det = self.coupon_detail.lower()
        
        # check expire on date
        m = self.date_re['expire_on'].search(det)
        if m:
            d = self.date_re['pure_date'].search(m.group(0)).group(0)
            d_tuple = d.split('/')
            if int(d_tuple[-1]) < 100:
                d = datetime.datetime.strptime(d, "%m/%d/%y")
            else:
                d = datetime.datetime.strptime(d, "%m/%d/%Y")
            return d
        # check if expires today
        m = self.date_re['expire_today'].search(det)
        if m:
            d = datetime.date.today()
            return d
        # check if expires tomorrow
        m = self.date_re['expire_tom'].search(det)
        if m:
            d = datetime.date.today() + datetime.timedelta(days=1)
            return d
        
        # couldnt get expiry date
        return None

