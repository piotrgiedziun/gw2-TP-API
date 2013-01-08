import Cookie
import os
import pickle
import uuid
import time

class CookiesManager(object):
	
	def __init__(self, http_cookie):
		self._cookie = Cookie.SimpleCookie(http_cookie)
	
	def set(self, index, value, expires_time=30*24*60*60):
		self._cookie[index] = value
		self._cookie[index]["path"] = "/"
		self._cookie[index]["expires"] = expires_time
		self._cookie[index]["version"] = 1
		
	def get(self, index, default=None):
		try:
			return self._cookie[index].value
		except:
			return default
			
	def remove(self, index):
		self.set(index, None, -1)
		
	def remove_all(self):
		for cookie in self._cookie:
			self.remove(cookie)
	
	def get_headers(self):
		headers = []
		
		# set cookie
		if len(self._cookie.output(header="Set-Cookie:")[len("Set-Cookie:"):]) > 0:
			headers.append(("Set-Cookie", self._cookie.output(header="Set-Cookie:")[len("Set-Cookie:"):]))
		
		# cookie
		if len(self._cookie.output(header="Cookie:")[len("Cookie:"):]) > 0:
			headers.append(("Cookie", self._cookie.output(header="Cookie:")[len("Cookie:"):]))
	
		return headers
			
class SessionManager(object):
	
	def __init__(self, cookiesManager):
		self._values = {}
		self._cookiesManager = cookiesManager
		self._sessionPath = ".session"
		
		# set session id / create session
		if self._cookiesManager.get("session", None) == None:
			self._session_id = uuid.uuid1()
			self.create_session()
		else:
			# session id validation
			try:
				#int(self._cookiesManager.get("session", None), 16)
				# TODO: file name validation !!
				self._session_id = self._cookiesManager.get("session", None)
			except:
				# create new session
				self._session_id = uuid.uuid1()
				self.create_session()
	
		# set file path		
		self._path = os.path.join(os.path.dirname(__file__), self._sessionPath)
		self._file_name = str(self._session_id)
		self._full_path = os.path.join(self._path, self._file_name)
				
		self._values = self._read_file()
		
	def _read_file(self):
		if not os.path.exists(self._path):
			os.makedirs(self._path)
		
		try:
			return pickle.load(open(self._full_path))
		except:
			return {}
			
	def _save_file(self):
		f = open(self._full_path, "wb")
		pickle.dump(dict(self._values), f)
		f.close() 
		
	def create_session(self):
		self._cookiesManager.set("session", self._session_id)
	
	def remove(self):
		self._cookiesManager.remove("session")
		
	def set(self, index, value):
		self._values[index] = value
		self._save_file()
		
	def get(self, index, default):
		try:
			return self._values[index]
		except:
			return default
			
