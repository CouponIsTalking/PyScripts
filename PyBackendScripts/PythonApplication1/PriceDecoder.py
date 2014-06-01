from htmlops import *
from misc import *
import re 

class PriceDecoder(object):
    def __init__(self, s, html):
        self.full_text = s
        self.html = html.replace(" ", "")
        
        self.numbered_html = re.sub(r'[^0-9.]', "", self.html)
        self.price = 0
        self.currency_code = ""
        self.is_old_price = False
        self.prices = []
        self.float_prices = []
        self.str_prices = []
        
        self.re_to_match_comma_in_price = re.compile(r'(?<=[0-9]),[ ]?(?=[0-9])')
        self.re_to_match_multiple_dollar_sign_series = re.compile(r'[$]+')
        self.re_for_multiple_spaces = re.compile(r'[ ]+')
        self.re_for_price_related_words = re.compile(r"(MRP|earlier|previous|before|was|old|list|market|retail|regular|reg|orig|normal|price|save|savings|our|cur|current|new|now|reduced|sale|clearance|discounted|discountprice|special|offer|tidebuy)")
        #regexes
        self.currency_code_regex = re.compile(r'(\b(?:\$|USD|US\$|USD\$|Usd|Us\$|Usd\$|usd|us\$|usd\$|EUR|Eur|JPY|Jpy|GBP|Gbp|AUD\$|AUD|AU\$|Aud\$|Aud|Au\$|CHF|Chf|CAD\$|CAD|CA\$|Cad\$|Cad|Ca\$|CNY|Cny|NZD\$|NZD|NZ\$|Nzd\$|Nzd|Nz\$|SEK|Sek|KR|Kr|RUB|Rub|HKD\$|HKD|HK\$|Hkd\$|Hkd|Hk\$|SGD\$|SGD|SG\$|Sgd\$|Sgd|Sg\$|INR[.]|Inr[.]|INR|Inr|RS[.]|Rs[.]|rs|RS|Rs|BRL\$|Brl\$|BRL|Brl|R\$|r\$|ARS\$|Ars|Taka|Tk|BDT))')
        
        #r"\b" removed from cu_regexes and cur_amount_regexes
        self.cur_regexes = {}
        self.cur_regexes['USD'] = re.compile(r'(?:USD|US\$|USD\$|Usd|Us\$|Usd\$|usd|us\$|usd\$)')
        self.cur_regexes['EUR'] = re.compile(r'(?:EUR|Eur)')
        self.cur_regexes['JPY'] = re.compile(r'(?:JPY|Jpy)')
        self.cur_regexes['GBP'] = re.compile(r'(?:GBP|Gbp)')
        self.cur_regexes['AUD'] = re.compile(r'(?:AUD\$|AUD|AU\$|Aud\$|Aud|Au\$)')
        self.cur_regexes['CHF'] = re.compile(r'(?:CHF|Chf)')
        self.cur_regexes['CAD'] = re.compile(r'(?:CAD\$|CAD|CA\$|Cad\$|Cad|Ca\$)')
        self.cur_regexes['CNY'] = re.compile(r'(?:CNY|Cny)')
        self.cur_regexes['NZD'] = re.compile(r'(?:NZD\$|NZD|NZ\$|Nzd\$|Nzd|Nz\$)')
        self.cur_regexes['SEK'] = re.compile(r'(?:SEK|Sek)')
        self.cur_regexes['KR'] =  re.compile(r'(?:KR|Kr)')
        self.cur_regexes['RUB'] = re.compile(r'(?:RUB|Rub)')
        self.cur_regexes['HKD'] = re.compile(r'(?:HKD\$|HKD|HK\$|Hkd\$|Hkd|Hk\$)')
        self.cur_regexes['SGD'] = re.compile(r'(?:SGD\$|SGD|SG\$|Sgd\$|Sgd|Sg\$)')
        self.cur_regexes['INR'] = re.compile(r'(?:INR[.]|Inr[.]|INR|Inr|RS[.]|Rs[.]|rs|RS|Rs)')
        self.cur_regexes['BRL'] = re.compile(r'(?:BRL\$|Brl\$|BRL|Brl|R\$|r\$)')
        self.cur_regexes['ARS'] = re.compile(r'(?:ARS\$|Ars)')
        self.cur_regexes['BDT'] = re.compile(r'(?:Taka|Tk|BDT)')
        self.cur_regexes['Generic_USD'] = re.compile(r'(?:\$)')
        
        self.cur_amount_regexes = {}
        self.cur_amount_regexes['USD'] = re.compile(r'(?:USD|US\$|USD\$|Usd|Us\$|Usd\$|usd|us\$|usd\$)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['EUR'] = re.compile(r'(?:EUR|Eur)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['JPY'] = re.compile(r'(?:JPY|Jpy)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['GBP'] = re.compile(r'(?:GBP|Gbp)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['AUD'] = re.compile(r'(?:AUD\$|AUD|AU\$|Aud\$|Aud|Au\$)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['CHF'] = re.compile(r'(?:CHF|Chf)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['CAD'] = re.compile(r'(?:CAD\$|CAD|CA\$|Cad\$|Cad|Ca\$)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['CNY'] = re.compile(r'(?:CNY|Cny)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['NZD'] = re.compile(r'(?:NZD\$|NZD|NZ\$|Nzd\$|Nzd|Nz\$)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['SEK'] = re.compile(r'(?:SEK|Sek)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['KR'] =  re.compile(r'(?:KR|Kr)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['RUB'] = re.compile(r'(?:RUB|Rub)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['HKD'] = re.compile(r'(?:HKD\$|HKD|HK\$|Hkd\$|Hkd|Hk\$)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['SGD'] = re.compile(r'(?:SGD\$|SGD|SG\$|Sgd\$|Sgd|Sg\$)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['INR'] = re.compile(r'(?:INR[.]|Inr[.]|INR|Inr|RS[.]|Rs[.]|rs|RS|Rs)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['BRL'] = re.compile(r'(?:BRL\$|Brl\$|BRL|Brl|R\$|r\$)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['ARS'] = re.compile(r'(?:ARS\$|Ars)[.: ]*\d*[.]?\d+')
        self.cur_amount_regexes['BDT'] = re.compile(r'(?:Taka|Tk|BDT)[.: ]*\d*[.]?\d+')

    # not using following routine right now   
    def process_html_for_cur_symbols(self):
        
        price_re = re.compile(r"\d*[.]?\d+")
        
        webrupee_sign_htmls = ["<span class=\"WebRupee\">`</span>", "<span class=\"WebRupee\"></span>" ]
        for cur_sign_html in webrupee_sign_htmls:
            if cur_sign_html in self.html:
                while True:
                    loc = self.html.find[cur_sign_html]
                    if loc < 0: break
                    self.html.replace(cur_sign_html, "INR")
                    loc += 3
                    
                
    def reset(self, s, html):
        self.full_text = s
        self.html = html.replace(" ", "")
        
        self.numbered_html = re.sub(r'[^0-9.]', "", self.html)
        self.price = 0
        self.currency_code = ""
        self.is_old_price = False
        self.prices = []
        self.float_prices = []
        self.str_prices = []
    
    def GetPrice(self):
        return self.price
        
    def IsOld(self):
        return self.is_old_price
        
    def GetCurrency(self):
        return self.currency_code
    
    
    def refine_price(self, prices):
        refined_prices = get_refined_prices(prices, self.html)
        return refined_prices
    
    def get_price_list_from_lines(self, lines):
        prices = []
        for line in lines:
            prices = prices + re.findall('\d*[.]?\d+', line)
        return prices
        
    def get_min_float_val_from_str(self, lines):
        
        prices = self.get_price_list_from_lines(lines)
        
        prices = self.refine_price(prices)
        float_prices = [float(x) for x in prices if float(x)]
        
        if not float_prices:
            return 0
        
        min_float_price = min(float_prices)
        
        for price in prices:
            if float(price) == min_float_price:
                return price
    
    def get_max_float_val_from_str(self, lines):
        
        prices = self.get_price_list_from_lines(lines)
        prices = self.refine_price(prices)
        float_prices = [float(x) for x in prices if float(x)]
        
        if not float_prices:
            return 0
        
        max_float_price = max(float_prices)
        
        for price in prices:
            if float(price) == max_float_price:
                return price
    
    
    def get_price_line_match(self, regexes, text):
        
        price_lines = []
        for regex in regexes:
            price_lines = price_lines + [m.group() for m in re.finditer(regex, text)]
            
        return price_lines
    
    def DecodeCurCode(self):
        
        if self.currency_code:
            return self.currency_code
        
        text = re.sub(' +',' ', self.full_text.replace(",", "").replace("\n", " ").replace("\r", " ").replace("\t", " ").strip())
        text = re.sub(r'(?<=([a-zA-Z] )|([a-z][a-z]))[.|:]+', ' ', text)
        text = self.re_to_match_comma_in_price.sub('', text)
        
        currency_code_regex = self.currency_code_regex
        cur_regexes = self.cur_regexes
        
        currency_code_matches = currency_code_regex.findall(text)
        currency_code_match_num = {}
        currency_code = ""
            
        if currency_code_matches:
            for cur_code in cur_regexes:
                currency_code_match_num[cur_code] = len(cur_regexes[cur_code].findall(text)) 
                
            for cur_code in currency_code_match_num:
                currency_code = cur_code if (cur_code !='Generic_USD') and ((not currency_code) or (currency_code_match_num[cur_code] > currency_code_match_num[currency_code])) else currency_code
                
            currency_code = 'USD' if ((not currency_code) and (cur_regexes['Generic_USD'].findall(text))) else currency_code
        
        if not currency_code:
            if "$" in text:
                currency_code = 'USD'
            else:
                currency_code = ""
        
        self.currency_code = currency_code
        return currency_code
        
    def removeOtherCurrencies(self, text, currency_code):
        if currency_code not in self.cur_regexes:
            return text
        
        for other_cur_code in self.cur_amount_regexes:
            if other_cur_code == currency_code:
                continue
            text = self.cur_amount_regexes[other_cur_code].sub("", text)
        
        return text
    
    def ReplaceCurCodeWithDollar(self, text, currency_code):
        
        if currency_code not in self.cur_regexes:
            return text
        
        clamped_dollared_text = self.cur_regexes[currency_code].sub("$", text)
        #if currency_code == 'USD':
        #    clamped_dollared_text = self.cur_regexes['Generic_USD'].sub("$", clamped_dollared_text)
        
        return clamped_dollared_text
    
    
    def DecodePrices(self):
        
        currency_code = self.DecodeCurCode()
        
        text = re.sub(' +',' ', self.full_text.replace(",", "").replace("\n", " ").replace("\r", " ").replace("\t", " ").strip())
        text = re.sub(r'(?<=([a-zA-Z] )|([a-z][a-z]))[.|:]+', ' ', text)
        clamped_text = self.re_for_multiple_spaces.sub('', text)
        #clamped_lower_text = clamped_text.lower()
        
        lower_text = text.lower()
        words = clamped_text.split(" ")
        
        clamped_dollared_text = self.ReplaceCurCodeWithDollar(clamped_text, currency_code)
        clamped_dollared_text = self.removeOtherCurrencies(clamped_dollared_text, currency_code) 
        clamped_dollared_text = self.re_to_match_multiple_dollar_sign_series.sub("$", clamped_dollared_text)
        #self.currency_code_regex.sub("$", clamped_text.lower())
        
        clamped_dollared_text = clamped_dollared_text.lower()
        
        prices = {}
        prices['reg'] = textIsPrice(clamped_dollared_text)
        prices['new'] = textIsNewPrice(clamped_dollared_text)
        prices['old'] = textIsOldPrice(clamped_dollared_text)
            
        
        #clamped_dollared_text = re.sub(r'(?<=([a-zA-Z]))[ ]', '', dollared_text)
        #clamped_dollared_text = re.sub('[ |:]+', '', dollared_text)
        
        prices = {}
        regexes = []
        #regexes.append('^\$\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$]?$')
        #regexes.append('^[\$]?\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})\$$')
        regexes.append('^\$\d*[.]?\d+[\$]?$')
        regexes.append('^\d*[.]?\d+\$$')
        regexes.append('^\$\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+[\$]?$')
        regexes.append('^\d*[.]?\d+[\$]?[-]\d*[.]?\d+\$$')
        match = self.get_price_line_match(regexes, clamped_dollared_text)
        prices['just'] = self.get_min_float_val_from_str(match) if match else 0
            
        
        regexes = []
        #regexes.append('(?:[^0-9a-zA-Z]*)(?:(price)*)(?:(earlier|previous|before|was|old)+)(?:(price)*)(?:[-]*)\$\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$]?(?:[.|-]*)(?:only|)')
        #regexes.append('(?:[^0-9a-zA-Z]*)(?:(price)*)(?:(earlier|previous|before|was|old)+)(?:(price)*)(?:[-]*)[\$]?\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$](?:[.|-]*)(?:only|)')
        regexes.append('^(?:(earlier|previous|before|was|old)*)(?:(price))[.|:]?[\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(earlier|previous|before|was|old)*)(?:(price))[.|:]?\$\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(earlier|previous|before|was|old)*)(?:(price))[.|:]?[\$]?\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+\$')
        regexes.append('^(?:(price))(?:(earlier|previous|before|was|old)*)[.|:]?[\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(price))(?:(earlier|previous|before|was|old)*)[.|:]?\$\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(price))(?:(earlier|previous|before|was|old)*)[.|:]?[\$]?\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+\$')
        match = self.get_price_line_match(regexes, clamped_dollared_text)
        prices['old'] = self.get_min_float_val_from_str(match) if match else 0
        
        regexes = []
        #regexes.append('(?:[^0-9a-zA-Z]*)(?:(price)*)(?:(our|cur|current|new|now|discounted|discountprice|special|offer)+)(?:(price)*)(?:[-]*)\$\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$]?(?:[.|-]*)(?:only|)')
        #regexes.append('(?:[^0-9a-zA-Z]*)(?:(price)*)(?:(our|cur|current|new|now|discounted|discountprice|special|offer)+)(?:(price)*)(?:[-]*)[\$]?\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$](?:[.|-]*)(?:only|)')
        regexes.append('^[\$]?\d*[.]?\d+[\$]?(?:(now|reduced|sale|clearance|discounted|discountprice|special|offer|tidebuy))(?:(price|))$') 
        regexes.append('^\$\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+[\$]?(?:(now|reduced|sale|clearance|discounted|discountprice|special|offer|tidebuy))(?:(price|))$')
        regexes.append('^[\$]?\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+\$(?:(now|reduced|sale|clearance|discounted|discountprice|special|offer|tidebuy))(?:(price|))$')
        regexes.append('^(?:(sale))[.|:]?[\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(our|cur|current|new|now|reduced|sale|clearance|discounted|discountprice|special|offer|tidebuy)*)(?:(price))[.|:]?[\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(our|cur|current|new|now|reduced|sale|clearance|discounted|discountprice|special|offer|tidebuy)*)(?:(price))[.|:]?\$\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(our|cur|current|new|now|reduced|sale|clearance|discounted|discountprice|special|offer|tidebuy)*)(?:(price))[.|:]?[\$]?\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+\$')
        regexes.append('^(?:(price))(?:(tidebuy|our|cur|current|new|now|reduced|sale|clearance|discounted|discountprice|special|offer)*)[.|:]?[\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(price))(?:(tidebuy|our|cur|current|new|now|reduced|sale|clearance|discounted|discountprice|special|offer)*)[.|:]?\$\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(price))(?:(tidebuy|our|cur|current|new|now|reduced|sale|clearance|discounted|discountprice|special|offer)*)[.|:]?[\$]?\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+\$')
        match = self.get_price_line_match(regexes, clamped_dollared_text)
        prices['new'] = self.get_min_float_val_from_str(match) if match else 0
            
        
        regexes = []
        #regexes.append('(?:[^0-9a-zA-Z]*)(?:(price)*)(?:(reg|orig|normal|price)+)(?:(price)*)(?:[-]*)\$\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$]?(?:[.|-]*)(?:only|)')
        #regexes.append('(?:[^0-9a-zA-Z]*)(?:(price)*)(?:(reg|orig|normal|price)+)(?:(price)*)(?:[-]*)[\$]?\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$](?:[.|-]*)(?:only|)')
        regexes.append('^(?:(list|market|retail|regular|reg|orig|normal|price)*)(?:(price))[.|:]?[\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(list|market|retail|regular|reg|orig|normal|price)*)(?:(price))[.|:]?\$\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(list|market|retail|regular|reg|orig|normal|price)*)(?:(price))[.|:]?[\$]?\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+\$')
        regexes.append('^(?:(price))(?:(market|retail|regular|reg|orig|normal|price)*)[.|:]?[\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(price))(?:(market|retail|regular|reg|orig|normal|price)*)[.|:]?\$\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+[\$]?')
        regexes.append('^(?:(price))(?:(market|retail|regular|reg|orig|normal|price)*)[.|:]?[\$]?\d*[.]?\d+[\$]?[-][\$]?\d*[.]?\d+\$')
        match = self.get_price_line_match(regexes, clamped_dollared_text)
        prices['reg'] = self.get_min_float_val_from_str(match) if match else 0
        
        
        #regexes = []
        #regexes.append('(?:[^0-9a-zA-Z]*)(?:[-]*)\$\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$]?(?:[.|-]*)(?:only|)')
        #regexes.append('(?:[^0-9a-zA-Z]*)(?:[-]*)[\$]?\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$](?:[.|-]*)(?:only|)')
        #match = self.get_price_line_match(regexes, clamped_dollared_text)
        #prices['bare'] = self.get_min_float_val_from_str(match) if match else 0
        
        
        regexes = []
        #regexes.append('(?:[^0-9a-zA-Z]*)(?:(save|saving|savings|off)+)(?:[-]*)\$\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$]?(?:[.|-]*)(?:only|)')
        #regexes.append('(?:[^0-9a-zA-Z]*)(?:[-]*)\$\d*[.]?\d+(?:([-][\$]?\d*[.]?\d+[\$]?){0,1})[\$]?(?:(save|saving|savings|off)+)')
        regexes.append('^(?:(save|saving|savings|off))[.|:]?\$\d*[.]?\d+')
        regexes.append('^\$\d*[.]?\d+[ ]?(?:(off))')
        match = self.get_price_line_match(regexes, clamped_dollared_text)
        prices['save'] = self.get_max_float_val_from_str(match) if match else 0
            
        
        float_prices = {}
        float_prices['cur_price'] = 0
        float_prices['old_price'] = 0
        float_prices['save_price'] = 0
        
        if ((not float_prices['cur_price']) and prices['new']) : float_prices['cur_price'] = float(prices['new'])
        if ((not float_prices['cur_price']) and prices['reg']) : float_prices['cur_price'] = float(prices['reg'])
        if ((not float_prices['cur_price']) and prices['just']) : float_prices['cur_price'] = float(prices['just'])
        #float_prices['cur_price'] = float(prices['bare']) if ((not float_prices['cur_price']) and prices['bare']) else 0
        
        if ((not float_prices['old_price']) and prices['old']) : float_prices['old_price'] = float(prices['old'])
        if ((not float_prices['save_price']) and prices['save']) : float_prices['save_price'] = float(prices['save'])
        
        str_prices = {}
        str_prices['cur_price'] = ""
        str_prices['old_price'] = ""
        str_prices['save_price'] = ""
        
        if ((not str_prices['cur_price']) and prices['new']) : str_prices['cur_price'] = str(prices['new'])
        if ((not str_prices['cur_price']) and prices['reg']) : str_prices['cur_price'] = str(prices['reg'])
        if ((not str_prices['cur_price']) and prices['just']) : str_prices['cur_price'] = str(prices['just'])
        #float_prices['cur_price'] = float(prices['bare']) if ((not float_prices['cur_price']) and prices['bare']) else None
        
        if ((not str_prices['old_price']) and prices['old']) : str_prices['old_price'] = str(prices['old'])
        if ((not str_prices['save_price']) and prices['save']) : str_prices['save_price'] = str(prices['save'])
        
        #print prices
        #print float_prices
        self.prices = prices
        self.float_prices = float_prices
        self.str_prices = str_prices
        
        return float_prices
    
    def textIsOldPrice(self):
        ret = self.float_prices['old_price'] if self.float_prices['old_price'] else 0
        return ret
        
    def textIsNewPrice(self):
        if self.prices['new'] and self.str_prices['cur_price'] and (self.str_prices['cur_price'] == self.prices['new']):
            return self.float_prices['cur_price']
        else:
            return 0
    
    def textIsPrice(self):
        ret = self.float_prices['cur_price'] if self.float_prices['cur_price'] else 0
        return ret
        
    def textIsOldPriceStr(self):
        ret = self.str_prices['old_price'] if self.float_prices['old_price'] else ""
        return ret
        
    def textIsNewPriceStr(self):
        if self.prices['new'] and self.str_prices['cur_price'] and (self.str_prices['cur_price'] == self.prices['new']):
            return self.str_prices['cur_price']
        else:
            return ""
    
    def textIsPriceStr(self):
        ret = self.str_prices['cur_price'] if self.float_prices['cur_price'] else ""
        return ret
    
    def getPricePosition(self):
        currency_code = self.DecodeCurCode()
        if not currency_code:
            return False
        
        text = re.sub(' +',' ', self.full_text.replace(",", "").replace("\n", " ").replace("\r", " ").replace("\t", " ").strip())
        text = re.sub(r'(?<=([a-zA-Z] )|([a-z][a-z]))[.|:]+', ' ', text)
        text = self.re_to_match_comma_in_price.sub('', text)
        
        dollared_text = self.ReplaceCurCodeWithDollar(text, currency_code)
        
        #clamped_text = re.sub('[ ]+', '', text).lower()
        clamped_dollared_text = self.re_for_multiple_spaces.sub("", dollared_text).lower()
        clamped_dollared_text = self.re_for_price_related_words.sub("", clamped_dollared_text)
        #re.compile(r"(MRP|earlier|previous|before|was|old|list|market|retail|regular|reg|orig|normal|price|save|savings|our|cur|current|new|now|reduced|sale|clearance|discounted|discountprice|special|offer|tidebuy)").sub("", clamped_text)
        
        #clamped_dollared_text = self.ReplaceCurCodeWithDollar(clamped_text, currency_code) 
        #
        match = re.search('\$\d*[.]?\d+', clamped_dollared_text)
        
        #print match.start
        return match.start()
    
    def textHasPriceInIt(self):
        text = re.sub(' +',' ', self.full_text.replace(",", "").replace("\n", " ").replace("\r", " ").replace("\t", " ").strip())
        text = re.sub(r'(?<=([a-zA-Z] )|([a-z][a-z]))[.|:]+', ' ', text)
        text = self.re_to_match_comma_in_price.sub('', text)
        #clamped_text = re.sub('[ ]+', '', text)
        clamped_text = self.re_for_multiple_spaces.sub("", text)
        #clamped_dollared_text = self.currency_code_regex.sub("$", clamped_text)
        
        currency_code = self.DecodeCurCode()
        if not currency_code:
            return False
        
        clamped_dollared_text = self.ReplaceCurCodeWithDollar(text, currency_code) 
        #
        match = re.search('\$\d*[.]?\d+', clamped_dollared_text)
        if match:
            return True
        
        return False
        
                    