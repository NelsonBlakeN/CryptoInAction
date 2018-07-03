#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

#define PORT 8080

using namespace std;

// SERVER CONNECTION ORDER:
// socket()
// bind()
// listen()
// accept()

int main() {
    // Create the socket that the server will listen on
    // AF_INET: Communication domain (IPv4)
    // SOCK_STREAM: Communication type (TCP)
    // Protocol: IP
    int socketfd = socket(AF_INET, SOCK_STREAM, 0);
    int accepted_socket;

    struct sockaddr_in address;             // Struct containing socket address information (IPv4)
    int addrlen = sizeof(address);
    address.sin_family = AF_INET;           // Address family (AF_INET)
    address.sin_port = htons(PORT);         // Port number
    address.sin_addr.s_addr = INADDR_ANY;   // Internet address

    // Bind socket to given address and port in "address"
    if(bind(socketfd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("Server failed to bind to port");
        exit(EXIT_FAILURE);
    }

    // Set server to passive mode, where it will wait for the
    // client to make a connection
    if(listen(socketfd, 3) < 0) {
        perror("Server failed to listen");
        exit(EXIT_FAILURE);
    }

    // Take the first connection request from a queue, create a
    // new socket file descriptor referring to the new connected socket.
    // Connection is now established, and data can be exchanged
    if((accepted_socket = accept(socketfd, (struct sockaddr*)&address, (socklen_t*)&addrlen)) < 0) {
        perror("Server failed to accept connection");
        exit(EXIT_FAILURE);
    }

    int numbytes;   // Number of bytes recieved from the client
    char buffer[1024] = {0};
    char* response = "This is a server response";           // Message sent by server
    numbytes = recv(accepted_socket, buffer, 1023, 0);      // Reading from the socket
    printf("%s\n", buffer);                                 // Printing the message
    send(accepted_socket, response, strlen(response), 0);   // Send a response
    printf("Server response sent\n");                       // Verification

    return 0;
}