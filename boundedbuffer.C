#include "boundedbuffer.H"
#include "semaphore.H"
#include <iostream>

BoundedBuffer::BoundedBuffer(int sz) {
    full.setVal(sz);
    empty.setVal(0);
    m.setVal(1);
}

void BoundedBuffer::produce(string r) {
    full.P();
    m.P();
    buf.push(r);
    m.V();
    empty.V();
}

string BoundedBuffer::consume() {
    empty.P();
    m.P();
    string response = buf.front(); buf.pop();
    m.V();
    full.V();
    return response;
}
