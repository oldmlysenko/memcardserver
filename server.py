#!/usr/bin/env python

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer

from memcard import MemCard



class MyHTTPHandler(BaseHTTPRequestHandler):

    memcard_db = MemCard('memcard','bak');

    
    file_tab = [    ("memcard.html"               , "text/html"               ), 
                    ("memcardedit.html"           , "text/html"               ),
                    ("serverapi.js"               , "text/javascript"         ),
                    ("cookies.js"                 , "text/javascript"         ),
                ]


 


    def execute_request_file(self,filename,mimetype):

        
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
        
        try:

            file = open(filename,mode='r')
            text = file.read()
            file.close()        
            print("Read "+str(len(text))+" from '"+filename+"'")
        
            self.wfile.write( text.encode("utf8") )
        except Exception as  e:
            print("Read '"+filename+"' error: "+str(e))

            



    def do_GET(self):
        page = self.path.strip('/\\ ')
        print("REQ: "+page)

        for ft in self.file_tab:
            if (page.startswith(ft[0])):    
                self.execute_request_file( ft[0],ft[1])
                return
            
            
        self.send_error(404)
            


    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length) 
            
            indatastr = post_data.decode("utf-8")
            indata  = json.loads(indatastr)                    
            outdata = {}
            
            print("REQ: ",indata)
            
            if (self.memcard_db.Process(indata,outdata)):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                text = json.dumps(outdata)
                self.wfile.write( text.encode("utf8") )
                return
            
            self.send_error(404)
            
        except Exception as  e:
            print("Post request error: "+str(e))        



class MyThreadingHTTPServer(ThreadingHTTPServer):

    def handle_error(self, request, client_address):
        print("Error on ",client_address)





def run(server_class=MyThreadingHTTPServer, handler_class=MyHTTPHandler, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print("Starting httpd server on %s:%i" % (addr,port))

    httpd.serve_forever()






if __name__ == "__main__":

    
    run(addr="192.168.0.35", port=33335)
