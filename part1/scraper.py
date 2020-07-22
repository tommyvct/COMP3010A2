#!/usr/bin/python3

import socket
import sys
import os


# try:
#     name = sys.argv[1]
#     if sys.argv[2].lower() == "yes" or sys.argv[2].lower() == "no":
#         response =  "1" if sys.argv[2] == "yes" else "0" #argv[2] == "yes" ? "1" : "0"
#     else:
#         print(f"Bad format\nExample usage:\n{str(os.path.basename(__file__))}  Rick yes\n{str(os.path.basename(__file__))}  Morty no")
#         exit(1)
# except IndexError:
#     print(f"Bad format\nExample usage:\n{str(os.path.basename(__file__))}  Rick yes\n{str(os.path.basename(__file__))}  Morty no")
#     exit(1)



name = "gdfsg"
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

# print(req.decode())
# print()
# print()
# print()

# Example POST request coming out from Chrome
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

# Debloated POST request to send
################################################################################
# POST /~wus2/cgi-bin/a.cgi HTTP/1.1
# Host: www-test.cs.umanitoba.ca
# Content-Length: 28
# Content-Type: application/x-www-form-urlencoded
#
# name=idsjuafabfbadf&accept=1
################################################################################
"""
/// @brief A test fuction to check if the server returned the thing we want.
///        It compares the result to check line by line, against a semi-hardcoded string.
/// @param toCheck string to check
/// @return `True` if check passed, `False` if failed.
///         If `-O` is not passed to interpreter(i.e. assersion is on), and a check failed, the function will `assert False` instead.
"""
def check(toCheck, name, response, comeback):
    # assert False is used intentionally to save typing.
    # the failing condition is already describe in the if condition
    if toCheck.find("chunked") == -1 and toCheck.find("Content-Length") != -1:
        print("not chunked, test not covered")
        assert False
        return False

    comeback_offset = 2 if comeback else 0

    # Build reference string
    REFERENCE = []
    REFERENCE.append("HTTP/1.1 200 OK")
    # skip Date
    # skip Server
    if not comeback:
        REFERENCE.append("Set-Cookie: name=" + name)
        REFERENCE.append("Set-Cookie: accept=" + response)
    # skip transfer encoding
    REFERENCE.append("Content-Type: text/html; charset=UTF-8")
    # skip 3 lines
    REFERENCE.append("""    <html>""")
    REFERENCE.append("""    <body>""")
    if comeback:
        REFERENCE.append("""<p style="color:green">Thanks for replying. Here's your previous response.</p>""")
    REFERENCE.append("""    <h1>You are Invited!</h1> """)
    REFERENCE.append("""    details goes here""")
    REFERENCE.append("""    <br/><br/><br/>""")
    REFERENCE.append("""    <form action="/~wus2/cgi-bin/a.cgi" method="POST">""")
    REFERENCE.append("""        <label for="name">Your name:</label>""")
    REFERENCE.append( f"        <input type=\"text\" name=\"name\" pattern=\".*[a-zA-Z].*\" title=\"At least 1 English letter\" value={name} autofocus required>")
    REFERENCE.append("""        <br/>""")
    REFERENCE.append("""        <p2>Would you accept the invitation?</p2>""")
    REFERENCE.append("""        <br/>""")
    if response == "0":
        REFERENCE.append("""        <input type="radio" name="accept" value="1" required > Accept""")
        REFERENCE.append("""        <input type="radio" name="accept" value="0" checked> Decline""")
    else:
        REFERENCE.append("""        <input type="radio" name="accept" value="1" required checked> Accept""")
        REFERENCE.append("""        <input type="radio" name="accept" value="0" > Decline""")
    REFERENCE.append("""        <br/>""")
    REFERENCE.append("""        <input type="submit" value="Submit">""")
    REFERENCE.append("""    </form>""")
    REFERENCE.append("""    <br/>""")
    REFERENCE.append("""        <form action="/~wus2/cgi-bin/a.cgi" method="GET">""")
    REFERENCE.append("""        <button name="Anonymize" type="submit">Anonymize</button>""")
    REFERENCE.append("""        </form>""")
    REFERENCE.append("""</body></html>""")

    # debloat responses from server
    processed = []
    toCheck = toCheck.splitlines(keepends = False)
    processed.append(toCheck[0])
    # skip Date
    # skip Server
    if not comeback:
        processed.append(toCheck[3]) # cookie
        processed.append(toCheck[4]) # cookie
    # skip transfer encoding
    processed.append(toCheck[6 - comeback_offset])   # content-type
    # skip 3 lines
    processed.append(toCheck[10 - comeback_offset])  # html
    processed.append(toCheck[11 - comeback_offset])  # body

    if comeback:
        processed.append(toCheck[10])
    elif  ((toCheck[12] != """<p style="color:green">Your reply has been submitted!</p>""") and 
            (toCheck[12] != """<p style="color:green">Your reply has been updated!</p>""")): 
        # print("FAIL 1")
        # print(toCheck[12])
        assert False
        return False


    # debloat HTML
    for i in range(13 - comeback_offset, len(toCheck)):
        if toCheck[i] == "" or toCheck[i].isspace():
            continue
        else:
            processed.append(toCheck[i])

    if (len(processed) != len(REFERENCE)):
        # print(processed, sep = '\n')
        # print("========================================================")
        # print(REFERENCE, sep = '\n')
        # print("FAIL 2")
        assert False
        return False

    for i in range(0, len(REFERENCE)):
        if (processed[i] != REFERENCE[i]):
            # print("FAIL 3")
            # print(processed[i] + " != " + REFERENCE[i])
            assert False
            return False

    # print("PASS")
    return True

