import os, sys

class Debugger(object):
	def __init__(self, ip="127.0.0.1", port="8080"):
		self.baseURL = "http://%s:%s" % (ip, port)
		
	def _make_request(self, url):
		print "Request URL=%s\n" % (url,)
		os.system( "lwp-request -m GET %s" % (url,) )
		print "\n"
		
	def request(self, url):
		self._make_request(self.baseURL+url)
		
if __name__ == "__main__":
	d = Debugger()
	
	try:	
		d.request(sys.argv[1])
	except:
		print "no URL parm found."