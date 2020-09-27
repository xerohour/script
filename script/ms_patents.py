#!/usr/bin/env python3
# This is a script 1 anon from 4chan wrote, and which I modified. The script
# will download all Microsoft patents. There are somewhere around 45500
# URLs / PDFs, so I set the range from 0 to 100 000, because it'll just finish
# and when you notice it hasn't created new files in a while, then you know the
# script is done fetching all the patents. If a URL can't be fetched, then the
# script will retry connecting 10 times, with a 10 second interval. After that
# the script gives up on that particular URL, and moves on to the next.

import requests
from requests import get
import bs4
import re
import time
import os

def download(url, file_name):
    if os.path.isfile(file_name):
        print('skipping ' + file_name + '...')
        return(True)
    connected = False
    tries_2 = 0
    while not connected:
         try:
             response = get(url)
             with open(file_name, 'wb') as file:
                 file.write(response.content)
             print('downloaded ' + str(num) + '\r\n')
             connected = True
         except:
             tries_2 = tries_2 + 1
             if tries_2 == 11:
                 connected = True
             else:
                 print('retrying ' + str(tries_2) + ' ' + url + '...')
                 time.sleep(10)
             pass

for num in range(0, 100000):
    start_url = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=" + str(num) + "&f=G&l=50&d=PTXT&p=1&S1=microsoft.ASNM.&OS=AN/microsoft&RS=AN/microsoft"
    headers = {'User-Agent':'HTC Mozilla/5.0 (Linux; Android 7.0; HTC 10 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36.'}

    connected = False
    tries = 0
    while not connected:
        try:
            content = requests.get(start_url,headers=headers)
            soup = bs4.BeautifulSoup(content.text,features='lxml')
            for t in soup.find_all('a', href=lambda x: x and 'View+first+page' in x):
                step2 = t['href'] + '&pagenum=0'
            sec_content = requests.get(step2)
            soup2 = bs4.BeautifulSoup(sec_content.text,features='lxml')
            download('http:' + soup2.find('embed').get('src'), soup2.find('embed').get('name') + '.pdf')
            connected = True
        except:
            tries = tries + 1
            if tries == 11:
                connected = True
            else:
                print('retrying ' + str(tries) + ' ' + start_url + '...')
                time.sleep(10)
            pass
