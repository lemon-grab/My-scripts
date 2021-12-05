#!/usr/bin/env python3

import optparse
from sys import argv
from termcolor import colored

def get_arguments():
   usage = "\npython3 caesar_decryptor.py -s <shift> \n or \n python3 caesar_decryptor.py (this will try them all)"
   parser = optparse.OptionParser(usage=usage)
   parser.add_option('-s' , "--shift" , dest="shift" , help="The shift cypher" , default="None")
   parser.add_option('-r',"--range", dest="range" , default="25")
   (options , arguments) = parser.parse_args()
   
   return options


def encrypt(text,s):
   result = ""
   # transverse the plain text
   for i in range(len(text)):
      char = text[i]      
      if (char.isupper()):
         result += chr((ord(char) + s-65) % 26 + 65)
      else:
         result += chr((ord(char) + s - 97) % 26 + 97)
   return result

def output(text,shift):
   print ("Plain Text : " + text)
   print ("Shift pattern : " + str(shift))
   print (colored("Cipher: " + str(encrypt(text,shift)),"red"))
   print(colored("---------------------------------------" , "grey"))

# Banner
print(colored("\n************************************************************************************", "green"))
print(colored(r"""██╗     ███████╗███╗   ███╗ ██████╗ ███╗   ██╗     ██████╗ ██████╗  █████╗ ██████╗ 
██║     ██╔════╝████╗ ████║██╔═══██╗████╗  ██║    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗
██║     █████╗  ██╔████╔██║██║   ██║██╔██╗ ██║    ██║  ███╗██████╔╝███████║██████╔╝
██║     ██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║    ██║   ██║██╔══██╗██╔══██║██╔══██╗
███████╗███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║    ╚██████╔╝██║  ██║██║  ██║██████╔╝
╚══════╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ """ , "red"))

print("\n* Copyright of Lemon Grab, 2021 *")
print(colored("\n************************************************************************************", "green"))

# Actual code
text = argv[1]
options = get_arguments()
shift = options.shift
# The final shift that you want the script to achive , by default its 25
theRange = int(options.range)

if shift == "None" :
   for i in range(1,theRange+1) :
      if i == 13 :
         print ("Plain Text : " + text)
         print (colored("Shift pattern : " + str(i),'green'))
         print (colored("Cipher: " + str(encrypt(text,i)),"green"))
         print(colored("---------------------------------------" , "grey"))
      else:   
       output(text,i)

if shift != "None" :
   shift = int(shift)
   output(text,shift)
   
