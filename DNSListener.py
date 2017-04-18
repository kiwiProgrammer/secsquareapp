#!/usr/bin/env python
  
import socket

import urllib2
import json

from dnslib import A, AAAA, CNAME, MX, RR, TXT
from dnslib import DNSHeader, DNSRecord, QTYPE

# Known hardcoded SecSquare server address
SECSQUARE_HOST_ADDRESS = "107.21.245.181"

def dns_handler(s, peer, data):
    request = DNSRecord.parse(data)
    id = request.header.id
    qname = request.q.qname
    qtype = request.q.qtype

    reply = DNSRecord(DNSHeader(id=id, qr=1, aa=1, ra=1), q=request.q)

    if "secsquare.herokuapp.com" == qname:
        # if the query is for SecSquare server
        reply.add_answer(RR(qname,qtype, rdata=A(SECSQUARE_HOST_ADDRESS)))
    else:
        # if query is for any other host names
        label = str(qname)
        raw_data = urllib2.urlopen("https://secsquare.herokuapp.com/api.php?name="+label).read()
        data = json.loads(raw_data)
        results = data['results']
        for entry in results:
            # put all results from SecSquare server into reply
            if 'MX' in entry['type']:
                reply.add_answer(RR(qname,qtype, rdata=MX(entry['target'])))
            elif 'AAAA' in entry['type']:
                reply.add_answer(RR(qname,qtype, rdata=AAAA(entry['ipv6'])))
            elif 'A' in entry['type']:
                reply.add_answer(RR(qname,qtype, rdata=A(entry['ip'])))
    print(reply) # print the DNS response for debugging purposes
    s.sendto(reply.pack(), peer)
  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 53))
  
while True:
    print "====== Waiting for connection"
    data, peer = s.recvfrom(8192)
    dns_handler(s,peer,data)
