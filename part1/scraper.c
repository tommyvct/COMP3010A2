#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <assert.h>
#include <stdbool.h>
#include <ctype.h>

#include <netdb.h> // For getaddrinfo
#include <unistd.h> // for close
#include <stdlib.h> // for exit

///
/// @brief A test fuction to check if the server returned the thing we want.
///        It compares the result to check line by line, against a semi-hardcoded string.
/// @param toCheck string to check
/// @param name name of user
/// @param response response from user, either `"1"` for "yes", `"0"` for "no"
/// @return `true` if check passed, `false` if failed.
///         If `NDEBUG` is not defined(i.e. assersion is on), and a check failed, the function will be asserted instead.
bool check(char toCheck[], char* name, char* response)
{
    assert(toCheck);
    assert(name);
    assert(response);

    const char* CRLF = "\n";

    int nameCookieLength = 20 + strlen(name);
    char nameCookie[nameCookieLength];
    memset(nameCookie, '\0', nameCookieLength);
    strcat(nameCookie, "Set-Cookie: name=");
    strcat(nameCookie, name);
    strcat(nameCookie, "\r");

    char acceptCookie[24] = "Set-Cookie: accept=";
    strcat(acceptCookie, response);
    strcat(acceptCookie, "\r");

    int nameInputLength = 125+strlen(name);
    char nameInput[nameInputLength];
    memset(nameInput, '\0', nameInputLength);
    strcat(nameInput, "        <input type=\"text\" name=\"name\" pattern=\".*[a-zA-Z].*\" title=\"At least 1 English letter\" value=");
    strcat(nameInput, name);
    strcat(nameInput, " autofocus required>");

    char* accpet;
    char* decline;

    if (strcmp(response, "0") == 0)
    {
        accpet = "        <input type=\"radio\" name=\"accept\" value=\"1\" required > Accept";
        decline = "        <input type=\"radio\" name=\"accept\" value=\"0\" checked> Decline";
    }
    else if (strcmp(response, "1") == 0)
    {
        accpet = "        <input type=\"radio\" name=\"accept\" value=\"1\" required checked> Accept";
        decline = "        <input type=\"radio\" name=\"accept\" value=\"0\" > Decline";
    }
    else
    {
        assert(strcmp(response, "0") == 0);
        assert(strcmp(response, "1") == 0);
        return false;
    }

    assert(accpet);
    assert(decline);

    // reference have 25 lines
    const char* const REFERENCE[] = 
    {
        "HTTP/1.1 200 OK\r",
        // skip Date
        // skip Server
        nameCookie,
        acceptCookie,
        // skip transfer encoding
        "Content-Type: text/html; charset=UTF-8\r",
        // skip 3 lines
        "    <html>",
        "    <body>",
        "    <h1>You are Invited!</h1> ",
        "    details goes here",
        "    <br/><br/><br/>",
        "    <form action=\"/~wus2/cgi-bin/a.cgi\" method=\"POST\">",
        "        <label for=\"name\">Your name:</label>",
        nameInput,
        "        <br/>",
        "        <p2>Would you accept the invitation?</p2>",
        "        <br/>",
        accpet,
        decline,
        "        <br/>",
        "        <input type=\"submit\" value=\"Submit\">",
        "    </form>",
        "    <br/>",
        "        <form action=\"/~wus2/cgi-bin/a.cgi\" method=\"GET\">",
        "        <button name=\"Anonymize\" type=\"submit\">Anonymize</button>",
        "        </form>",
        "</body></html>",
    };
    
    #define skip     token = strtok(NULL, CRLF)
    #define refcmp(i) token = strtok(NULL, CRLF); /*printf("%d: %s &&  %s\n", i, token, REFERENCE[i]);*/ if (strcmp(token, REFERENCE[i]) != 0) {assert(strcmp(token, REFERENCE[i]) != 0); return false;}

    char* token = strtok(toCheck, CRLF);
    char* congrats;
    if (strcmp(token, REFERENCE[0]) != 0) {assert(strcmp(token, REFERENCE[0]) != 0); return false;}
    skip; // Date
    skip; // Server
    refcmp(1);
    refcmp(2);
    skip;
    refcmp(3);
    skip;
    skip;
    // skip;
    refcmp(4);
    refcmp(5);
    
    token = strtok(NULL, CRLF); // 12 
    if (strcmp(token, "<p style=\"color:green\">Your reply has been submitted!</p>") != 0 && 
        strcmp(token, "<p style=\"color:green\">Your reply has been updated!</p>") != 0)
    {
        //printf("congrat: %s \n", token);
        assert(strcmp(token, "<p style=\"color:green\">Your reply has been submitted!</p>") != 0 && 
                strcmp(token, "<p style=\"color:green\">Your reply has been updated!</p>") != 0);
        return false;
    }

    for (int i = 6; i <= 20; i++)
    {
        refcmp(i);
    }
    skip;
    refcmp(21);
    refcmp(22);
    refcmp(23);
    skip;
    refcmp(24);

    return true;
}

