#include <stdio.h>

/*
    File: simpleclient.C

    Author: R. Bettati
            Department of Computer Science
            Texas A&M University
    Date  : 2012/07/11

    Simple client main program for MP2 in CSCE 313
*/

/*--------------------------------------------------------------------------*/
/* DEFINES */
/*--------------------------------------------------------------------------*/

    /* -- (none) -- */

/*--------------------------------------------------------------------------*/
/* INCLUDES */
/*--------------------------------------------------------------------------*/

#include <cassert>
#include <string.h>
#include <iostream>
#include <sstream>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <pthread.h>
#include <map>

#include <errno.h>
#include <unistd.h>

#include "NetworkRequestChannel.H"
#include "boundedbuffer.H"

using namespace std;

// Total number of request and worker threads
// TODO: These probabky only need to be set to 1
int reqThreadCount = 0;
int workThreadCount = 0;

// Mutex for atomic printing
pthread_mutex_t mprint;

/*--------------------------------------------------------------------------*/
/* LOCAL FUNCTIONS -- SUPPORT FUNCTIONS */
/*--------------------------------------------------------------------------*/

void print_time_diff(struct timeval * tp1, struct timeval * tp2) {
    /* Prints to stdout the difference, in seconds and museconds, between
       two timevals.
    */

    long sec = tp2->tv_sec - tp1->tv_sec;
    long musec = tp2->tv_usec - tp1->tv_usec;
    if (musec < 0) {
        musec += 1000000;
        sec--;
    }
    printf(" [sec = %ld, musec = %ld] ", sec, musec);

}

void atomicprint(string s) {
    pthread_mutex_lock(&mprint);
    cout << s << endl;
    pthread_mutex_unlock(&mprint);
}

// Convert integer to string
string int2string(int number) {
    stringstream ss;    // Create a stringstream
    ss << number;       // Add number to the stream
    return ss.str();    // Return a string with the contents of the stream
}

// Defines request thread (named rts)
typedef struct req_thread {
    int num;              // Number of requests (-n)
    BoundedBuffer* wbb;   // Worker bounded buffer: contains requests
    string name;          // Name of user

    req_thread(int m, BoundedBuffer* bb, string n) {
        num = m;
        wbb = bb;
        name = n;
    }
} rts;

// When started, a thread with this function will put the
// specified number of requests on the bounded buffer, to
// be read by the event thread.
// Lastly, it will send "DONE" to the buffer, so the worker
// knows that the thread is done.
// TODO: Change this from "name" to a given message to encrypt.
void* request_thread_func(void* args) {
    rts* r = (rts*)args;
    for(int i = 0; i < r->num; ++i) {
        string request = "data " + r->name;
        r->wbb->produce(request);
    }
    r->wbb->produce("DONE");
}

// Defines event thread (named ets)
typedef struct eventThread {
    BoundedBuffer* bb;
    map<string, BoundedBuffer*> stat_map;
    NetworkRequestChannel** reqChannelArray;

    eventThread(BoundedBuffer* b, map<string, BoundedBuffer*> m, NetworkRequestChannel** r) {
        bb = b;
        stat_map = m;
        reqChannelArray = r;
    }
} ets;

