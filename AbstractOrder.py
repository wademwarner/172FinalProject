


class AbstractOrder:
	
	def __init__(self, id):
		self.id = id
		
	def __str__(self):
		return "Order %d "% (self.id)