# sample response from server
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

# What if something went wrong
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
resp = s.recv(4096).decode("utf-8")
s.close()
# print('Received:')
# print(resp)

check(resp, name, response, False)



# Example  coming out from Chrome
################################################################################
# GET /~wus2/cgi-bin/a.cgi HTTP/1.1
# Host: www-test.cs.umanitoba.ca
# Connection: keep-alive
# Cache-Control: max-age=0
# DNT: 1
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# Accept-Encoding: gzip, deflate
# Accept-Language: en-CA,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5
# Cookie: name=asdfsadf; accept=1; lastModified=0
################################################################################

# Debloated GET request
################################################################################
# GET /~wus2/cgi-bin/a.cgi HTTP/1.1
# Host: www-test.cs.umanitoba.ca
# Cookie: name=asdfsadf; accept=1; lastModified=0
################################################################################

# example server response
################################################################################
# HTTP/1.1 200 OK
# Date: Wed, 22 Jul 2020 08:29:25 GMT
# Server: Apache/2.4.6 (Scientific Linux) OpenSSL/1.0.2k-fips PHP/5.4.16 mod_wsgi/3.4 Python/2.7.5
# Transfer-Encoding: chunked
# Content-Type: text/html; charset=UTF-8
#
# 369
#
#     <html>
#     <body>
# <p style="color:green">Thanks for replying. Here's your previous response.</p>
#
#     <h1>You are Invited!</h1> 
#     details goes here
#     <br/><br/><br/>
#
#     <form action="/~wus2/cgi-bin/a.cgi" method="POST">
#         <label for="name">Your name:</label>
#         <input type="text" name="name" pattern=".*[a-zA-Z].*" title="At least 1 English letter" value=gdfsg autofocus required>
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


# build request string
req = b""
req += b"GET /~wus2/cgi-bin/a.cgi HTTP/1.1\r\n"
req += b"Host: www-test.cs.umanitoba.ca\r\n"
req += str.encode(f"Cookie: name={name}; accept={response}\r\n\r\n")


# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect(("www-test.cs.umanitoba.ca", 80))
s.sendall(req)
resp = s.recv(4096).decode("utf-8")
s.close()
# print('Received:')
# print(resp)

check(resp, name, response, True)
print("Success.")
