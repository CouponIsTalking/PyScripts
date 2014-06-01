import sys
import os
import traceback, os.path
from grouper import *

urls = []
urls.append(["http://www.rei.com/product/836772/merrell-nikita-waterproof-winter-boots-womens", 1])
urls.append(["http://www.victoriassecret.com/sleepwear/luxe-satin/lace-appliqu-satin-slip-very-sexy?ProductID=150088&CatalogueType=OLS", 1])
urls.append(["http://www.latindancefashions.com/shop/index.php?main_page=product_info&cPath=159_162&products_id=5259", 1])
urls.append(["http://www1.macys.com/shop/product/holiday-2013-red-hot-sleeveless-sequined-dress-look?ID=1143223&CategoryID=61879#fn=sp%3D1%26spc%3D54%26ruleId%3D2%26slotId%3D4", 1])
urls.append(["http://www.titlenine.com/product/445236.do?sortby=ourPicks&from=fn#.UoUxQvleZhx", 1])
urls.append(["http://www.etsy.com/listing/128827293/feather-ring-sterling-silver-stacking?ref=br_feed_4&br_feed_tlp=jewelry", 1])
urls.append(["http://www.dsw.com/shoe/nike+dual+fusion+lite+lightweight+running+shoe+-+mens?prodId=285370&category=dsw12cat1060005&activeCats=cat20192,dsw12cat1060005", 1])
urls.append(["http://www.anthropologie.com/anthro/product/clothes-new/29245875.jsp?cm_sp=Grid-_-29245875-_-Regular_0", 1])
urls.append(["http://www.jcrew.com/womens_category/CashmereShop/PRDOVR~53268/53268.jsp", 1])
urls.append(["http://shop.nordstrom.com/s/rbl-military-jumpsuit/3562432?origin=category&contextualcategoryid=0&fashionColor=&resultback=0", 1])
urls.append(["http://www.ae.com/web/browse/product.jsp?productId=1144_9704_443&catId=cat6470451", 1])
urls.append(["http://www.anntaylor.com/one-button-tweed-jacket/321485?colorExplode=false&skuId=14764806&catid=cata000013&productPageType=fullPriceProducts&defaultColor=7030", 1])
urls.append(["http://us.asos.com/ASOS-Slim-Fit-Suit-Pants-in-Black/yjj1r/?sgid=4905&cid=16752&sh=0&pge=0&pgesize=36&sort=-1&clr=Black&mporgp=L0FTT1MtU2xpbS1GaXQtU3VpdC1pbi1CbGFjay8.", 1])
urls.append(["http://athleta.gap.com/browse/product.do?cid=1000054&vid=1&pid=918993&mlink=46750,7184035,TSAlacrity9_24&clink=7184035", 1])
urls.append(["http://www1.bloomingdales.com/shop/product/modern-fiction-leather-cap-toe-oxfords?ID=831579&CategoryID=1001314#fn=spp%3D1%26ppp%3D96%26sp%3D1%26rid%3D82%26spc%3D139", 1])
urls.append(["http://www.ahalife.com/product/3766/white-inspirational-t-shirt", 1])
urls.append(["http://www.qvc.com/Chaps-Mens-Faux-Shearling-Aviator-Style-Jacket-Mens-Apparel-Fashion.product.A321924.html?sc=A321924-Targeted&cm_sp=VIEWPOSITION-_-2-_-A321924&catentryImage=http://images-p.qvc.com/is/image/a/24/a321924.001?$uslarge$", 1])
urls.append(["http://www.burton.com/default/2l-flare-down-snowboard-jacket/W14-10011100.html?start=2&cgid=womens-ak", 1])
urls.append(["http://shop.lululemon.com/products/clothes-accessories/tops-long-sleeve/Avenue-Pullover?catId=cat230015&RecsID=prod2380230-US&pfm=recs", 1])
urls.append(["http://www.forever21.com/Product/Product.aspx?BR=f21&Category=bottom_pants&ProductID=2000065458&VariantID=", 1])
urls.append(["http://www.target.com/p/mossimo-womens-ultrasoft-cocoon-cardigan-assorted-colors/-/A-14502863?reco=Rec|pdp|14502863|NonGenreCategoryTopSellers|item_page.vertical_1&lnk=Rec|pdp|NonGenreCategoryTopSellers|item_page.vertical_1", 1])
urls.append(["http://www.ebay.com/itm/NWT-Gap-CABLE-KNIT-MOCK-NECK-SWEATER-XXL-Black-Marled-Soft-Chunky-Wool-Blend-2XL-/261318525967", 1])
urls.append(["http://fab.com/product/black-biker-jacket-459747/?ref=browse&pos=15", 1])
urls.append(["http://www.hollisterco.com/shop/us/dudes-skinny-jeans/hollister-skinny-jeans-1150452_01", 1])
urls.append(["http://www.gillyhicks.com/shop/us/shop-all-tops-long-sleeve-graphic-tees/cheeky-definition-graphic-hoodie-1315169_01", 1])
#urls.append(["http://www1.macys.com/shop/product/ralph-lauren-polo-red-gift-set?ID=1050356&CategoryID=30088#fn=sp%3D1%26spc%3D1472%26ruleId%3D57%26slotId%3Drec(2)", 1])
urls.append(["http://www1.macys.com/shop/product/nautica-shorts-ripstop-cargo-shorts?ID=823983&CategoryID=3310#fn=sp%3D1%26spc%3D700%26ruleId%3D19%26slotId%3D1", 1])
urls.append(["http://www.abercrombie.com/shop/us/mens-skinny-jeans/a-and-f-skinny-jeans-981564_01", 1])
#urls.append(["http://www.ae.com/web/browse/product.jsp?productId=1144_9704_443&catId=cat6470451", 1])
urls.append(["http://www.lanebryant.com/active/active-view-all/striped-active-hoodie/20230c20233p193524/index.pro?selectedColor=Heather%20charcoal&selectedSize=26%2F28", 1])
urls.append(["http://usa.tommy.com/shop/en/thb2cus/men/suits-dressshirts-men/7838185", 1])
urls.append(["http://www.hollisterco.com/shop/us/denim-high-rise-super-skinny-bettys/hollister-super-skinny-jeans-1204796_01", 1])
urls.append(["http://www.adidas.com/us/product/womens-training-techfit-rock-it-bra/AC748?cid=G69981&breadcrumb=sxZu3Z1z134u8Z1z13071Z1z11zrf", 1])
#urls.append(["http://store.johnnybrouk.com/detail.cfm?USR=0&USRTemp=41582.1036458&ID=15&PicID=15&Position=4&Gender=2&Department=1&Styles=1&couleur=0&MySize=0&Currency=", 1])
urls.append(["http://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=8543052&CatId=8809", 1])
urls.append(["http://www.loft.com/julie-skinny-corduroy-pants/314298?colorExplode=false&skuId=14505287&catid=catl000015&productPageType=fullPriceProducts&defaultColor=7512", 1])
#urls.append(["http://shop.guess.com/en/Catalog/View/women/vests/sleeveless-tailored-suiting-vest/W33N40W3U10", 1]) # uses canvas :(
urls.append(["http://www.fairindigo.com/Fair-Indigo-Organic-Cotton-Essential/dp/B00DQ0ABIC?field_availability=-1&field_browse=6482657011&id=Fair+Indigo+Organic+Cotton+Essential&ie=UTF8&refinementHistory=generic_text_9-bin%2Cgeneric_text_10-bin%2Ccolor_map%2Csize_name%2Cbrandtextbin%2Cprice%2Csubjectbin&searchNodeID=6482657011&searchPage=1&searchRank=relevancerank&searchSize=12", 1])
urls.append(["http://www.matatraders.com/bohemian-tops/sylvia-blouse/prod_756.html", 1])
urls.append(["http://www.gap.com/browse/product.do?cid=92001&vid=1&pid=351511202", 1])
urls.append(["http://www.walmart.com/ip/Hanes-Women-s-Printed-Thermal-Underwear-Crew-Tee-and-Leggings/22012383", 1])
urls.append(["http://store.americanapparel.net/product/?productId=rnt74", 1])
urls.append(["http://www.calvinklein.com/webapp/wcs/stores/servlet/SearchDisplay?Color=PEBBLE+LIZARD+PRINT&showResultsPage=true&langId=-1&beginIndex=0&productId=438503&sType=SimpleSearch&pageSize=16&pageView=image&catalogId=12101&errorViewName=ProductDisplayErrorView&categoryId=48764&storeId=10751&viewAll=N&ddkey=http:en/ck/women-panties/51443266", 1])
urls.append(["http://www.shop.puma.com/Archive-Logo-Hoodie/pna566442,en_US,pd.html?cgid=290001&source=Trending_Now_1_1_text&vid=#!color%3D02%26size%3DUS_S", 1])
urls.append(["http://www.nixon.com/us/en/womens/tanks-tees/weft-s-s-scoop-tee-w-S1881.html?sku=S1881696-01", 1])
urls.append(["http://us.shop.elementbrand.com/p/womens/tops/dana-ss-knit?style=J9624DAN&clr=BLK", 1])
urls.append(["http://www.express.com/clothing/ankle+rolled+destroyed+boyfriend+jean/pro/6995673/cat2005", 1])


