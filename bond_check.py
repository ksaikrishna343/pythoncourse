#!/bin/python

import sys
import re

try:
    file = open('/proc/net/bonding/bond0', 'r')
except IOError:
    print('Bonding file doesnot exist!')
    sys.exit()
        
def usage():
        print('''USAGE: %s [options] [bond_interface]
Options:
        --help, -h      This usage document
Arguments:
        bond_interface  The bonding interface to query, eg. 'bond0'. Default is 'bond0'.
''' % (sys.argv[0]))
        sys.exit(1)

# Parse arguments
try:
        iface = sys.argv[1]
        if iface in ('--help', '-h'):
                usage()
except IndexError:
        iface = 'bond0'

# Grab the inf0z from /proc
try:
        bond = open('/proc/net/bonding/%s' % iface).read()
except IOError:
        print("ERROR: Invalid interface {}".format(iface))
        usage()

# Parse and output
active = 'NONE'
Link = 'NONE'
slaves = ''
state = 'OK'
links = ''
bond_status = ''
for line in bond.splitlines():
        i = re.match('^Currently Active Slave: (.*)', line)
        if i:
                active = i.groups()[0]

        i = re.match('^Slave Interface: (.*)', line)
        if i:
                s = i.groups()[0]
                slaves += ', %s' % s

#        i = re.match('^Link Failure Count: (.*)', line)
#        if i:
#                l = i.groups()[0]
#                links += ', %s' % l

        i = re.match('^MII Status: (.*)', line)
        if i:
                s = i.groups()[0]
                if slaves == '':
                        bond_status = s
                else:
                        slaves += ' %s' % s
                if s != 'up':
                        state = 'FAULT'

print("%s: %s (%s), Active Slave: %s, PriSlave: %s (%s), SecSlave: %s (%s)"  % (iface, state, bond_status, active, slaves.split(',')[1].split()[0], slaves.split(',')[1].split()[1], slaves.split(',')[2].split()[0], slaves.split(',')[2].split()[1]))

#bond0: OK (up), Active Slave: enp0s10, PriSlave: enp0s10 (up), SecSlave: enp0s9 (up)
