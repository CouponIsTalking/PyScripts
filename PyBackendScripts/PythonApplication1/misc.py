import httplib
import datetime
import re
from urlparse import urlparse
from urlparse import urljoin
from urlparse import parse_qs

from StringIO import StringIO
import lxml.html
from lxml import etree

def do_rectangles_intersect(ax1, ax2, ay1, ay2, bx1, bx2, by1, by2):
    
#    max_x = max(ax1,ax2,bx1,bx2)
#    min_x = min(ax1,ax2,bx1,bx2)
#    max_y = max(ay1,ay2,by1,by2)
#    min_y = min(ay1,ay2,by1,by2)
#    
#    if (max_x-min_x <= ax2+bx2-ax1-bx1) and (maxy-min_y <= ay2+by2-ay1-by1):
#        return True
#    else:
#        return False
    
    if ((bx1 <= ax1) and (ax1 <= bx2)) or ((bx1 <= ax2) and (ax2 <= bx2)):
        if ((by1 <= ay1) and (ay1 <= by2)) or ((by1 <= ay2) and (ay2 <= by2)):
            return True
    return False
  
def create_full_path_from_bgimage_prop(bg_img, baseurl):
    url_matches = re.findall(r'\"(.+?)\"', bg_img)
    full_path = get_full_path(url_matches[0], baseurl) if (url_matches and url_matches[0]) else ""
    return full_path

def get_full_path (imagelink, baseurl):
    imagelink_netloc = urlparse(imagelink).netloc
    if not imagelink_netloc:
        imagelink = urljoin(baseurl, imagelink)
    return imagelink

def is_image_present_in_og_image_meta_tag(imagelink, baseurl, et1):
    
    if not imagelink:
        return False
    
    imagelink = AddHTTP(get_full_path(imagelink, baseurl))
    
    meta_element = et1.xpath("//meta")
    for x in meta_element:
        if x.get("property") == "og:image":
            content = x.get("content")
            if content.lower() == imagelink.lower():
                return True
    
    return False

def image_position_in_pinterest_link(imagelink, baseurl, et1):
    
    if not imagelink:
        return ""
    
    imagelink = AddHTTP(get_full_path(imagelink, baseurl))
    
    pinterest_pos = ""
    
    meta_element = et1.xpath("//a")
    for x in meta_element:
        href = x.get("href")
        if href:
            netloc = urlparse(href).netloc
            if "pinterest.com" in netloc:
                if pinterest_pos:
                    pinterest_pos = ""
                    break
                
                qs = urlparse(href).query
                parsed_qs = parse_qs(qs)
                if ('media' in parsed_qs) and (len(parsed_qs['media']) > 0):
                    if parsed_qs['media'][0].lower() == imagelink.lower():
                        pinterest_pos = "media_0"
    
    return pinterest_pos

def get_xpath_of_lxml_element(element, et1):
    # takes element as first arg, and etree as second arg
    full_xpath = et1.getpath(element)
    
    parent = element
    level = 0
    full_xpath_words = full_xpath.split('/')
    new_xpath = ""
    
    while parent is not None:
        level = level + 1
        idname = parent.get('id')
        if idname:
            new_xpath = "//" + parent.tag + "[@id='"+idname+ "']" + new_xpath
            full_xpath = new_xpath
            break
        
        new_xpath = "/" + full_xpath_words[0-level] + new_xpath
        parent = parent.getparent()
    
    return full_xpath
         
def seg_prop_from_xpath(xpath):
    if not xpath:
        return False
    index_of_at = xpath.find("/@")
    if -1==index_of_at:
        return False
    
    path = xpath[0:index_of_at]
    prop = xpath[index_of_at+2:]
    return [path, prop]

def does_xpath_ends_with_prop(xpath):
    if not xpath:
        return False
    if xpath.find('/@') > 0:
        return True
    return False

def add_atsrc_if_needed(xpath):
    if not xpath:
        return xpath
    if does_xpath_ends_with_prop(xpath):
        return xpath
    else:
        return xpath + "/@src"
    
