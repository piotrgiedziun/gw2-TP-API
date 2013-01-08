""" Layer being responsible for network communication"""
import urllib, urllib2, cookielib, json

class ConnectionManager( object ):
  
  _LOGIN_URL = 'https://account.guildwars2.com/login?redirect_uri=http%3A%2F%2Ftradingpost-live.ncplatform.net%2Fauthenticate%3Fsource%3D%252F&game_code=gw2'
  _logged = False
  
  def __init__( self, login_data ):
    self._ACCOUNT_EMAIL = login_data['email']
    self._ACCOUNT_PASSWORD = login_data['password']
    
    self.cj = cookielib.CookieJar()
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
  
  def login( self ):
    self._logged = False
    
    try:
      self.opener.addheaders = [('Referer', 'https://account.guildwars2.com/login')]
      resp = self.opener.open( self._LOGIN_URL,
        urllib.urlencode({'email' : self._ACCOUNT_EMAIL, 'password' : self._ACCOUNT_PASSWORD})
      )
      self._logged = True
    except urllib2.URLError, e:
      if not hasattr(e, "code"):
        raise Exception("Unkown error occurred")
      return e.code
    
    if "The account name or password you entered is invalid." in resp.read():
      return 400

    return True

  def request( self, page, parms = "", relogin = False ):
    try:
      self.opener.addheaders = [('Referer', 'https://tradingpost-live.ncplatform.net')]
      resp = self.opener.open('https://tradingpost-live.ncplatform.net/ws/%s.json?%s' % (page, parms,))
      return json.loads(resp.read())
    except urllib2.URLError, e:
      if not hasattr(e, "code"):
        raise Exception("Unkown error occurred")
      elif e.code == 401 and not relogin:
        self.login()
        return self.request(page, parms, True)
      elif e.code == 404:
        raise Exception("Server down")
      else:
        raise Exception("Can't connect to server")
        
    