from get_related_prods import *

def test_get_related_prods():
    
    rp = GetRelatedProds("", "")
    rp.set_tool('selenium')
    #related_prods_by_page_url("http://www.latindancefashions.com/shop/index.php?main_page=product_info&cPath=159_162&products_id=5259")
    
    for urls in url_groups:
        for url in urls:
            rp.move_to_url(url)
            rp.extract_related_prods()
    
    #related_prods_by_page_url("http://athleta.gap.com/browse/product.do?cid=1000054&vid=1&pid=918993&mlink=46750,7184035,TSAlacrity9_24&clink=7184035")

#test_get_related_prods()

rp = GetRelatedProds("", "")
rp.set_tool('selenium')
rp.move_to_url("http://www.adidas.com/us/product/mens-soccer-brazil-city-tee/AB207?cid=G91049&breadcrumb=u2Z1z124qoZ1z13071Z1z11zrf")
rp.set_tool('urllib2')
rp.extract_related_prods()
rp.print_related_prods_links()