def simplify_xpath_before_idtag(xpath):
    if not xpath:
        return xpath
    
    index_of_id = xpath.find("@id=")
    if index_of_id > 0:
        slash_index = xpath.rfind("/",0, index_of_id)
        xpath= "/" + xpath[slash_index:]
    return xpath
            
def get_website_name_for_tracker_update(url):
	
	url = url.lower()
	if url.startswith("http://"):
		url = url[len("http://"):]
	if url.startswith("https://"):
		url = url[len("https://"):]
	indexOfSlash = url.find("/")
	if indexOfSlash>0:
		url = url[:indexOfSlash]
		
	return url
	
	
# incomplete, define rectangle distance
def rectangle_dist(ax1, ax2, ay1, ay2, bx1, bx2, by1, by2):
    
    x_dist = min(abs(ax1-bx1), abs(ax1-bx2), abs(ax2-bx1), abs(ax2-bx2))
    y_dist = min(abs(ay1-by1), abs(ay1-by2), abs(ay2-by1), abs(ay2-by2))

def html_to_words(html):
    html = re.sub('[\.<>=\\/"|~|!|@|#|$|%|^|&|*|(|)|{|}| |1|2|3|4|5|6|7|8|9|0]+',' ', html)
    html = html.rstrip().lstrip().lower()
    html = re.sub(' +',' ', html)
    words = html.split(' ')
    return words
    
def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub("[' ']+",' ', text)
    text = text.strip()
    return text

def nicely_clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    text = re.sub("[' ']+",' ', text)
    text = text.strip()
    return text
    
def nicely_clean_word_list(text):
    text = nicely_clean_text(text)
    words = [w for w in re.split('\W', text) if w]
    return words
    
def clean_product_title(title):
    title = re.sub('[\.|-| |\!]+',' ', title).strip()
    title = re.sub(' +',' ', title)
    words = title.split(' ')
    new_title = ""
        
    for w in words:
        if w == ':':
            break
        if w.lower() == 'by':
            break
        else:
            new_title = new_title + " " + w
        
    return new_title.strip()
            
def is_str_the_title(str, doc_title, sitename):
    sitename = sitename.lower()
    doc_title = doc_title.lower()
    words = nicely_clean_word_list(clean_product_title(str.lower()))
    
    qualifying_words = 0
    
    for w in words:
        if w == "by":
            break
        elif w == "new":
            pass
        elif w in sitename:
            pass
        else:
            if w not in doc_title:
                return False
            qualifying_words += 1
    
    if qualifying_words >= 2:    
        return True
    else:
        return False
        
def get_numeric_words(text):
    return [w for w in re.sub('[ ]+', ' ', re.sub('[^0-9]', ' ', text)).split(' ') if w]
  

def get_numstrs_in_str(s, min_num_str_len):
    num_words = get_numeric_words(s)
    num_words = filter(lambda x: len(x) >= min_num_str_len, num_words)
    return num_words

def get_id_from_xpath(xpath):
    index_of_id = xpath.find("@id=")
    if index_of_id < 0:
        return ""
    idname = xpath[xpath.find("@id=") + 5:xpath.find("]", xpath.find("@id="))-1]
    return idname

def get_id_substituted_xpath(xpath, str_to_look_in):
    idname = get_id_from_xpath(xpath)
    num_words = get_numstrs_in_str(idname, 4)
    for key_word in num_words:
        ds = ""
        for c in key_word:
            ds += "\d"
        idname_with_regex = idname.replace(key_word, ds)
        pat = re.compile(idname_with_regex)
        new_matches = pat.search(str_to_look_in)
        if not new_matches:
            continue
        new_match = new_matches.group(0)
        orig_match = pat.search(xpath).group(0)
        new_xpath = xpath.replace(orig_match, new_match, 1)
        return new_xpath
    return xpath

