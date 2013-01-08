import unittest
from web import ConnectionManager
from config import Config
from trade import TradeWorker

class TradeTest( unittest.TestCase ):
  
  def __init__( self, testCaseName ):
    (unittest.TestCase).__init__(self, testCaseName)
    self.tw = TradeWorker(Config().getData())
  
  def testItem( self ):
    self.assertEqual(self.tw.get_item(19726).name, "Soft Wood Log")
    
  def testMultipleItems( self ):
    self.assertEqual(self.tw.get_items([19726, 19727])[19726].name, "Soft Wood Log")
    
  def testTrends( self ):
    self.assertTrue(len(self.tw.get_trends()) > 0)

class ConnectionManagerTest( unittest.TestCase ):

  def testInvalidLogin( self ):
    conn = ConnectionManager({
      'email': 'misspelled_email@email.com',
      'password': 'misspelled_password'
    })
    self.assertEqual(conn.login(), 400)
    
  def testValidLogin( self ):
    conn = ConnectionManager(Config().getData())
    self.assertTrue(conn.login())
    
if __name__ == '__main__':
  print "make sure you set correct data in config.py"
  unittest.main()