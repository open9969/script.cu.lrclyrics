﻿# -*- Mode: python; coding: utf-8; tab-width: 8; indent-tabs-mode: t; -*-
"""
Scraper for http://www.lyrdb.com/

taxigps
"""

import os
import urllib
import socket
import re
import difflib
from utilities import *

__title__ = "lyrdb.com"
__priority__ = '120'
__lrc__ = True

socket.setdefaulttimeout(10)

class LyricsFetcher:
    def __init__( self ):
        self.base_url = "http://www.lyrdb.com/karaoke/"

    def get_lyrics(self, artist, song):
        log( "%s: searching lyrics for %s - %s" % (__title__, artist, song))
        try:
            url = 'http://www.lyrdb.com/karaoke/?q=%s+%s&action=search' %(artist.replace(' ','+').lower(), song.replace(' ','+').lower())
            f = urllib.urlopen(url)
            Page = f.read()
        except:
            log( "%s: %s::%s (%d) [%s]" % (
                   __title__, self.__class__.__name__,
                   sys.exc_info()[ 2 ].tb_frame.f_code.co_name,
                   sys.exc_info()[ 2 ].tb_lineno,
                   sys.exc_info()[ 1 ]
                   ))
            return None

        links_query = re.compile('<tr><td class="tresults"><a href="/karaoke/([0-9]+).htm">(.*?)</td><td class="tresults">(.*?)</td>')
        urls = re.findall(links_query, Page)
        links = []
        for x in urls:
            if (difflib.SequenceMatcher(None, artist.lower(), x[2].lower()).ratio() > 0.8)
                  and (difflib.SequenceMatcher(None, song.lower(), x[1].lower()).ratio() > 0.8):
                links.append( ( x[2] + ' - ' + x[1], x[0], x[2], x[1] ) )
        if len(links) == 0:
            lyrics = None
            return lyrics
        elif len(links) == 1:
            lyrics = self.get_lyrics_from_list(links[0])
            return lyrics
        else:
            return links

    def get_lyrics_from_list(self, link):
        title,Id,artist,song = link
        log('%s %s %s' %(Id, artist, song))
        try:
            url = 'http://www.lyrdb.com/karaoke/downloadlrc.php?q=%s' %(Id)
            f = urllib.urlopen(url)
            Page = f.read()
        except:
            log( "%s: %s::%s (%d) [%s]" % (
                   __title__, self.__class__.__name__,
                   sys.exc_info()[ 2 ].tb_frame.f_code.co_name,
                   sys.exc_info()[ 2 ].tb_lineno,
                   sys.exc_info()[ 1 ]
                   ))
            return None
        return Page