error_url_file = open("error_urls.txt", "w")
total_exceptions = 0

def test_test_urls(aUrl, error_url_file, total_exceptions):
    gr = Grouper(aUrl)
    try:
    #if 1:
        gr.extract()
    #try:
        a = 1
    except MemoryError, e:
        print "Memory Error"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print "More info"
        top = traceback.extract_stack()[-1]
        print ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])])
        error_url_file.write(aUrl)
        total_exceptions = total_exceptions + 1
        
    except Exception, e:
        print "Exception"
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print "More info"
        top = traceback.extract_stack()[-1]
        print ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])])
        print e
        error_url_file.write(aUrl)
        total_exceptions = total_exceptions + 1
        
    #gr.extract()
    gr.deinit()
    print "###############"


# actual tests
urls = urls[::-1]
i = len(urls)-1
while i>=0:
    url = urls[i]
    if ("gap.com" not in url[0]):
        i = i-1
        continue
    #url = urls[len(urls)-1-i]
    print "##################"
    print url[0]
    if url[1]:# and ("lanebryant" in url[0]):
        test_test_urls(url[0], error_url_file, total_exceptions)
    i = i-1

print "$$$$$$$$$$$####################$$$$$$$$$$$$$$$$$$$$$$"
print "$$$$$$$$$$$####################$$$$$$$$$$$$$$$$$$$$$$"
print str(total_exceptions) + " EXCEPTIONS SO FAR"
print "$$$$$$$$$$$####################$$$$$$$$$$$$$$$$$$$$$$"
print "$$$$$$$$$$$####################$$$$$$$$$$$$$$$$$$$$$$"

from more_test_urls import *
for url in test_urls:
    print "##################"
    print url
    test_test_urls(url, error_url_file, total_exceptions)

error_url_file.close()

while True:
    time.sleep(10);

