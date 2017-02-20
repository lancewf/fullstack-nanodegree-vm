from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from restaurant_data import RestaurantQuery

class webserverHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			
			if self.path.startswith("/restaurants") and self.path.endswith("/edit"):
				parts = self.path.split('/')

				if len(parts) == 4:
					restaurantId = int(parts[2])
					self._editRestaurantsResponse(restaurantId)
					return
			if self.path.startswith("/restaurants") and self.path.endswith("/delete"):
				parts = self.path.split('/')

				if len(parts) == 4:
					restaurantId = int(parts[2])
					self._deleteRestaurantsResponse(restaurantId)
					return

			if self.path.endswith("/hello"):
				self.helloResponse()
				return
			if self.path.endswith("/hola"):
				self.holaResponse()
				return
			if self.path.endswith("/restaurants"):
				self._restaurantsResponse()
				return
			if self.path.endswith("/new"):
				self._newRestaurantsResponse()
				return
		except:
			self.send_error(404, "File Not Found %s" %self.path)

	def do_POST(self):
		try:
			self.send_response(301)

			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile, pdict)

			if self.path.endswith("/hello"):
				messagecontent = fields.get('message')
				output = ""
				output += "<html><body>"
				output += "<h2>Okay, how about this:</h2>"
				output += "<h1>%s</h1>" % messagecontent[0]
				output += self._formHtml()
				output += "</body></html>"
				self.wfile.write(output)
				return
			if self.path.endswith('/restaurants/new'):
				restaurantName = fields.get('restaurant_name')[0]
				query = RestaurantQuery()
				query.createNewRestaurant(restaurantName)
				query.close()
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return
			if self.path.startswith("/restaurants") and self.path.endswith("/edit"):
				restaurantNewName = fields.get('restaurant_new_name')[0]
				restaurantId = int(fields.get('restaurant_id')[0])
				query = RestaurantQuery()
				query.renameRestaurant(restaurantId, restaurantNewName)
				query.close()
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return
			if self.path.startswith("/restaurants") and self.path.endswith("/delete"):
				restaurantId = int(fields.get('restaurant_id')[0])
				query = RestaurantQuery()
				query.deleteRestaurant(restaurantId)
				query.close()
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return


		except IOError:
			self.send_error(404, 'not sure what is going on')

	def _deleteRestaurantsResponse(self, restaurantId):
		try:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			query = RestaurantQuery()
			restaurant = query.getRestaurantFromId(restaurantId)
			query.close()

			if restaurant != None:
				output = ""
				output += "<html><body>"
				output += "<h1>Are you sure you want to delete %s?</h1>" % restaurant.name
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurant.id
				output += "<input name='restaurant_id' type='hidden' value='%s' >" % restaurant.id
				output += "<input type='submit' value='Delete'>"
				output += "</form>"
				output += "</body></html>"
				self.wfile.write(output)
			else:
				response = 'restaurant with ID' + restaurantId + " was not found"
				self.send_error(404, response)

			return
		except:
			print("Unexpected error:", sys.exc_info()[0])
			raise

	def _editRestaurantsResponse(self, restaurantId):
		try:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			query = RestaurantQuery()
			restaurant = query.getRestaurantFromId(restaurantId)
			query.close()

			if restaurant != None:
				output = ""
				output += "<html><body>"
				output += "<h1>%s</h1>" % restaurant.name
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant.id
				output += "<input name='restaurant_new_name' type='text' value='%s' >" % restaurant.name
				output += "<input name='restaurant_id' type='hidden' value='%s' >" % restaurant.id
				output += "<input type='submit' value='Rename'>"
				output += "</form>"
				output += "</body></html>"
				self.wfile.write(output)
			else:
				response = 'restaurant with ID' + restaurantId + " was not found"
				self.send_error(404, response)

			return
		except:
			print("Unexpected error:", sys.exc_info()[0])
			raise

	def _newRestaurantsResponse(self):

		try:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			output = ""
			output += "<html><body>"
			output += "<h1>Make a New Restaurant</h1>"
			output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
			output += "<input name='restaurant_name' type='text' >"
			output += "<input type='submit' value='Create'>"
			output += "</form>"
			output += "</body></html>"
			self.wfile.write(output)
			return
		except:
			print("Unexpected error:", sys.exc_info()[0])
			raise

	def _restaurantsResponse(self):

		try:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			query = RestaurantQuery()
			restaurants = query.getAllRestaurants()
			query.close()
			output = ""
			output += "<html><body>"
			output += "<ul>"
			for restaurant in restaurants:
				output += "<li> <h2>" + restaurant.name + " </h2> <br />" 
				output += "<a href='/restaurants/" + str(restaurant.id) + "/edit'>Edit</a> <br /> "
				output += "<a href='/restaurants/" + str(restaurant.id) + "/delete'>Delete</a>"
				output += "</li>"
			output += "</ul>"
			output += "<a href='/restaurants/new'>Make a New Restaurant Here</a>"
			output += "</body></html>"

			self.wfile.write(output)
			return
		except:
			print("Unexpected error:", sys.exc_info()[0])
			raise
			

	def helloResponse(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		output = ""
		output += "<html><body> Hello!"
		output += self._formHtml()
		output += "</body></html>"
		self.wfile.write(output)
		print output
		return

	def holaResponse(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		output = ""
		output += "<html><body> &#161Hola! <a href = '/hello' > Back to Hello</a>"
		output += self._formHtml()
		output += "</body></html>"
		self.wfile.write(output)
		print output
		return

	def _formHtml(self):
		output = "<form method='POST' enctype='multipart/form-data' action='hello'>"
		output += "<h2> What would you like me to say?</h2><input name='message' type='text' >"
		output += "<input type='submit' value='Submit'>"
		output += "</form>"

		return output


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()
