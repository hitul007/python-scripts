# File download script
import urllib2
mp3file = urllib2.urlopen("http://www.example.com/songs/mp3.mp3")
with open('test.mp3','wb') as output:
    output.write(mp3file.read())

