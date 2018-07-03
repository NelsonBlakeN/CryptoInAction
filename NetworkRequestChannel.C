#include "NetworkRequestChannel.H"

// Client side
NetworkRequestChannel::NetworkRequestChannel(const string _server_host_name, const unsigned short _port_no) {

    struct addrinfo hints, *serv_addr;
    int status;

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if((status = getaddrinfo(_server_host_name.c_str(), to_string(_port_no).c_str(), &hints, &serv_addr)) != 0) {
        perror("Client failed to get address info");
        exit(EXIT_FAILURE);
    }

    // Create a socket descriptor to use in later system calls
    if((socketfd = socket(serv_addr->ai_family, serv_addr->ai_socktype, serv_addr->ai_protocol)) < 0) {
        perror("Client failed to create socket");
        exit(EXIT_FAILURE);
    }

    // Connect client to port on server
    if(connect(socketfd, serv_addr->ai_addr, serv_addr->ai_addrlen) < 0) {
        perror("Client failed to connect");
        exit(EXIT_FAILURE);
    }
}

// Server side
NetworkRequestChannel::NetworkRequestChannel(const unsigned short _port_no, void * (*connection_handler) (void *), int backlog) {

    struct addrinfo hints, *serv_addr;
    int status;

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE;

    if((status = getaddrinfo(NULL, to_string(_port_no).c_str(), &hints, &serv_addr)) != 0) {
        perror("Server failed to get address info");
        exit(EXIT_FAILURE);
    }

    if((socketfd = socket(serv_addr->ai_family, serv_addr->ai_socktype, serv_addr->ai_protocol)) < 0) {
        perror("Server failed to create socket");
        exit(EXIT_FAILURE);
    }

    // Bind socket to given address and port
    if(bind(socketfd, serv_addr->ai_addr, serv_addr->ai_addrlen) < 0) {
        perror("Server failed to bind to port");
        exit(EXIT_FAILURE);
    }

    // Set the server to passive mode, where it will wait for the
    // client to make a connection
    if(listen(socketfd, backlog) < 0) {
        perror("Server failed while listening");
        exit(EXIT_FAILURE);
    }

    printf("Server was initialized successfully and is accepting request\n");

    struct sockaddr_storage their_addr;
    socklen_t addr_size;
    int connected_sockfd;
    while(true) {
        addr_size = sizeof(their_addr);
        connected_sockfd = accept(socketfd, (struct sockaddr*)&their_addr, (socklen_t*)&addr_size);
        printf("A connection was accepted on %i\n", connected_sockfd);
        if(connected_sockfd < 0) {
            perror("Server failed to accept connection");
            exit(EXIT_FAILURE);
        }
        NetworkRequestChannel* new_chan = new NetworkRequestChannel(connected_sockfd);
        pthread_t thread;
        pthread_create(&thread, NULL, connection_handler, new_chan);
        printf("A new thread was created for this process\n");
    }

    // Wait for incoming connections
}

NetworkRequestChannel::NetworkRequestChannel(int new_sock) {
    socketfd = new_sock;
}

NetworkRequestChannel::~NetworkRequestChannel() {
    close(socketfd);
}

string NetworkRequestChannel::send_request(string request) {
    cwrite(request);
    string resp = cread();
    return resp;
}

const int MAXMSG = 255;

string NetworkRequestChannel::cread() {
    char buffer[MAXMSG];
    int numbytes = recv(socketfd, buffer, MAXMSG, 0);
    if(numbytes < 0) {
        perror("Failed to read the request");
        return "quit";
    }
    if(numbytes == 0) {
        perror("Recv returned 0");
        return "quit";
    }
    buffer[numbytes] = '\0';
    string str = buffer;
    return str;
}

int NetworkRequestChannel::cwrite(string _msg) {
    int len;
    char s[MAXMSG];
    strcpy(s, _msg.c_str());
    int bytes_sent = send(socketfd, s, strlen(s)+1, 0);
    if(bytes_sent <= 0) {
        perror("Failed to send the request");
        exit(EXIT_FAILURE);
    }
    return bytes_sent;
}

int NetworkRequestChannel::get_sock() {
    return socketfd;
}