// Event thread function
// Single encompassing thread that handles thread tasks
void* event_handler_func(void* args) {
    map<int, string> fdToName;      // Notebook of file descriptors to their name
    ets* eventThread = (ets*) args; // Convert args to event thread struct
    fd_set readset;                 // Set of file descriptors (sockets)

    // Initialize set to zero
    FD_ZERO(&readset);

    // Initialize all file descriptors in readset to the fd (socket) of the channel
    int max_fd = 0;
    for(int i = 0; i < workThreadCount; ++i) {
        FD_SET(eventThread->reqChannelArray[i]->get_sock(), &readset);
        if(eventThread->reqChannelArray[i]->get_sock() > max_fd)
            max_fd = eventThread->reqChannelArray[i]->get_sock();
    }
    max_fd = max_fd + 1;

    // Initialize notebook (fdToName), channels
    // Check if the request from boundedBuffer is DONE, quit if so
    for(int i = 0; i < workThreadCount; ++i) {
        int x = eventThread->reqChannelArray[i]->get_sock();
        string request = eventThread->bb->consume();

        // Decrement request thread counter, don't store DONE
        while(request == "DONE") {
            reqThreadCount--;
            if(reqThreadCount == 0) {
                // No more request threads: send QUITs equal to num channels to bb
                for(int j = 0; j < workThreadCount; ++j) {
                    eventThread->bb->produce("quit");
                }
            }
            request = eventThread->bb->consume();
        }

        if(request == "quit") {
            workThreadCount--;
            // If worker counter is 0, send quit requests to stats threads and break
            if(workThreadCount==0) {
                for(auto x : eventThread->stat_map) {
                    x.second->produce("quit");
                }
                for(int j = 0; j < workThreadCount; ++j) {
                    eventThread->reqChannelArray[j]->send_request("quit");
                }
                break;
            }
        }
        eventThread->reqChannelArray[i]->cwrite(request);
        string name = request.substr(5);
        fdToName[x] = name;
    }
    int orig_wtc = workThreadCount;
    // Continuously read from channels, process reply
    while(true) {
        // Reset state
        FD_ZERO(&readset);
        for(int j = 0; j < orig_wtc; ++j) {
            FD_SET(eventThread->reqChannelArray[j]->get_sock(), &readset);
        }

        // Find a modified file descriptor
        select(max_fd, &readset, NULL, NULL, NULL);

        // Look for modified file descriptor based on ISSET flag in fd
        int i;  // Contains index of request channel that has a reply
        for(i = 0; i < orig_wtc; ++i) {
            if(FD_ISSET(eventThread->reqChannelArray[i]->get_sock(), &readset)) break;
        }
        // Pull new reply from channel
        string reply = eventThread->reqChannelArray[i]->cread();

        // Save the fd
        int chan_fd = eventThread->reqChannelArray[i]->get_sock();
        // Save the name of the person in the reply
        string name = fdToName[chan_fd];
        // Put the data reply on the stats bounded buffer for the histogram
        eventThread->stat_map[name]->produce(reply);
        // Get a new request
        string request = eventThread->bb->consume();

        // While request is "DONE," decrement req thread counter, get new reply
        while(request == "DONE") {
            reqThreadCount--;
            if(reqThreadCount == 0) {
                // If req thread counter == 0, send QUITs equal to num channels to bb
                for(int j = 0; j < orig_wtc; ++j) {
                    eventThread->bb->produce("quit");
                }
            }
            request = eventThread->bb->consume();
        }

        // When request == quit, decrement worker counter
        if(request == "quit") {
            workThreadCount--;
            // If worker counter is 0, send quit requests to stats threads
            // and break out of main loop
            if(workThreadCount==0) {
                for(auto x : eventThread->stat_map) {
                    x.second->produce("quit");
                }
                // Loop through reqChannelArray, cwrite (or send_request) "quit" for each
                for(int j = 0; j < orig_wtc; ++j) {
                    eventThread->reqChannelArray[j]->send_request("quit");
                }

                // End program
                break;
            }
        }
        else {
            fdToName[chan_fd] = request.substr(5);             // Change current channel to name on new request
            eventThread->reqChannelArray[i]->cwrite(request);  // Write the new request to the to the channel
        }
    }
}

// Define a statistics thread.
// TODO: change to be a decryption thread.
typedef struct stat_thread {
    vector<int>* hist;
    BoundedBuffer* sbb;

    stat_thread(vector<int>* h, BoundedBuffer* s) {
        hist = h;
        sbb = s;
    }
} sts;

// Function run by statistics thread
// TODO: (Probably) change this to decypt a message from the buffer.
void* stat_thread_func(void* args) {
    sts* stat_thread = (sts*)args;
    while(true) {
        string reply = stat_thread->sbb->consume();
        if(reply == "quit") {
            break;
        }
        else {
            int rep = atoi(reply.c_str());
            stat_thread->hist->at(rep/10)++;
        }
    }
}

/*--------------------------------------------------------------------------*/
/* MAIN FUNCTION */
/*--------------------------------------------------------------------------*/