///
/// @brief A test fuction to check if the server returned the thing we want.
///        It compares the result to check line by line, against a semi-hardcoded string.
/// @param toCheck string to check
/// @param name name of user
/// @param response response from user, either `"1"` for "yes", `"0"` for "no"
/// @return `true` if check passed, `false` if failed.
///         If `NDEBUG` is not defined(i.e. assersion is on), and a check failed, the function will asserted instead.
bool check2(char toCheck[], char* name, char* response)
{
    assert(toCheck);
    assert(name);
    assert(response);

    const char* CRLF = "\n";

    int nameInputLength = 125+strlen(name);
    char nameInput[nameInputLength];
    memset(nameInput, '\0', nameInputLength);
    strcat(nameInput, "        <input type=\"text\" name=\"name\" pattern=\".*[a-zA-Z].*\" title=\"At least 1 English letter\" value=");
    strcat(nameInput, name);
    strcat(nameInput, " autofocus required>");

    char* accpet;
    char* decline;

    if (strcmp(response, "0") == 0)
    {
        accpet = "        <input type=\"radio\" name=\"accept\" value=\"1\" required > Accept";
        decline = "        <input type=\"radio\" name=\"accept\" value=\"0\" checked> Decline";
    }
    else if (strcmp(response, "1") == 0)
    {
        accpet = "        <input type=\"radio\" name=\"accept\" value=\"1\" required checked> Accept";
        decline = "        <input type=\"radio\" name=\"accept\" value=\"0\" > Decline";
    }
    else
    {
        assert(strcmp(response, "0") == 0);
        assert(strcmp(response, "1") == 0);
        return false;
    }

    assert(accpet);
    assert(decline);

    // reference have 24 lines
    const char* const REFERENCE[] = 
    {
        "HTTP/1.1 200 OK\r",
        // skip Date
        // skip Server
        // skip transfer encoding
        "Content-Type: text/html; charset=UTF-8\r",
        // skip 3 lines
        "    <html>",
        "    <body>",
        "<p style=\"color:green\">Thanks for replying. Here's your previous response.</p>",
        "    <h1>You are Invited!</h1> ",
        "    details goes here",
        "    <br/><br/><br/>",
        "    <form action=\"/~wus2/cgi-bin/a.cgi\" method=\"POST\">",
        "        <label for=\"name\">Your name:</label>",
        nameInput,
        "        <br/>",
        "        <p2>Would you accept the invitation?</p2>",
        "        <br/>",
        accpet,
        decline,
        "        <br/>",
        "        <input type=\"submit\" value=\"Submit\">",
        "    </form>",
        "    <br/>",
        "        <form action=\"/~wus2/cgi-bin/a.cgi\" method=\"GET\">",
        "        <button name=\"Anonymize\" type=\"submit\">Anonymize</button>",
        "        </form>",
        "</body></html>",
    };
    
    char* token = strtok(toCheck, CRLF);
    char* congrats;
    if (strcmp(token, REFERENCE[0]) != 0) {assert(strcmp(token, REFERENCE[0]) != 0); return false;}
    skip; // Date
    skip; // Server
    skip; // encoding
    refcmp(1);
    skip;
    skip;

    for (int i = 2; i <= 19; i++)
    {
        refcmp(i);
    }

    skip;
    refcmp(20);
    refcmp(21);
    refcmp(22);
    skip;
    refcmp(23);

    return true;
}

