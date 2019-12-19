# Zaycev2Dune

Finds and Plays a song from Zaycev.Net/Z1.Fm/Mp3Party --> Dune HD

*Requires Beautifulsoup*



**a)prepare:**

pip3 install -r requirements.txt 

     edit zay.py file and put in your Dune HD url etc.



**b) use (example):**

     python3 zay.py --name 'рюмка водки лепс'



**c) enjoy the music on your DuneHD**

     works with playlists (run.sh)



===============================================================================


##  Additionally and advanced:

1) **run.sh** runs a playlist

2) **formsefon.sh** helps to play after downloading temp file (usually a better way)

   *apply option -s. e.g "python3 zay.py -s --name 'рюмка водки лепс'"*

3) to use the last option you have to install curl via optware to your dune hd 

   (**optware.sh** is included)
   
4) Python zay.py file in extendable. You can include plugins for other mp3 stores to it.

   For details go to **line 65 in zay.py**
   
   
   
