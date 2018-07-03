/*
    File: semaphore.H

    Author: R. Bettati
            Department of Computer Science
            Texas A&M University
    Date  : 08/02/11

*/

/*--------------------------------------------------------------------------*/
/* INCLUDES */
/*--------------------------------------------------------------------------*/

#include <pthread.h>
#include "semaphore.H"

/* -- CONSTRUCTOR/DESTRUCTOR */

using namespace std;

Semaphore::Semaphore(int _val) {
    pthread_mutex_init(&m, NULL);
	pthread_cond_init(&c, NULL);
    pthread_mutex_lock(&m);
    value = _val;
    pthread_mutex_unlock(&m);
}

Semaphore::Semaphore() {
	pthread_mutex_init(&m, NULL);
	pthread_cond_init(&c, NULL);
    pthread_mutex_lock(&m);
    value = 999;
    pthread_mutex_unlock(&m);
}

Semaphore::~Semaphore() {

}

/* -- SEMAPHORE OPERATIONS */

void Semaphore::setVal(int v) {
    pthread_mutex_lock(&m);
    value = v;
    pthread_mutex_unlock(&m);
}

int Semaphore::getVal() {
    return value;
}

int Semaphore::P() {
    pthread_mutex_lock(&m);
    value--;
    if (value < 0) {
        pthread_cond_wait(&c, &m);
    }
    pthread_mutex_unlock(&m);
}
int Semaphore::V() {
    pthread_mutex_lock(&m);
    value++;
    if (value <= 0) {
        pthread_cond_signal(&c);
    }
    pthread_mutex_unlock(&m);
}

