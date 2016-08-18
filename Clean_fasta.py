# -*- coding: utf-8 -*-
"""
@author: Yannick NAMOUR
@date  : 08/2016

Formatting of a fasta file without blank lines, without duplicate entries,
and with sequences on a single line.

IN  : file.fasta
OUT : file.fasta

COMMANDE TYPE : python Clean_fasta.py old_name.fasta new_name.fasta

"""
#import
from __future__ import print_function
import sys
import os
#
import logging
logging.basicConfig(filename='log_Clean_fasta.txt', \
    format="%(asctime)s -- %(name)s -- %(levelname)s:%(message)s'", \
    level=logging.DEBUG)
#
import argparse
PARSING = argparse.ArgumentParser(description="Formatting of a fasta file \
    without blank lines, without duplicate entries and with sequences on a \
    single line.", epilog="Release of 16 AUG 2016")
PARSING.add_argument("old_file", help="file to transform")
PARSING.add_argument("new_file", help="name of the new file")
PARSING.add_argument('-d', action="store_true", default=False, \
    help="display the names and sequences in console")
PARSING.add_argument('-n', action="store", type=int, \
    help="expected number of sequences")
PARSING.add_argument("--version", action='version', version="%(prog)s 1.0")
ARGUMENTS = PARSING.parse_args()
#import
#
print ("START Cleanfasta.py on", ARGUMENTS.old_file, file=sys.stdout)
print (os.uname(), file=sys.stdout)
print ("---------------------------------------", file=sys.stdout)
logging.debug(os.uname())
logging.debug("START Cleanfasta.py on %s", ARGUMENTS.old_file)
#
#start reading the file
with open(ARGUMENTS.old_file, "r") as fichier_lu:
    CONTENU = fichier_lu.readlines()
#end reading the file
#
#start transformation
DICTIONARY = {}
HEAD = ""
SEQ = ""
FINAL_LINE = 0
SIZE = len(CONTENU)
DELETED = False
#
for elt in CONTENU:
    LINE = elt.rstrip("\n\r\t ") #clean the ends of lines
    #
    FINAL_LINE += 1 #check if that's the final line
    #
    if LINE.startswith(">") or FINAL_LINE == SIZE:
        if HEAD != "": #delete empty header
            if FINAL_LINE == SIZE and not LINE.startswith(">"):
                SEQ += LINE
            if SEQ != "": #delete empty sequence
                if HEAD not in DICTIONARY: #filtration of the duplicate entries
                    DICTIONARY[HEAD] = SEQ #filling of the dictionary
                else:
                    DELETED = True
                    print ("**********DUPLICATE ENTRY :", HEAD, \
                        file=sys.stderr)
                    logging.debug("duplicate entry")

                if ARGUMENTS.d: #display in console
                    if DELETED:
                        print ("**********DUPLICATE ENTRY : next sequence deleted", \
                            file=sys.stdout)
                    print (">"+HEAD, file=sys.stdout)
                    print (SEQ[0:25], "<- start ", " end->", SEQ[-25:], \
                        file=sys.stdout)
                    print (len(SEQ), "bases or amino acids", file=sys.stdout)
                    print ("---------------------------------------", \
                        file=sys.stdout)
            HEAD = ""
            SEQ = ""
            DELETED = False
        HEAD = LINE[1:]
    else:
        if LINE != "":
            SEQ += LINE
    del elt
#
print ("identified sequences :", len(DICTIONARY), file=sys.stdout)
logging.debug("identified sequences : %s", len(DICTIONARY))
if ARGUMENTS.n: #check the number of sequences
    if ARGUMENTS.n == len(DICTIONARY):
        print ("-n the expected number of sequences is correct :", ARGUMENTS.n, \
            file=sys.stdout)
    else:
        print ("-n the expected number of sequences is wrong :", ARGUMENTS.n, \
            file=sys.stdout)
        print ("**********ERROR**********", file=sys.stderr)
        print ("-n the expected number of sequences is wrong :", ARGUMENTS.n, \
            file=sys.stderr)
        print ("please try to check or modify the initial file", file=sys.stderr)
        print ("**********ERROR**********", file=sys.stderr)
        logging.debug("-n the expected number of sequences is wrong")
del HEAD, SEQ, LINE, CONTENU, SIZE, FINAL_LINE
#end transformation
#
#start writing the final file
FINAL_FILE = open(ARGUMENTS.new_file, "w") #final file
#
NB_SEQ = 0
#
for c, v in DICTIONARY.items():
    NB_SEQ += 1
    if NB_SEQ != len(DICTIONARY):
        FINAL_FILE.write(">"+c+"\n"+v+"\n")
    else:
        FINAL_FILE.write(">"+c+"\n"+v)
    del c, v
#
FINAL_FILE.close()
#
print ("file created :", ARGUMENTS.new_file, file=sys.stdout)
logging.debug("file created : %s", ARGUMENTS.new_file)
del DICTIONARY, NB_SEQ
#end writing the final file.
#
print ("---------------------------------------", file=sys.stdout)
print ("END Cleanfasta.py on", ARGUMENTS.old_file, file=sys.stdout)
logging.debug("END Clean_fasta.py on %s", ARGUMENTS.old_file)
logging.debug("---------------------------------------")
