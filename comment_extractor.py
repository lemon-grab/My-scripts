import sys, getopt
import urllib
import urllib2
from bs4 import BeautifulSoup
from bs4 import Comment
from pyfiglet import Figlet
import re
import time
import os
from time import sleep
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse



print("\n\n")
# DEAULT values
urlFlag = 0
outputFlag = 0
recursive_flag = 0
# GET ALL ARFUMENTS
arguments = sys.argv
# SAVE ALL ARGUMENTS EXCEPT FOR FIRST WHICH IS SCRIPT name
arguments_list = arguments[1:]

# DEFINING WHICH SWITCH ARE VALID AND WHICH ARE NOT FOR getopt
short_options = "hu:vor"
long_options = ["help","url=","verbose","output"]

try:
    arguments, values = getopt.getopt(arguments_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)

# Evaluate given options
for current_argument, current_value in arguments:
    if current_argument in ("-v", "--verbose"):
        print ("Enabling verbose mode")
        verboseFlag = 1
    elif current_argument in ("-h", "--help"):
        print ("comment_parser.py -u [url]\n")
        print ("comment_parser.py -u [url] -o --> File will be saved as urlName[comments].txt\n")
        print ("comment_parser.py -u [url] --output\n")
        print ("comment_parser.py --url=[url]")
        print (" -r for recursive i.e extract all links from url and from all links it will extract comment. currently only level1 is supported")
        print ("If -r is not used then comments of url is only extracted")
    elif current_argument in ("-u", "--url"):
        urlFlag = 1
        url = current_value
        #striping http and https to make it as a filename
        folderName = re.compile(r"https?://(www\.)?")
        folderName=folderName.sub('', url).strip().strip('/')
    elif current_argument in ("-o", "--output"):
        outputFlag = 1
    elif current_argument in ("-r"):
        recursive_flag = 1


if urlFlag == 1:
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    # print(the_page)
    soup = BeautifulSoup(the_page,'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    all_a_tags = soup.find_all('a')
    all_links = []
    if recursive_flag == 1:
        for links in all_a_tags:
            print(links.get('href'))
            all_links.append(links.get('href'))

        for rec_links in all_links:

            try:
                parsed_url = urlparse(rec_links)
                if parsed_url.netloc == '' and parsed_url.path != '':
                    rec_links = url+rec_links
                print('[ + ] URL: '+ rec_links+ ' -------')
                rec_req = urllib2.Request(rec_links, headers=headers)
                rec_response = urllib2.urlopen(rec_req)
                rec_the_page = rec_response.read()
                # print(the_page)
                rec_soup = BeautifulSoup(rec_the_page,'html.parser')
                rec_comments = rec_soup.find_all(string=lambda text: isinstance(text, Comment))

                rec_fileName = re.compile(r"https?://(www\.)?")
                rec_fileName=rec_fileName.sub('', rec_links).strip().strip('/')
                #replacing slash because it is not allowed in file name
                rec_fileName = rec_fileName.replace('/','|')


                for c in rec_comments:
                    if outputFlag == 1:
                        try:
                            os.mkdir(folderName)
                            # os.cd(folderName)
                                #f = open(filepath, "a")
                        except OSError:
                            print ("Creation of the directory failed")

                        with open(folderName+'/'+rec_fileName+"[comments].txt","a+") as file_object:
                            file_object.seek(0)
                            data = file_object.read(100)
                            if len(data) > 0 :
                                file_object.write("\n")
                            file_object.write("\n")
                            file_object.write("<!-- "+c+ " -->")
                            file_object.write("\n\n")
                            file_object.write("==============================================")
                    print("<!-- "+c+ " -->")
                    print("==============================================")
            except ValueError:
                #checksLogger.error('URLError = ' + str(e.reason))
                print('[ - ] Failed to connect skipping this url...')
                continue




    else:
        for c in comments:
            if outputFlag == 1:
                with open(folderName+"[comments].txt","a+") as file_object:
                    file_object.seek(0)
                    data = file_object.read(100)
                    if len(data) > 0 :
                        file_object.write("\n")
                    file_object.write("\n")
                    file_object.write("<!-- "+c+ " -->")
                    file_object.write("\n\n")
                    file_object.write("==============================================")
            print("<!-- "+c+ " -->")
            print("==============================================")


    # url = sys.argv[1]
    # # comments = re.findall("^<!-- -->$",soup)
    #
    # print(soup.prettify())
    # print(soup.title)
    # print(soup.title.name)
    # print(soup.title.string)
    # # print(soup.find_all('a'))
    # for link in soup.find_all('a'):
    #     print(link.get('href'))
    # print(soup.b.string)