int main(int argc, char * argv[]) {

    // pid_t pid = fork();
    // if(pid==0) {
    //     execv("./dataserver", NULL);
    //     return 0;
    // }

    int numRequests = 0;      // Number of data requests per person
    int buffSize    = 0;      // Size of bounded buffer between request and worker threads
    int numWorkers  = 0;      // Number of worker threads
    string host     = "";     // Name of server host
    int port        = 0;      // Port number of server host

    // Command line arguments
    for(int i = 1; i < argc; ++i) {
        if(strcmp(argv[i], "-n") == 0) {
            numRequests = atoi(argv[i+1]);
        }
        else if(strcmp(argv[i], "-b") == 0) {
            buffSize = atoi(argv[i+1]);
        }
        else if(strcmp(argv[i], "-w") == 0) {
            numWorkers = atoi(argv[i+1]);
            workThreadCount = numWorkers;
        }
        else if(strcmp(argv[i], "-h") == 0) {
            host = argv[i+1];
        }
        else if(strcmp(argv[i], "-p") == 0) {
            port = atoi(argv[i+1]);
        }
    }

    BoundedBuffer boundedBuffer(buffSize);

    // Generate request threads
    // Threads that send requests to the server
    // Pass in -n argument
    pthread_t joe_thread_r;
    rts joe_args_r(numRequests, &boundedBuffer, "Joe Smith");
    pthread_create(&joe_thread_r, NULL, request_thread_func, (void*)&joe_args_r);

    pthread_t john_thread_r;
    rts john_args_r(numRequests, &boundedBuffer, "John Doe");
    pthread_create(&john_thread_r, NULL, request_thread_func, (void*)&john_args_r);

    pthread_t jane_thread_r;
    rts jane_args_r(numRequests, &boundedBuffer, "Jane Smith");
    pthread_create(&jane_thread_r, NULL, request_thread_func, (void*)&jane_args_r);

    reqThreadCount = 3;

    // Generate statistics threads
    pthread_t joe_thread_s;
    BoundedBuffer joe_sbb(numRequests);
    vector<int> joe_hist(10);
    sts joe_args_s(&joe_hist, &joe_sbb);
    pthread_create(&joe_thread_s, NULL, stat_thread_func, (void*)&joe_args_s);

    pthread_t john_thread_s;
    BoundedBuffer john_sbb(numRequests);
    vector<int> john_hist(10);
    sts john_args_s(&john_hist, &john_sbb);
    pthread_create(&john_thread_s, NULL, stat_thread_func, (void*)&john_args_s);

    pthread_t jane_thread_s;
    BoundedBuffer jane_sbb(numRequests);
    vector<int> jane_hist(10);
    sts jane_args_s(&jane_hist, &jane_sbb);
    pthread_create(&jane_thread_s, NULL, stat_thread_func, (void*)&jane_args_s);

    // atomicprint("Establishing control channel... ");
    // NetworkRequestChannel chan("control", RequestChannel::CLIENT_SIDE);
    // atomicprint("done.");

    // Generate the single event thread, which holds all
    // of the request channels (sockets) that the requests are sent on.
    NetworkRequestChannel* reqChannelArray[workThreadCount];
    for(int i = 0; i < workThreadCount; ++i) {
    //     string reply = chan.send_request("newthread");
        reqChannelArray[i] = new NetworkRequestChannel(host, port);
    }
    pthread_t event_handler;
    map<string, BoundedBuffer*> stat_map;
    stat_map["Joe Smith"]  = &joe_sbb;
    stat_map["John Doe"]   = &john_sbb;
    stat_map["Jane Smith"] = &jane_sbb;
    ets e_thread_args(&boundedBuffer, stat_map, reqChannelArray);
    pthread_create(&event_handler, NULL, event_handler_func, (void*)&e_thread_args);

    pthread_join(joe_thread_s, NULL);
    pthread_join(john_thread_s, NULL);
    pthread_join(jane_thread_s, NULL);

    // chan.send_request("quit");

    cout << "=+=+=+= Printing Joe's Histogram" << endl;
    for(int i = 0; i < joe_hist.size(); ++i) {
        cout << "Bucket [" << i << "]: ";
        for(int j = 0; j < joe_hist[i]; ++j) {
            cout << "+";
        }
        cout << endl;
    }

    cout << "=+=+=+= Printing John's Histogram" << endl;
    for(int i = 0; i < john_hist.size(); ++i) {
        cout << "Bucket [" << i << "]: ";
        for(int j = 0; j < john_hist[i]; ++j) {
            cout << "+";
        }
        cout << endl;
    }

    cout << "=+=+=+= Printing Jane's Histogram" << endl;
    for(int i = 0; i < jane_hist.size(); ++i) {
        cout << "Bucket [" << i << "]: ";
        for(int j = 0; j < jane_hist[i]; ++j) {
            cout << "+";
        }
        cout << endl;
    }
}

// int main() {

//     printf("Creating a sample client\n");
//     NetworkRequestChannel client("127.0.0.1", 8080);

//     printf("Sending a request to the server\n");
//     client.send_request("data John Smith");

// }
