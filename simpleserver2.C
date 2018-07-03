#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>

#define MYPORT "3490"   // Port that clients are connecting to
#define BACKLOG 10      // How many pending connections the queue will hold
#define MAXDATASIZE 100

// SERVER CONNECTION ORDER:
// socket()
// bind()
// listen()
// accept()

int main() {
    int status, socketfd, connected_sockfd;
    struct addrinfo hints;      // Information about address
    struct addrinfo *servinfo;  // Points to results
    struct sockaddr_storage client_addr;
    socklen_t addr_size;
    char buf[MAXDATASIZE];

    memset(&hints, 0, sizeof(hints));   // Make sure struct is empty
    hints.ai_family = AF_UNSPEC;        // Don't care IPv4 or IPv6
    hints.ai_socktype = SOCK_STREAM;    // TCP stream sockets
    hints.ai_flags = AI_PASSIVE;        // Assign the address of my local host

    if ((status = getaddrinfo(NULL, MYPORT, &hints, &servinfo)) != 0) {
        perror("Server failed to get address info");
    }
    // servinfo now points to a linked list of 1 or more addrinfo structs
    // Do things until you don't need servinfo anymore

    // Create a socket descriptor to use in later system calls
    socketfd = socket(servinfo->ai_family, servinfo->ai_socktype, servinfo->ai_protocol);

    // Associate that socket with a port on the machine
    bind(socketfd, servinfo->ai_addr, servinfo->ai_addrlen);

    freeaddrinfo(servinfo); // free the linked-list

    // Wait for incoming connections
    listen(socketfd, BACKLOG);

    // Client wants to connect() to the port being listen()ed to
    // Retreive pending connection
    // Returns new file descriptor to use for this single connection
    // (Original is waiting for more connections)
    addr_size = sizeof(client_addr);
    connected_sockfd = accept(socketfd, (struct sockaddr *)&client_addr, &addr_size);

    // Recieve a message
    int numbytes;
    numbytes = recv(connected_sockfd, buf, MAXDATASIZE-1, 0);
    buf[numbytes] = '\0';
    printf("Server recieved: %s\n");

    char* resp = "This is a response from the server";
    int len, bytes_sent;
    len = strlen(resp);
    bytes_sent = send(connected_sockfd, resp, len, 0);
    printf("Sent a response back to the client\n");

    close(connected_sockfd);
    close(socketfd);

}