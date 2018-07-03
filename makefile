# makefile

all: dataserver client

semaphore.o: semaphore.H semaphore.C
	g++ -c -g semaphore.C

NetworkRequestChannel.o: NetworkRequestChannel.H NetworkRequestChannel.C
	g++ -c -g NetworkRequestChannel.C

boundedbuffer.o: boundedbuffer.H boundedbuffer.C semaphore.o
	g++ -c -g boundedbuffer.C

dataserver: dataserver.C NetworkRequestChannel.o
	g++ -g -o dataserver dataserver.C NetworkRequestChannel.o -lpthread

client: client.C NetworkRequestChannel.o NetworkRequestChannel.o boundedbuffer.o semaphore.o
	g++ -g -o client client.C NetworkRequestChannel.o boundedbuffer.o semaphore.o -lpthread

clean:
	rm *.o fifo* client server
