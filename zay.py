import requests
from bs4 import BeautifulSoup
import argparse
import re
import sys


dune_url='http://192.168.77.50/cgi-bin/do?cmd=start_file_playback&media_url='

parser = argparse.ArgumentParser(description='A ZAYTSEV NET!')
parser.add_argument("--name", required=True, type=str, help="Song name")
parser.add_argument("-q", default=False, action='store_true', help="Quiet mode")
args = parser.parse_args()
name=re.sub(r'\s+','+', args.name)
if not args.q: print('searching '+name)

def dun_req(t):
    try:
       res=requests.get(t)
       res=res.json()['url']
       if not requests.get(dune_url+res).ok:
           sys.exit(2)
    except: return


page=requests.get('https://zaycev.net/search.html?query_search='+name)
soup = BeautifulSoup(page.content, 'html.parser')

a1=soup.find_all(class_='musicset-track-list__items')

a2=[y for x in a1 for y in x.findAll('div') if y.get_attribute_list(key='data-url')!=[None]]

a3=[(y.get_attribute_list(key='data-url')[0], y.getText(), y.find(class_='musicset-track__duration')) for y in a2]

un=set()

a4=[un.add(a[1]) or (a[1], a[2].get_text(), 'https://zaycev.net'+a[0]) for a in a3 if a[2] and not a[1] in un]

if args.q and a4:
    dun_req(a4[0][2])
    sys.exit(0)

for i in range(len(a4)):
    if a4[i]:
       print('found: ')
       print(a4[i])
       y=input('play? y/n')
       if y!='y': continue
       else:
           dun_req(a4[i][2])
           break
