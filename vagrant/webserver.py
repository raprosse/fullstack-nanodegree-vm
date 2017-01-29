from BaseHTTPServer import BaseHTTPRequestHandler, BaseHTTPServer

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except: KeyboardInterrupt:
		print "^C entered, stopping webserver..."
		server.socket.close()


if __name__ == '__main__':
	main()