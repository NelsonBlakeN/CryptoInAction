# Cryptography In Action

## Description
This repository contains the code base for the final project in CSCE 465 - Computer Network and Security with Abner Mendoza.

The purpose of this project is to demonstrate implementations of various encryption methods, both public and private key, by sending messages over a public TCP socket. This project will also sniff and attempt to decode these messages in a man-in-the-middle style attack.

## Algorithms
Below are the algorithms that (potentially) are included in this project:

* RSA Encryption
* Diffie-Hellman Key Exchange
* AES-128
* DES
* One Time Pad
* El Gamal Encryption
* RSA Signatures
* El Gamal signatures
* DSA

## Main Function
1. A connection is set up between client and server, and possibly a public key is exchanged.
2. A message is created and encrypted using one of the above methods (RSA, AES, OTP, etc)
3. The encrypted message is signed, using any given signature algorithm
4. This message is recieved by the target, verified, decrypted, and read.

### Secondary Features
* Either a malicious server intercepts the data (client sends to eve first), or packet sniffer intercepts and tries to read message off the wire.
* Time and plot brute force decryption attempts using known breaking algorithms (Shank's, Pohlig Hellman, p-1 factoring)
