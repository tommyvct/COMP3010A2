#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <assert.h>

#include <netdb.h> // For getaddrinfo
#include <unistd.h> // for close
#include <stdlib.h> // for exit

int main (int argc, char **argv)
{
    if (argc != 3 && (strcmp(argv[2], "yes") != 0 || strcmp(argv[2], "no") != 0))
    {
        printf("Bad format\nExample usage:\n%s Rick yes\n%s Morty no\n", argv[0], argv[0]);
        return 1;
    }


    int socket_desc;
    struct sockaddr_in server_addr;
    char server_message[2000], client_message[2000];
    char address[100];

    struct addrinfo *result;
    
    // Clean buffers:
    memset(server_message,'\0',sizeof(server_message));
    memset(client_message,'\0',sizeof(client_message));
    
    // Create socket:
    socket_desc = socket(AF_INET, SOCK_STREAM, 0);
    
    if(socket_desc < 0){
        printf("Unable to create socket\n");
        return -1;
    }
    
    printf("Socket created successfully\n");

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
    printf("Convert...\n");
    inet_ntop (server_addr.sin_family, &server_addr.sin_addr, address, 100);
    printf("Connecting to %s\n", address);
    // Send connection request to server:
    if(connect(socket_desc, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0){
        printf("Unable to connect\n");
        exit(EXIT_FAILURE);
    }
    printf("Connected with server successfully\n");
    

    char name[] = "idsjuafabfbadf";
    char response[] = "0";

    int post_request_length = 15 + (int) strlen(name);
    char post_request[post_request_length];
    memset(post_request, '\0', post_request_length);
    snprintf(post_request, post_request_length, "name=%s&accept=%s", name, response);
    
    int content_length_length = snprintf(NULL, 0, "%d", post_request_length) + 1;
    char content_length[content_length_length];
    memset(content_length, '\0', content_length_length);
    snprintf(content_length, content_length_length, "%d", post_request_length - 1);
    
    int request_length = 154 + (int) strlen(name);
    char request[request_length];
    memset(request, '\0', strlen(request));

    strcat(request, "POST /~wus2/cgi-bin/a.cgi HTTP/1.1\r\n");
    strcat(request, "Host: www-test.cs.umanitoba.ca\r\n");
    strcat(request, "Content-Length: ");
    strcat(request, content_length);
    strcat(request, "\r\n");
    strcat(request, "Content-Type: application/x-www-form-urlencoded\r\n\r\n");
    strcat(request, post_request);


    // printf("Sending:\n########################\n%s\n#######################\n", request);
    // Send the message to server:
    printf("Sending request, %lu bytes\n", strlen(request));
    if(send(socket_desc, request, strlen(request), 0) < 0){
        printf("Unable to send message\n");
        return -1;
    }
    
    // Receive the server's response:
    if(recv(socket_desc, server_message, sizeof(server_message), 0) < 0){
        printf("Error while receiving server's msg\n");
        return -1;
    }
    // Close the socket:
    close(socket_desc);
    
    assert(strstr(server_message, "200 OK") != NULL);
    
    printf("Server's response: %s\n",server_message);


    return 0;
}
