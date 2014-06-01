from SeleniumReader import *
from web_interface import *
from StringIO import StringIO
import lxml.html
from lxml import etree
from misc import *

class FeatureExtractor:
    
    def print_stuff(self):
        to_dump = {'title': self.title, 'price': self.price, 'pimg': self.main_product_image}
        i = 0
        for pimg in self.product_images:
            i+=1
            key = 'pimg'+str(i)
            to_dump[key] = pimg
        print to_dump
    
    def update_prod_info_in_db(self):
        
        company_website = get_website_name_for_tracker_update(self.url)
        prod_info = {'company_website': company_website, 'prod_link': self.url, 'title': self.title, 'price': self.price, 'sale_price': self.sale_price, 'regular_price': self.regular_price, 'was_price': self.was_price, 'pimg': self.main_product_image}
        
        i = 0
        for pimg in self.product_images:
            i+=1
            key = 'pimg'+str(i)
            prod_info[key] = pimg
        
        retval = self.wi.update_prod_info_in_db(prod_info)
        return retval
    
    def deinit(self):
        if self.reader_present:
            self.reader.deinit()
        
    def __init__(self, url):
        
        self.look_for_size_and_color = 0
        self.reader = None
        self.url = url
        self.reader_present = False;
        self.urllib2_present = False;
        self.t = None #lxml.html.fromstring(self.orig_page_source)
        
        self.title = ""
        self.price = ""
        self.sale_price = ""
        self.regular_price = ""
        self.was_price = ""
        self.price_set = {}
        self.product_images = []
        self.real_images_lxml_ele = []
        self.main_product_image = ""
        
        self.wi = WebInterface()
        
        self.tracker_info = self.wi.get_tracker_info(self.url) if self.url else None
        
        self.mode = 'fast'
        
    def reinit(self, url):
        self.look_for_size_and_color = 0
        self.url = url
        self.reader_present = False;
        self.urllib2_present = False;
        
        self.title = ""
        self.price = ""
        self.sale_price = ""
        self.regular_price = ""
        self.was_price = ""
        self.price_set = {}
        self.product_images = []
        self.real_images_lxml_ele = []
        self.main_product_image = ""
        
        self.tracker_info = self.wi.get_tracker_info(self.url)
        
        self.mode = 'fast'
        
        if self.tracker_info:
            return True
        else:
            return False
