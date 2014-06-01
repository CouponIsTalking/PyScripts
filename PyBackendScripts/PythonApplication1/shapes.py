class Grid(object):
	def __init__(self, x , y, w, h, tag, eid):
		self.xs = [x]
		self.ys = [y]
		self.w = w
		self.h = h
		self.tag = tag
		self.eids = [eid]
	
	# will blindly append x,y,eid to the grid list
	def add(self, x, y, eid):
		self.xs.append(x)
		self.xs.append(x+self.w)
		self.ys.append(y)
		self.ys.append(y+self.h)
		self.eids.append(eid)
	
	def write(self):
		print self.eids
	
	def getTag(self):
		return self.tag
	
	def getEids(self):
		return self.eids
	
	
	def isInGrid(self, x, y, w, h, tag):
		foundXMatch = False
		foundYMatch = False
		
		if self.tag != tag:
			return False
			
		if self.w != w:
			return False
		if self.h != h:
			return False
			
		#print self.w
		for a in self.xs:
			x1 = abs(x-a)
			x2 = abs(x+w-a)
			#print min(x1, x2)			
			if min (x1, x2) <= self.w +5:
				foundXMatch = True
				break
		
		if not foundXMatch:
			#print "foundXMatch false"
			return False
		#else:
			#print "foundXMatch true"
			
		#print self.h
		
		for b in self.ys:
			y1 = abs(y-b)
			y2 = abs(y+h-b)
			#print min(y1,y2)
			if min (y1, y2) <= self.h +5:
				foundYMatch = True
				break
				
		if not foundYMatch:
			#print "foundYMatch false"
			return False
		#else:
			#print "foundYMatch true"
		
		return True


# elements must be added in a sorted fashion		
class RectangleStack(object):
	def __init__(self, x1, y1, x2, y2, w, h, tag, eid1, eid2):
		self.xs = []
		self.ys = []
		self.eids = []
		
		if x1 == x2:
			self.xs = [x1,x2]
			if y1 < y2:
				self.ys = [y1, y2]
				self.eids = [eid1, eid2]
			else:
				self.ys = [y2, y1]
				self.eids = [eid2, eid1]
		
		if y1 == y2:
			self.ys = [y1, y2]
			if x1 < x2:
				self.xs = [x1, x2]
				self.eids = [eid1, eid2]
			else:
				self.xs = [x2, x1]
				self.eids = [eid2, eid1]
		
		self.w = w
		self.h = h
		self.tag = tag
		
	def getTag(self):
		return self.tag
	
	def getEids(self):
		return self.eids;
	
	
	def add(self, x, y, eid):
		
		if self.xs[0] == x:
			self.xs.append(x)
			if y < self.ys[0]:
				self.ys = [y] + self.ys
				self.eids = [eid] + self.eids
			else:
				self.ys.append(y)
				self.eids.append(eid)
			return
		
		if self.ys[0] == y:
			self.ys.append(y)
			if x < self.xs[0]:
				self.xs = [x] + self.xs
				self.eids = [eid] + self.eids
			else:
				self.xs.append(x)
				self.eids.append(eid)
			return
		
	
	def write(self):
		print self.eids
		
	def isInStack(self, x, y, w, h, tag):
		xAligned = True
		yAligned = True
		
		if self.tag != tag:
			return False
		
		if self.w != w:
			return False
		if self.h != h:
			return False
			
		for a in self.xs:
			if x != a:
				xAligned = False
				break
		
		for b in self.ys:
			if y != b:
				yAligned = False
				break
		
		i = 0
		while i < len(self.xs):
			if x == self.xs[i] and y == self.ys[i]:
				return True
			i = i+1
		
		if (not xAligned) and (not yAligned):
			return False
				
		if xAligned:
			if y - self.ys[0] == self.ys[0] - self.ys[1]:
				return True
			len_ys = len(self.ys)
			
			if y - self.ys[len_ys-1] == self.ys[len_ys-1] - self.ys[len_ys-2]:
				return True
			
		if yAligned:
			if x - self.xs[0] == self.xs[0] - self.xs[1]:
				return True
			len_xs = len(self.xs)
			
			if x - self.xs[len_xs-1] == self.xs[len_xs-1] - self.xs[len_xs-2]:
				return True
				
		return False


	def test(self):
		
		r = RectangleStack(10,15,10,25, 20, 30, 'div', 100, 110)
		print r.isInStack(10, 45, 20, 30, 'div')
		print r.isInStack(10, 15, 20, 30, 'div')
		print r.isInStack(10, 25, 20, 30, 'div')
		print r.isInStack(10, 5, 20, 30, 'div')
		print r.isInStack(10, 35, 20, 30, 'div')
		print r.isInStack(10, 20, 20, 30, 'div')  # you have to add y sorted values
		
		if r.isInStack(10, 45, 20, 30, 'div'):
			r.add(10,45, 120)
		
		if r.isInStack(10, 15, 20, 30, 'div'):
			r.add(10,15, 130)
		
		if r.isInStack(10, 25, 20, 30, 'div'):
			r.add(10,25, 140)
			
		if r.isInStack(10, 5, 20, 30, 'div'):
			r.add(10,5, 150)
			
		if r.isInStack(10, 35, 20, 30, 'div'):
			r.add(10,35, 160)
			
		if r.isInStack(10, 20, 20, 30, 'div'):  # you have to add y sorted values
			r.add(10,20, 170)
			
		if r.isInStack(10, 45, 20, 30, 'a'):
			r.add(10,5, 180)
			
		if r.isInStack(0, -5, 20, 30, 'div'):
			r.add(10,35, 190)
			
		if r.isInStack(0, 100, 20, 30, 'a'):  # you have to add y sorted values
			r.add(10,20, 200)
		
		if r.isInStack(10, 45, 20, 30, 'div'):
			r.add(10,5, 210)
			
		if r.isInStack(0, -5, 20, 30, 'div'):
			r.add(10,35, 220)
			
		if r.isInStack(0, 100, 20, 30, 'div'):  # you have to add y sorted values
			r.add(10,20, 230)
			
		r.write()

