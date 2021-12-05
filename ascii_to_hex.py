#!/usr/bin/env python3
import optparse

def get_arguments():
		usage = "ascii_to_hex.py -t 'text'"
		parser = optparse.OptionParser(usage=usage)
		parser.add_option("-t", dest="text",help="The string that you want to convert")
		parser.add_option("-c" , dest="clear",help="clear from spaces",default="None")
		(options , arguments) = parser.parse_args()
		if not options.text :
			parser.error("[-] Please specify the string's vaule , or use --help for more info")
		return options

def converter(value):
	converted_string = value.encode('utf-8').hex()
	o = []
	while converted_string :
		o.append(converted_string[:2])
		converted_string = converted_string[2:]
	result = ""
	for i in o :
		result = result + i + " "
	return result

options = get_arguments()
if options.clear == "None" :
	print(converter(options.text))
else :
	result = converter(options.text)
	print(result.replace(" " , ""))