#    def GetMetaInfoFromDB(self, website):
#        wi = WebInterface()
#        self.tracker_info = wi.get_tracker_info(website)
    
    # uses get_regex_substituted_xpath    
    
    def set_mode(self, new_mode):
        if (new_mode == 'fast' or new_mode == 'accurate'):
            self.mode = new_mode
            return True
        else:
            return False
    
    def generate_guessed_tracker_info(self, page):
        tracker_info = self.tracker_info
        guessed_tracker_info = tracker_info.copy()
        xpath_keys = ["titlexpath", "pricexpath", "title_price_xpath", "oldpricexpath", "pimg_xpath", "pimg_xpath1", "pimg_xpath2", "pimg_xpath3", "pimg_xpath4", "pimg_xpath5", "urllib2_pimg_xpath1", "urllib2_pimg_xpath2", "urllib2_pimg_xpath3", "urllib2_pimg_xpath4", "urllib2_pimg_xpath5", "image_and_title_parent_xpath", "image_and_details_container_xpath"]
        for xpath_key in xpath_keys:
            xpath_regex_key = xpath_key + "_regex"
            if xpath_regex_key in tracker_info:
                idname = get_id_from_xpath(tracker_info[xpath_key])
                if not idname:
                    continue
                regex = "".join(map(lambda c: c if (c>'9' or c <'0') else '\d', idname))
                improved_regex = re.sub(r"(\\d\\d)(\\d)+", "\d\d(\d)+", regex)
                guessed_tracker_info[xpath_key] = get_regex_substituted_xpath(tracker_info[xpath_key], improved_regex, page)
        
        self.guessed_tracker_info = guessed_tracker_info
        return guessed_tracker_info
        
    
    def build_regex_substituted_tracker_info(self, page):
        tracker_info = self.tracker_info
        adjusted_tracker_info = tracker_info.copy()
        
        xpath_keys = ["titlexpath", "pricexpath", "title_price_xpath", "oldpricexpath", "saleprxpath_onsale", "regprxpath_onsale", "wasprxpath_onsale", "pricerootxpath", "priceofferxpath", "pimg_xpath", "pimg_xpath1", "pimg_xpath2", "pimg_xpath3", "pimg_xpath4", "pimg_xpath5", "urllib2_pimg_xpath1", "urllib2_pimg_xpath2", "urllib2_pimg_xpath3", "urllib2_pimg_xpath4", "urllib2_pimg_xpath5", "image_and_title_parent_xpath", "image_and_details_container_xpath"]
        for xpath_key in xpath_keys:
            xpath_regex_key = xpath_key + "_regex"
            if xpath_regex_key in tracker_info:
                regex = tracker_info[xpath_key + "_regex"]
                adjusted_tracker_info[xpath_key] = get_regex_substituted_xpath(tracker_info[xpath_key], regex, page)
        
        self.orig_tracker_info = self.tracker_info
        self.tracker_info = adjusted_tracker_info
        
        secondary_tracker_info = self.orig_tracker_info.copy()
        for xpath_key in secondary_tracker_info:
            xpath_regex_key = xpath_key + "_regex"
            if xpath_regex_key in tracker_info:
                regex = secondary_tracker_info[xpath_regex_key]
                improved_regex = re.sub(r"(\\d\\d)(\\d)+", "\d\d(\d)+", regex)
                #print improved_regex
                secondary_tracker_info[xpath_key] = get_regex_substituted_xpath(secondary_tracker_info[xpath_key], improved_regex, page)
        
        self.secondary_tracker_info = secondary_tracker_info.copy()
        #for k in self.secondary_tracker_info:
        #    print k + " : " + self.secondary_tracker_info[k]
        #print "--------"
        #for k in self.tracker_info:
        #    print k + " : " + self.tracker_info[k]
        #self.secondary_tracker_info = self.tracker_info
    
    def customize_tracker_info(self, page):
        tracker_info = self.tracker_info
        adjusted_tracker_info = tracker_info.copy()
        adjusted_tracker_info['titlexpath'] = get_id_substituted_xpath(tracker_info['titlexpath'], page)
        adjusted_tracker_info['title_price_xpath'] = get_id_substituted_xpath(tracker_info['title_price_xpath'], page)
        adjusted_tracker_info['pricexpath'] = get_id_substituted_xpath(tracker_info['pricexpath'], page)
        adjusted_tracker_info['oldpricexpath'] = get_id_substituted_xpath(tracker_info['oldpricexpath'], page)
        adjusted_tracker_info['saleprxpath_onsale'] = get_id_substituted_xpath(tracker_info['saleprxpath_onsale'], page)
        adjusted_tracker_info['regprxpath_onsale'] = get_id_substituted_xpath(tracker_info['regprxpath_onsale'], page)
        adjusted_tracker_info['wasprxpath_onsale'] = get_id_substituted_xpath(tracker_info['wasprxpath_onsale'], page)
        adjusted_tracker_info['pricerootxpath'] = get_id_substituted_xpath(tracker_info['pricerootxpath'], page)
        adjusted_tracker_info['priceofferxpath'] = get_id_substituted_xpath(tracker_info['priceofferxpath'], page)
        adjusted_tracker_info['pimg_xpath'] = get_id_substituted_xpath(tracker_info['pimg_xpath'], page)
        adjusted_tracker_info['pimg_xpath1'] = get_id_substituted_xpath(tracker_info['pimg_xpath1'], page)
        adjusted_tracker_info['pimg_xpath2'] = get_id_substituted_xpath(tracker_info['pimg_xpath2'], page)
        adjusted_tracker_info['pimg_xpath3'] = get_id_substituted_xpath(tracker_info['pimg_xpath3'], page)
        adjusted_tracker_info['pimg_xpath4'] = get_id_substituted_xpath(tracker_info['pimg_xpath4'], page)
        adjusted_tracker_info['pimg_xpath5'] = get_id_substituted_xpath(tracker_info['pimg_xpath5'], page)
        adjusted_tracker_info['image_and_title_parent_xpath'] = get_id_substituted_xpath(tracker_info['image_and_title_parent_xpath'], page)
        adjusted_tracker_info['image_and_details_container_xpath'] = get_id_substituted_xpath(tracker_info['image_and_details_container_xpath'], page)
        adjusted_tracker_info['is_image_in_og_image_meta_tag'] = tracker_info['is_image_in_og_image_meta_tag']
        adjusted_tracker_info['pinterest_position'] = tracker_info['pinterest_position']
        self.orig_tracker_info = self.tracker_info
        self.tracker_info = adjusted_tracker_info
        
   
    def enableUrllib2(self):
        
        page_content = self.wi.get_a_webpage(self.url)
        self.orig_page_source = page_content
        if self.orig_page_source:
            self.doc_etree = etree.parse(StringIO(self.orig_page_source), etree.HTMLParser())
            self.urllib2_present = True;
    
    def enableReader(self):
        self.reader_present = True
        page_load_timeout = 20;
        
        if self.reader is not None:
           self.reader.moveTo(self.url)
        else: 
            self.reader = SeleniumReader(self.url, page_load_timeout);
        
        self.reader.verbose = 0
        self.reader.getDriver().implicitly_wait(3);
        self.orig_page_source = self.reader.getPageSource()
        self.doc_etree = etree.parse(StringIO(self.orig_page_source), etree.HTMLParser())
    
    def getBaseName(self):
        return get_website_name_for_tracker_update(self.url)
    
    def moveTo(self, new_page):
        cur_base_page = get_website_name_for_tracker_update(self.url)
        new_base_page = get_website_name_for_tracker_update(new_page)
        if cur_base_page != new_base_page:
            return False
        
        self.url = new_page
        if self.reader_present:
            self.reader.moveTo(new_page)
        self.title = ""
        self.price = ""
        self.product_images = []
        
        return True
    
    def GetTitle(self):
        title = self.GetTitleUsingUrllib2()
        if not title:
            title = self.GetTitleUsingSelenium()
        
        return title
    
    def GetPriceFromXpathKeyUsingUrllib2(self, key, context=''):
        price = ""
        if not self.urllib2_present:
            return price
        
        price_html = ""
        t = self.t;
        try:
            price_xpath = self.tracker_info[key]
            if price_xpath and price_xpath != "/":
                price_xpath = simplify_xpath_before_idtag(price_xpath)
                price = textHasPrice(self.GetTextFromXPath(price_xpath))
                if price:
                    price_html = etree.tostring(self.doc_etree.xpath(price_xpath)[0]).strip()
        except:
            a = 1
        
        if price and price_html:
            price = self.RefinePrice(str(price), price_html)
        
        if not price: # incase price found is zero or none somewhere
            price = ""
        
        return price

    def GetPriceFromXpathKeyUsingSelenium(key, context=''):
        price = ""
        price_html = ""
        
        if not self.reader_present:
            return price
        
        t = self.t;
        try:
            price_xpath = simplify_xpath_before_idtag(self.tracker_info[key])
            if price_xpath and price_xpath != "/":
                price_element = self.reader.getElementByXPath(price_xpath)
                if price_element:
                    price = textHasPrice(price_element.text.strip())
                    if price:
                        price_html = readWebElementAttr(price_element, 'outerHTML')
                        
        except:
            a = 1
        
        if price == None:
            price = "" 
        elif price and price_html:
            price = self.RefinePrice(str(price), price_html)
        else:
            price = str(price).strip()
            if price.startswith("$"):
                price = price[1:]
        
        #if price:
        #    price = price.strip()
        
        return price
        
            
    def GetPriceFromXpathKey(self, key, method):
        if 'urllib2' == method:
            price = self.GetPriceFromXpathKeyUsingUrllib2(key)
        elif 'selenium' == method:
            price = self.GetPriceFromXpathKeyUsingSelenium(key)
        return price
        
    def GetSalePriceSet(self, method):
        sale_price = self.GetPriceFromXpathKey('saleprxpath_onsale', method)
        regular_price = self.GetPriceFromXpathKey('regprxpath_onsale', method)
        was_price = self.GetPriceFromXpathKey('wasprxpath_onsale', method)
        if sale_price or regular_price or was_price:
            return {'sale_price':sale_price, 'regular_price':regular_price, 'was_price':was_price}
        else:
            return None
        
    def GetRegularPriceSet(self, method):
        regular_price = self.GetPriceFromXpathKey('pricexpath', method)
        was_price = self.GetPriceFromXpathKey('oldpricexpath', method)
        if regular_price or was_price:
            return {'regular_price':regular_price, 'was_price':was_price}
        else:
            return None
        
    def GetPrice(self):
        price_set = self.GetPriceUsingUrllib2()
        if price_set:
            price = self.calc_price_from_price_set(price_set)
            if not price:
                # not using price set in selenium yet
                price = self.GetPriceUsingSelenium()
                return price
        
        
        return ""
 
    def GetProductImage(self):
        pimg = self.GetProductImageUsingUrllib2()
        if not pimg:
            pimg = self.GetProductImageUsingSelenium()
        
        return pimg
    
       
    def GetTextFromXPath(self, xpath_to_check):
        
        req_text = ""        
        try:
