#!/usr/bin/python

import base64, SocketServer, sys
import binascii
import hashlib
import os
from signal import SIGTERM, SIGCHLD, signal, alarm
import random

def conv(l):
	return int(l, 16);

def back(l):
	return hex(l)[2:];

def xor(s, r):
	xorW = r % 16;
	res = "";
	for i in s:
		res += back(conv(i) ^ xorW)
	return res;

def add(s, r):
	addW = r % 16;
	res = "";
	for i in s:
		res += back((conv(i) + addW) % 16);
	return res;

def perm(s, r):
	res = "";
	for i in xrange(len(s)):
		res += s[(i + r) % len(s)];
	return res;

def arthSeq(s, r):
	res = "";
	j = 1;
	for i in s:
		res += back((conv(i) + r * j) % 16);
		j += 1
	return res;

def preXor(s, r):
	res = "";
	p = back(r % 16);
	for i in s:
		res += back((conv(i) ^ conv(p)));
		p = i;
	return res;

def sumPre(s, r):
	res = "";
	totalS = r % 16;
	for i in s:
		totalS += conv(i);
		res += back(totalS % 16);
	return res;

def swapXor(s, r):
	res = "";
	xorW = r % 16;
	for i in xrange(0, len(s), 2):
		if i + 1 < len(s):
			res += back(conv(s[i + 1]) ^ xorW) + back(conv(s[i]) ^ xorW);
		else:
			res += back(conv(s[i]) ^ xorW);
	return res;

def valid(s):
	if len(s) > 64:
		return False;
	for i in s:
		if not i in "0123456789abcdef":
			return False;
	return True;

FLAG = ""

def randStr(b):
	return binascii.hexlify(os.urandom(b));

class ServerHandler(SocketServer.BaseRequestHandler):

	def read_until(self, end):
		s = ''
		while not s.endswith(end):
			t = self.request.recv(1)
			if not t:
				return s;
			s += t;
		return s

	def fail(self, message):
		self.request.sendall(message + "\n");
		self.request.close();

	def handle(self):
		alarm(300);
		self.request.sendall("Alphabet is '0123456789abcdef', max len is 64\n");
		posFuncs1 = [xor, xor, add, add, arthSeq, perm];
		random.shuffle(posFuncs1);
		posFuncs2 = [preXor, sumPre, swapXor, preXor];
		random.shuffle(posFuncs2);
		posFuncs = posFuncs1 + posFuncs2;
		triesDone = 0;
		maxTries = 21;
		maxRounds = len(posFuncs);
		for i in xrange(len(posFuncs)):
			need = randStr(16);
			randVal = ord(os.urandom(1));
			func = posFuncs[i];
			encry = func(need, randVal);
			if i == len(posFuncs1):
				self.request.sendall("Begin hard rounds!\n");
			self.request.sendall("You need to send a string that encrypts to '" + encry + "'\n");
			gotIt = False;
			while not gotIt:
				if triesDone >= maxTries:
					self.request.sendall("Too many tries\n");
					self.request.close();
					return;
				self.request.sendall("Guess " + str(triesDone) + "/" + str(maxTries) + " (Round " + str(i + 1) + "/" + str(maxRounds) + ")\n");
				got = self.read_until("\n")[:-1];
				triesDone += 1;
				if not valid(got):
					self.request.sendall("Invalid characters or length\n");
					self.request.close();
					return;
				res = func(got, randVal);
				self.request.sendall(res + "\n");
				if res == encry:
					self.request.sendall("You got it!\n");
					gotIt = True;
		self.request.sendall(FLAG + "\n");
		self.request.close();

class ThreadedServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
	pass;

if __name__ == "__main__":
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])

	FLAG = open('flag.txt', 'r').read()
	server = ThreadedServer((HOST, PORT), ServerHandler)
	server.allow_reuse_address = True
	server.serve_forever()
