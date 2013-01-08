class iLikePizzaException(Exception):
	'''
	Simple one value exception
	
	Usage:
		throw iLikePizzaException("message")	
	'''
	def __init__(self, message):
		self.error = message
		
	def __str__(self):
		return repr(self.error)