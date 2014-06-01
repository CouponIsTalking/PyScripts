from grouper import *
from misc import *
import collections

class XPathPatrnMaker(object):
 
    def __init__(self, urls):
        
        """description of class"""
        self.urls = urls
        self.grs = []
        for url in urls:
            self.grs.append(Grouper(url))
        
    def deinit(self):
        for gr in self.grs:
            gr.deinit()
    
    def getProductDivs(self):
        while True:
            pimg_srces = []
            for gr in self.grs:
                div = gr.decodeProductDiv()
                pimg_srces.append(gr.pimg_src)
        
            #ensure product divs are different
            dup_images = [x for x, y in collections.Counter(pimg_srces).items() if (x and (y > 1))]
            if dup_images:
                for gr in self.grs:
                    gr.clearProductImgDiv()
                    for img_src in dup_images:
                        gr.banCurProdImgSrc(img_src)
            else:
                break
        
    def runGroupers(self):
        
        for gr in self.grs:
            gr.removeOutgoingElements()
        
        self.getProductDivs()
        
        for gr in self.grs:
            gr.extract()
    
    def generate_patrn_from_xpaths(self):
        
        regexes = {}
        
        xpaths = {}
        xpaths['titlexpaths'] = []
        xpaths['pricexpaths'] = []
        xpaths['title_price_xpaths'] = []
        xpaths['oldpricexpaths'] = []
        xpaths['pimg_xpaths'] = []
        xpaths['pimg_xpaths1'] = []
        xpaths['pimg_xpaths2'] = []
        xpaths['pimg_xpaths3'] = []
        xpaths['pimg_xpaths4'] = []
        xpaths['pimg_xpaths5'] = []
        xpaths['urllib2_pimg_xpaths1'] = []
        xpaths['urllib2_pimg_xpaths2'] = []
        xpaths['urllib2_pimg_xpaths3'] = []
        xpaths['urllib2_pimg_xpaths4'] = []
        xpaths['urllib2_pimg_xpaths5'] = []
        xpaths['details_xpaths'] = []
        xpaths['image_and_title_parent_xpaths'] = []
        xpaths['image_and_details_container_xpaths'] = []

        for gr in self.grs:
            xpaths['titlexpaths'].append(gr.tracker_info['titlexpath'])
            xpaths['pricexpaths'].append(gr.tracker_info['pricexpath'])
            xpaths['title_price_xpaths'].append(gr.tracker_info['title_price_xpath'])
            xpaths['oldpricexpaths'].append(gr.tracker_info['oldpricexpath'])
            xpaths['pimg_xpaths'].append(gr.tracker_info['pimg_xpath'])
            xpaths['pimg_xpaths1'].append(gr.tracker_info['pimg_xpath1'])
            xpaths['pimg_xpaths2'].append(gr.tracker_info['pimg_xpath2'])
            xpaths['pimg_xpaths3'].append(gr.tracker_info['pimg_xpath3'])
            xpaths['pimg_xpaths4'].append(gr.tracker_info['pimg_xpath4'])
            xpaths['pimg_xpaths5'].append(gr.tracker_info['pimg_xpath5'])
            xpaths['urllib2_pimg_xpaths1'].append(gr.tracker_info['urllib2_pimg_xpath1'])
            xpaths['urllib2_pimg_xpaths2'].append(gr.tracker_info['urllib2_pimg_xpath2'])
            xpaths['urllib2_pimg_xpaths3'].append(gr.tracker_info['urllib2_pimg_xpath3'])
            xpaths['urllib2_pimg_xpaths4'].append(gr.tracker_info['urllib2_pimg_xpath4'])
            xpaths['urllib2_pimg_xpaths5'].append(gr.tracker_info['urllib2_pimg_xpath5'])
            xpaths['details_xpaths'].append(gr.tracker_info['details_xpath'])
            xpaths['image_and_title_parent_xpaths'].append(gr.tracker_info['image_and_title_parent_xpath'])
            xpaths['image_and_details_container_xpaths'].append(gr.tracker_info['image_and_details_container_xpath'])
            
            
        for k in xpaths:
            regexes[k.replace("xpaths", "xpath") + "_regex"] = get_id_regex_from_xpaths(xpaths[k])
        
        self.regexes = regexes
        print "########################################################"
        print "####### Generated Patterns #####################"
        for k in self.regexes:
            print [k, self.regexes[k]]
        print "####### Generated Patterns End #####################"
        print "########################################################"
    
    def update_regex_in_db(self):
        wi = WebInterface()
        wi.update_regexes_in_tracker_info(self.regexes, self.urls[0])

    
    def doTheDew(self):
        self.runGroupers()
        self.generate_patrn_from_xpaths()
        self.update_regex_in_db()
    
    