def get_regex_substituted_xpath(xpath, regex, str_to_look_in):
    #print xpath
    #print regex
    if not xpath:
        return xpath
    
    if not regex:
        return xpath
    #print [regex, xpath];
    idname = xpath[xpath.find("@id=") + 5:xpath.find("]", xpath.find("@id="))-1]
    pat = re.compile(regex)
    
    matches = pat.search(idname)
    if not matches:
        return xpath
    
    expr_in_idname = matches.group(0)
    expr_pos = matches.start(0)
    idname_with_regex = idname[:expr_pos] + idname[expr_pos:].replace(expr_in_idname, regex, 1)
    pat = re.compile(idname_with_regex)
    
    new_matches = pat.search(str_to_look_in)
    if not new_matches:
        return xpath
    # match found, now build the new xpath
    new_match = new_matches.group(0)
    orig_match = pat.search(xpath).group(0)
    new_xpath = xpath.replace(orig_match, new_match, 1)
    return new_xpath
    

def get_id_regex_from_xpaths(xpaths):
    #assumes that all xpaths are of equal length, having similar pattern
    
    for xpath in xpaths:
        if (not xpath) or (len(xpath) < 2):
            return ""
    
    expr = ""
    start_pat = -1
    end_pat = -1
    ids = map(lambda x: get_id_from_xpath(x), xpaths)
    ids_len = len(ids[0])
    
    print xpaths
    if ids_len == 0:
        return expr
    
    i = 0
    while (i < ids_len) and (start_pat == -1):
        c = ids[0][i]
        for id in ids:
            if id[i] != c:
                start_pat = i
                break
        i+=1
    
    reversed_ids = map(lambda x: x[::-1], ids)
    i = 0
    while (i < ids_len) and (end_pat == -1):
        c = reversed_ids[0][i]
        for reversed_id in reversed_ids:
            if reversed_id[i] != c:
                end_pat = i
                break
        i+=1
    
    if start_pat == -1:
        return expr
    
    pat_str = ids[0][start_pat: len(ids[0])-end_pat]
    expr = ""
    
    for c in pat_str:
        if c.isdigit():
            expr += "\d"
        elif c.isalpha():
            expr += "[a-zA-Z]"
        else:
            c = re.escape(c)
            expr += c
        
    return expr


def find_product_id_in_xpaths(xpaths):
    for xpath in xpaths:
        num_words = get_numstrs_in_str(xpath)
    
def get_words_before_sub_text(text, sub_text, look_from_end):
    
    if look_from_end:
        sub_text_index = text.rfind(sub_text)
    else:
        sub_text_index = text.find(sub_text)
        
    if sub_text_index > 0:
        text_before_sub_text = text[:sub_text_index]
        text_before_sub_text = text_before_sub_text.replace("\n", " ")
        #text_before_sub_text = re.sub('[\.<>=\\/"|~|!|@|#|$|%|^|&|*|(|)|{|}| |1|2|3|4|5|6|7|8|9|0]+',' ', text_before_sub_text)
        words_before_sub_text = [w for w in re.split('\W', text_before_sub_text) if w]
        return words_before_sub_text
    
    return []
    
def ins_in_map (k, map, v):
    if k not in map:
        map[k] = []
    map[k].append(v)

def get_refined_prices(prices, html):
    if not prices:
        return []
        
    refined_prices = []
    for price in prices:
        price = price.strip()
        if price.startswith("$"):
            price = price[1:]
        if len(price)>=3:
            possible_cents = price[-2:]
            possible_dollar = price[:-2]
            ih = html
            if (">$"+possible_dollar+"<" in ih) and (">"+possible_cents+"<" in ih):
                price = possible_dollar + "." + possible_cents
            elif (">"+possible_dollar+"<" in ih) and (">"+possible_cents+"<" in ih) :
                price = possible_dollar + "." + possible_cents
            elif (">"+possible_dollar+".<" in ih) and (">"+possible_cents+"<" in ih) :
                price = possible_dollar + "." + possible_cents
            elif (">"+possible_dollar+"<" in ih) and (">."+possible_cents+"<" in ih) :
                price = possible_dollar + "." + possible_cents
                
        refined_prices.append(price)
    
    return refined_prices
    
