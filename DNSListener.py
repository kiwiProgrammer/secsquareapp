#!/usr/bin/env python
  
import SocketServer
import threading
import urllib2
import json

from dnslib import A, AAAA, CNAME, MX, RR, TXT
from dnslib import DNSHeader, DNSRecord, QTYPE

# Known hardcoded SecSquare server address
SECSQUARE_HOST_ADDRESS = "107.21.245.181"

class SecSquareUDP(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data= self.request[0]
        self.socket = self.request[1]
        self.dns_handler(self.data, self.socket)
    
    def dns_handler(self, data, socket):
        request = DNSRecord.parse(data)
        id = request.header.id
        qname = request.q.qname
        qtype = request.q.qtype

        print (qname)
        if "secsquare.herokuapp.com" == qname:
            reply = DNSRecord(DNSHeader(id=id, qr=1, aa=1, ra=1), q=request.q)
            # if the query is for SecSquare server
            reply.add_answer(RR(qname,qtype, rdata=A(SECSQUARE_HOST_ADDRESS)))
        else:
            # if query is for any other host names
            label = str(qname)
            raw_data = urllib2.urlopen("https://secsquare.herokuapp.com/api.php?name="+label).read()
            data = json.loads(raw_data)
            results = data['results']
            reply = DNSRecord(DNSHeader(id=id, qr=1, aa=1, ra=1), q=request.q)
            for entry in results:
                # put all results from SecSquare server into reply
                if 'MX' in entry['type']:
                    #reply.add_answer(RR(qname,qtype, rdata=MX(entry['target'])))
                    continue
                elif 'AAAA' in entry['type']:
                    #reply.add_answer(RR(qname,qtype, rdata=AAAA(entry['ipv6'])))
                    continue
                elif 'A' in entry['type'] and 'ip' in entry:
                    reply.add_answer(RR(qname,qtype, rdata=A(entry['ip'])))
        print(reply) # print the DNS response for debugging purposes
        socket.sendto(reply.pack(), self.client_address)
  
server = SocketServer.ThreadingUDPServer(('127.0.0.1', 53), SecSquareUDP)
server_thread = threading.Thread(target=server.serve_forever)
#server_thread.daemon = True
server_thread.start()

    #dns_handler(s,peer,data)
