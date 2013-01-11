from django.http import HttpResponse
import json
from gw2api.trade import TradeWorker
from gw2api.config import Config

print "login in progress"
tw = TradeWorker(Config().getData())
tw.force_login()
print "logged"

def get_trends(request):
	global tw
	objects = []

	for item in tw.get_trends():
		objects.append({
			'name': item.name,
			'url': item.icon,
			'description': ("Rarity: " + item.rarity)
		})

	return HttpResponse(json.dumps(objects))