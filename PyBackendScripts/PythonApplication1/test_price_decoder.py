from PriceDecoder import *
from htmlops import *
import lxml.html
from lxml import etree

price_html = ""

lines = open("price_html2.txt", "r").readlines()
for line in lines: 
    if line:
        price_html += line

price_html = removeCommentsAndJS(price_html)
price_text = etree.tostring(etree.fromstring(price_html, etree.HTMLParser()), encoding="utf-8",  method="text")
#pd = PriceDecoder(price_text, price_html) 
pd = PriceDecoder("Price us$ 23.54\n\n if some comdition", "") 
prices = pd.DecodePrices()
print prices

price_html = "<span class=\"amount\">Tk195</span>"
pd = PriceDecoder("Tk195", price_html)
prices = pd.DecodePrices()
print prices

price_html = """<p> <strong>Market Price : </strong><span class='oldPrice'>$
            5.71            </span> <br>
            <strong>Sale Price : </strong>$
            5.71            <br>
            <!-- min /max order limit -->
            <strong>Minimum order limit : </strong>
            10            <br>
            <strong>Maximum order limit : </strong>
            300            <br>            
            <strong>Weight per quantity : </strong>
            0.14 kg<br>   
            <!-- made in/made of -->
			<strong>Made in : </strong>
            Nepal<br>
            <strong>Made of : </strong>
            Wool<br>     
            <!--  Discounts -->
            <strong>Has Discount ?: </strong>
            No<br>
            		<!-- Product colors been moved here (C in backups)-->	
	  
          </p>"""
text = """Market Price : $ 5.71
Sale Price : $ 5.71
Minimum order limit : 10
Maximum order limit : 300
Weight per quantity : 0.14 kg
Made in : Nepal
Made of : Wool
Has Discount ?: No"""
pd = PriceDecoder(text, price_html)
prices = pd.DecodePrices()
print prices