def textHasDollarPrice(s):
    s=s.strip().lower()
    s=s.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", "")
    s=s.replace("usd$", "$").replace("us$", "$").replace("usd", "$")
    
    match = re.search('\$\d*[.]?\d+', s)
    if match:
        return True
    if not s:
        match = re.search('\d*[.]?\d+\$', s)
        if match:
            return True
    
    return False
    

def textIsPrice(s):
    s = s.strip().lower()
    s = re.sub(',','', s)
    
    if s:
        s = s.replace("\n", "").replace("\t", "").replace("\r", "").replace(" ", "")
    
    s=s.replace("usd$", "$")
    s=s.replace("us$", "$")
    s=s.replace("usd", "$")
    
    if s and s != "$":
        match = re.search('^\$\d*[.]?\d+[\$]?$', s)
        if match:
            return textHasPrice(s)
            #return match.group(0)
        if not match:
            match = re.search('^\d*[.]?\d+\$$', s)
        if not match:
            match = re.search('^\d*[.]?\d+\$[-]\d*[.]?\d+\$$', s)
        
        if not match:
            match = re.search('^price[.|:]?\$\d*[.]?\d+$', s)
        
        if not match:
            match = re.search('^price[.|:]?\$\d*[.]?\d+[-]\$\d*[.]?\d+$', s)
        
        if not match:
            match = re.search('^price[.|:]?\$\d*[.]?\d+[-]\$\d*[.]?\d+$', s)
        
        if match:
            return textHasPrice(s)
            #return match.group(0)
            
#		match = re.search('\$\d*[.]?\d*', s)
#		if match:
#			return match.group(0)
    
    return None

def textIsNewPrice(s):
    s = s.strip().lower()
    s = re.sub(',','', s)
    
    if s:
        s = s.replace(":", "")
    if s:
        s = s.replace("\n", "")
    if s:
        s = s.replace("\t", "")
    if s:
        s = s.replace("\r", "")
    if s:
        s = s.replace(" ", "")
    
    s=s.replace("usd$", "$")
    s=s.replace("us$", "$")
    s=s.replace("usd", "$")
    
    if s and s != "$":
        match = re.search('^now[.]?\$\d*[.]?\d+[\$]?$', s)
        if match:
            return textHasPrice(s)
        
        match = re.search('^now[.]?\$\d*[.]?\d+[-]\$\d*[.]?\d+$', s)
        if match:
            return textHasPrice(s)
        
        match = re.search('^only[.]?\$\d*[.]?\d+$', s)
        if match:
            return textHasPrice(s)
        
        match = re.search('^only[.]?\$\d*[.]?\d+[-]\$\d*[.]?\d+$', s)
        if match:
            return textHasPrice(s)
        
#		match = re.search('\$\d*[.]?\d*', s)
#		if match:
#			return match.group(0)
    
    return None

def textIsOldPrice(s):
    s = s.strip().lower()
    s = re.sub(',','', s)
    
    if s:
        s = s.replace(":", "")
    if s:
        s = s.replace("\n", "")
    if s:
        s = s.replace("\t", "")
    if s:
        s = s.replace("\r", "")
    if s:
        s = s.replace(" ", "")
    
    s=s.replace("usd$", "$")
    s=s.replace("us$", "$")
    s=s.replace("usd", "$")
    
    if s and s != "$":
        match = re.search('^was[.]?\$\d*[.]?\d+[\$]?$', s)
        if match:
            return textHasPrice(s)
        
        match = re.search('^was[.]?\$\d*[.]?\d+[-]\$\d*[.]?\d+$', s)
        if match:
            return textHasPrice(s)
        
        match = re.search('^old[.]?\$\d*[.]?\d+$', s)
        if match:
            return textHasPrice(s)
            
        match = re.search('^old[.]?\$\d*[.]?\d+[-]\$\d*[.]?\d+$', s)
        if match:
            return textHasPrice(s)
            
        match = re.search('^orig[.]?\$\d*[.]?\d+$', s)
        if match:
            return textHasPrice(s)
            
        match = re.search('^orig[.]?\$\d*[.]?\d+[-]\$\d*[.]?\d+$', s)
        if match:
            return textHasPrice(s)
        
