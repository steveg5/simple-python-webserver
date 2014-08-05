#Copyright Jon Berg , turtlemeat.com

import string,cgi,time
from os import curdir, sep
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
#import pri

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.path = self.path.replace("/", "")
            print("Get received [", curdir, "][", sep, "]", self.path)
            if self.path.endswith(".html"):
                print(curdir + sep + self.path)
                #f = open(curdir + sep + self.path) #self.path has /test.html
                f = open(self.path) #self.path has /test.html
#note that this potentially makes every file on your computer readable by the internet
# This is a line that I added
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(bytes(f.read(), 'UTF-8'))
                print("Closing file")
                f.close()
                print("Returning")
                return
            if self.path.endswith(".esp"):   #our dynamic content
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                print("hey today is the " + str(time.localtime()[7]))
                self.wfile.write(bytes("hey today is the " + str(time.localtime()[7]), 'UTF-8'))
                self.wfile.write(bytes(" day in the year " + str(time.localtime()[0]) + "<br />", 'UTF-8'))
                self.wfile.write(bytes("Is this the 5 minute argument?", 'UTF-8'))
                return
                
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)
            
            self.end_headers()
            upfilecontent = query.get('upfile')
            print ("filecontent", upfilecontent[0])
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            self.wfile.write(upfilecontent[0]);
            
        except :
            pass

def main():
    try:
        server = HTTPServer(('', 80), MyHandler)
        print ('started httpserver...')
        server.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    main()

