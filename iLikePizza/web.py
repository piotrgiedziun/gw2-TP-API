import re
import inspect
from cgi import escape
from exception import *
from types import UnboundMethodType
from cookies import CookiesManager, SessionManager
from database import DatabaseManager
import mimetypes
import os.path

class Application(object):
	'''
	Application class
	Request handlers
	
	Usage:
		application = iLikePizza.web.Application([
			(r"/", Handler),
			(r"/", Handler.method),
		])
		
	The constructor for this class takes in a list of (regexp URL, request class or request method) tuples
	When application recive request will call:
		- when second list parm is class like (r"/([a-zA-Z_]+)", ExampleHandler)
			- ExampleHandler.post(parms) when recive POST request
			- ExampleHandler.get(parms) when recive GET request
		- when second list parm is method like (r"/", ExampleHandler.getData)
			- ExampleHandler.getData(parms)
			
	Getting url parms is really easy, you can get them by two ways:
		- method parms
			ex. for (r"/([0-9]+)/([0-9]*)", ExampleHandler) url schema
			
			class ExampleHandler(iLikePizza.web.Request):
				def get(self, id, code=0):
					print "id = %d code = %d" % (id, code)
					
			- for request [url]/10/15 will return
				id = 10 code = 15
		
			- for request [url]/10/ will return
				id = 10 code = 0
					
			As you can notice you can set default parameter values (code=None)
					
		- self.vars variable
			ex. for (r"/([0-9]+)/([0-9]*)", ExampleHandler) url schema
			
			class ExampleHandler(iLikePizza.web.Request):
				def get(self):
					id = self.vars[1]
					try:
						code = self.vars[2]
					except:
						code = 0
				
					print "id = %d code = %d" % (id, code)
			
	
	'''
	def __init__(self, urls):
		self.urls = urls
		
	def server_application(self, environ, start_response):
		'''
		By default handle POST and GET request.
		For DELETE, UPDATE, PUT, HEAD you have to make custom method
		'''
		path = environ.get('PATH_INFO', '').lstrip('/')
		
		for regex, callback in self.urls:
			match = re.search(regex, path)
			if match is not None:

				if type(callback) == UnboundMethodType: 
					callbackObject = callback.im_class(environ)
				else:
					callbackObject = callback(environ)
					
				callbackObject.vars = match.groups()
				
				try:
					if type(callback) == UnboundMethodType:
						callback(
							callbackObject,
							*self.callback_parms(callback, callbackObject.vars)
						)
					elif environ['REQUEST_METHOD'] == "GET":
						callbackObject.get(
							*self.callback_parms(callbackObject.get, callbackObject.vars)
						)
					elif environ['REQUEST_METHOD'] == "POST":
						callbackObject.post(
							*self.callback_parms(callbackObject.post, callbackObject.vars)
						)
						
					return callbackObject._return_response(start_response)
					
				except iLikePizzaException, (e):
					return self.error(environ, start_response, e.error)
				#except Exception, (e):
				#	print "Error: %s" % (e,)
				#	return self.error(environ, start_response, "Unkown Internal Error. More info in server console.")
				
		return self.error_404(environ, start_response)
		
	def callback_parms(self, callbackObjectFunction, inputParms):
		outputParms = []
		callbackParmCount = len(inspect.getargspec(callbackObjectFunction).args)-1
		
		if (callbackParmCount > len(inputParms)):
			raise iLikePizzaException("Invalid number of parms")
		
		for parm in inputParms[:callbackParmCount]:
			outputParms.append(parm)
			
		return outputParms
		
	def close(self):
		if hasattr(self.server_application, 'close'):
			self.server_application.close()
		
	def listen(self, ip="127.0.0.1", port=8080):
		'''
		Run Simple Server
		Default values:
		- ip = 127.0.0.1 (localhost)
		- port = 8080
		'''
		print "server on http://%s:%s/" % (ip, port)
		
		from wsgiref.simple_server import make_server
		server = make_server(ip, port, self.server_application)
		server.serve_forever()
		
	def error_404(self, environ, start_response):
		start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
		return ['Not Found']
		
	def error(self, environ, start_response, message):
		start_response('500 INTERNAL SEVER ERROR', [('Content-Type', 'text/plain')])
		return [message]

class Static(object):

	folder = "assets/"

	def __init__(self, environ):
		self.file_to_read = None
		self.file_to_read_mime = None

	def handle(self, name):
		file_path = os.path.join(self.folder, name)
		if not "." in file_path:
			return

		file_ext = ("."+file_path.split(".")[-1])
		mimetypes.init()

		if os.path.exists(file_path) and file_ext in mimetypes.types_map:
			self.file_to_read = file_path
			self.file_to_read_mime = mimetypes.types_map[file_ext]


	def _return_response(self, start_response):

		if self.file_to_read == None:
			return 

		headers = [
			('Content-Type', self.file_to_read_mime),
		]

		start_response('200 OK', headers)

		return open(self.file_to_read).read()

class Request(object):
	
	def __init__(self, environ):
		self._responseHTML = []
		self._cookiesManager = CookiesManager(environ.get("HTTP_COOKIE",""))
		self._sessionManager = SessionManager(self._cookiesManager)
		self.initialize()

	def _return_response(self, start_response):
		headers = [
			('Content-Type', 'text/html'),
		]

		headers += self._cookiesManager.get_headers()
		
		start_response('200 OK', headers)

		return self._responseHTML[:]
				
	def initialize(self):
		pass
		
	def get(self):
		pass
		
	def get(self):
		pass
		
	def set_session(self, index, value):
		self._sessionManager.set(index, value)
		
	def get_session(self, index, default):
		return self._sessionManager.get(index, default)
		
	def isset_session(self, index):
		pass
	
	def remove_session(self):
		self._sessionManager.remove()
		
	def set_cookie(self, index, value):
		self._cookiesManager.set(index, value)
		
	def get_cookie(self, index, default=None):
		return self._cookiesManager.get(index, default)
		
	def isset_cookie(self, index):
		pass
		
	def remove_cookie(self, index):
		self._cookiesManager.remove(index)
		
	def write(self, content):
		self._responseHTML.append(content)
		
	def render(self, file, **parms):
		f = open(file)
		for index in range(0, len(parms)-1):
			print parms[index]

		self._responseHTML.append(f.read())