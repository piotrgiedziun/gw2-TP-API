"""Tools class"""

class obj( object ):
  """This class provide dict to object transformation
  
  doctest:
  >>> obj({'item': 'value'}).item
  'value'
  >>> obj({'parent': {'child1':1, 'child2':2}, 'parent2': 'item'}).parent.child1
  1
  """
  def __init__( self, d ):
    for a, b in d.items():
      if isinstance(b, (list, tuple)):
        setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
      else:
        setattr(self, a, obj(b) if isinstance(b, dict) else b)