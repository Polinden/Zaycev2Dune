# Dune Techno Zayats

&nbsp;

## Finds and plays songs from Zaycev/... --> Dune HD 

### The public API is used. No hacks. You may listen all songs Zaycev regards as downloadable

### Dune HD was tested. You might need some tweaks to use this tool with other devices

&nbsp;
&nbsp;

*Lang: Python 3.7. Libs required: Beautifulsoup, requests, python-Levenshtein, fuzzywuzzy*

&nbsp;
&nbsp;

**a)prepare:**

    pip3 install -r requirements.txt

    edit zay.py file and put in your Dune local ip, folders etc.

&nbsp;

**b) use (example):**

    python3 zay.py --name 'рюмка водки лепс'

    python3 zay.py -s -p --name 'рюмка водки лепс'

&nbsp;

**c) enjoy the music on your Dune (other media)**

    works with playlists (run.sh is explained bellow)

&nbsp;
&nbsp;

===============================================================================

## Advanced usage:

1) **run.sh** runs playlists. Usage: *"run.sh my_list"*

   You may form a list by yourself *(a)* writing down the songs names or *(b)* let **zay.py** 
   do it for you. In the second case please add *option -p* to a command line. File **crazy_playlist** 
   (attached here) has been prepared with both *(a) and (b)* options. If you set this *option* 
   **zay.py -p** will add info about chosen and played songs to **crazy_playlist** file. This info 
   includes a song url together with its name in order for **zay.py** no longer search it when you "run" a playlist.
   If you put in a playlist only songs names then *run.sh* will make the engine to trace such songs down in the web.

2) **formsefon.sh** is a helper for *zay.py*. It allows to play a song after downloading it 
to your Dune in a temp file (please specify a folder with free access etc. as **dune_ftp,
dune_user, dune_ssh_pass** variables in the *lines 17-19 in zay.py*). This is usually a better way for unstable connection

   To use this advantage set the option *-s*. e.g *"python3 zay.py -s --name 'рюмка водки лепс'"*

3) the last option is available for you if you get *"curl"* and *"ssh"* installed on your Dune HD by the help of *optware*. Only then your Dune could receive and perform the command to download mp3 file

   **optware.sh** - installation script is included, in case you don't have your own. Not to mention "root" access to Dune! 

   On the other side, your commanding device in order to send a command to Dune (via ssh) should be provided with 
   **"except"** util (to automate a password typing). Install it (e.g. *sudo apt-get install except, brew install except, 
   etc.*). This option is used here but is not the only one possible. There is a famouse "web interface for wget plugin" 
   for Dune that could be considered as an alternative to our idea.
   
   If abovementioned (2 and 3 points) is a *headache* for you, just drop it and don't use *-s* potion!

4) **zay.py** file is not limited by a fixed mp3-stocks list. Just the opposite, it is fully *extendable*.

   You are free to include/replace, so to say, **"plugins snippets"** with different mp3 deposits. For details go to *the line 87 in zay.py*
   You may initially test your new plugin in a jupiter notebook (a notebook is included here in  *test.ibynb* file)
