import lxml.html
from lxml.html import etree
from htmlops import *

from SeleniumReader import *
from tag_classifier import *
from misc import *


class lxmlops(object):
	
	def __init__(self, source):
		
		self.source = None
		self.tree1 = None
		self.etree1 = None
		self.buildTreeFromSource(source)
		self.tag_dict = Tags()
	
	def buildTreeFromUrl(self, url_or_reader):
		self.reader = None
		if isinstance(url_or_reader, str):
			self.reader = SeleniumReader(url_or_reader);
			
		elif isinstance(url_or_reader, SeleniumReader):
			self.reader = url_or_reader
		else:
			print "~~~~~~~~~ Bad param to constructor ~~~~~~~~~~~~~"
			return
		
		self.source = self.reader.getPageSource()
		self.buildTreeFromSource(self.source)


	def buildTreeFromSource(self, source):
		
		if not source:
			return
		#self.source = source
		self.source = removeCommentsAndJS(removeHeads(source))
		self.tree1 = lxml.html.fromstring(self.source)
		self.etree1 = etree.ElementTree(self.tree1)
		
		return
	
	def findXPathByOuterHtml(self, to_find_outer_htmls):
		
		if not to_find_outer_htmls:
			return []
		
		root = self.tree1
		etree1 = self.etree1
		
		xpaths = []
		found_htmls = []
		for outer_html in to_find_outer_htmls:
			found_htmls.append( False )
			xpaths.append(None)
		levelSortedChildList = []
		nextChildId = 0
		levelSortedChildList.append(root)
		
		while nextChildId < len(levelSortedChildList):
			nextChild = levelSortedChildList[nextChildId]
					
			#check if we are looking for this outerhtml
			element_outer_html = lxml.html.tostring(nextChild)
			if len(element_outer_html) < 70 and "<option" in element_outer_html:
				print element_outer_html
				print to_find_outer_htmls[0]
				print (element_outer_html == to_find_outer_htmls[0])
				print "--"
			i = 0
			while i < len(to_find_outer_htmls):
				if not found_htmls[i]:
					outer_html = to_find_outer_htmls[i]
					if abs(len(outer_html) - len(element_outer_html)) <= 10:
						if self.compareOuterHtml(outer_html, element_outer_html):
							found_htmls[i] = True
							xpaths[i] = etree1.getpath(nextChild)
				i = i+1
			
			itsChildren = list(nextChild)
			for c in itsChildren:
				levelSortedChildList.append(c)
			
			nextChildId = nextChildId + 1
		
		return xpaths
	
	def clickElements(self, xpaths):
		eles = l.reader.getElementsByXPath(xpaths[0])
		if not eles:
			print 'no element found'
		for e in eles:
			e.click()
		
		return
	
	def compareOuterHtml(self, outer_html1, outer_html2):
		
		outer_html1 = removeCommentsAndJS(outer_html1).strip()
		outer_html2 = removeCommentsAndJS(outer_html2).strip()
		
		if not outer_html1:
			return 0
		if not outer_html2:
			return 0
		
		tree1 = lxml.html.fromstring(outer_html1)			
		etree1 = etree.ElementTree(tree1)
		tree2 = lxml.html.fromstring(outer_html2)			
		etree2 = etree.ElementTree(tree2)
		
		if tree1.tag != tree2.tag:
			return 0
		
		div_compare_mem = {}
		
		result = 0
		if tree1.tag == 'option':
			result = self.compareOptionTag(tree1, etree1, tree2, etree2)
		elif tree1.tag == 'img':
			result = self.compareImgTag(tree1, etree1, tree2, etree2)
		elif tree1.tag == 'a':
			result = self.compareATag(tree1, etree1, tree2, etree2)
		elif tree1.tag == 'li':
			result = self.compareLITag(div_compare_mem, tree1, etree1, tree2, etree2)
		elif tree1.tag == 'ul':
			result = self.compareULTag(div_compare_mem, tree1, etree1, tree2, etree2)
		elif tree1.tag == 'div':
			result = self.compareElements(div_compare_mem, tree1, etree1, tree2, etree2)
		return result
	
	def compareLITag(self, div_compare_mem, l1, etree1, l2, etree2):
		return self.compareElements(div_compare_mem, l1, etree1, l2, etree2);
	
	def compareULTag(self, div_compare_mem, ul1, etree1, ul2, etree2):
		return self.compareElements(div_compare_mem, ul1, etree1, ul2, etree2);
	
	
	def compareTextContent(self, c1, c2):
		str1 = c1.text_content().encode("ascii","ignore")
		str2 = c2.text_content().encode("ascii","ignore")
		
		if str1 and str2 and str1 == str2:
			return 1
		
		return 0
	
	def compareLeafDivTag(self, c1, etree1, tree2, etree2):
		
		if c1.tag == 'div' and tree2.tag == 'div':
			if self.compareTextContent(c1, tree2) == 1:
				return 1
		
		return 0
	
	def compareATag(self, c1, etree1, tree2, etree2):
		
		if c1.tag == 'a' and tree2.tag == 'a':
			if self.compareTextContent(c1, tree2) == 1:
				return 1
		
		return 0
	
	def compareOptionTag(self, c1, etree1, tree2, etree2):
		
		if c1.tag == 'option' and tree2.tag == 'option':
			if self.compareTextContent(c1, tree2) == 1:
				return 1
		
		return 0
	
	def compareImgTag(self, c1, etree1, tree2, etree2):
		
		if c1.tag != 'img' or tree2.tag != 'img':
			return 0
		
		xpath1 = etree1.getpath(c1)
		xpath2 = etree2.getpath(tree2)
		imgsrc1 = etree1.xpath(xpath1+'/@src')
		imgsrc2 = etree1.xpath(xpath2+'/@src')
		
		#if xpath1 and xpath2 and xpath1 == xpath2 and imgsrc1 == imgsrc2:
		if imgsrc1 == imgsrc2:
			str1 = c1.text_content().encode("ascii","ignore")
			str2 = tree2.text_content().encode("ascii","ignore")	
			if (not str1) and (not str2):
				return 1
			if str1 == str2:
				return 1
		
		return 0
	
	
	def compareElements(self, div_compare_mem, div1, etree1, div2, etree2):
		# if we have already compared these 2 divs, then dont compare again
		# simply return stored comparison result
		#
		pre_calc_result = self.getMem(div_compare_mem, div1, etree1, div2, etree2) 
		if pre_calc_result == 0 or pre_calc_result == 2:
			return 0
		
		if pre_calc_result == 1:
			return pre_calc_result
		
		# set the comparison result as true
		result = 1
		
		#few base conditions
		
		# if div tags dont match, compare will fail
		if div1.tag != div2.tag:
			result = 0
		
		# if number of childs dont match, compare will fail
		childs1 = list(div1)
		childs2 = list(div2)
		if len(childs1) != len(childs2):
			result = 0
		
		# if comparision failed, so far, then store the comparison's result
		# and return
		if result == 0:
			self.setMem(div_compare_mem, div1, etree1, div2, etree2, result)
			return 0
		
		if len(childs1) == 0:
			if div1.tag == 'a' and self.compareATag(div1, etree1, div2, etree2) == 1:
				result = 1
			elif div1.tag == 'img' and self.compareImgTag(div1, etree1, div2, etree2) == 1:
				result = 1
			elif div1.tag == 'option' and self.compareOptionTag(div1, etree1, div2, etree2) == 1:
				result = 1
			elif self.compareTextContent(div1, div2) == 1:
				result = 1
			else:
				result = 0
		
		else:
			# except img div, we should compare the text content of divs
			compareText = 1
			if div1.tag == 'img':
				compareText = 0
		
			if compareText == 1 and self.compareTextContent(div1, div2) == 0:
				result = 0
			else:
				result = 1
				for c1 in childs1:
					#xpath1 = etree1.getpath(c1)
					#children2 = etree2.xpath(xpath1)
					match_found = 0
					for c2 in childs2:
						if self.compareElements(div_compare_mem, c1, etree1, c2, etree2) == 1:
							match_found = 1
							break
					if match_found == 0:
						result = 0
						break
					
		self.setMem(div_compare_mem, div1, etree1, div2, etree2, result)
		
		return result
	
	def getMem(self, div_compare_mem, div1, etree1, div2, etree2):
		#global div_compare_mem;
		
		xpath1 = etree1.getpath(div1)
		xpath2 = etree2.getpath(div2)
		
		if (xpath1, xpath2) in div_compare_mem:
			return div_compare_mem[(xpath1, xpath2)]
		else:
			div_compare_mem[(xpath1, xpath2)] = -1
			return -1
	
	def setMem(self, div_compare_mem, div1, etree1, div2, etree2, result):
		#global div_compare_mem;
		
		xpath1 = etree1.getpath(div1)
		xpath2 = etree2.getpath(div2)	
		div_compare_mem[(xpath1, xpath2)] = result
		print div_compare_mem
		return div_compare_mem[(xpath1, xpath2)]

	#############################
	###############
	def getSelectBox(self):
		
		root = self.tree1
		etree1 = self.etree1
		
		sizeSelectBoxesXpaths = []
		optionsXPaths_selectbox = []
		
		selectboxes = []
		options_selectbox = []
		childlist = [root]
		eno = 0
		while eno < len(childlist):
			nextEle = childlist[eno]
			if nextEle.tag and nextEle.tag == 'select':
				selectboxes.append(nextEle)
			else:
				childlist = childlist + list(nextEle)
			eno = eno+1
		
		for selectbox in selectboxes:
			parentno = 0
			pEle = selectbox
			cont = False
			while True:
				text = pEle.text_content().encode("ascii", "ignore")
				text = clean_text(text)
				words = [w for w in re.split('\W', text) if w]
				print words
				if words and (self.tag_dict.isSizeHintWord(words[0].lower()) or self.tag_dict.isSizeHintWord(words[-1].lower())):
					cont = True
					break
				elif "color" in text or "review" in text or "qty" in text or "rating" in text:
					break
				if parentno > 3:
					break
				else:
					pEle = pEle.getparent()
					parentno = parentno + 1
			
			if cont:
				sizeSelectBoxesXpaths.append(etree1.getpath(selectbox))
				options_xpaths = []
				options = []
				childlist = [selectbox]
				eno =0
				while eno < len(childlist):
					nextEle = childlist[eno]
					if nextEle.tag and nextEle.tag == 'option':
						options.append(nextEle)
					else:
						childlist = childlist + list(nextEle)
					eno = eno+1
				
				for op in options:
					op_text = op.text_content().encode("ascii", "ignore")
					if self.tag_dict.isSizeType(op_text):
						options_xpaths.append(etree1.getpath(op))
				
				optionsXPaths_selectbox.append(options_xpaths)
			
		return sizeSelectBoxesXpaths, optionsXPaths_selectbox
	
	
	#############################
	###############
	def getImgTags(self):
		
		root = self.tree1
		etree1 = self.etree1
		
		colorImgBoxesXpaths = []
		colorImgRoot = None
		colorImgRootXpath = None
		imgXPaths = []
		
		imgboxes = []
		options_selectbox = []
		childlist = [root]
		eno = 0
		while eno < len(childlist):
			nextEle = childlist[eno]
			if nextEle.tag and nextEle.tag == 'img':
				imgboxes.append(nextEle)
			else:
				childlist = childlist + list(nextEle)
			eno = eno+1
		
		pEle = None
		for imgbox in imgboxes:
			parentno = 0
			pEle = imgbox
			cont = False
			while True:
				text = pEle.text_content().encode("ascii", "ignore")
				text = clean_text(text)
				words = [w for w in re.split('\W', text) if w]
				#print words
				if words:
					if (self.tag_dict.isColorWord(words[0].lower()) or self.tag_dict.isColorHintWord(words[0].lower())):
						cont = True
						break
					elif self.tag_dict.getColorName(words[-1]):
						pass
					#elif "size" in text or "review" in text or "qty" in text or "rating" in text:
					else:
						print words
						break
				if parentno > 4:
					break
				else:
					pEle = pEle.getparent()
					parentno = parentno + 1
			
			if cont:
				colorImgBoxesXpaths = []
				colorImgRootXpath = etree1.getpath(pEle)
				imgs = []
				childlist = [pEle]
				eno =0
				while eno < len(childlist):
					nextEle = childlist[eno]
					if nextEle.tag and nextEle.tag == 'img':
						imgs.append(nextEle)
					else:
						childlist = childlist + list(nextEle)
					eno = eno+1
				
				for op in imgs:
					op_outerhtml = lxml.html.tostring(op)
					color = self.tag_dict.getColorFromHtml(op_outerhtml)
					if color:
						colorImgBoxesXpaths.append(etree1.getpath(op))
				
				break
			
		return colorImgRootXpath, colorImgBoxesXpaths

