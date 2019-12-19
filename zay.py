#! /usr/local/bin/python3


import requests
from bs4 import BeautifulSoup
import argparse
import re
import sys
import time
import os
import subprocess


#edit this data to work with your dune hd
dune_url='http://192.168.77.50'
dune_api=dune_url+'/cgi-bin/do?cmd=start_file_playback&media_url='
dune_ftp="/D"
dune_user="root"
dune_ssh_pass=""

pat="{}"
dn=os.path.dirname(os.path.abspath(__file__))
play_load=f"{dn}/formsefon.sh  {pat} {dune_url} {dune_ftp} {dune_user} {dune_ssh_pass}"


def getContent(u, name):
   try:
      s = requests.Session()
      u1=u.split('/'); ubase=u1[0]+'//'+u1[2]
      res=s.get(ubase, headers={'User-Agent': 'Mozilla/5.0'})
      page=s.get(u+name)
      return BeautifulSoup(page.content, 'html.parser')
   except: return None

def getSubContent(u, too):
   try:
      page=requests.get(u)
      s='page'+too
      return eval(s)
   except: return None

def seconds(s):
   try:
      s1=s.split(':')
      return  int(s1[0])*60+int(s1[1])
   except: return 0


def dun_req(res, too, quiet=False, shell=False):
   try:
      if too:
         res=getSubContent(res, too)
      if not quiet: print('playing.. {}'. format(res))
      if not shell:
         res=requests.get(dune_api+res, timeout=10)
         if not res.ok: raise Exception()
      else:
         subprocess.call([play_load.format(res)], stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
   except ValueError: return
   except Exception as e:  sys.exit(2)


def main(song_name, quiet, shell):

    #plugins that query service, use BeautifulSoup to parse responce and return data in 
    #format  [('trackname', 'url://*.mp3', 'command_after_sub_request', 'time')]
    #example [('skyfall adele', 'http://kachay/download/ad.mp3', '', '2:43')]
    #you can test plugin first in jupiter note that you can find the folder (tester.ipynb)

    #=====================================================================================================================
    #zaycev
    soup1=getContent('https://zaycev.net/search.html?query_search=', song_name)
    a1=soup1.find_all('div', class_='musicset-track-list__items')
    a2=sum((a.find_all('div', class_='musicset-track clearfix') for a in a1), [])
    a3=[(a.get_text(), 'https://zaycev.net'+a.get_attribute_list(key='data-url')[0], a) for a in a2]
    a4=[(a[0], a[1], ".json()['url']", a[2].find(class_='musicset-track__duration').get_text()) for a in a3]

    #=====================================================================================================================
    #mp3party
    soup2=getContent('http://mp3party.net/search?q=', song_name)
    b1=soup2.findAll('div', class_='song-item')
    b2=[(a.find('div', class_='name'), a.find('span', class_="time").get_text(), a.find('div', class_='play-btn')) for a in b1]
    b3=[(a[0].get_text().replace('\n',''), a[2].get_attribute_list('href')[0], '', a[1]) for a in b2]

    #=====================================================================================================================
    #z1.fm
    soup3=getContent('https://z1.fm/mp3/search?keywords=', song_name)
    s1=soup3.find('div', class_="whb_box").findAll('div', class_="songs-list-item")
    s2=sum((a.findAll('span') for a in s1), [])
    s3=[(a.get_attribute_list('data-title')[0], a.get_attribute_list('data-url')[0],  a.get_attribute_list('data-time')[0]) for a in s2]
    s4=list(filter(lambda x: x[0] and x[1], s3))
    s5=[(a[0], 'https://z1.fm'+a[1], '', '00:'+a[2]) for a in s4]

    #=====================================================================================================================
    #you may add your section here and then
    #join plugins results together
    sa=a4+b3+s5 #+ your result


    sa=list(filter(lambda x: seconds(x[3])>30, sa))
    un=set()
    ar=[un.add(a[0]+a[3]) or a for a in sa if a[0]+a[3] not in un]

    if quiet and ar:
        dun_req(ar[0][1], ar[0][2], quiet, shell)
        print(seconds(ar[0][3]))

    else:
      for i in range(len(ar)):
        if ar[i]:
           print('found: {:>4})'.format(i+1), end=' ')
           print('{} - {}sec.'.format(ar[i][0], ar[i][3]))
           y=input('play? y/n/q  ')
           if y=='q': return
           elif y=='y':
               dun_req(ar[i][1], ar[i][2], quiet, shell)
               break



parser = argparse.ArgumentParser(description='Techno Zayats!')
parser.add_argument("--name", required=True, type=str, help="A Song name")
parser.add_argument("-q", default=False, action='store_true', help="Quiet mode")
parser.add_argument("-s", default=False, action='store_true', help="Download first mode. Dune HD has top have the root access")
args = parser.parse_args()
main(re.sub(r'\s+','+', args.name), args.q, args.s)



