

import requests
from bs4 import BeautifulSoup
import argparse
import re
import sys
import time
import os
import subprocess
from fuzzywuzzy import fuzz
import xml.etree.ElementTree as ET


#edit this data to work with your dune hd
dune_url='http://192.168.77.50'
dune_api=dune_url+'/cgi-bin/do?cmd=start_file_playback&media_url='
dune_ftp="/D"
dune_user="root"
dune_ssh_pass=""
playlist_name="crazy_playlist"

pat="{}"
dn=os.path.dirname(os.path.abspath(__file__))
play_script=f"{dn}/formsefon.sh"
play_load=f"{pat} {dune_url} {dune_ftp} {dune_user} {dune_ssh_pass}"


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

def add_to_playlist(name, url, time):
    delimited_str=f'{name} -##!##-  {url} -##!##-  {time}{os.linesep}'
    with open(f'{dn}/{playlist_name}', 'a+') as fpl:
        fpl.write(delimited_str)

def chech_result_dune(res):
    try:
        if isinstance(res, bytes): res=res.decode()
        res='<?xml version'+res.split('<?xml version')[1]
        myroot = ET.fromstring(res)
        q=myroot.findall("*[@name='command_status']")
        q=q[0].attrib['value']
        return q=='ok'
    except: return True

def dun_req(name, url, too, time, quiet=False, via_ftp=False, playlist=False, rcc=""):
   try:
      if too:
         url=getSubContent(url, too)
      if not via_ftp:
         res=requests.get(dune_api+url, timeout=10)
         if not res.ok: raise Exception()
         rcc=res.text
      else:
          rcc=subprocess.Popen([play_script, play_load.format(url)], stdout=subprocess.PIPE).communicate()[0]
      #if successfully playing then add to playlist and inform user
      if not quiet: print('OK. Playing {}, wait {}sec'. format(name, time))
      else: print(seconds(time))
      rcc=chech_result_dune(rcc)
      if playlist and rcc: 
          add_to_playlist(name, url, time)
      return rcc
   except ValueError as e: print(e); return
   except Exception as e:  print(e); sys.exit(2)

def prepare_name(name):
    name = re.sub(r'[\W]+',' ', name)
    name = re.sub(r'\s+','+', name)
    return name


def main(song_name, quiet, via_ftp, playlist, dest='', time=''):

    #don't search mode. url is known from playlist
    if dest:
        if not time: time='2:22'
        dun_req(song_name, dest, '', time, quiet=True, via_ftp=via_ftp, playlist=False)
        return

    song_name=prepare_name(song_name)

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
    a4=[(re.sub(r'\d+:\d+','', a[0]), a[1],".json()['url']", a[2].find(class_='musicset-track__duration').get_text()) for a in a3]

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

    #url is not none and duration>30sec and unique name in list
    sa=list(filter(lambda a: seconds(a[3])>30 and a[1], sa))
    un=set()
    ar=[un.add(a[0]+a[3]) or a for a in sa if a[0]+a[3] not in un]

    #fuzzy search and sort 
    if True: ar = sorted(ar, key=lambda a: -fuzz.partial_ratio(song_name, a[0]))

    if quiet and ar:
        for a in ar:
            if dun_req(*a, quiet, via_ftp, playlist):
               return 0

    else:
      i=1
      for a in ar:
           print('found: {:>4})'.format(i), end=' ')
           print('{} - {}sec.'.format(a[0], a[3]))
           y=input('play? y/n/q  ')
           if y=='q': return 0
           elif y=='y':
               if dun_req(*a, quiet, via_ftp, playlist):
                   return 0
               else: 
                   print("error while playing")
           i+=1



parser = argparse.ArgumentParser(description='Techno Zayats!')
parser.add_argument("--name", required=True, type=str, help="A Song name")
parser.add_argument("-q", default=False, action='store_true', help="Quiet mode")
parser.add_argument("-s", default=False, action='store_true', help="Download first mode. Dune HD has to have the root access")
parser.add_argument("-p", default=False, action='store_true', help="With adding to palylist")
parser.add_argument("--dest", required=False, type=str, help="URL already known (don't search mode)")
parser.add_argument("--time", required=False, type=str, help="Song time (for 'don't search mode)")

args = parser.parse_args()
main(*args.__dict__.values())