///
/// @brief Encapsulated web socket access.
/// @param request C-string holds the request
/// @param server_message out parameter, a C-string holds the response from server
/// @param server_message_length length of message to recevive
void sendNrequest(char* request, char* server_message, int server_message_length)
{
    int socket_desc;
    struct sockaddr_in server_addr;
    char address[100];

    struct addrinfo *result;
        
    // Create socket:
    socket_desc = socket(AF_INET, SOCK_STREAM, 0);
    
    if(socket_desc < 0){
        printf("Unable to create socket\n");
        exit(EXIT_FAILURE);
    }
    
    // printf("Socket created successfully\n");

    struct addrinfo hints;
    memset (&hints, 0, sizeof (hints));
    hints.ai_family = PF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags |= AI_CANONNAME;
    
    // get the ip of the page we want to scrape
    int out = getaddrinfo ("www-test.cs.umanitoba.ca", NULL, &hints, &result);
    // fail gracefully
    if (out != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(out));
        exit(EXIT_FAILURE);
    }
    
    // ai_addr is a struct sockaddr
    // so, we can just use that sin_addr
    struct sockaddr_in *serverDetails =  (struct sockaddr_in *)result->ai_addr;
    
    // Set port and IP the same as server-side:
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(80);
    //server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    server_addr.sin_addr = serverDetails->sin_addr;
    
    // converts to octets
    // printf("Convert...\n");
    inet_ntop (server_addr.sin_family, &server_addr.sin_addr, address, 100);
    // printf("Connecting to %s\n", address);
    // Send connection request to server:
    if(connect(socket_desc, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0){
        printf("Unable to connect\n");
        exit(EXIT_FAILURE);
    }
    // printf("Connected with server successfully\n");

    // printf("Sending:\n########################\n%s\n#######################\n", request);
    // Send the message to server:
    // printf("Sending request, %lu bytes\n", strlen(request));
    if(send(socket_desc, request, strlen(request), 0) < 0){
        printf("Unable to send message\n");
        exit(EXIT_FAILURE);
    }
    
    // Receive the server's response:
    if(recv(socket_desc, server_message, server_message_length, 0) < 0){
        printf("Error while receiving server's msg\n");
        exit(EXIT_FAILURE);
    }
    // Close the socket:
    close(socket_desc);
}


bool containsAlpha(const char s[])
{
    unsigned char c;

    for (int i = 0; i < strlen(s); i++)
    {
        if (isalpha(s[i]))
        {
            return true;
        }
    }
    return false;
}

int main (int argc, char **argv)
{
    if (argc != 3 || (strcmp(argv[2], "yes") != 0 && strcmp(argv[2], "no") != 0) || !containsAlpha(argv[1]))
    {
        printf("Bad format\nExample usage:\n%s Rick yes\n%s Morty no\n", argv[0], argv[0]);
        return 1;
    }


    // char name[] = "idsjuafabfbadf";
    // char response[] = "0";
    char* name = argv[1];
    char* response = (strcmp(argv[2], "yes") == 0 ? "1" : "0");

    // prepare post request payload string
    int post_request_length = 15 + (int) strlen(name);
    char post_request[post_request_length];
    memset(post_request, '\0', post_request_length);
    snprintf(post_request, post_request_length, "name=%s&accept=%s", name, response);
    
    // prepare content length number
    int content_length_length = snprintf(NULL, 0, "%d", post_request_length) + 1;
    char content_length[content_length_length];
    memset(content_length, '\0', content_length_length);
    snprintf(content_length, content_length_length, "%d", post_request_length - 1);
    
    // build the whole post request string
    int request_length = 154 + (int) strlen(name);
    char* request = calloc(request_length, sizeof(char));

    strcat(request, "POST /~wus2/cgi-bin/a.cgi HTTP/1.1\r\n");
    strcat(request, "Host: www-test.cs.umanitoba.ca\r\n");
    strcat(request, "Content-Length: ");
    strcat(request, content_length);
    strcat(request, "\r\n");
    strcat(request, "Content-Type: application/x-www-form-urlencoded\r\n\r\n");
    strcat(request, post_request);

    char* server_message = calloc(2000, sizeof(char));
    sendNrequest(request, server_message, 2000);
    // printf("Server's response:\n%s", server_message);
    if (!check(server_message, name, response))
    {
        printf("%s\n", "Test 1 failed.");
        free(request);
        free(server_message);
        return(2);
    }

    free(request);
    free(server_message);


    // prepare the GET request
    request_length = 95 + (int) strlen(name);
    request = calloc(request_length, sizeof(char));

    // prepare cookie string 
    int cookie_string_length = 24 + (int) strlen(name);
    char cookie_string[cookie_string_length];
    memset(cookie_string, '\0', cookie_string_length);
    snprintf(cookie_string, cookie_string_length, "Cookie: name=%s; accept=%s", name, response);

    // build the GET request string
    strcat(request, "GET /~wus2/cgi-bin/a.cgi HTTP/1.1\r\n");
    strcat(request, "Host: www-test.cs.umanitoba.ca\r\n");
    strcat(request, cookie_string);
    strcat(request, "\r\n\r\n");

    server_message = calloc(2000, sizeof(char));
    sendNrequest(request, server_message, 2000);
    // printf("Server's response:\n%s", server_message);
    if (!check2(server_message, name, response))
    {
        printf("%s\n", "Test 2 failed.");
        free(request);
        free(server_message);
        return(2);
    }

    free(request);
    free(server_message);

    printf("Success.\n");
    return 0;
}
