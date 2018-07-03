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

int rtc = 0;
int wtc = 0;
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

string int2string(int number) {
    stringstream ss;    //create a stringstream
    ss << number;       //add number to the stream
    return ss.str();    //return a string with the contents of the stream
}

typedef struct req_thread {
    int num;              // Number of requests   // -n
    BoundedBuffer* wbb;   // Contains requests
    string name;          // Name of user

    req_thread(int m, BoundedBuffer* bb, string n) {
        num = m;
        wbb = bb;
        name = n;
    }
} rts;

void* request_thread_func(void* args) {
    rts* r = (rts*)args;
    for(int i = 0; i < r->num; ++i) {
        string request = "data " + r->name;
        r->wbb->produce(request);
    }
    r->wbb->produce("DONE");
}

typedef struct event_thread {
    BoundedBuffer* bb;
    map<string, BoundedBuffer*> stat_map;
    NetworkRequestChannel** RCA;

    event_thread(BoundedBuffer* b, map<string, BoundedBuffer*> m, NetworkRequestChannel** r) {
        bb = b;
        stat_map = m;
        RCA = r;
    }
} ets;

void* event_handler_func(void* args) {
    map<int, string> fd_to_name;        // Notebook of file descriptors to their name
    ets* event_thread = (ets*) args;
    fd_set readset;

    // Initialize set to zero
    FD_ZERO(&readset);

    // Initialize all file descriptors to the fd of the channel
    int max_fd = 0;
    for(int i = 0; i < wtc; ++i) {
        FD_SET(event_thread->RCA[i]->get_sock(), &readset);
        if(event_thread->RCA[i]->get_sock() > max_fd)
            max_fd = event_thread->RCA[i]->get_sock();
    }
    max_fd = max_fd + 1;

    // Initialize notebook (fd_to_name), channels
    // Check if the request from bb is DONE, quit
    // If DONE: (in while loop) decrement request thread counter, don't place in book
    for(int i = 0; i < wtc; ++i) {
        int x = event_thread->RCA[i]->get_sock();
        string request = event_thread->bb->consume();
        while(request == "DONE") {
            rtc--;
            if(rtc == 0) {
                // If req thread counter == 0, send QUITs equal to num channels to bb
                for(int j = 0; j < wtc; ++j) {
                    event_thread->bb->produce("quit");
                }
            }
            request = event_thread->bb->consume();
        }
        if(request == "quit") {
            wtc--;
            // If worker counter is 0, send quit requests to stats threads and break
            if(wtc==0) {
                for(auto x : event_thread->stat_map) {
                    x.second->produce("quit");
                }
                for(int j = 0; j < wtc; ++j) {
                    event_thread->RCA[j]->send_request("quit");
                }
                break;
            }
        }
        event_thread->RCA[i]->cwrite(request);
        string name = request.substr(5);
        fd_to_name[x] = name;
    }
    int orig_wtc = wtc;
    // Continuously read from channels, process reply
    while(true) {
        // Reset state
        FD_ZERO(&readset);
        for(int j = 0; j < orig_wtc; ++j) {
            FD_SET(event_thread->RCA[j]->get_sock(), &readset);
        }

        // Find a modified file descriptor
        select(max_fd, &readset, NULL, NULL, NULL);

        // Look for modified file descriptor based on ISSET flag in fd
        int i;
        for(i = 0; i < orig_wtc; ++i) {
            if(FD_ISSET(event_thread->RCA[i]->get_sock(), &readset)) break;
        }
        // Pull new reply from channel
        string reply = event_thread->RCA[i]->cread();

        // Save the fd
        int chan_fd = event_thread->RCA[i]->get_sock();
        // Save the name of the person in the reply
        string name = fd_to_name[chan_fd];
        // Put the data reply on the stats bounded buffer for the histogram
        event_thread->stat_map[name]->produce(reply);
        // Get a new request
        string request = event_thread->bb->consume();

        // While request is "DONE," decrement req thread counter, get new reply
        while(request == "DONE") {
            rtc--;
            if(rtc == 0) {
                // If req thread counter == 0, send QUITs equal to num channels to bb
                for(int j = 0; j < orig_wtc; ++j) {
                    event_thread->bb->produce("quit");
                }
            }
            request = event_thread->bb->consume();
        }

        // When request == quit, decrement worker counter
        if(request == "quit") {
            wtc--;
            // If worker counter is 0, send quit requests to stats threads
            // and break out of main loop
            if(wtc==0) {
                for(auto x : event_thread->stat_map) {
                    x.second->produce("quit");
                }
                // Loop through RCA, cwrite (or send_request) "quit" for each
                for(int j = 0; j < orig_wtc; ++j) {
                    event_thread->RCA[j]->send_request("quit");
                }
                break;
            }
        }
        else {
            // Change current channel to name on new request
            fd_to_name[chan_fd] = request.substr(5);
            // Write the new request to the to the channel
            event_thread->RCA[i]->cwrite(request);
        }
    }
}

