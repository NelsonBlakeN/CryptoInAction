#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

#define PORT 8080           // The port the client will be connecting to
#define MAXDATASIZE 1024    // Max number of bytes we can get at once

using namespace std;

// CLIENT CONNECTION ORDER:
// socket()
// connect()
// send()

int main() {
    struct sockaddr_in address;
    int sock = 0, numbytes;
    struct sockaddr_in server_addr;
    char request[32] = "This is a request from the client";
    char buffer[1024] = {0};

    // Create socket for client to communicate on
    if((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Client failed to create socket");
        exit(EXIT_FAILURE);
    }

    // Zero out memory of server address
    memset(&server_addr, '0', sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);

    // Convert IPv4 address from text to binary
    if(inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr) <= 0) {
        perror("Invalid address");
        exit(EXIT_FAILURE);
    }

    // Connect client to port on server
    if(connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Client failed to connect");
        exit(EXIT_FAILURE);
    }

    send(sock, request, strlen(request), 0);
    printf("Sent client request\n");
    numbytes = recv(sock, buffer, MAXDATASIZE-1, 0);
    printf("%s\n", buffer);
}