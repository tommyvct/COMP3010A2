#!/usr/bin/python3
# -*- coding=utf-8 -*-

import os
import sys
import json

# if no chatlog file, create one
# if POST request, replace the chatlog file with the incoming one
# else if GET request, read the chatlog file and print it back as is
# else something else, 400 Bad request

chatlogFile = "part2chatlog.json"


if not os.path.exists(chatlogFile):
    with open(chatlogFile, "w") as newChatlog:
        newChatlog.write('{"lastModified" : 0, "chatHistoryArray" : []}')

# print("Set-Cookie: Last-Modified=1595251041")

if os.environ["REQUEST_METHOD"] == "GET":
    with open(chatlogFile, "r") as chatlog:
        temp = chatlog.read()
        # compares time, if update needed
        if int(os.environ["HTTP_COOKIE"].split('=')[1]) <= json.loads(temp)["lastModified"]:
            print("Content-type:text/html")
            print()
            print()
            print(temp)
        else:
            print("Status: 304 Not Modified")
            print("Content-type:text/html")
            print()
            print()
elif os.environ["REQUEST_METHOD"] == "POST":
    with open(chatlogFile, "w") as chatlog:
        chatlog.write(sys.stdin.read(int(os.environ["CONTENT_LENGTH"])))
        print("Content-type:text/html")
        print()
        print()
else:
    print("Status: 400 Bad Request")
    print("Content-type:text/html")
    print()
    print()
    print("400 Bad Request")
