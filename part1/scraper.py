#!/usr/bin/python3

import socket
import sys
import os


try:
    name = str.encode(sys.argv[1])
    response =  "1" if sys.argv[2] == "yes" else "2" #argv[2] == "yes" ? "1" : "0"
except IndexError:
    print(f"Bad format\nExample usage:\n{str(os.path.basename(__file__))}  Rick yes\n{str(os.path.basename(__file__))}  Morty no")
finally:
    exit(1)



name = "idsjuafabfbadf"
response = "1"

# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect(("www-test.cs.umanitoba.ca", 80))

# build request string
req = b""
req += b"POST /~wus2/cgi-bin/a.cgi HTTP/1.1\r\n"
req += b"Host: www-test.cs.umanitoba.ca\r\n"
req += str.encode(f"Content-Length: {14 + len(name)}\r\n")
req += b"Content-Type: application/x-www-form-urlencoded\r\n\r\n"

req += str.encode(f"name={name}&accept={response}")

print(req.decode())
print()
print()
print()



################################################################################
# POST /~wus2/cgi-bin/a.cgi HTTP/1.1
# Host: www-test.cs.umanitoba.ca
# Content-Length: 28
# Content-Type: application/x-www-form-urlencoded
#
# name=idsjuafabfbadf&accept=1
################################################################################


################################################################################
# POST /~wus2/cgi-bin/a.cgi HTTP/1.1\r\n
# Host: www-test.cs.umanitoba.ca
# Connection: keep-alive
# Content-Length: 19
# Cache-Control: max-age=0
# Origin: http://www-test.cs.umanitoba.ca
# Upgrade-Insecure-Requests: 1
# DNT: 1
# Content-Type: application/x-www-form-urlencoded
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# Referer: http://www-test.cs.umanitoba.ca/~wus2/cgi-bin/a.cgi?Anonymize=
# Accept-Encoding: gzip, deflate
# Accept-Language: en-CA,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5
# Cookie: name=; accept=
# 
# name=fdsaf&accept=1
################################################################################

################################################################################
# HTTP/1.1 200 OK
# Date: Sat, 18 Jul 2020 21:10:34 GMT
# Server: Apache/2.4.6 (Scientific Linux) OpenSSL/1.0.2k-fips PHP/5.4.16 mod_wsgi/3.4 Python/2.7.5
# Set-Cookie: name=idsjuafabfadf
# Set-Cookie: accept=1
# Transfer-Encoding: chunked
# Content-Type: text/html; charset=UTF-8
#
# 35a
#
#     <html>
#     <body>
# <p style="color:green">Your reply has been updated!</p>
#
#     <h1>You are Invited!</h1> 
#     details goes here
#     <br/><br/><br/>
#
#     <form action="/~wus2/cgi-bin/a.cgi" method="POST">
#         <label for="name">Your name:</label>
#         <input type="text" name="name" pattern=".*[a-zA-Z].*" title="At least 1 English letter" value=idsjuafabfadf autofocus required>
#         <br/>
#         <p2>Would you accept the invitation?</p2>
#         <br/>
#         <input type="radio" name="accept" value="1" required checked> Accept
#         <input type="radio" name="accept" value="0" > Decline
#         <br/>
#         <input type="submit" value="Submit">
#     </form>
#     <br/>
#
#
#         <form action="/~wus2/cgi-bin/a.cgi" method="GET">
#         <button name="Anonymize" type="submit">Anonymize</button>
#         </form>
#
# </body></html>
################################################################################

################################################################################
# HTTP/1.1 400 Bad Request
# Date: Sat, 18 Jul 2020 21:02:17 GMT
# Server: Apache/2.4.6 (Scientific Linux) OpenSSL/1.0.2k-fips PHP/5.4.16 mod_wsgi/3.4 Python/2.7.5
# Connection: close
# Content-Type: text/html; charset=iso-8859-1
#
# <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
# <html><head>
# <title>400 Bad Request</title>
# </head><body>
# <h1>Bad Request</h1>
# <p>Your browser sent a request that this server could not understand.<br />
# </p>
# </body></html>
# <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
# <html><head>
################################################################################


s.sendall(req)
data = s.recv(2048)

resp = data.decode("utf-8")

assert (resp.find("200 OK") != -1), resp

print('Received:')
# It's in bytes, convert to text
print(data.decode("utf-8"))



