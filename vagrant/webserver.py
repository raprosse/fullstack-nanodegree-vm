from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
#from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
			if self.path.endswith("/restaurants"):
				
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				for restaurant in restaurants:
					output += restaurant.name
					output +="</br>"
					output +="<a href='restaurants/%s/edit'>Edit</a>" % restaurant.id
					output +="</br>"
					output +="<a href='restaurants/%s/delete'>Delete</a>" % restaurant.id
					output +="<br><br>"
					
				output +="<h1><a href= '/restaurants/new'>Make a New Restaurant Here</a></h1>"
				output += "</body></html>"
				
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>New Restaurant</h1>"
				output +="<a href = '/restaurants'>Back to Restaurants</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<input name='restaurant_name' type='text' placeholder = 'New Resaurant Name'><input type='submit' value='Create'>"
				output += "</form></body></html>"

				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/edit"):
				rest_id = self.path.split('/')[2]
				restaurant = session.query(Restaurant).filter_by(id =int(rest_id)).one()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>%s</h1>" % restaurant.name
				output +="<a href = '/restaurants'>Back to Restaurants</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % rest_id
				output += "<input name='restaurant_name' type='text' placeholder = 'Edit Resaurant Name'><input type='submit' value='Update'>"
				output += "</form></body></html>"

				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/delete"):
				rest_id = self.path.split('/')[2]
				restaurant = session.query(Restaurant).filter_by(id =int(rest_id)).one()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Are you sure you want to delete %s</h1>" % restaurant.name
				output +="<a href = '/restaurants'>Back to Restaurants</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % rest_id
				output +="<input type='submit' value='Delete'>"
				output += "</form></body></html>"

				self.wfile.write(output)
				print output
				return

		except IOError:
			self.send_error(404, "File not found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('restaurant_name')
					print messagecontent[0]
					restaurant = Restaurant(name=messagecontent[0])
					session.add(restaurant)
					session.commit()

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('restaurant_name')
					rest_id = self.path.split('/')[2]
					restaurant = session.query(Restaurant).filter_by(
						id =int(rest_id)).one()
					if restaurant != []:
						restaurant.name = messagecontent[0]
						session.add(restaurant)
						session.commit()

			if self.path.endswith("/delete"):
				rest_id = self.path.split('/')[2]
				restaurant = session.query(Restaurant).filter_by(
					id =int(rest_id)).one()
				if restaurant != []:
					session.delete(restaurant)
					session.commit()

			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.send_header('Location', '/restaurants')
			self.end_headers()

			return

		except:
			pass
		

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print " entered, stopping webserver..."
		server.socket.close()
if __name__ == '__main__':
	main()