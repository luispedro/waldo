#!/usr/local/bin/python

import sys, httplib
from xml.dom import implementation
from xml.dom.ext import PrettyPrint
from xml.dom.minidom import parse
import StringIO

# define namespaces used
ec = "http://schemas.xmlsoap.org/soap/encoding/"
soapEnv = "http://schemas.xmlsoap.org/soap/envelope/"
req = "http://ws.mgi.jax.org/xsd/request"
bt = "http://ws.mgi.jax.org/xsd/batchType"

# create DOM document
domdoc = implementation.createDocument(None, '', None)

# create SOAP envelope and namespace
seObj = domdoc.createElementNS(soapEnv, "SOAP-ENV:Envelope")
seObj.setAttributeNS(soapEnv, "SOAP-ENV:encodingStyle", ec)

# add SOAP envelope to the root
domdoc.appendChild(seObj)

# create SOAP header and add it to the SOAP envelope
header = domdoc.createElement("SOAP-ENV:Header")
seObj.appendChild(header)

# create SOAP body and add it to the SOAP envelope
body = domdoc.createElement("SOAP-ENV:Body")

# create submitDocument element
submitDoc = domdoc.createElement("submitDocument")

# create the desired request element and sub-elements 
# in the appropriate namespace

# request is a batchMarkerRequest
request = domdoc.createElementNS(req, "req:batchMarkerRequest")

# create IDSet and assign appropriate IDType attribute
set = domdoc.createElementNS(req, "req:IDSet")
set.setAttribute("IDType", "symbol")

# create id elements and add to IDSet element
id1 = domdoc.createElementNS(bt, "bt:id")
id1.appendChild(domdoc.createTextNode("pax6"))
id2 = domdoc.createElementNS(bt, "bt:id")
id2.appendChild(domdoc.createTextNode("trp53"))

# add id elements to IDSet element
set.appendChild(id1)
set.appendChild(id2)

# create resturnSet element and sub-elements
returnSet = domdoc.createElementNS(req, "req:returnSet")
att1 = domdoc.createElementNS(bt, "bt:attribute")
att1.appendChild(domdoc.createTextNode("nomenclature"))
returnSet.appendChild(att1)
att2 = domdoc.createElementNS(bt, "bt:attribute")
att2.appendChild(domdoc.createTextNode("location"))
returnSet.appendChild(att2)
att3 = domdoc.createElementNS(bt, "bt:attribute")
att3.appendChild(domdoc.createTextNode("entrezGene"))
returnSet.appendChild(att3)
att4 = domdoc.createElementNS(bt, "bt:attribute")
att4.appendChild(domdoc.createTextNode("ensembl"))
returnSet.appendChild(att4)
att5 = domdoc.createElementNS(bt, "bt:attribute")
att5.appendChild(domdoc.createTextNode("vega"))
returnSet.appendChild(att5)

# create returnAdditionalInfo element 
additionalInfo = domdoc.createElementNS(req, "req:returnAdditionalInfo")
additionalInfo.appendChild(domdoc.createTextNode("mp"))

# add IDSet to batchMarkerRequest element
request.appendChild(set)

# add resturnSet to batchMarkerRequest element
request.appendChild(returnSet)

# add returnAdditionalInfo to batchMarkerRequest element
request.appendChild(additionalInfo)

# add batchMarkerRequest to submitDocument element
submitDoc.appendChild(request)

# add submitDocument to SOAP body
body.appendChild(submitDoc)

# add SOAP body to SOAP envelope
seObj.appendChild(body)

# format SOAP request for display
soapStrOut = StringIO.StringIO()
PrettyPrint(domdoc, soapStrOut)

# view the soap request
print soapStrOut.getvalue()

# construct the header and send the request
webservice = httplib.HTTP("services.informatics.jax.org")
webservice.putrequest("POST", "http://services.informatics.jax.org/mgiws")
webservice.putheader("Host", "services.informatics.jax.org")
webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
webservice.putheader("Content-length", "%d" % len(soapStrOut.getvalue()))
webservice.putheader("SOAPAction", "submitDocument")
webservice.endheaders()
webservice.send(soapStrOut.getvalue())

# get the response and display it
statuscode, statusmessage, header = webservice.getreply()
print "Response: ", statuscode, statusmessage
print "headers: ", header

# view the soap response()
f = webservice.getfile()
data = f.read() # Get the raw HTML
f.close()

print "Response: ", statuscode, statusmessage
print "headers: ", header

print data
