from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
#from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Hello</h1>!"
				output +="<a href = '/hola'>Back to Hola</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
				output += "<h2>What would you like me to say?</h2>"
				output += "<input name='message' type='text'><input type='submit' value='Submit'>"
				output += "</form></body></html>"

				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""

				output += "<html><body>"
				output += "<h1>&#161Hola!</h1>"
				output +="<a href = '/hello'>Back to Hello</a>"

				output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
				output += "<h2>What would you like me to say?</h2>"
				output += "<input name='message' type='text'><input type='submit' value='Submit'>"
				
				output += "</form></body></html>"
				
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/restaurant"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				for name in DBquery():
					output +="<h1>%s</h1>" % name
					output +="<h1><a href= '/edit'>Edit</a></h1>"
					output +="<h1><a href= '/delete'>Delete</a></h1>"
					output +="<br>"

				output +="<h1><a href= '/newrestaurant'>Make a New Restaurant Here</a></h1>"
				output += "</body></html>"
				
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/newrestaurant"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>New Restaurant</h1>"
				output +="<a href = '/restaurant'>Back to Restaurants</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurant'>"
				output += "<h2>Enter New Restaurant Name</h2>"
				output += "<input name='message' type='text'><input type='submit' value='Create'>"
				output += "</form></body></html>"

				self.wfile.write(output)
				print output
				return

		except IOError:
			self.send_error(404, "File not found %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')

			output = ""

			output += "<html><body>"
			output += "<h2> Okay, how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent[0] 

			output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
			output += "<h2>What would you like me to say?</h2>"
			output += "<input name='message' type='text'><input type='submit' value='Submit'> "

			output += "</form></body></html>"

			self.wfile.write(output)
			print output

		except:
			pass

def DBquery():
		engine = create_engine('sqlite:///restaurantmenu.db')
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		result = session.query(Restaurant.name).order_by(Restaurant.name.asc()).all()
		return result

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