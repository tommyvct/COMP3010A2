#!/usr/bin/python
# -*- coding=utf-8 -*-

import os
import socket
import subprocess


PORT = 8888
WWWROOT = "/Users/tommyvct/Desktop/web_files"

# set up socket
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ss.bind(("127.0.0.1", PORT))
ss.listen(5)


def request(status):
    """returns a part of header if 200, or the whole body if 404, etc"""
    ret = b""
    if status == 200:
        ret += b"HTTP/1.1 200 OK\r\n"
        ret += b"Server: crapserver\r\n"
    elif status == 404:
        ret += b"HTTP/1.1 404 Not Found\r\n"
        ret += b"Server: crapserver\r\n"
        ret += b"Content-Type: text/html; charset=UTF-8\r\n"
        ret += b"Connection: close\r\n\r\n"
        ret += b"<html>"
        ret += b"<head><title>404 Not Found</title></head>"
        ret += b"<body>"
        ret += b"<center><h1>404 Not Found</h1></center>"
        ret += b"<hr><center>crapserver</center>"
        ret += b"</body>"
        ret += b"</html>"
    elif status == 400:
        ret += b"HTTP/1.1 400 Bad Request\r\n"
        ret += b"Server: crapserver\r\n"
        ret += b"Content-Type: text/html; charset=UTF-8\r\n"
        ret += b"Connection: close\r\n\r\n"
        ret += b"<html>"
        ret += b"<head><title>400 Bad Request</title></head>"
        ret += b"<body>"
        ret += b"<center><h1>400 Bad Request</h1></center>"
        ret += b"<hr><center>crapserver</center>"
        ret += b"</body>"
        ret += b"</html>"
    elif status == 500:
        ret += b"HTTP/1.1 500 Internal Error\r\n"
        ret += b"Server: crapserver\r\n"
        ret += b"Content-Type: text/html; charset=UTF-8\r\n"
        ret += b"Connection: close\r\n\r\n"
        ret += b"<html>"
        ret += b"<head><title>500 Internal Error</title></head>"
        ret += b"<body>"
        ret += b"<center><h1>500 Internal Error</h1></center>"
        ret += b"<hr><center>crapserver</center>"
        ret += b"</body>"
        ret += b"</html>"
    else:
        raise NotImplementedError
    return ret


def get_static_file(filename, header_only=False):
    """Read a the given file, return then along with the header."""
    if filename == "/":
        filename = "/index.html"
    try:
        f = open(WWWROOT + filename, "rb")
        ret = f.read()
        f.close()
        if header_only:
            return b"Content-Length: " + bytes(str(len(ret))) + b"\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
        else:
            return b"Content-Length: " + bytes(str(len(ret))) + b"\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n" + ret
    except Exception as e:
        print(e)
        return None


def run_cgi(cgi, req_type, req_content, cookie=None):
    """CGI handler. It mapd the given request to appropriate place, and run it"""
    new_env = os.environ.copy()
    if cookie is not None:
        new_env['HTTP_COOKIE'] = cookie
    runner_stdin = None
    if req_type == "GET":
        if req_content != "":
            new_env['QUERY_STRING'] = req_content
    elif req_type == "POST":
        new_env['CONTENT_LENGTH'] = str(len(req_content))
        runner_stdin = bytes(req_content)
    else:
        raise NotImplementedError
    try:
        runner = subprocess.Popen(WWWROOT + cgi, stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=new_env, cwd=os.path.dirname(WWWROOT + cgi))
    except Exception as e:
        print(e)
        return request(500)
    # for post req
    (runner_stdout, runner_stderr) = runner.communicate(input=runner_stdin)
    if runner.returncode != 0:  # abnormal state
        return request(500)
    if runner_stdout.decode().split("\r\n")[0].find("Status") == -1:
        return request(200) + runner_stdout
    return runner_stdout


while True:
    """main loop"""
    (cs, address) = ss.accept()
    recv = cs.recv(2000).decode()
    # print("################### IN ##########################")
    # print(recv)

    tosend = b''

    try:
        req_type = recv.splitlines()[0].split()[0]
        req_file = recv.splitlines()[0].split()[1]

        tosend += request(200)
        if req_file.find(".cgi") == -1:  # static file
            if req_type == "GET":
                temp = get_static_file(req_file)
                if temp is not None:
                    tosend += temp
                else:
                    tosend = request(404)
            elif req_type == "HEAD":
                temp = get_static_file(req_file, header_only=True)
                if temp is not None:
                    tosend += temp
                else:
                    tosend = request(404)
            else:
                tosend = request(400)
        else:  # CGI
            # handle cookie
            cookie = None
            for a in recv.splitlines():
                aa = a.replace("\r", "").replace("\n", "").split(": ")
                if aa[0] == "Cookie":
                    cookie = aa[1]
                    break

            if req_type == "GET":
                try:
                    tosend = run_cgi(req_file.split("?")[0], "GET", req_file.split("?")[1], cookie)
                except IndexError:
                    tosend = run_cgi(req_file.split("?")[0], "GET", "", cookie)
            elif req_type == "POST":
                tosend = run_cgi(req_file.split("?")[0], "POST", recv.split("\r\n")[-1], cookie)
            else:
                tosend = request(400)
    except Exception as e:
        print(e)
        tosend = request(500)
    finally:
        cs.sendall(tosend)
        cs.close()

    # print("################### OUT ##########################")
    # print(tosend.decode(0))


# GET / HTTP/1.1
# Host: localhost:8888
# Connection: keep-alive
# Cache-Control: max-age=0
# DNT: 1
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# Sec-Fetch-Site: none
# Sec-Fetch-Mode: navigate
# Sec-Fetch-User: ?1
# Sec-Fetch-Dest: document
# Accept-Encoding: gzip, deflate, br
# Accept-Language: en-CA,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5


# GET /favicon.ico HTTP/1.1
# Host: localhost:8888
# Connection: keep-alive
# Pragma: no-cache
# Cache-Control: no-cache
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
# DNT: 1
# Accept: image/webp,image/apng,image/*,*/*;q=0.8
# Sec-Fetch-Site: same-origin
# Sec-Fetch-Mode: no-cors
# Sec-Fetch-Dest: image
# Referer: http://localhost:8888/
# Accept-Encoding: gzip, deflate, br
# Accept-Language: en-CA,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5
