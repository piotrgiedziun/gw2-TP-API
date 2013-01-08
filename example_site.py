import iLikePizza.web
import json
from gw2api.trade import TradeWorker
from gw2api.config import Config

class staticFilesHandler(iLikePizza.web.Static):
	folder = "public"

class mainHanlder(iLikePizza.web.Request):

	def get(self):
		self.render("index.html")

class apiHandler(iLikePizza.web.Request):

	def get_trends(self):
		global tw
		
		objects = []

		for item in tw.get_trends():
			objects.append({
				'name': item.name,
				'url': item.icon,
				'description': ("Rarity: " + item.rarity)
			})

		self.write(json.dumps(objects))

application = iLikePizza.web.Application([
	(r'^$', mainHanlder),
	(r'api/get_trends$', apiHandler.get_trends),
	(r'public/([a-zA-Z_.]*)$', staticFilesHandler.handle),
])

if __name__ == "__main__":
	# one instance of worker
	print "connecting to API, please wait..."
	tw = TradeWorker(Config().getData())
	tw.force_login()

	application.listen()