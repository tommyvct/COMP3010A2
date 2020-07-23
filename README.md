# COMP3010 Assignment 2
## Part 1: A1 scraper
### Compile:
* for C version:
    ```
    clang -o scraper scraper.c
    ```
    Pass `-DNDEBUG` to `clang` to disable assertion.
* for Python version, run it with Python 3
    ```
    python3 scraper.py
    ```
    Pass `-O` to the Python interpreter to disable assertion.
### Running:
* Both the program have the same behaviour.
    
* The program only accept 2 and only 2 params, namely the name and their response.
    The name should contain at least 1 English letter, and the response can only be `yes` or `no`.

    Following will be printed out if params cannot be recognized:
    ```
    Bad format
    Example usage:
    scraper.py  Rick yes
    scraper.py  Morty no
    ```

* There are 2 tests in the program. If any one of then failed, the program will print out `Test 1 failed` or `Test 2 failed`.

* If everything went alright, `Success` will be printed.

## Part 2: Simple chat platform
Already deployed [here](http://www-test.cs.umanitoba.ca/~wus2/chat.html).

The client side polls from the corresponding CGI every 100ms. It pools the whole chat history and send the whole thing back if something changed.

The CGI program creates a JSON file to store all the chat and a last modified time in the form of Unix epoch time. It sends the whole file out on a valid `GET` request, and overwrite the file on a valid `POST` request. 

### JSON
The JSON looks like this:
```
{
    "lastModified": 1595492515,
    "chatHistoryArray": [
        {
            "name": "Tommy",
            "message": "asdilufgas"
        },
        {
            "name": "Omar",
            "message": "fasdfasdadfgsdfas"
        }
    ]
}
```

### Known problem
Non-English character (especially Chinese and Japanese) will mess the JSON up. Normal English words and punctuation would work just fine. Delete the JSON file will bring it back to normal.

## Part 3: CrapPY web server
Run it with `python`:
```
python crapserver.py
```
Thanks to our MACLAB, which still running macOS High Sierra, it is Python 2 compatiable.

It can serve any file and CGI script with extension of `.cgi`.

It stays quite when waiting for connection. When a client trying to `GET` a certain page, it will get that page and send it back with the header. 

If a request cannot be understand, a `400` error page will be returned.
If a file if not found, a `404` error page will be returned.
if an exception is raised within the CGI program, a `500` error page will be returned.

It will also print out any handled execption.

## Configuration
Modify the value of `PORT` and `WWWROOT` in the beginning of the file.

### Known problems
It is capable to serve all the files provided in `web_files` folder. But it won't work or work well under following situation:

1. It cound not handle my CGI script from assignment 1, maybe caused by python 3 incompatibility or the hyper wierd FS mapping of MACLAB. It seems that it was stuggling to find itself. 

    But it works on my computer, using `python3` on macOS Catalina. Only minor modification is neede on the CGI script (change `/~wus2/cgi-bin/a.cgi` to just `/a.cgi`).

2. Extreme lag when if multiple (2+) client exitst, due to single threading.