typedef struct stat_thread {
    vector<int>* hist;
    BoundedBuffer* sbb;

    stat_thread(vector<int>* h, BoundedBuffer* s) {
        hist = h;
        sbb = s;
    }
} sts;

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

    int n = 0;      // Number of data requests per person
    int b = 0;      // Size  of bounded buffer between request and worker threads
    int w = 0;      // Number of worker threads
    string h = "";  // Name of server host
    int p = 0;      // Port number of server host

    // Command line arguments
    for(int i = 1; i < argc; ++i) {
        if(strcmp(argv[i], "-n") == 0) {
            n = atoi(argv[i+1]);
        }
        else if(strcmp(argv[i], "-b") == 0) {
            b = atoi(argv[i+1]);
        }
        else if(strcmp(argv[i], "-w") == 0) {
            w = atoi(argv[i+1]);
            wtc = w;
        }
        else if(strcmp(argv[i], "-h") == 0) {
            h = argv[i+1];
        }
        else if(strcmp(argv[i], "-p") == 0) {
            p = atoi(argv[i+1]);
        }
    }

    BoundedBuffer bb(b);

    struct timeval begin;
    struct timeval end;

    gettimeofday(&begin, 0);

    // Generate request threads
    // Pass in -n argument
    pthread_t joe_thread_r;
    rts joe_args_r(n, &bb, "Joe Smith");
    pthread_create(&joe_thread_r, NULL, request_thread_func, (void*)&joe_args_r);

    pthread_t john_thread_r;
    rts john_args_r(n, &bb, "John Doe");
    pthread_create(&john_thread_r, NULL, request_thread_func, (void*)&john_args_r);

    pthread_t jane_thread_r;
    rts jane_args_r(n, &bb, "Jane Smith");
    pthread_create(&jane_thread_r, NULL, request_thread_func, (void*)&jane_args_r);

    rtc = 3;

    // Generate statistics threads
    pthread_t joe_thread_s;
    BoundedBuffer joe_sbb(n);
    vector<int> joe_hist(10);
    sts joe_args_s(&joe_hist, &joe_sbb);
    pthread_create(&joe_thread_s, NULL, stat_thread_func, (void*)&joe_args_s);

    pthread_t john_thread_s;
    BoundedBuffer john_sbb(n);
    vector<int> john_hist(10);
    sts john_args_s(&john_hist, &john_sbb);
    pthread_create(&john_thread_s, NULL, stat_thread_func, (void*)&john_args_s);

    pthread_t jane_thread_s;
    BoundedBuffer jane_sbb(n);
    vector<int> jane_hist(10);
    sts jane_args_s(&jane_hist, &jane_sbb);
    pthread_create(&jane_thread_s, NULL, stat_thread_func, (void*)&jane_args_s);

    // atomicprint("Establishing control channel... ");
    // NetworkRequestChannel chan("control", RequestChannel::CLIENT_SIDE);
    // atomicprint("done.");

    NetworkRequestChannel* RCA[wtc];
    for(int i = 0; i < wtc; ++i) {
    //     string reply = chan.send_request("newthread");
        RCA[i] = new NetworkRequestChannel(h, p);
    }
    pthread_t event_handler;
    map<string, BoundedBuffer*> stat_map;
    stat_map["Joe Smith"]  = &joe_sbb;
    stat_map["John Doe"]   = &john_sbb;
    stat_map["Jane Smith"] = &jane_sbb;
    ets e_thread_args(&bb, stat_map, RCA);
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
