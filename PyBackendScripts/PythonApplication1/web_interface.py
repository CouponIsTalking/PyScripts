import sys
import urllib
import urllib2
import const
from const import *

import misc
from misc import *

import BeautifulSoup
from BeautifulSoup import BeautifulSoup, Comment
import htmlops
import json

class WebInterface:
    def test_update_tracker_info(self):
        tracker_info = {}
        website = get_website_name_for_tracker_update("http://www.express.com/clothing/ankle+rolled+destroyed+boyfriend+jean/pro/6995673/cat2005")
        
        tracker_info['website'] = website
        tracker_info['title-xpath'] =  "//div[@id='cat-pro-con-detail']/h1"
        tracker_info['price-xpath'] =  "//div[@id='cat-pro-con-detail']/div[2]/strong/span/span[2]"
        tracker_info['product-img-xpath'] =  "//div[@id='flyout']/div[1]/div[1]/div[2]/img"
        tracker_info['title_and_price-xpath'] =  "//div[@id='cat-pro-con-detail']"
        tracker_info['title_price_css'] = json.dumps({'price-css': {'color': 'rgba(255, 0, 0, 1)', 'font-size': '17px', 'font-family'	: 'Arial,sans-serif', 'font-weight': '400'}, 'title-css': {'color': 'rgba(0, 0,	0, 1)', 'font-size': '13px', 'font-family': 'Arial,sans-serif', 'font-weight': '700'}})
        tracker_info['details_xpath'] = ""
        self.update_tracker_info(tracker_info)
        
    
    ## -------------------------------
    ## Given a tracker info
    ## update the database with new 
    ## stats
    ## -------------------------------
    def update_tracker_info (self, tracker_info):
        
        data = {
                    'website' : tracker_info['website'],
                    'titlexpath' : tracker_info['titlexpath'],
                    'pricexpath' : tracker_info['pricexpath'],
                    'oldpricexpath' : tracker_info['oldpricexpath'],
                    'price_cur_code' : tracker_info['price_cur_code'],
                    'old_price_cur_code' : tracker_info['old_price_cur_code'],
                    'pimg_xpath' : tracker_info['pimg_xpath'],
                    'pimg_xpath1' : tracker_info['pimg_xpath1'],
                    'pimg_xpath2' : tracker_info['pimg_xpath2'],
                    'pimg_xpath3' : tracker_info['pimg_xpath3'],
                    'pimg_xpath4' : tracker_info['pimg_xpath4'],
                    'pimg_xpath5' : tracker_info['pimg_xpath5'],
                    'urllib2_pimg_xpath1' : tracker_info['urllib2_pimg_xpath1'],
                    'urllib2_pimg_xpath2' : tracker_info['urllib2_pimg_xpath2'],
                    'urllib2_pimg_xpath3' : tracker_info['urllib2_pimg_xpath3'],
                    'urllib2_pimg_xpath4' : tracker_info['urllib2_pimg_xpath4'],
                    'urllib2_pimg_xpath5' : tracker_info['urllib2_pimg_xpath5'],
                    'image_and_details_container_xpath' : tracker_info['image_and_details_container_xpath'],
                    'image_and_title_parent_xpath' : tracker_info['image_and_title_parent_xpath'],
                    'title_price_xpath' : tracker_info['title_price_xpath'],
                    'title_price_css' : tracker_info['title_price_css'],
                    'details_xpath' : tracker_info['details_xpath'],
                    'is_image_in_og_image_meta_tag' : tracker_info['is_image_in_og_image_meta_tag'],
                    'pinterest_position' : tracker_info['pinterest_position']
                  }
        
        update_url = SITE_NAME+'/tracker_infos/add_tracker_info_from_script/'+ PYTHON_VERIFICATION_CODE;
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        data = urllib.urlencode(data)
        req = urllib2.Request(update_url, data, headers)
        try :
            print update_url
            response = urllib2.urlopen(req)
            print response
            r = response.read()
            f = open("test.html", "w")
            f.write(r)
            f.close()
            print "tracker_info_update called"
        except Exception, e:
            print "Error in updating db"
            print e
            return 0
        
        #returned_page = response.read()
        #print returned_page
        # TODO : read the page and verify that the project was added successfully.
        
        return 1
    
    ## -------------------------------
    ## Given a tracker's regex infos
    ## update the database with new 
    ## stats
    ## -------------------------------
    def update_regexes_in_tracker_info (self, trackers_regex_info, website):
        
        data = { 'website' : get_website_name_for_tracker_update(website) }
        for key in trackers_regex_info:
            data[key] = trackers_regex_info[key]
        
        
        update_url = SITE_NAME+'/tracker_infos/add_regex_info_from_script/'+ PYTHON_VERIFICATION_CODE;
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        data = urllib.urlencode(data)
        req = urllib2.Request(update_url, data, headers)
        try :
            print update_url
            response = urllib2.urlopen(req)
            print response
            r = response.read()
            f = open("test_regex.html", "w")
            f.write(r)
            f.close()
            print "tracker_info_update called"
        except Exception, e:
            print "Error in updating db"
            print e
            return 0
        
        #returned_page = response.read()
        #print returned_page
        # TODO : read the page and verify that the project was added successfully.
        
        return 1
    
    
    ## -------------------------------
    ## add a news to AB
    ## -------------------------------
    def add_news (self, news):
        
        data = {
                    'company_id' : -1,
                    'product_id':0,
                    'title' : news['title'],
                    'desc' : news['desc'],
                    'link' : news['link'],
                    'topic1' : news['topic1'],
                    'state' : news['state'],
                    'type':news['type']
                  }
        
        update_url = SITE_NAME+'/contents/add_from_script/'+ PYTHON_VERIFICATION_CODE;
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        data = urllib.urlencode(data)
        req = urllib2.Request(update_url, data, headers)
        try :
            print update_url
            response = urllib2.urlopen(req)
            print response
            r = response.read()
            f = open("test.html", "w")
            f.write(r)
            f.close()
            print "news update called"
        except Exception, e:
            print "Error in updating db"
            print e
            return 0
        
        #returned_page = response.read()
        #print returned_page
        # TODO : read the page and verify that the project was added successfully.
        
        return 1
    
    ## -------------------------------
    ## Given a stats of a blogger
    ## update the database with new 
    ## stats
    ## -------------------------------
    def update_blogger_matrix (self, bloggerid, matrixes):
        
        fbdata = matrixes[0]
        twdata = matrixes[1]
        pinterestdata = matrixes[2]
        instagramdata = matrixes[3]
        
        data = {
                    'id' : addslashes(bloggerid),
                    'fb' : {'likes' : -1, 'followers' : -1, 'active_conversations' : -1 },
                    'twitter' : {'tweets' : -1, 'followers' : -1, 'following' : -1 },
                    'instagram' : {'posts' : -1, 'followers' : -1, 'following' : -1 },
                    'pinterest' : {'likes' : -1, 'pins' : -1, 'boards' : -1, 'followers' : -1, 'following' : -1},
                  
                  }
        
        update_url = SITE_NAME+'/bloggers/update_blogger_stats/'+ PYTHON_VERIFICATION_CODE;
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        data = urllib.urlencode(data)
        req = urllib2.Request(update_url, data, headers)
        try :
            print update_url
            response = urllib2.urlopen(req)
            print response
            print "db updated for blogger " + str(bloggerid)
        except Exception, e:
            print "Error in updating db"
            print e
            return 0
        
        #returned_page = response.read()
        #print returned_page
        # TODO : read the page and verify that the project was added successfully.
        
        return 1
    
    def test_get_tracker_info(self):
        return self.get_tracker_info("http://www.target.com/p/mossimo-womens-ultrasoft-cocoon-cardigan-assorted-colors/-/A-14502863?reco=Rec|pdp|14502863|NonGenreCategoryTopSellers|item_page.vertical_1&lnk=Rec|pdp|NonGenreCategoryTopSellers|item_page.vertical_1")
    
    
    def update_prod_info_in_db(self, prod_info):
        
        url_to_call = SITE_NAME+'/products/update_prod_info_from_script/'+ PYTHON_VERIFICATION_CODE;
        
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(url_to_call, urllib.urlencode(prod_info), headers)
        retval = '0'
        
        try :
            #print url_to_call
            response = urllib2.urlopen(req)
            response_page = response.read()
            #print response_page
            
            clean_response_page = htmlops.removeCommentsAndJS(response_page)
            soup = BeautifulSoup(clean_response_page)
            #print clean_response_page
            # pull the divs
            div = soup.find('div', attrs={'class' : '_result_'})
            #print main_div
            #print "print beautiful soup over"
            #print divs
            #build up result set
            retval = div['retval'].encode("ascii", "ignore")
            
                        
            #print resultset
            # returl thus prepared url list :)
            
        except :
            print "FATAL ERROR : Couldnt update prod info"
            print "Unexpected error:", sys.exc_info()[0]
            raise
            
        #print resultset
        return '1' == retval
        
    def test_update_backend_job_status(self):
        result = self.update_backend_job_status('1', 1)
        print result
        
    def update_backend_job_status(self, job_id, new_status):
        
        url_to_call = SITE_NAME+'/backend_ops/update_backend_job_status/'+ PYTHON_VERIFICATION_CODE;
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        data = {'job_id' : job_id, 'new_status' : new_status}
        req = urllib2.Request(url_to_call, urllib.urlencode(data), headers)
        retval = '0'
        
        try :
            #print url_to_call
            response = urllib2.urlopen(req)
            response_page = response.read()
            #print response_page
            
            clean_response_page = htmlops.removeCommentsAndJS(response_page)
            soup = BeautifulSoup(clean_response_page)
            #print clean_response_page
            # pull the divs
            div = soup.find('div', attrs={'class' : '_result_'})
            #print main_div
            #print "print beautiful soup over"
            #print divs
            #build up result set
            retval = div['retval'].encode("ascii", "ignore")
            
                        
            #print resultset
            # returl thus prepared url list :)
            
        except :
            print "FATAL ERROR : Couldnt get tracker info"
            print "Unexpected error:", sys.exc_info()[0]
            raise
            
        #print resultset
        return '1' == retval
            
    def test_update_get_prod_detail_jobs(self):
        links = ["link1.html", "link2.html"]
        result = self.update_get_prod_detail_jobs(links)
        print result
        
    def update_get_prod_detail_jobs(self, prod_page_links):
        
        data = {}
        key_index = 0
        for link in prod_page_links:
            data[str(key_index)] = link
            key_index += 1 
        
        url_to_call = SITE_NAME+'/backend_ops/add_get_prod_detail_jobs/'+ PYTHON_VERIFICATION_CODE;
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(url_to_call, urllib.urlencode(data), headers)
        retval = '0'
        
        try :
            #print url_to_call
            response = urllib2.urlopen(req)
            response_page = response.read()
            #print response_page
            
            clean_response_page = htmlops.removeCommentsAndJS(response_page)
            soup = BeautifulSoup(clean_response_page)
            #print clean_response_page
            # pull the divs
            div = soup.find('div', attrs={'class' : '_result_'})
            #print main_div
            #print "print beautiful soup over"
            #print divs
            #build up result set
            retval = div['retval'].encode("ascii", "ignore")
            
                        
            #print resultset
            # returl thus prepared url list :)
            
        except :
            print "FATAL ERROR : Couldnt get tracker info"
            print "Unexpected error:", sys.exc_info()[0]
            raise
            
        #print resultset
        return '1' == retval
        
    def get_pending_jobs(self, job_types_str):
        
        
        data = {'job_types_str' : job_types_str}
        
        url_to_call = SITE_NAME+'/backend_ops/get_pending_jobs/'+ PYTHON_VERIFICATION_CODE;
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(url_to_call, urllib.urlencode(data), headers)
        resultset = []
        
        try :
            #print url_to_call
            response = urllib2.urlopen(req)
            response_page = response.read()
            #print response_page
            
            clean_response_page = htmlops.removeCommentsAndJS(response_page)
            soup = BeautifulSoup(clean_response_page)
            #print clean_response_page
            # pull the divs
            divs = soup.findAll('div', attrs={'class' : '_single_backend_op_'})
            #print main_div
            #print "print beautiful soup over"
            #print divs
            #build up result set
            for div in divs:
                resultset.append( { 
                            'type':div['type'].encode("ascii", "ignore"), 
                            'url':div['url'].encode("ascii", "ignore"),
                            'pid':div['pid'].encode("ascii", "ignore"), 
                            'id' : div['id'].encode("ascii", "ignore"), 
                        } );
                        
            #print resultset
            # returl thus prepared url list :)
            
        except :
            print "FATAL ERROR : Couldnt get tracker info"
            print "Unexpected error:", sys.exc_info()[0]
            raise
            
        #print resultset
        return resultset
    
    #--------------------------------------------
    # gets tracker info
    #--------------------------------------------
    def get_tracker_info ( self, website ):
        
        url_to_call = SITE_NAME+'/tracker_infos/get_tracker_info_from_script/'+ PYTHON_VERIFICATION_CODE;
        data = {'website' : get_website_name_for_tracker_update(website) }
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        data = urllib.urlencode(data)
        req = urllib2.Request(url_to_call, data, headers)
        resultset = None
        
        try :
            #print url_to_call
            response = urllib2.urlopen(req)
            response_page = response.read()
            #print response_page
            
            clean_response_page = htmlops.removeCommentsAndJS(response_page)
            soup = BeautifulSoup(clean_response_page)
            #print clean_response_page
            # pull the divs
            div = soup.find('div', attrs={'id' : '_tracker_info_'})
            csses_div = soup.find('div', attrs={'id' : 'csses'})
            #print main_div
            #print "print beautiful soup over"
            
            #build up result set
            resultset = { 
                        'titlexpath':div['titlexpath'].encode("ascii", "ignore"), 
                        'title_price_xpath':div['title_price_xpath'].encode("ascii", "ignore"), 
                        'pricexpath':div['pricexpath'].encode("ascii", "ignore"), 
                        'oldpricexpath':div['oldpricexpath'].encode("ascii", "ignore"), 
                        'saleprxpath_onsale':div['saleprxpath_onsale'].encode("ascii", "ignore"), 
                        'regprxpath_onsale':div['regprxpath_onsale'].encode("ascii", "ignore"), 
                        'wasprxpath_onsale':div['wasprxpath_onsale'].encode("ascii", "ignore"), 
                        'pricerootxpath':div['pricerootxpath'].encode("ascii", "ignore"), 
                        'priceofferxpath':div['priceofferxpath'].encode("ascii", "ignore"), 
                        'saleprxpath_onsale_regex':div['saleprxpath_onsale_regex'].encode("ascii", "ignore"), 
                        'regprxpath_onsale_regex':div['regprxpath_onsale_regex'].encode("ascii", "ignore"), 
                        'wasprxpath_onsale_regex':div['wasprxpath_onsale_regex'].encode("ascii", "ignore"), 
                        'pricerootxpath_regex':div['pricerootxpath_regex'].encode("ascii", "ignore"), 
                        'priceofferxpath_regex':div['priceofferxpath_regex'].encode("ascii", "ignore"), 
                        'pimg_xpath': div['pimg_xpath'].encode("ascii", "ignore"), 
                        'pimg_xpath1': div['pimg_xpath1'].encode("ascii", "ignore"), 
                        'pimg_xpath2': div['pimg_xpath2'].encode("ascii", "ignore"), 
                        'pimg_xpath3': div['pimg_xpath3'].encode("ascii", "ignore"), 
                        'pimg_xpath4': div['pimg_xpath4'].encode("ascii", "ignore"), 
                        'pimg_xpath5': div['pimg_xpath5'].encode("ascii", "ignore"), 
                        'urllib2_pimg_xpath1': div['urllib2_pimg_xpath1'].encode("ascii", "ignore"), 
                        'urllib2_pimg_xpath2': div['urllib2_pimg_xpath2'].encode("ascii", "ignore"), 
                        'urllib2_pimg_xpath3': div['urllib2_pimg_xpath3'].encode("ascii", "ignore"), 
                        'urllib2_pimg_xpath4': div['urllib2_pimg_xpath4'].encode("ascii", "ignore"), 
                        'urllib2_pimg_xpath5': div['urllib2_pimg_xpath5'].encode("ascii", "ignore"), 
                        'image_and_title_parent_xpath': div['image_and_title_parent_xpath'].encode("ascii", "ignore"), 
                        'image_and_details_container_xpath': div['image_and_details_container_xpath'].encode("ascii", "ignore"), 
                        'csses': json.loads(csses_div.text.encode("ascii", "ignore")), 
                        'details_xpath':div['details_xpath'].encode("ascii", "ignore"),
                        'titlexpath_regex':div['titlexpath_regex'].encode("ascii", "ignore"), 
                        'title_and_price_xpath_regex':div['title_price_xpath_regex'].encode("ascii", "ignore"), 
                        'pricexpath_regex':div['pricexpath_regex'].encode("ascii", "ignore"), 
                        'oldpricexpath_regex':div['oldpricexpath_regex'].encode("ascii", "ignore"), 
                        'pimg_xpath_regex': div['pimg_xpath_regex'].encode("ascii", "ignore"), 
                        'pimg_xpath1_regex': div['pimg_xpath_regex'].encode("ascii", "ignore"), 
                        'pimg_xpath2_regex': div['pimg_xpath2_regex'].encode("ascii", "ignore"), 
                        'pimg_xpath3_regex': div['pimg_xpath3_regex'].encode("ascii", "ignore"), 
                        'pimg_xpath4_regex': div['pimg_xpath4_regex'].encode("ascii", "ignore"), 
                        'pimg_xpath5_regex': div['pimg_xpath5_regex'].encode("ascii", "ignore"), 
                        'urllib2_pimg_xpath1_regex': div['urllib2_pimg_xpath1_regex'].encode("ascii", "ignore"), 
                        'urllib2_pimg_xpath2_regex': div['urllib2_pimg_xpath2_regex'].encode("ascii", "ignore"), 
                        'urllib2_pimg_xpath3_regex': div['urllib2_pimg_xpath3_regex'].encode("ascii", "ignore"), 
                        'urllib2_pimg_xpath4_regex': div['urllib2_pimg_xpath4_regex'].encode("ascii", "ignore"), 
                        'urllib2_pimg_xpath5_regex': div['urllib2_pimg_xpath5_regex'].encode("ascii", "ignore"), 
                        'image_and_title_parent_xpath_regex': div['image_and_title_parent_xpath_regex'].encode("ascii", "ignore"), 
                        'image_and_details_container_xpath_regex': div['image_and_details_container_xpath_regex'].encode("ascii", "ignore"),
                        'is_image_in_og_image_meta_tag': div['is_image_in_og_image_meta_tag'].encode("ascii", "ignore"), 
                        'pinterest_position': div['pinterest_position'].encode("ascii", "ignore")
                    } 
                        
            #print resultset
            # returl thus prepared url list :)
            
        except KeyError, e:
            print "################# Error Start ##################"
            print "Likely bad tracker info"
            print website
            print "################# Error End ##################"
            
        except Exception, e:
            print "################# Error Start ##################"
            print "FATAL ERROR : Couldnt get tracker info"
            print "Unexpected error:", sys.exc_info()[0]
            print "################# Error End ##################"
            raise
            
        return resultset
        
    
    def get_selfpage(self, url, data=None):
        if not data: data={}
        data['pcode'] = PYTHON_VERIFICATION_CODE
        response_page = self.get_a_webpage(url, data)
        return response_page
    
    def get_a_webpage(self, url, data=None):
        response_page = ""
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        
        data = urllib.urlencode(data) if data else None;
        
        req = urllib2.Request(url, data, headers)
        response = None
        response_page = ""
        try :
            response = urllib2.urlopen(req)
            response_page = response.read()            
        except:
            pass
        
        if response: response.close()
        
        return response_page
    
    #--------------------------------------------
    # gets urls to parse 
    # return value is html page that needs to be 
    # parsed further to extract urls 
    #--------------------------------------------
    def get_bloggers_url ( self ):
        
        url_to_call = SITE_NAME+'/bloggers/get_list_for_parsing/'+ PYTHON_VERIFICATION_CODE;
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        
        req = urllib2.Request(url_to_call, None, headers)
        try :
            print url_to_call
            response = urllib2.urlopen(req)
            response_page = response.read()
            
            clean_response_page = htmlops.removeCommentsAndJS(response_page)
            soup = BeautifulSoup(clean_response_page)
            #print clean_response_page
            # pull the divs
            main_div = soup.findAll('div', attrs={'id' : '_parsing_urls_'})
            #print main_div
            #print "print beautiful soup over"
            
            #build up result set
            resultset = []
            for div in main_div:
                resultset.append( 
                    { 
                        'blog':div['blog'].encode("ascii", "ignore"), 
                        'facebooklink':div['facebooklink'].encode("ascii", "ignore"), 
                        'twitterlink':div['twitterlink'].encode("ascii", "ignore"), 
                        'instagramlink':div['instagramlink'].encode("ascii", "ignore"), 
                        'pinterestlink': div['pinterestlink'].encode("ascii", "ignore"), 
                        'bloggerid':div['bloggerid'].encode("ascii", "ignore"), 
                        'ready_to_parse':div['ready_to_parse'].encode("ascii", "ignore")
                    } 
                );
            
            #print resultset
            # returl thus prepared url list :)
            return resultset
        except :
            print "FATAL ERROR : Couldnt get url list"
            print "Unexpected error:", sys.exc_info()[0]
            raise
            return None
            
    def price_update ( self, prod_id, new_price ):
        
        url_to_call = SITE_NAME+'/products/update_price_from_script/'+ PYTHON_VERIFICATION_CODE;
        
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        data = {'prod_id' : prod_id, 'new_price' : new_price}
        data = urllib.urlencode(data)
        req = urllib2.Request(url_to_call, data, headers)
        
        try :
            print url_to_call
            response = urllib2.urlopen(req)
            response_page = response.read()
            print response_page;
            return response_page
        except :
            print "FATAL ERROR : web interface to update price failed"
            print "Unexpected error:", sys.exc_info()[0]
            raise
            return None
    
    def get_prod_list_for_price_update ( self ):
        
        url_to_call = SITE_NAME+'/products/plist_for_price_check/'+ PYTHON_VERIFICATION_CODE;
        
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        
        req = urllib2.Request(url_to_call, None, headers)
        response_page = ""    
        
        try :
            print url_to_call
            response = urllib2.urlopen(req)
            response_page = response.read()
        except :
            print "FATAL ERROR : web interface to get product list failed"
            print "Unexpected error:", sys.exc_info()[0]
            raise
            return None
        
        try:
        #if 1:
            products = json.loads(response_page)
            if products and (response_page != products):
                return products
            else:
                return None
        #else:
        except:
            print "FATAL ERROR: json decoding of page failed"
        