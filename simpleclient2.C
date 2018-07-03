#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>

#define PORT "3490"         // The port that the client connects to
#define MAXDATASIZE 100     // Max bytes we can get at once

// CLIENT CONNECTION ORDER:
// getaddrinfo()
// socket()
// connect()
// send()

int main() {
    int status, socketfd;
    struct addrinfo hints;
    struct addrinfo *servinfo;  // Will point to results
    char buf[MAXDATASIZE];      // Contain data recieved

    memset(&hints, 0, sizeof(hints));   // Make sure struct is empty
    hints.ai_family = AF_UNSPEC;        // Don't care IPv4 or IPv6
    hints.ai_socktype = SOCK_STREAM;     // TCP stream sockets
    hints.ai_flags = AI_PASSIVE;        // Assign the address of my local host

    // Get ready to connect
    status = getaddrinfo(NULL, "3490", &hints, &servinfo);
    // servinfo now points to a linked list of 1 or more addrinfo structs

    // Create a socket descriptor to use in later system calls
    socketfd = socket(servinfo->ai_family, servinfo->ai_socktype, servinfo->ai_protocol);

    // Connect to remote host
    connect(socketfd, servinfo->ai_addr, servinfo->ai_addrlen);

    freeaddrinfo(servinfo); // free the linked-list

    // Create and send a message
    char *msg = "This is a message from the client";
    int len, bytes_sent;
    len = strlen(msg);
    bytes_sent = send(socketfd, msg, len, 0);
    printf("Sent a message to the server\n");

    // Recieve a message
    int numbytes;
    numbytes = recv(socketfd, buf, MAXDATASIZE-1, 0);
    buf[numbytes] = '\0';
    printf("Client recieved: %s\n", buf);

    close(socketfd);
}