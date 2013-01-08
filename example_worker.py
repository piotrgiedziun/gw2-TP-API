# -*- coding: utf-8 -*-
from gw2api.trade import TradeWorker
from gw2api.config import Config
  
def main():
  tw = TradeWorker(Config().getData())
  print tw.get_item(19726).name
  try:
    print tw.get_item(19726).name
    
    print tw.get_items([19727, 19728])[0].name
    
    for item in tw.get_trends():
      print item.name
  except:
    print "server down"
  
if __name__ == '__main__':
  main()