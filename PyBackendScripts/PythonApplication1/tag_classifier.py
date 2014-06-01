import re
from misc import *
import TagNames.beauty_prod_names
import TagNames.color_names
import TagNames.elec_item_names
import TagNames.jewellery_item_names
import TagNames.kitchen_item_names
import TagNames.watch_item_names


class Tags:

    def __init__(self):
        self.promotypes = self.PromotionTypeList()
        self.appareltypes = self.ApparelTypeList()
        self.exclusiontypes = self.exclusions_list()
        self.colornames = self.BuildColorName()
        self.jeweltypes = self.JewelTypeList()
    
    def deinit(self):
        self.promotypes = {}
        self.appareltypes = {}
        self.exculsiontypes = {}
        self.colornames = {}
    
    def hasCommonIndexes(self, dict1, dict2):
    
        for x in dict1:
            if x in dict2:
                return 1
        
        return 0
    
    def isQuantityWord(self, s):
        if not s:
            return False
        
        s = s.rstrip().lstrip().lower()
        s = re.sub(' +',' ', s)
        if s == "quantity :" or s == "quantity:" or s == "qty :" or s == "qty:":
            return True
        else:
            return False
    
    def isQuantityHintWord(self, s):
        if not s:
            return False
        
        s = s.rstrip().lstrip().lower()
        s = re.sub(' +',' ', s)
        if s == "quantity" or s == "qty":
            return True
        else:
            return False
    
    
    def isColorHintWord(self, s):
        if not s:
            return False
        
        s = s.rstrip().lstrip().lower()
        s = re.sub(' +','', s)
        if s == "color" or s== "colors":
            return True
        else:
            return False
    
    
    def isColorWord(self, s):
        if not s:
            return False
        
        s = s.rstrip().lstrip().lower()
        s = re.sub(' +','', s)
        if s.startswith("color :") or s.startswith("color:"):
            return True
        else:
            return False
    
    # hint words is just a hint, not exactly a size specifier like "size :"
    # size specifier has some sense of certainity unlike size hint
    def isSizeHintWord(self, s):
        if not s:
            return False
        
        s = s.rstrip().lstrip().lower()
        s = re.sub(' +','', s)
        if s == "size" or s == "sizes":
            return True
        if s == "waist":
            return True
        if s == "height":
            return True
        if s == "length":
            return True
        if s == "bust":
            return True
        else:
            return False
    
    def isSizeWord(self, s):
        if not s:
            return False
        
        s = s.rstrip().lstrip().lower()
        s = re.sub(' +','', s)
        if s.startswith("size :") or s.startswith("size:"):
            return True
        if s.startswith("waist :") or s.startswith("waist:"):
            return True
        if s.startswith("height :") or s.startswith("height:"):
            return True
        if s.startswith("length :") or s.startswith("length:"):
            return True
        if s.startswith("bust :") or s.startswith("bust:"):
            return True
        else:
            return False
    
    def isColorSquare(self, w, h):
        
        # find elements of size less than 30x30
        if w > 30 or h > 30:
            return False
        
        if w < 5 or h < 5:
            return False
        
        # skewed rectangle
        if w < 0.7 *h or h < 0.7*w:
            return False
            
        return True
    
    def isBigColorSquare(self, w, h):
        
        # find elements of size less than 50x50
        if w > 50 or h > 50:
            return False
        
        if w < 5 or h < 5:
            return False
        
        # skewed rectangle
        if w < 0.7 *h or h < 0.7*w:
            return False
            
        return True
        
    
    def isSizeType(self, size):
        
        if not size:
            return False
            
        sizetypes1 = {}
        sizetypes1['XXS'] = 1
        sizetypes1['XS'] = 1
        sizetypes1['S'] = 1
        sizetypes1['M'] = 1
        sizetypes1['L'] = 1
        sizetypes1['XL'] = 1
        sizetypes1['XXL'] = 1
        
        sizetypes1['xxS'] = 1
        sizetypes1['xs'] = 1
        sizetypes1['s'] = 1
        sizetypes1['m'] = 1
        sizetypes1['l'] = 1
        sizetypes1['xl'] = 1
        sizetypes1['xxl'] = 1
        
        sizetypes2 = ['extra small', 'small', 'medium', 'large', 'extra large', 'x-small', 'xx-small', 'x-large', 'xx-large']
        
        formatted_size = size.rstrip().lstrip()
        formatted_size = re.sub(' +','', formatted_size)
        # 1/2 letter size should be caps
        if formatted_size in sizetypes1:
            return True
        
        formatted_size = size.rstrip().lstrip().lower()
        formatted_size = re.sub(' +','', formatted_size)
        
        if len(formatted_size) == 1:
            if formatted_size[0] >= '0' and formatted_size[0] <= '9':
                return True
        
        if len(formatted_size) == 2:
            if formatted_size[0] >= '0' and formatted_size[0] <= '9' and formatted_size[1] >= '0' and formatted_size[1] <= '9':
                return True
        
        if len(formatted_size) == 3:
            if formatted_size[0] >= '0' and formatted_size[0] <= '9' and formatted_size[1] >= '0' and formatted_size[1] <= '9' and (formatted_size[2] == 'w' or formatted_size[2] == 'h'):
                return True
        
        formatted_size = size.rstrip().lstrip().lower()
        for s in sizetypes2:
            formatted_size_with_space = re.sub(' +',' ', formatted_size)
            formatted_size_without_space = re.sub(' +','', formatted_size)
            
            if formatted_size_with_space.startswith(s):
                return True
            
            if formatted_size_without_space == s:
                return True
        
        formatted_size = size.strip().lower()
        formatted_size = clean_text(formatted_size)
        words = [w for w in re.split('\W', formatted_size) if w]		
        # now may be we can analyze on with word level meanings
            
        return False
    
    
    def createDictWithWords(self, s):
        
        a = {}
        firstindex = 0
        secondindex = s.find(' ')
        while secondindex != -1:
            a[s[firstindex:secondindex]] = 1
            firstindex = secondindex + 1
            secondindex = s.find(' ', firstindex)
        
        a[s[firstindex:]] = 1
        
        return a
            
    def isPromoType(self, tag):
        
        tag = tag.lower()
        a = self.createDictWithWords(tag)
        if self.hasCommonIndexes(a, self.promotypes) == 1:
            return 1
                
        return 0
    
    def isWatchType(self, tag):
        
        tag = tag.lower()
        a = self.createDictWithWords(tag)
        if self.hasCommonIndexes(a, TagNames.watch_item_names.watch_items) == 1:
            return 1
                
        return 0
    
    def isKitchenType(self, tag):
        
        tag = tag.lower()
        a = self.createDictWithWords(tag)
        if self.hasCommonIndexes(a, TagNames.kitchen_item_names.kitchen_items) == 1:
            return 1
                
        return 0
    
    def isElecItemType(self, tag):
        
        tag = tag.lower()
        a = self.createDictWithWords(tag)
        if self.hasCommonIndexes(a, TagNames.elec_item_names.elec_items) == 1:
            return 1
                
        return 0
    
    def isBeautyProdType(self, tag):
        
        tag = tag.lower()
        a = self.createDictWithWords(tag)
        if self.hasCommonIndexes(a, TagNames.beauty_prod_names.beauty_items) == 1:
            return 1
                
        return 0
    
    def isApparelType(self, tag):
        
        tag = tag.lower()
        a = self.createDictWithWords(tag)
        if self.hasCommonIndexes(a, self.appareltypes) == 1:
            return 1
                
        return 0
    
    def isJewelType(self, tag):
        
        tag = tag.lower()
        a = self.createDictWithWords(tag)
        if self.hasCommonIndexes(a, self.jeweltypes) == 1:
            return 1
                
        return 0
    
    def isProductType(self, tag):
        
        if self.isApparelType(tag) or self.isJewelType(tag) or self.isBeautyProdType(tag):
            return 1
        if self.isElecItemType(tag) or self.isKitchenType(tag) or self.isWatchType(tag):
            return 1
        
        return 0
    
    def isExclusionType(self, tag):
        
        tag = tag.lower()
        a = self.createDictWithWords(tag)
        if self.hasCommonIndexes(a, self.exclusiontypes) == 1:
            return 1
                
        return 0
        
    
    def PromotionTypeList(self):
        a = {}
        a['sale'] = 1
        a['deal'] = 1
        a['deals'] = 1
        a['clearance'] = 1
        
        return a
        
    def JewelTypeList(self):
        a = {}
        a["jewel"] = 1
        a['jewelery'] = 1
        a['earring'] = 1
        a['earcuff'] = 1
        a["studs"] = 1	
        a['chain'] = 1
        a['circlet'] = 1
        a["coronet"] = 1
        a["diadem"] = 1		
        a["ferroniere"] = 1
        a["tiara"] = 1
        a['necklace'] = 1
        a['armlet'] = 1
        a["bracelet"] = 1
        a["bangle"] = 1		
        a["anklet"] = 1
        a["locket"] = 1		
        a["ring"] = 1
        a["breastplate"] = 1
        a["brass"] = 1
        
        b = {}
        for x in a:
            y = x.lower()
            b[y] = 1
        
        merged_b = dict(b.items() + TagNames.jewellery_item_names.jewellery_item.items())
        
        z = {}
        for y in merged_b:
            z[y] = 1
            if y[len(y)-1] != 's':
                z[y+"s"] = 1
        
        return z
    
        
    def ApparelTypeList(self):
        a = {}
        a['woman'] = 1
        a['women'] = 1
        a["woman's"] = 1
        a["women's"] = 1	
        a['man'] = 1
        a['men'] = 1
        a["man's"] = 1
        a["men's"] = 1		
        
        a["Accessories"] = 1
        a["Alarm Watches"] = 1
        a["Analog Digital Watches"] = 1
        a["Analog Watches"] = 1
        a["Apparel & Outerwear"] = 1
        a["Argyle Socks"] = 1
        a["Arm Bands"] = 1
        a["Arm Compression Sleeves"] = 1
        a["Arm Warmers"] = 1
        a["Athletic Accessories"] = 1
        a["Athletic Apparel"] = 1
        a["Athletic Capris"] = 1
        a["Athletic Pants"] = 1
        a["Athletic Shorts"] = 1
        a["Athletic Socks"] = 1
        a["Automatic Watches"] = 1
        a["Aviator Hats"] = 1
        a["Baby Bibs"] = 1
        a["Baby Gear"] = 1
        a["Balaclavas"] = 1
        a["Ballet Tutus"] = 1
        a["Bandanas"] = 1
        a["Bands"] = 1
        a["Barbeque"] = 1
        a["Baseball Caps"] = 1
        a["Baselayers"] = 1
        a["Bathrobe"] = 1
        a["Bath Robe"] = 1
        a["Bathing Suit"] = 1
        a["BDUs"] = 1
        a["Beach Cover-Ups"] = 1
        a["Beanie"] = 1
        a["Belt Buckles"] = 1
        a["Belt"] = 1
        a["Berets"] = 1
        a["Bike Socks"] = 1
        a["Bikini Bathing Suits"] = 1
        a["Bikini Bottoms"] = 1
        a["Bikini Panties"] = 1
        a["Bikini Tops"] = 1
        a["Bikinis"] = 1
        a["Blazers"] = 1
        a["Blouses"] = 1
        a["Board Shorts"] = 1
        a["Body Shapers"] = 1
        a["Bodysuit"] = 1
        a["Bomber Jackets"] = 1
        a["Boonie Hats"] = 1
        a["Boot Socks"] = 1
        a["Bow Ties"] = 1
        a["Boxer Briefs"] = 1
        a["Boxer Shorts"] = 1
        a["Boxers"] = 1
        a["Boy Shorts"] = 1
        a["Boyleg Briefs"] = 1
        a["Boyleg Panties"] = 1
        a["Boylegs"] = 1
        a["Bra Accessories"] = 1
        a["Bra Straps"] = 1
        a["Bracelet Watches"] = 1
        a["Bracelets"] = 1
        a["Braces"] = 1
        a["Bras"] = 1
        a["Briefs"] = 1
        a["Bucket Hats"] = 1
        a["Button Down Shirts"] = 1
        a["Calf Socks"] = 1
        a["Camcorders"] = 1
        a["Camera Accessories"] = 1
        a["Camis"] = 1
        a["Capris"] = 1
        a["Cardigans"] = 1
        a["Cargo Pants"] = 1
        a["Cargo Shorts"] = 1
        a["Carry On Luggage"] = 1
        a["Casual Bottoms"] = 1
        a["Casual Socks"] = 1
        a["Cello Cases"] = 1
        a["Ceramic Watches"] = 1
        a["Choli"] = 1
        a["Christmas Socks"] = 1
        a["Chronograph Watches"] = 1
        a["Civil War Hats"] = 1
        a["Clip Watches"] = 1
        a["Clocks"] = 1
        a["Cocktail Dresses"] = 1
        a["Cold Weather"] = 1
        a["Competition Swimwear"] = 1
        a["Compression Sleeves"] = 1
        a["Compression Socks"] = 1
        a["Compression Tights"] = 1
        a["Cotton Blend Socks"] = 1
        a["Cotton Bras"] = 1
        a["Cotton Shirts"] = 1
        a["Cotton Socks"] = 1
        a["Coveralls"] = 1
        a["Cowboy Hats"] = 1
        a["Crew Socks"] = 1
        a["Cropped Bottoms"] = 1
        a["Cycling Apparel"] = 1
        a["Cycling Socks"] = 1
        a["Denim Jackets"] = 1
        a["Designer Accessories"] = 1
        a["Designer Belts"] = 1
        a["Designer Small Leather Goods"] = 1
        a["Designer Watches"] = 1
        a["Diabetic Socks"] = 1
        a["Diamond Watches"] = 1
        a["Diaper Bags"] = 1
        a["Digital Watches"] = 1
        a["Dive Watches"] = 1
        a["Down Jackets"] = 1
        a["Dress Pants"] = 1
        a["Dress Shirts"] = 1
        a["Dress Socks"] = 1
        a["Dress Watches"] = 1
        a["Dresses"] = 1
        a["Ear Muffs"] = 1
        a["Evening Dresses"] = 1
        a["Exercise Equipment"] = 1
        a["Face Masks"] = 1
        a["Fashion Accessories"] = 1
        a["Fashion Socks"] = 1
        a["Fashion Tape"] = 1
        a["Fashion Watches"] = 1
        a["Fedoras"] = 1
        a["Felt Hats"] = 1
        a["Fingerless Gloves"] = 1
        a["Fishing Hats"] = 1
        a["Fishnet Tights"] = 1
        a["Fitness Apparel"] = 1
        a["Flannel Shirts"] = 1
        a["Flare Pants"] = 1
        a["Flat Caps"] = 1
        a["Fleece Accessories"] = 1
        a["Fleece Outerwear"] = 1
        a["Floppy Sun Hats"] = 1
        a["Foot Care"] = 1
        a["Formal Gloves"] = 1
        a["Full Briefs"] = 1
        a["Gardening Hats"] = 1
        a["Gel Bras"] = 1
        a["Ghost Socks"] = 1
        a["Glove"] = 1
        a["Gold Watches"] = 1
        a["Golf Apparel"] = 1
        a["Graphic T Shirts"] = 1
        a["Grill Accessories"] = 1
        a["Gym Shorts"] = 1
        a["Hair Accessories"] = 1
        a["Hair Pins"] = 1
        a["Hats"] = 1
        a["Hats/Headwear"] = 1
        a["Headbands"] = 1
        a["Helmet Covers"] = 1
        a["Henley Shirts"] = 1
        a["Hi Cut Briefs"] = 1
        a["Hi Cut Panties"] = 1
        a["High Leg Briefs"] = 1
        a["Hip Briefs"] = 1
        a["Hipster Panties"] = 1
        a["Homburgs"] = 1
        a["Hoodies"] = 1
        a["Hunting Boots"] = 1
        a["Infinity Scarves"] = 1
        a["Intimates"] = 1
        a["iPhone Accessories"] = 1
        a["Jackets"] = 1
        a["Jean"] = 1
        a["Jeans"] = 1
        a["Jerseys"] = 1
        a["Jewelry"] = 1
        a["Jumpsuits"] = 1
        a["Kids Accessories"] = 1
        a["Kitchen Accessories"] = 1
        a["Knee High Socks"] = 1
        a["Knee Socks"] = 1
        a["Knit Hats"] = 1
        a["Knit Socks"] = 1
        a["Kurta"] = 1
        a["Lace Bras"] = 1
        a["Lace Socks"] = 1
        a["Layettes"] = 1
        a["Learn to Swim"] = 1
        a["Leather Apparel"] = 1
        a["Leather Goods"] = 1
        a["Leather Hats"] = 1
        a["Leather Jackets"] = 1
        a["Leather Wristbands"] = 1
        a["Leg Compression Sleeves"] = 1
        a["Leg Warmers"] = 1
        a["Leggings"] = 1
        a["Lehenga"] = 1
        a["Leotards"] = 1
        a["Lingerie"] = 1
        a["Logo T Shirts"] = 1
        a["Long Sleeve Shirts"] = 1
        a["Long Underwear"] = 1
        a["Loose-Fit"] = 1
        a["Luxury Belts"] = 1
        a["Luxury Watches"] = 1
        a["Maxi Dresses"] = 1
        a["Mechanical Watches"] = 1
        a["Mesh Shirts"] = 1
        a["Mesh Shorts"] = 1
        a["Mid Calf Socks"] = 1
        a["Military Watches"] = 1
        a["Minimizer Bras"] = 1
        a["Mittens"] = 1
        a["Mountain Bike Socks"] = 1
        a["Multi-Sport"] = 1
        a["Neck Ties"] = 1
        a["Neck Warmers"] = 1
        a["Neckwear"] = 1
        a["Newsboy Caps"] = 1
        a["Nightgown"] = 1
        a["Nightshirts"] = 1
        a["Novelty Socks"] = 1
        a["Nylons"] = 1
        a["One Piece Bathing Suits"] = 1
        a["One Pieces"] = 1
        a["Over Knee Socks"] = 1
        a["Padded Bras"] = 1
        a["Pajama Sets"] = 1
        a["Pajama"] = 1
        a["Panties"] = 1
        a["Pants"] = 1
        a["Pantyhose"] = 1
        a["Parkas"] = 1
        a["Pea Coats"] = 1
        a["Ped Socks"] = 1
        a["Personal Hygiene Products"] = 1
        a["Plaid Shirts"] = 1
        a["Plus Size Bras"] = 1
        a["Polo Shirts"] = 1
        a["Polyester Shirts"] = 1
        a["Ponchos"] = 1
        a["Puffy Jackets"] = 1
        a["Pullover"] = 1
        a["Push up bras"] = 1
        a["Quarter Socks"] = 1
        a["Quartz Watches"] = 1
        a["Raincoat"] = 1
        a["Rain Hats"] = 1
        a["Rain Jackets"] = 1
        a["Rash Guards"] = 1
        a["Riding Chaps"] = 1
        a["Robes"] = 1
        a["Rompers"] = 1
        a["Safari Hats"] = 1
        a["Salwar"] = 1
        a["Saree"] = 1
        a["Sari"] = 1
        a["Satin Bras"] = 1
        a["Scally Caps"] = 1
        a["Scarves"] = 1
        a["Scratch Resistant Watches"] = 1
        a["Seamless Socks"] = 1
        a["Separates"] = 1
        a["Shapewear"] = 1
        a["Shaping Panties"] = 1
        a["Shawls"] = 1
        a["Sheepskin Hats"] = 1
        a["Sheer Socks"] = 1
        a["Sherwani"] = 1
        a["Shoe Trees"] = 1
        a["Short Sleeve Shirts"] = 1
        a["Shorts"] = 1
        a["Shoulder Bags"] = 1
        a["Silver Watches"] = 1
        a["Singlets"] = 1
        a["Skeleton Watches"] = 1
        a["Ski Gloves"] = 1
        a["Ski Hats"] = 1
        a["Ski Jackets"] = 1
        a["Ski Pants"] = 1
        a["Ski Socks"] = 1
        a["Skinny Jeans"] = 1
        a["Skirts"] = 1
        a["Skorts"] = 1
        a["Skull Caps"] = 1
        a["Sleepwear"] = 1
        a["Sleeveless Dresses"] = 1
        a["Sleeveless Tops"] = 1
        a["Slipper Socks"] = 1
        a["Slouch Socks"] = 1
        a["Small Leather"] = 1
        a["Snap Pants"] = 1
        a["Socks"] = 1
        a["Socks/Hosiery"] = 1
        a["Softshell Jackets"] = 1
        a["Spa Accessories"] = 1
        a["Sport Watches"] = 1
        a["Sports Apparel"] = 1
        a["Sports Bras"] = 1
        a["Sports Socks"] = 1
        a["Square Watches"] = 1
        a["Stainless Steel Watches"] = 1
        a["Stockings"] = 1
        a["Stockings/Tights"] = 1
        a["Strapless Bras"] = 1
        a["Straw Hats"] = 1
        a["String Bikinis"] = 1
        a["Striped Socks"] = 1
        a["Suede Hats"] = 1
        a["Suit"] = 1
        a["Sun Dresses"] = 1
        a["Sun Hats"] = 1
        a["Sun Protection Hats"] = 1
        a["Sunsuits"] = 1
        a["Support Socks"] = 1
        a["Suspenders"] = 1
        a["Sweater Dresses"] = 1
        a["Sweater Vests"] = 1
        a["Sweaters"] = 1
        a["Sweatpants"] = 1
        a["Sweatshirts"] = 1
        a["Swim Aids"] = 1
        a["Swim Shirts"] = 1
        a["Swim Shorts"] = 1
        a["Swim Trunks"] = 1
        a["Swimwear"] = 1
        a["Swimwear Shorts"] = 1
        a["Swiss Watches"] = 1
        a["T-Shirts"] = 1
        a["Tank Tops"] = 1
        a["Tankinis"] = 1
        a["Tennis Apparel"] = 1
        a["Tennis Socks"] = 1
        a["Thermal Underwear"] = 1
        a["Thigh High Socks"] = 1
        a["Thong Panties"] = 1
        a["Tie Dye Shirts"] = 1
        a["Ties"] = 1
        a["Tight-Fit"] = 1
        a["Tights"] = 1
        a["Titanium Watches"] = 1
        a["Toe Socks"] = 1
        a["Top Hats"] = 1
        a["Track Jackets"] = 1
        a["Track Pants"] = 1
        a["Trapper Hats"] = 1
        a["Travel Accessories"] = 1
        a["Travel Alarm Clocks"] = 1
        a["Travel Clocks"] = 1
        a["Trench Coats"] = 1
        a["Triathlon Apparel"] = 1
        a["Trouser Socks"] = 1
        a["Tube Socks"] = 1
        a["Tunics"] = 1
        a["Turtlenecks"] = 1
        a["Tutus"] = 1
        a["Two Piece Sweatsuits"] = 1
        a["Underwear & Bras"] = 1
        a["Underwear Bottoms"] = 1
        a["Underwear Tops"] = 1
        a["Underwire Bras"] = 1
        a["Unitards"] = 1
        a["Urban Clothes"] = 1
        a["Vests"] = 1
        a["Visor Beanies"] = 1
        a["Visors"] = 1
        a["Waders"] = 1
        a["Walking Socks"] = 1
        a["Wallets"] = 1
        a["Watch"] = 1
        a["Watches"] = 1
        a["Watches/Wristwear"] = 1
        a["Water Resistant Watches"] = 1
        a["Waterproof Boots"] = 1
        a["Waterproof Watches"] = 1
        a["Western Apparel"] = 1
        a["Wetsuits"] = 1
        a["Wide Brim Hats"] = 1
        a["Windbreakers"] = 1
        a["Winter Hats"] = 1
        a["Winter Headwear"] = 1
        a["Winter Jackets"] = 1
        a["Wirefree Bras"] = 1
        a["Wool Hats"] = 1
        a["Wool Socks"] = 1
        a["Work Pants"] = 1
        a["Workwear"] = 1
        a["Wrist Watches"] = 1
        a["Wristbands"] = 1
        a["Yoga Accessories"] = 1
        a["Yoga Bottoms"] = 1
        a["Yoga Mats"] = 1
        a["Yoga Tops"] = 1

        a["Baby Grow"] = 1
        a["Bag"] = 1
        a["Ball Gown"] = 1
        a["Belt"] = 1
        a["Bikini"] = 1
        a["Blazer"] = 1
        a["Blouse"] = 1
        a["Boots"] = 1
        a["Bow Tie"] = 1
        a["Boxers"] = 1
        a["Bra"] = 1
        a["Bra & Knicker Set"] = 1
        a["Briefs"] = 1
        a["Camisole"] = 1
        a["Cardigan"] = 1
        a["Cargos"] = 1
        a["Catsuit"] = 1
        a["Chemise"] = 1
        a["Coat"] = 1
        a["Corset"] = 1
        a["Cravat"] = 1
        a["Cufflinks"] = 1
        a["Cummerbund"] = 1
        a["Dinner Jacket"] = 1
        a["Dress"] = 1
        a["Dressing Gown"] = 1
        a["Dungarees"] = 1
        a["Fleece"] = 1
        a["Gloves"] = 1
        a["Hair Accessory"] = 1
        a["Hat"] = 1
        a["Hoody"] = 1
        a["Jacket"] = 1
        a["Jeans"] = 1
        a["Jewellery"] = 1
        a["Jogging Suit"] = 1
        a["Jumper"] = 1
        a["Kaftan"] = 1
        a["Kilt"] = 1
        a["Knickers"] = 1
        a["Kurta"] = 1
        a["Lingerie"] = 1
        a["Nightgown"] = 1
        a["Nightwear"] = 1
        a["Overalls"] = 1
        a["Pashmina"] = 1
        a["Polo Shirt"] = 1
        a["Poncho"] = 1
        a["Pyjamas"] = 1
        a["Robe"] = 1
        a["Romper"] = 1
        a["Sandals"] = 1
        a["Sarong"] = 1
        a["Scarf"] = 1
        a["Shawl"] = 1
        a["Shellsuit"] = 1
        a["Shirt"] = 1
        a["Shorts"] = 1
        a["Skirt"] = 1
        a["Slippers"] = 1
        a["Socks"] = 1
        a["Stockings"] = 1
        a["Suits"] = 1
        a["Sunglasses"] = 1
        a["Sweatshirt"] = 1
        a["Swimming Costume"] = 1
        a["Swimming Shorts"] = 1
        a["Swimming Trunks"] = 1
        a["Swimwear"] = 1
        a["Tee"] = 1
        a["T-Shirt"] = 1
        a["TShirt"] = 1
        a["Tailcoat"] = 1
        a["Tankini"] = 1
        a["Thong"] = 1
        a["Tie"] = 1
        a["Tights"] = 1
        a["Top"] = 1
        a["Tracksuit"] = 1
        a["Trainers"] = 1
        a["Trousers"] = 1
        a["Underwear"] = 1
        a["Vest"] = 1
        a["Vest Underwear"] = 1
        a["Waistcoat"] = 1
        a["Waterproof"] = 1
        a["Zip"] = 1
        
        a["Long-sleeve"] = 1
        a["Shoes"] = 1
        a["Boot"] = 1
        
        b = {}
        for x in a:
            y = x.lower()
            b[y] = 1
            indexof_space = y.find(' ')
            if indexof_space != -1:
                z = y[:indexof_space]
                b[z] = 1
                z = y[indexof_space+1:]
                b[z] = 1
        
        z = {}
        for y in b:
            z[y] = 1
            if y[len(y)-1] != 's':
                z[y+"s"] = 1
        
        return z
        

    def exclusions_list(self):
        
        a = {}
        a['contact'] = 1
        a['contactus'] = 1
        a['about'] = 1
        a['aboutus'] = 1	
        a['privacy'] = 1
        a['privacypolicy'] = 1
        a['policies'] = 1	
        a['policy'] = 1
        a['company'] = 1
        a['careers'] = 1
        a['career'] = 1
        a['job'] = 1
        a['jobs'] = 1
        a['sign'] = 1
        a['signin'] = 1
        a['login'] = 1
        a['logout'] = 1
        a['signout'] = 1
        a['exit'] = 1
        a['password'] = 1
        a['email'] = 1
        a['forgot'] = 1
        a['change'] = 1
        a['forgotpassword'] = 1
        a['forgetpassword'] = 1
        a['changepassword'] = 1
        a['account'] = 1
        a['accounts'] = 1
        a['cart'] = 1
        a['carts'] = 1
        a['detail'] = 1
        a['details'] = 1
        a['blog'] = 1
        a['phone'] = 1
        a['facebook'] = 1
        a['twitter'] = 1
        a['store'] = 1
        a['locate'] = 1
        a['locator'] = 1
        a['stores'] = 1
        a['terms'] = 1
        a['term'] = 1
        a['conditions'] = 1
        a['condition'] = 1
        a['pay'] = 1
        a['bill'] = 1
        a['investor'] = 1
        a['site'] = 1
        a['help'] = 1
        
        return a
        
    
    def getColorFromHtml(self, html):
        words = html_to_words(html)
        colors = []
        for w in words:
            color = self.getColorName(w)
            if color:
                colors.append(color)
        if colors:
            return colors[0]
        else:
            return None
    
    
    def getColorName(self, c):
        
        if not c:
            return None
        
        if c.lower() in self.colornames:
            return c
        else:
            return None
    
    
    def BuildColorName(self):
        colors = {}
            
        colors['light'] = 1
        colors['dark'] = 1
        
        colors["fire brick"] = 1
        colors["cadet blue"] = 1
        colors["indigo"] = 1
        colors["sea green"] = 1
        colors["gold"] = 1
        colors["pale goldenrod"] = 1
        colors["yellow"] = 1
        colors["slate gray"] = 1
        colors["lightsea green"] = 1
        colors["light yellow"] = 1
        colors["pale turquoise"] = 1
        colors["navajo white"] = 1
        colors["silver"] = 1
        colors["chartreuse"] = 1
        colors["misty rose"] = 1
        colors["black"] = 1
        colors["indian red"] = 1
        colors["crimson"] = 1
        colors["brown"] = 1
        colors["turquoise"] = 1
        colors["dark magenta"] = 1
        colors["old lace"] = 1
        colors["cyan"] = 1
        colors["green yellow"] = 1
        colors["darksea green"] = 1
        colors["darkolive green"] = 1
        colors["gray"] = 1
        colors["goldenrod"] = 1
        colors["dark violet"] = 1
        colors["mediumviolet red"] = 1
        colors["mediumspring green"] = 1
        colors["teal"] = 1
        colors["dark orange"] = 1
        colors["peach puff"] = 1
        colors["deep pink"] = 1
        colors["lavender"] = 1
        colors["forest green"] = 1
        colors["dim gray"] = 1
        colors["thistle"] = 1
        colors["violet"] = 1
        colors["navy"] = 1
        colors["orchid"] = 1
        colors["blue"] = 1
        colors["honeydew"] = 1
        colors["burly wood"] = 1
        colors["purple"] = 1
        colors["dark red"] = 1
        colors["cornsilk"] = 1
        colors["red"] = 1
        colors["bisque"] = 1
        colors["khaki"] = 1
        colors["wheat"] = 1
        colors["dark gray"] = 1
        colors["royal blue"] = 1
        colors["sky blue"] = 1
        colors["mediumslate blue"] = 1
        colors["gainsboro"] = 1
        colors["lemon chiffon"] = 1
        colors["cornflower blue"] = 1
        colors["midnight blue"] = 1
        colors["light grey"] = 1
        colors["plum"] = 1
        colors["hot pink"] = 1
        colors["aqua"] = 1
        colors["dark khaki"] = 1
        colors["pale green"] = 1
        colors["beige"] = 1
        colors["azure"] = 1
        colors["darkslate gray"] = 1
        colors["dark salmon"] = 1
        colors["light blue"] = 1
        colors["sienna"] = 1
        colors["dodger blue"] = 1
        colors["sandy brown"] = 1
        colors["blue violet"] = 1
        colors["lime"] = 1
        colors["seashell"] = 1
        colors["light pink"] = 1
        colors["fuchsia"] = 1
        colors["dark goldenrod"] = 1
        colors["dark blue"] = 1
        colors["peru"] = 1
        colors["lightgoldenrod yellow"] = 1
        colors["lightsky blue"] = 1
        colors["white"] = 1
        colors["darkslate blue"] = 1
        colors["olive drab"] = 1
        colors["ghost white"] = 1
        colors["ivory"] = 1
        colors["blanched almond"] = 1
        colors["light salmon"] = 1
        colors["steel blue"] = 1
        colors["light coral"] = 1
        colors["orange"] = 1
        colors["olive"] = 1
        colors["moccasin"] = 1
        colors["medium blue"] = 1
        colors["dark orchid"] = 1
        colors["light cyan"] = 1
        colors["floral white"] = 1
        colors["light green"] = 1
        colors["dark cyan"] = 1
        colors["coral"] = 1
        colors["aquamarine"] = 1
        colors["rosy brown"] = 1
        colors["spring green"] = 1
        colors["saddle brown"] = 1
        colors["maroon"] = 1
        colors["medium turquoise"] = 1
        colors["magenta"] = 1
        colors["lime green"] = 1
        colors["tan"] = 1
        colors["yellow green"] = 1
        colors["pink"] = 1
        colors["lawn green"] = 1
        colors["medium aquamarine"] = 1
        colors["lightslate gray"] = 1
        colors["mint cream"] = 1
        colors["dark turquoise"] = 1
        colors["snow"] = 1
        colors["papaya whip"] = 1
        colors["lavender blush"] = 1
        colors["orange red"] = 1
        colors["lightsteel blue"] = 1
        colors["medium orchid"] = 1
        colors["salmon"] = 1
        colors["medium purple"] = 1
        colors["deepsky blue"] = 1
        colors["antique white"] = 1
        colors["chocolate"] = 1
        colors["tomato"] = 1
        colors["white smoke"] = 1
        colors["linen"] = 1
        colors["green"] = 1
        colors["paleviolet red"] = 1
        colors["mediumsea green"] = 1
        colors["slate blue"] = 1
        colors["powder blue"] = 1
        colors["dark green"] = 1
        
        maincolors = []
        for c in colors:
            i = c.rfind(' ')
            if i > 0:
                maincolors.append(c[i+1:])
        
        for c in maincolors:
            colors[c] = 1
                
        return colors
    
