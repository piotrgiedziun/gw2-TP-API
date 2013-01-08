"""Guild Wars 2 - Trade Post API"""
from web import ConnectionManager
from tools import obj

class TradeWorker( object ):
  
  def __init__( self, login_data ):
    self.connnection = ConnectionManager( login_data )
  
  """
    force connection manager to login
  """
  def force_login( self ):
    self.connnection.login()

  """
    get trands items

    reuturn tuple of objects
  """
  def get_trends( self ):      
    result = []
    data = self.connnection.request('trends')
  
    if not 'items' in data:
      return result
    
    for item in data['items']:
      if 'name' in data['items'][item]:
        result.append(obj(data['items'][item]))
  
    return result
  
  """
    get items by ids

    reuturn dict of objects
      key - id
      value - object data
  """
  def get_items( self, items ):
    result = {}
    data = self.connnection.request('search', 'ids='+(",".join([str(i) for i in items])))
    
    if not 'results' in data:
      return result
      
    for item in data['results']:
      if 'name' in item:
        result[int(item['data_id'])] = obj(item)

    return result
  
  """
    get item by id

    return one object
  """
  def get_item( self, item_id ):
    data = self.connnection.request('search', 'ids=%d' % (item_id,))
  
    if not 'results' in data:
      return None
    
    return obj(data['results'][0])