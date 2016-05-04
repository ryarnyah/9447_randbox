from pwn import *
import string
import re

base = "0123456789abcdef"

def read_next():
    pr = r.readline()
    to_find = re.search('\'([0-9A-Za-z]+)\'', pr).group(1)
    print('To find %s' % (to_find))
    return to_find

def solve1():
    print("########## solve1")
    to_find = read_next()
    # envoi de la chaine simple
    r.sendline(base)
    print(r.readline())
    result = r.readline()
    print('Computed %s' % (result))

    to_send = ''
    idx = 0
    for c in to_find:
        to_send = to_send + base[result.find(c)]
    print(to_send)
    r.sendline(to_send)
    print(r.readline())
    print(r.readline())
    return (r.readline().find("You got it!") != -1)

def solve2():
    print("########## solve2")
    to_find = read_next()
    # envoi de la chaine simple
    r.sendline('0' * 16)
    print(r.readline())
    result = r.readline()

    to_send = ''
    idx = 0
    for c in to_find:
        to_sub = int(result[idx % 16], 16)
        to_send = to_send + format((int(c, 16) - to_sub) % 16, 'x')
        idx = idx + 1
    print(to_send)
    r.sendline(to_send)
    print(r.readline())
    print(r.readline())
    return (r.readline().find("You got it!") != -1)

def solve5():
    print("########## solve5")
    to_find = read_next()
    # envoi de la chaine simple
    r.sendline(to_find)
    print(r.readline())
    result = r.readline()
    print('Computed %s' % (result))
    # Recher decalage
    to_strip = result.find(to_find[:2])
    print('To strip %s' % (to_strip))
    to_send = to_find[to_strip:] + to_find[:to_strip]
    print(to_send)
    r.sendline(to_send)
    print(r.readline())
    print(r.readline())
    return (r.readline().find("You got it!") != -1)

def solve7():
    print("########## solve7")
    to_find = read_next()
    # envoi de la chaine simple
    r.sendline('0')
    print(r.readline())
    result = r.readline()[0]

    to_send = ''
    for c in to_find:
        to_add = format(int(c, 16) ^ int(result, 16), 'x')
        result = to_add
        to_send += to_add
    print(to_send)
    r.sendline(to_send)
    print(r.readline())
    print(r.readline())
    return (r.readline().find("You got it!") != -1)

def solve8():
    print("########## solve7")
    to_find = read_next()
    # envoi de la chaine simple
    r.sendline('0')
    print(r.readline())
    result = int(r.readline()[0], 16)

    to_send = ''
    for c in to_find:
        to_add = (int(c, 16) - result) % 16
        result = (result + to_add) % 16
        to_send += format(to_add, 'x')
    print(to_send)
    r.sendline(to_send)
    print(r.readline())
    print(r.readline())
    return (r.readline().find("You got it!") != -1)

def solve10():
    print("########## solve10")
    to_find = read_next()
    # envoi de la chaine simple
    r.sendline(to_find)
    print(r.readline())
    result = r.readline()

    to_send = ''
    for c in result:
        if c in "0123456789abcdef":
            to_send += c
    print('To send %s' % to_send)
    #r.interactive()

    r.sendline(to_send)
    print(r.readline())
    print(r.readline())
    return (r.readline().find("You got it!") != -1)

r = remote('192.168.99.100', 9447)
print(r.readline())
# Random select simple Challenge
# Challenge 1
solve1()
# Challenge 2
solve5()
# Challenge 3
solve1()
# Challenge 4
solve1()
# Challenge 5
solve1()
# Challenge 6
solve2()
# Begin hard rounds!Begin hard rounds!
print(r.readline())
# Random select hard Challenge
# Challenge 7
solve7()
# Challenge 8
solve8()
# Challenge 9
solve10()
# Challenge 10
solve7()
# 9447{crYpt0_m4y_n0T_Be_S0_haRD}
print('Flag is %s' % r.readline())
r.close()
