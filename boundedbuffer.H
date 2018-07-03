#include <queue>
#include "semaphore.H"
#include <string>
#include <stdio.h>

using namespace std;

class BoundedBuffer {

private:
    queue<string> buf;
    Semaphore m;    // Mutex
    Semaphore full;
    Semaphore empty;

public:
    BoundedBuffer(int s);

    void produce(string r);
    string consume();

};