#		match = re.search('\$\d*[.]?\d*', s)
#		if match:
#			return match.group(0)
    
    return None


def textHasPrice(s):
    
    dollarIndex = 0
    s = s.strip()
    s = re.sub(' +','', s)
    s = re.sub(',','', s)
    s=s.replace("usd$", "$")
    s=s.replace("us$", "$")
    s=s.replace("usd", "$")
    
    
    price_text = ""
    match = re.search('\$\d*[.]?\d+', s)
    if match:
        price_text = match.group(0)[1:]
    if not price_text:
        match = re.search('\d*[.]?\d+\$', s)
        if match:
            price_text = match.group(0)[:-1]
    if not price_text:
        match = re.search('\d*[.]?\d+', s)
        if match:
            price_text = match.group(0)
    
    s = "$" + price_text
        
    lastIndex = len(s) - 1
    
    while dollarIndex <= lastIndex:
    
        while dollarIndex <= lastIndex:
            if s[dollarIndex] == '$':
                break
            else:
                dollarIndex = dollarIndex + 1
        
        i = dollarIndex +1
        beforeDec = 0
        afterDec = 0
        
#		while i <= lastIndex and s[i] == ' ':
#			i = i + 1
            
        while i <= lastIndex and s[i] <= '9' and s[i] >= '0':
            beforeDec = beforeDec * 10 + (int)(s[i]) 
            i = i+1
        
#		while i <= lastIndex and s[i] == ' ':
#			i = i + 1
            
        if i <= lastIndex and s[i] == '.':
            i = i+1
        
#		while i <= lastIndex and s[i] == ' ':
#			i = i + 1
            
        while i <= lastIndex and s[i] <= '9' and s[i] >= '0':
            afterDec = afterDec * 10 + (int)(s[i]) 
            i = i+1
        
        # assumes that price has to be greater than 0.0
        if beforeDec > 0 or afterDec > 0:
            return (float)(str(beforeDec)+'.'+str(afterDec))
        
        dollarIndex = i
        
    
    return None
    
def haveDifferentBaseSite(cur_url, div_url):
    site_name1 = urlparse(AddHTTP(cur_url))[1] #get netloc
    site_name2 = urlparse(AddHTTP(div_url))[1] #get netloc
    if site_name2.startswith("#"):
        return False
    
    if site_name2.startswith("/"):
        return False
    
    if site_name1.find('.') >= 0 and site_name2.find('.') >= 0:
        mparts1 = site_name1.encode("ascii","ignore").lower().split(".")
        mparts2 = site_name2.encode("ascii","ignore").lower().split(".")
        i = 1
        j = min(len(mparts1), len(mparts2))
        mismatch_number = 1000
        while i <= j:
            if mparts1[0-i] == mparts2[0-i]:
                i = i+1
            else:
                mismatch_number = i
                break
        
        if mismatch_number <= 2 :
            return True
    
    return False
    

def doesStrEndsWithImgExt(str):
    str = str.lower()
    if str.endswith('.jpg') or str.endswith('.png') or str.endswith('.jpeg') or str.endswith('.bmp'):
        return True
    else:
        return False
 
   
def pointsToAnImage(div_url):
    # if the url is taking to a purely image page, we keep that url
    div_url_lower = div_url.lower()
    if "scene7" in div_url_lower:
        return True
    
    if doesStrEndsWithImgExt(div_url_lower): #.endswith('.jpg') or div_url_lower.endswith('.png') or div_url_lower.endswith('.jpeg') or div_url_lower.endswith('.bmp'):
        return True
    else:
        parse_object = urlparse(div_url)
        conn = httplib.HTTPConnection(parse_object.netloc)
        conn.request("HEAD", parse_object.path)
        res = conn.getresponse()
        headers = res.getheaders()        
        for (name, val) in headers:
            if ('content-type' == name) and ('image' in val):
                return True
            if ('location' == name) and doesStrEndsWithImgExt(val):
                return True
    
    return False

