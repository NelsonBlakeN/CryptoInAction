#include <string>
#include <cstring>
#include <sstream>
#include <sys/stat.h>
#include "NetworkRequestChannel.H"

using namespace std;

string int2string(int number) {
    stringstream ss;
    ss << number;
    return ss.str();
}

void process_hello(NetworkRequestChannel & _channel, const string & _request) {
    _channel.cwrite("Hello to you too!");
}

void process_data(NetworkRequestChannel & _channel, const string & _request) {
    usleep(1000 + (rand() % 5000));

    _channel.cwrite(int2string(rand() % 100));
}

void process_request(NetworkRequestChannel & _channel, const string & _request) {
    if(_request.compare(0, 4, "data") == 0) {
        process_data(_channel, _request);
    }
    else if(_request.compare(0, 5, "hello") == 0) {
        process_hello(_channel, _request);
    }
    else {
        _channel.cwrite("unknown request");
    }
}

void* connection_handler(void* args) {
    NetworkRequestChannel nrc = *(NetworkRequestChannel*) args;
    while(true) {
        string request = nrc.cread();

        if(request.compare("quit") == 0) {
            nrc.cwrite("bye");
            usleep(10000);      // Give the other end a bit of time.
            break;              // Break out of the loop.
        }

        process_request(nrc, request);
    }
}

int main(int argc, char * argv[]) {
    int b = 0;      // Size of backlog
    int p = 0;      // Port number of server host

    // Command line arguments
    for(int i = 1; i < argc; ++i) {
        if(strcmp(argv[i], "-b") == 0) {
            b = atoi(argv[i+1]);
        }
        else if(strcmp(argv[i], "-p") == 0) {
            p = atoi(argv[i+1]);
        }
    }
    NetworkRequestChannel server(p, connection_handler, b);

}