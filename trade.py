"""Guild Wars 2 - Trade Post API"""
from web import ConnectionManager
from tools import obj

class TradeWorker( object ):
  
  def __init__( self, login_data ):
    self.connnection = ConnectionManager( login_data )
    #self.connnection.login() 
    
  def get_trends( self ):      
    result = []
    data = self.connnection.request('trends')
  
    if not 'items' in data:
      return result
    
    for item in data['items']:
      if 'name' in data['items'][item]:
        result.append(obj(data['items'][item]))
  
    return result
  
  def get_items( self, items ):
    result = []
    data = self.connnection.request('search', 'ids='+(",".join([str(i) for i in items])))
    
    if not 'results' in data:
      return result
      
    print data['results']  
      
    for item in data['results']:
      if 'name' in item:
        result.append(obj(item))

    return result
  
  def get_item( self, item_id ):
    data = self.connnection.request('search', 'ids=19726')
  
    if not 'results' in data:
      return None
    
    return obj(data['results'][0])