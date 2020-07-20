#!/usr/bin/python3
# -*- coding=utf-8 -*-

import os
import sys


chatlogFile = "part2chatlog.json"
#/Users/tommyvct/GitHub/COMP3010A2/
if not os.path.exists(chatlogFile):
    with open(chatlogFile, "w") as newChatlog:
        newChatlog.write('{"chatHistoryArray":[]}')

if os.environ["REQUEST_METHOD"] == "GET":
    with open(chatlogFile, "r") as chatlog:
        print("Content-type:text/html")
        print()
        print()
        print(chatlog.read())
elif os.environ["REQUEST_METHOD"] == "POST":
    with open(chatlogFile, "w") as chatlog:
        chatlog.write(sys.stdin.read(int(os.environ["CONTENT_LENGTH"])))
        print("Content-type:text/html")
        print()
        print()
        print(chatlog.read())
else:
    print("Status: 400 Bad Request")
    print("Content-type:text/html")
    print()
    print()
    print("400 Bad Request")