#        if 1:
            parent_paths = xpath_to_check.split("*/")
            i = 0
            tp = len(parent_paths)
            html = self.orig_page_source
            while i<tp:
                sub_etree = etree.parse(StringIO(html), etree.HTMLParser())
                temp_path = parent_paths[i]
                temp_path = temp_path if 0==temp_path.find("//") else "//"+temp_path
                temp_path = temp_path[:-1] if temp_path[-1] == "/" else temp_path
                eles = sub_etree.xpath(temp_path)
                if eles is not None:
                    element = eles[0]
                if i < tp-1:
                    html = etree.tostring(element)
                    html = "<html><body>"+html+"</body></html>"
                if i==tp-1:
                    path_n_prop = seg_prop_from_xpath(temp_path)
                    if path_n_prop or temp_path.endswith("/text()"):
                        req_text_striped = element.strip()
                    else:
                        html = etree.tostring(element)
                        req_text_striped = etree.tostring(element, encoding="utf-8", method="text").strip()
                    req_text = req_text_striped
                i=i+1
#        try:
#            a = 1
        except Exception, e:
            raise
            pass
            
#            path_n_prop = seg_prop_from_xpath(xpath_to_check)
#            eles = self.doc_etree.xpath(xpath_to_check)
#            
#            if (eles is not None) and len(eles) >= 1:
#                element = eles[0]
#                if path_n_prop:
#                    req_text_striped = element.strip()
#                else:
#                    element_html = etree.tostring(element)
#                    req_text_striped = etree.tostring(element, encoding="utf-8", method="text").strip()
#                req_text = req_text_striped
#        except Exception, e:
#            raise
#            pass
        
        return req_text
    
    
    def GetTitleUsingUrllib2(self):
        title = ""
        if not self.urllib2_present:
            return title
        
        t = self.t;
        try:
            title_xpath = self.tracker_info['titlexpath']
            if title_xpath and title_xpath != "/":
                title_xpath = simplify_xpath_before_idtag(title_xpath)
                title = self.GetTextFromXPath(title_xpath)
            if not title:
                title = self.GetTextFromXPath("//title")
        except:
            a = 1
        
        return clean_product_title(title)
    
    def GetTitleUsingSelenium(self):
        title = ""
        if not self.reader_present:
            return title
        
        t = self.t;
        try:
            title_xpath = simplify_xpath_before_idtag(self.tracker_info['titlexpath'])
            if title_xpath and title_xpath != "/":
                title_element = self.reader.getElementByXPath(title_xpath)
                if title_element:
                    title = title_element.text
            if not title:
                title = self.reader.getDriver().title
        except:
            a = 1
        
        if title:
            title = title.strip()
        
        return clean_product_title(title)
    
    def RefinePrice(self, price, price_html):
        
        price = price.strip()
        if price.startswith("$"):
            price = price[1:]
        if len(price)>=3:
            possible_cents = price[-2:]
            possible_dollar = price[:-2]
            ih = price_html.replace(" ", "")
            if ((">$"+possible_dollar+"<" in ih) or (">"+possible_dollar+"<" in ih)) and (">"+possible_cents+"<" in ih):
                #price = possible_dollar + "." + possible_cents
                if possible_dollar[-1] == '.':
                    price = possible_dollar + possible_cents
                else:
                    price = possible_dollar + "." + possible_cents
            
        return price
        
    def GetPriceFromTitleAndPriceStr(self, title_and_price_str):
        price = ""
        ss = title_and_price_str.split("\n")
        for s in ss:
            if not s:
                continue
            s = s.strip()
            if not s:
                continue
            
            new_price = textIsNewPrice(s)
            if new_price:
                price = new_price
                break
                            
            this_price = textIsPrice(s)
            if this_price and this_price > 0:
                if not price:
                    price = this_price
                elif this_price < price:
                    price = this_price
        
        return str(price)
    
    
    def GetPriceUsingUrllib2(self):
        
        price_set = {}
        if not self.urllib2_present:
            return price_set
        sale_price_set = self.GetSalePriceSet('urllib2');
        prices = []
        if sale_price_set:
            if sale_price_set['sale_price']:
                prices.append(float(sale_price_set['sale_price']))
            if sale_price_set['regular_price']:
                prices.append(float(sale_price_set['regular_price']))
            if sale_price_set['was_price']:
                prices.append(float(sale_price_set['was_price']))
            
        regular_price_set = self.GetRegularPriceSet('urllib2');
        if regular_price_set:
            if regular_price_set['regular_price']:
                prices.append(float(regular_price_set['regular_price']))
            if regular_price_set['was_price']:
                prices.append(float(regular_price_set['was_price']))
        
        prices.sort()
        total_prices = len(prices)
        if total_prices >= 3:
            price_set['was_price'] = prices[2]
        if total_prices >= 2:
            price_set['regular_price'] = prices[1]
        if total_prices >= 1:
            price_set['sale_price'] = prices[0]
        
        return price_set;
        
        # return here
        price = ""
        if not self.urllib2_present:
            return price
        
        price_html = ""
        t = self.t;
        try:
            price_xpath = self.tracker_info['pricexpath']
            if price_xpath and price_xpath != "/":
                price_xpath = simplify_xpath_before_idtag(price_xpath)
                price = textHasPrice(self.GetTextFromXPath(price_xpath))
                if price:
                    price_html = etree.tostring(self.doc_etree.xpath(price_xpath)[0]).strip()
                    
            if not price:
                title_and_price_xpath = self.tracker_info['title_price_xpath']
                if title_and_price_xpath and title_and_price_xpath != "/":
                    title_and_price_xpath = simplify_xpath_before_idtag(title_and_price_xpath)
                    title_and_price = self.GetTextFromXPath(title_and_price_xpath)
                    price = self.GetPriceFromTitleAndPriceStr(title_and_price)
                    if price:
                        price_html = etree.tostring(self.doc_etree.xpath(title_and_price_xpath)[0]).strip()
        except:
            a = 1
        
        if price and price_html:
            price = self.RefinePrice(str(price), price_html)
        
        if not price: # incase price found is zero or none somewhere
            price = ""
        
        return price
    
    # not using concept of price set in selenium yet
    def GetPriceUsingSelenium(self):
        price = ""
        price_html = ""
        
        if not self.reader_present:
            return price
        
        t = self.t;
        try:
            price_xpath = simplify_xpath_before_idtag(self.tracker_info['pricexpath'])
            if price_xpath and price_xpath != "/":
                price_element = self.reader.getElementByXPath(price_xpath)
                if price_element:
                    price = textHasPrice(price_element.text.strip())
                    if price:
                        price_html = readWebElementAttr(price_element, 'outerHTML')
                        
        except:
            a = 1
        
        if not price:
            try:
                title_and_price_xpath = simplify_xpath_before_idtag(self.tracker_info['title_price_xpath'])
                if title_and_price_xpath and title_and_price_xpath != "/":
                    title_and_price_xpath_element = self.reader.getElementByXPath(title_and_price_xpath)
                    if title_and_price_xpath_element:
                        title_and_price = title_and_price_xpath_element.text
                        price = self.GetPriceFromTitleAndPriceStr(title_and_price)
                        if price:
                            price_html = readWebElementAttr(title_and_price_xpath_element, 'outerHTML')
                            
            except:
                a = 1
        
        if price == None:
            price = ""
        elif price and price_html:
            price = self.RefinePrice(str(price), price_html)
        else:
            price = str(price).strip()
            if price.startswith("$"):
                price = price[1:]
        
        #if price:
        #    price = price.strip()
        
        return price
    
        
    def GetProductImageFromPinPos(self):
        pin_pos = self.tracker_info['pinterest_position']
        # check if we know the pin pos
        if not pin_pos or (('0' == pin_pos) or (0==pin_pos)):
            return ""
        
        pin_pos_words = pin_pos.split( )
        pin_start = self.orig_page_source.find("pinterest.com/pin/create/button")
        pin_end1 = self.orig_page_source.find("\"",pin_start)
        pin_end1 = 1000000 if pin_end1 == -1 else pin_end1
        pin_end2 = self.orig_page_source.find("'",pin_start)
        pin_end2 = 1000000 if pin_end2 == -1 else pin_end2
        pin_end = min(pin_end1, pin_end2)
        
        if 1000000 == pin_end:
            return ""
        if pin_start == pin_end:
            return ""
        
        pin = self.orig_page_source[pin_start:pin_end]
        pin = pin[pin.find(pin_pos_words[0]) + len(pin_pos_words[0]) : ]
        if len(pin_pos_words)>1:
            img_end = pin.find(pin_pos_words[1])
            pin = pin[:img_end] if img_end != -1 else pin
        pin = urllib.unquote(pin).encode("ascii","ignore")
        if pin:
            return pin
        
        return ""
    
    def GetProductImageUsingUrllib2(self):
        product_image = ""
        if not self.urllib2_present:
            return product_image
        
        t = self.t;
        pimg_xpaths = []
        if('1'==self.tracker_info['is_image_in_og_image_meta_tag']):
            pimg_xpaths.append("//html/head/meta[@property='og:image']/@content")
        
        pimg_xpaths.append(self.tracker_info['urllib2_pimg_xpath1'])
        pimg_xpaths.append(self.tracker_info['urllib2_pimg_xpath2'])
        pimg_xpaths.append(self.tracker_info['urllib2_pimg_xpath3'])
        pimg_xpaths.append(self.tracker_info['urllib2_pimg_xpath4'])
        pimg_xpaths.append(self.tracker_info['urllib2_pimg_xpath5'])
        
        pimg_xpaths.append(self.tracker_info['pimg_xpath'])
        if (self.tracker_info['pimg_xpath1']) and (self.tracker_info['pimg_xpath'] != self.tracker_info['pimg_xpath1']):
            pimg_xpaths.append(self.tracker_info['pimg_xpath1'])
        
        pimg_xpaths.append(self.tracker_info['pimg_xpath2'])
        pimg_xpaths.append(self.tracker_info['pimg_xpath3'])
        pimg_xpaths.append(self.tracker_info['pimg_xpath4'])
        pimg_xpaths.append(self.tracker_info['pimg_xpath5'])
        real_images = []
        for xpath in pimg_xpaths:
            try:
                if xpath and xpath != "/" and xpath != 'NULL':
                    xpath = simplify_xpath_before_idtag(xpath)
                    product_images = self.doc_etree.xpath(add_atsrc_if_needed(xpath))
                    if (product_images is not None) and (len(product_images)>=1):
                        product_image = product_images[0].strip()
                        if product_image:
                            product_image_netloc = urlparse(product_image)[1]
                            if not product_image_netloc:
                                product_image = urljoin(self.url, product_image)
                            real_images.append(AddHTTP(product_image))
                            self.real_images_lxml_ele.append(self.doc_etree.xpath(xpath)[0])
                        
            except Exception, e:
                a = 1
        
        if not real_images:
            pin_image = self.GetProductImageFromPinPos()
            if pin_image:
                real_images.append(pin_image)
        
        return real_images
    
    def GetProductImageUsingSelenium(self):
        
        product_image = ""
        if not self.reader_present:
            return product_image
        
        t = self.t;
        pimg_xpaths = []
        pimg_xpaths.append(self.tracker_info['pimg_xpath1'])
        pimg_xpaths.append(self.tracker_info['pimg_xpath2'])
        pimg_xpaths.append(self.tracker_info['pimg_xpath3'])
        pimg_xpaths.append(self.tracker_info['pimg_xpath4'])
        pimg_xpaths.append(self.tracker_info['pimg_xpath5'])
        real_images = []
        for xpath in pimg_xpaths:
            try:
                if xpath and xpath != "/" and xpath != 'NULL':
                    xpath = simplify_xpath_before_idtag(xpath)
                    path_n_prop = seg_prop_from_xpath(xpath)
                    if path_n_prop:
                        xpath = path_n_prop[0]
                        prop = path_n_prop[1]
                    else:
                        prop = 'src'
                    
                    pimg_element = self.reader.getElementByXPath(xpath)#+'/@src')
                    img_src = "";
                    if pimg_element:
                        img_src = readWebElementAttr(pimg_element, prop)
                    if img_src:
                        product_image = img_src.strip()
                        real_images.append(product_image)
            except:
                a = 1
        
        return real_images
    
    def doesElementStrHasGivenPrice(self, price, ele):
        req_text = etree.tostring(ele, encoding="utf-8", method="text")
        if req_text:
            sentence_list = req_text.split('\n')
            for s in sentence_list:
                s = s.strip()
                text_price = textIsPrice(s)
                if not text_price:
                    text_price = textIsNewPrice(s)
                if text_price and (text_price == price):
                    return True
        
        return False
        
    def getDeepestChildWithSamePrice(self, price, top_ele):
        
        es = [top_ele]
        req_ele = top_ele
        i = 0
        while i < len(es):
            has_price = self.doesElementStrHasGivenPrice(price, es[i])
            if has_price: # if it has price, then go deeper
                req_ele = es[i]
                es = es + list(es[i])
            i += 1
                    
        return req_ele
        
    
    def ExtractDetailAroundLxmlImage(self):
        
        title = price = ""
        image_covering_ele = self.real_images_lxml_ele[0]
        
        req_info_found = False
        sentence_list = [""]
        
        while image_covering_ele != None:
            req_text_striped = etree.tostring(image_covering_ele, encoding="utf-8", method="text").strip()   
            if req_text_striped:
                sentence_list = req_text_striped.split('\n')
                for s in sentence_list:
                    s = s.strip()
                    price = textIsNewPrice(s)
                    if not price:
                        price = textIsPrice(s)
                    if price:
                        req_info_found = True
                        break
                # get out of outer loop
                if req_info_found:
                    break
            image_covering_ele = image_covering_ele.getparent()
        
        doc_title = self.GetTextFromXPath("//title")
        sitename = urlparse(self.url).netloc
        if req_info_found:
            for s in sentence_list:
                if is_str_the_title(s, doc_title, sitename):
                    title = s
                    break
                
            price_ele = self.getDeepestChildWithSamePrice(price, image_covering_ele)
            price_html = etree.tostring(price_ele)
            price = self.RefinePrice(str(price), price_html)
                        
        ret = {'title' : title, 'price' : price}
        #if req_info_found:
        #    ret = self.dfs_lxml_tree_to_get_title_and_price(image_covering_ele, ret['title'], ret['price'])
            
        return ret
        
    def dfs_lxml_tree_to_get_title_and_price(self, ele, title, price):
        
        ret = {'title': title, 'price' : price}
        
        str = etree.tostring(ele, encoding="utf-8", method="text").strip()
        words = nicely_clean_word_list(str)
        if (not str) or (len(words) < 2):
            return ret
        
        if not title:
            doc_title = self.GetTextFromXPath("//title")
            if is_str_the_title(str, doc_title, self.url):
                title = req_text_striped
        
        if not price:
            element_html = etree.tostring(ele)
            price = textHasPrice(str)
            if price:
                price = self.RefinePrice(str(price), element_html)
        
        ret = {'title': title, 'price' : price}
        if title and price:
            return ret
        
        childs = list(ele)
        for e in childs:
            ret = dfs_lxml_tree_to_get_title_and_price(e, title, price)
            if ret['title'] and ret['price']:
                break
        
        return ret
        
    def get_surrouding_details(self):
        self.enableUrllib2()
        #self.customize_tracker_info(self.orig_page_source)
        self.build_regex_substituted_tracker_info(self.orig_page_source)
        
        self.product_images = self.GetProductImageUsingUrllib2()
        if ((not self.title) or (not self.price)) and self.product_images:
            ret = self.ExtractDetailAroundLxmlImage()
            self.title = ret['title']
            self.price = ret['price']
        
        if self.product_images:
            for img in self.product_images:
                if img:
                    self.main_product_image = img
                    break
        
    def get_details_using_urllib2(self):
        
        self.enableUrllib2()
        self.build_regex_substituted_tracker_info(self.orig_page_source)
        self.generate_guessed_tracker_info(self.orig_page_source)
        
        self.title = self.GetTitleUsingUrllib2()
        #self.oldprice = self.GetOldPriceUsingUrllib2()
        self.price_set = self.GetPriceUsingUrllib2()
        if self.price_set:
            self.calc_price_from_price_set()
        self.product_images = self.GetProductImageUsingUrllib2()
        
        temp_tracker_info = self.tracker_info.copy()
        self.tracker_info = self.secondary_tracker_info
        if (not self.title):
            self.title = self.GetTitleUsingUrllib2()
        if (not self.price_set):
            self.price_set = self.GetPriceUsingUrllib2()
            if self.price_set:
                self.calc_price_from_price_set()
        if (not self.product_images):
            self.product_images = self.GetProductImageUsingUrllib2()
        # reset tracker info to original
        self.tracker_info = temp_tracker_info
        
        # try guessed tracker now
        temp_tracker_info = self.tracker_info.copy()
        self.tracker_info = self.guessed_tracker_info
        if (not self.title):
            self.title = self.GetTitleUsingUrllib2()
        if (not self.price_set):
            self.price_set = self.GetPriceUsingUrllib2()
            if self.price_set:
                self.calc_price_from_price_set()
        if (not self.product_images):
            self.product_images = self.GetProductImageUsingUrllib2()
        # reset tracker info to original
        self.tracker_info = temp_tracker_info
        
    def get_details_using_selenium(self):
        
        self.enableReader()
        self.build_regex_substituted_tracker_info(self.orig_page_source)
        self.generate_guessed_tracker_info(self.orig_page_source)
        
        self.title = self.GetTitleUsingSelenium()
        self.price = self.GetPriceUsingSelenium()
        self.product_images = self.GetProductImageUsingSelenium()
            
        temp_tracker_info = self.tracker_info.copy()
        self.tracker_info = self.secondary_tracker_info
        if (not self.title):
            self.title = self.GetTitleUsingSelenium()
        if (not self.price):
            self.price = self.GetPriceUsingSelenium()
        if (not self.product_images):
            self.product_images = self.GetProductImageUsingSelenium()
        # reset tracker info to original
        self.tracker_info = temp_tracker_info
        
        # try guessed tracker now
        temp_tracker_info = self.tracker_info.copy()
        self.tracker_info = self.guessed_tracker_info
        if (not self.title):
            self.title = self.GetTitleUsingSelenium()
        if (not self.price):
            self.price = self.GetPriceUsingSelenium()
        if (not self.product_images):
            self.product_images = self.GetProductImageUsingSelenium()
        # reset tracker info to original
        self.tracker_info = temp_tracker_info
        
    def calc_price_from_price_set(self, price_set=None):
        if not price_set:
            price_set = self.price_set
        
        if price_set:
            self.sale_price = price_set['sale_price'] if "sale_price" in price_set else -1
            self.regular_price = price_set['regular_price'] if "regular_price" in price_set else -1
            self.was_price = price_set['was_price'] if "was_price" in price_set else -1
        else:
            self.sale_price = -1
            self.regular_price = -1
            self.was_price = -1
        
        if self.sale_price != -1:
            self.price = self.sale_price
        elif self.regular_price != -1:
            self.price = self.regular_price
        elif self.was_price != -1:
            self.price = self.was_price
        else:
            self.price = ""
        
        return self.price
         
    def get_details(self):
        
        if self.mode == 'fast':   #default mode
            self.get_details_using_urllib2()
        elif self.mode == 'accurate':
            self.get_details_using_selenium()    
          
        if self.product_images:
            for img in self.product_images:
                if img:
                    self.main_product_image = img
                    break
        
    def run(self):
        if not self.tracker_info:
            return False
        
        self.get_details()
        return True
    
    def test(self):
        
        test_urls = []
        test_urls.append("")
        test_urls.append("")
        test_urls.append("")
        test_urls.append("")
        test_urls.append("")
        test_urls.append("")
        test_urls.append("")
        test_urls.append("")
        test_urls.append("")
        
        for url in test_urls:
            fe = FeatureExtractor(url)
            fe.run()
            fe.deinit()
    