# assumes that both urls passed in are valid
# , checks if clicking div_url will take outside of the current page given by curl
def isOutgoingLink(curl, div_url):
    
    if not div_url:
        return False
    
    if curl == div_url:
        return False
    
    if True == div_url.startswith(curl+"#"):
        return False
    
    if "javascript" in div_url:
        return False
        
    return True
    
def AddHTTP(s):
    
    # check here if s is a valid url
    # right now we only check for emptiness
    if not s:
        return s
    
    orig_s = s
    if orig_s.find("//") == 0:
        return "http:"	+ orig_s
    
    s=s.lower()
    http_index = s.find("http://")
    https_index = s.find("https://")
    
    if http_index == -1 and https_index == -1:
        return "http://" + orig_s
        
    return orig_s


def addslashes(s):
    d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)

def getTodayMonthDateString(format):
    
    today = datetime.date.today()
    return today.strftime(format)

def getYesterdayMonthDateString(format):

    yesterday = datetime.date.today() - datetime.timedelta(1)
    return yesterday.strftime(format)

def getDigit(s):
    digit = 0
    for c in s:
        if c >= '0' and c <= '9':
            digit = digit*10 + int(c)
        else:
            return 0
            
    return digit
    
def getDate(s):
    date = 0
    for c in s:
        if c>='0' and c<='9':
            date = date*10 + int(c)
        else:
            return 0;
    
    if date >= 1 and date <= 31:
        return date;
    else:
        return 0
        
def getMonth(s):
    
    s = s.lower()
    
    if s == "jan" or s == "january":
            return 1
    if s == "feb" or s == "february":
            return 2
    if s == "mar" or s == "march":
            return 3
    if s == "apr" or s == "april":
            return 4
    if s == "may" or s == "may":
            return 5
    if s == "jun" or s == "jun":
            return 6
    if s == "july" or s == "july":
            return 7
    if s == "aug" or s == "august":
            return 8
    if s == "sep" or s == "september":
            return 9
    if s == "oct" or s == "october":
            return 10
    if s == "nov" or s == "november":
            return 11
    if s == "dec" or s == "december":
            return 12

    return 0;

def lineHasMonthName(s):
    
    s = s.lower()
    
    shortname = []
    shortname.append("jan")
    shortname.append("feb")
    shortname.append("mar")
    shortname.append("apr")
    shortname.append("may")
    shortname.append("jun")
    shortname.append("jul")
    shortname.append("aug")
    shortname.append("sep")
    shortname.append("oct")
    shortname.append("nov")
    shortname.append("dec")
    
    longname = []
    longname.append("january")
    longname.append("february")
    longname.append("march")
    longname.append("april")
    longname.append("may")
    longname.append("jun")
    longname.append("july")
    longname.append("august")
    longname.append("september")
    longname.append("october")
    longname.append("november")
    longname.append("december")
    
    i = 0
    while i < len(shortname):
        
        # if line contains full long name of the month, then return index at that point
        if s.find(longname[i]) >= 0:
            return longname[i]
            
        # else if short month name exists then ensure that it has terminating characters before and after it
        elif s.find(shortname[i]) >= 0:
            
            p = s.find(shortname[i])
            q = p + len(shortname[i])
            
            terminating_char_before_p = -1
            terminating_char_at_q = -1
            
            # is there terminating char before index p or at index p-1 ?
            if p == 0:
                terminating_char_before_p = 1
            else:
                if s[p-1] < 'a' or s[p-1] > 'z': # note that the string is all lower case
                    terminating_char_before_p = 1
            
            
            # is there a terminating char at index q ?
            if q == len(s):
                terminating_char_at_q = 1
            else:
                if s[q] < 'a' or s[q] > 'z':  # note that the string is all lower case
                    terminating_char_at_q = 1
            
            if terminating_char_before_p == 1 and terminating_char_at_q == 1:
                return longname[i]
        
        
        # increment 'i'
        i = i+1
        
        
    
        
    return -1
    
