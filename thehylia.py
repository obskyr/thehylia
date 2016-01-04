#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A script to download full soundtracks from The Hylia.

# __future__ import for forwards compatibility with Python 3
from __future__ import print_function
from __future__ import unicode_literals

# --- Install prerequisites---

# (This section in `if __name__ == '__main__':` is entirely unrelated to the
# rest of the module, and doesn't even run if the module isn't run by itself.)

if __name__ == '__main__':
    import imp # To check modules without importing them.

    requiredModules = [
        ['requests', 'requests'], # Some modules don't have the same pypi name as
        ['bs4', 'beautifulsoup4'] # import name. Therefore, two entries per module.
    ]

    def moduleExists(module):
        try:
            imp.find_module(module[0])
        except ImportError:
            return False
        return True
    def neededInstalls(requiredModules=requiredModules):
        uninstalledModules = []
        for module in requiredModules:
            if not moduleExists(module):
                uninstalledModules.append(module)
        return uninstalledModules

    def install(package):
        pip.main(['install', '--quiet', package])
    def installModules(modules, verbose=True):
        for module in modules:
            if verbose:
                print("Installing {}...".format(module[1]))
            install(module[1])
    def installRequiredModules(needed=None, verbose=True):
        needed = neededInstalls() if needed is None else needed
        installModules(neededInstalls(), verbose)

    needed = neededInstalls()
    if needed: # Only import pip if modules are actually missing.
        try:
            import pip # To install modules if they're not there.
        except ImportError:
            print("You don't seem to have pip installed!")
            print("Get it from https://pip.readthedocs.org/en/latest/installing.html")

    installRequiredModules(needed)

# ------

import requests
from bs4 import BeautifulSoup

import sys
import os

import re # For the syntax error in the HTML.
try:
    from urllib import unquote
except ImportError: # Python 3
    from urllib.parse import unquote

# Different printin' for different Pythons.
normal_print = print
def print(*args, **kwargs):
    encoding = sys.stdout.encoding or 'utf-8'
    if sys.version_info[0] > 2: # Python 3 can't print bytes properly (!?)
        # This lambda is ACTUALLY a "reasonable"
        # way to print Unicode in Python 3. What.
        printEncode = lambda s: s.encode(encoding, 'replace').decode(encoding)
        unicodeType = str
    else:
        printEncode = lambda s: s.encode(encoding, 'replace')
        unicodeType = unicode
    
    args = [
        printEncode(arg)
        if isinstance(arg, unicodeType) else arg
        for arg in args
    ]
    normal_print(*args, **kwargs)

def getSoup(*args, **kwargs):
    r = requests.get(*args, **kwargs)
    content = r.content

    # --- Fix errors in thehylia's HTML
    removeRe = re.compile(br"^</td>\s*$", re.MULTILINE)
    content = removeRe.sub(b'', content)
    
    badDivTag = b'<div style="padding: 7px; float: left;">'
    badDivLength = len(badDivTag)
    badDivStart = content.find(badDivTag)
    while badDivStart != -1:
        badAEnd = content.find(b'</a>', badDivStart)
        content = content[:badAEnd] + content[badAEnd + 4:]
        
        badDivEnd = content.find(b'</div>', badDivStart)
        content = content[:badDivEnd + 6] + b'</a>' + content[badDivEnd + 6:]
        
        badDivStart = content.find(badDivTag, badDivStart + badDivLength)
    # ---
    
    return BeautifulSoup(content, 'html.parser')

class NonexistentSoundtrackError(Exception):
    def __init__(self, ostName=""):
        super(NonexistentSoundtrackError, self).__init__(ostName)
        self.ostName = ostName
    def __str__(self):
        if not self.ostName or len(self.ostName) > 80:
            s = "The soundtrack does not exist."
        else:
            s = "The soundtrack \"{ost}\" does not exist.".format(ost=self.ostName)
        return s

def getOstContentSoup(ostName):
    url = "http://anime.thehylia.com/soundtracks/album/" + ostName
    soup = getSoup(url)
    contentSoup = soup.find(id='content_container')('div')[1].find('div')
    if contentSoup.find('p', string="No such album"):
        raise NonexistentSoundtrackError(ostName)
    return contentSoup

def getSongPageUrlList(soup):
    table = soup('table')[0]
    anchors = table('a')
    urls = [a['href'] for a in anchors]
    return urls

def getImageInfo(soup):
    images = []
    anchors = soup('a', target='_blank')
    for a in anchors:
        url = a['href']
        name = url.rsplit('/', 1)[1]
        info = [name, url]
        images.append(info)
    return images

def getFileList(ostName):
    """Get a list of songs from the OST with ID `ostName`."""
    # Each entry is in the format [name, url].
    soup = getOstContentSoup(ostName)
    songPageUrls = getSongPageUrlList(soup)
    songs = [getSongInfo(url) for url in songPageUrls]
    images = getImageInfo(soup)
    files = songs + images
    return files

def getSongInfo(songPageUrl):
    """Get the file name and URL of the song at `songPageUrl`. Return a list of [songName, songUrl]."""
    info = []
    soup = getSoup(songPageUrl)
    info.append(getSongName(soup))
    info.append(getSongUrl(soup))
    return info
def getSongName(songPage):
    extensionRe = re.compile(r'^.*\.\S+$')
    infoParagraph = songPage.find(id='content_container').find(
        lambda t: t.name == 'p' and next(t.stripped_strings) == 'Album name:')
    name = infoParagraph('b')[1].get_text()
    if not extensionRe.match(name):
        name = unquote(getSongUrl(songPage).split('/')[-1])
    return name
def getSongUrl(songPage):
    url = songPage.find(id='content_container').find('table',
        class_='blog').find('div').find_all('b')[-1].find('a')['href']
    return url

def download(ostName, path="", verbose=False):
    """Download an OST with the ID `ostName` to `path`."""
    if verbose:
        print("Getting song list...")
    songInfos = getFileList(ostName)
    totalSongs = len(songInfos)
    for songNumber, (name, url) in enumerate(songInfos):
        downloadSong(url, path, name, verbose=verbose,
            songNumber=songNumber + 1, totalSongs=totalSongs)
def downloadSong(songUrl, path, name="song", numTries=3, verbose=False,
    songNumber=None, totalSongs=None):
    """Download a single song at `songUrl` to `path`."""
    if verbose:
        numberStr = ""
        if songNumber is not None and totalSongs is not None:
            numberStr += str(songNumber).zfill(len(str(totalSongs)))
            numberStr += "/"
            numberStr += str(totalSongs)
            numberStr += ": "
        print("Downloading {}{}...".format(numberStr, name))

    tries = 0
    while tries < numTries:
        try:
            if tries and verbose:
                print("Couldn't download {}. Trying again...".format(name))
            song = requests.get(songUrl)
            break
        except requests.ConnectionError:
            tries += 1
    else:
        if verbose:
            print("Couldn't download {}. Skipping over.".format(name))
        return

    try:
        with open(os.path.join(path, name), 'wb') as outfile:
            outfile.write(song.content)
    except IOError:
        if verbose:
            print("Couldn't save {}. Check your permissions.".format(name))

def search(term):
    """Return a list of OST IDs for the search term `term`."""
    soup = getSoup("http://anime.thehylia.com/search",
        params={'search': term})

    headerParagraph = soup.find(id='content_container').find('p',
        string=re.compile(r"^Found [0-9]+ matching albums for \".*\"\.$"))
    anchors = headerParagraph.find_next_sibling('p')('a')
    ostNames = [a['href'].split('/')[-1] for a in anchors]

    return ostNames

# --- And now for the execution. ---

if __name__ == '__main__':
    def doIt(): # Only in a function to be able to stop after errors, really.
        try:
            ostName = sys.argv[1].decode(sys.getfilesystemencoding())
        except AttributeError: # Python 3's argv is in Unicode
            ostName = sys.argv[1]
        except IndexError:
            print("No soundtrack specified! As the first parameter, use the name the soundtrack uses in its URL.")
            print("If you want to, you can also specify an output directory as the second parameter.")
            print("You can also search for soundtracks by using your search term as parameter - as long as it's not an existing soundtrack.")
            return
        try:
            outPath = sys.argv[2]
        except IndexError:
            outPath = ostName

        madeDir = False
        if not os.path.isdir(outPath):
            os.mkdir(outPath)
            madeDir = True

        try:
            download(ostName, outPath, verbose=True)
        except NonexistentSoundtrackError:
            try:
                searchTerm = ' '.join([a.decode(sys.getfilesystemencoding())
                    for a in sys.argv[1:]
                ]).replace('-', ' ')
            except AttributeError: # Python 3, again
                searchTerm = ' '.join(sys.argv[1:]).replace('-', ' ')
            
            searchResults = search(searchTerm)
            print("\nThe soundtrack \"{}\" does not seem to exist.".format(
                ostName))

            if searchResults: # aww yeah we gon' do some searchin'
                print()
                print("These exist, though:")
                for name in searchResults:
                    print(name)

            if madeDir:
                os.rmdir(outPath)
            return
        except requests.ConnectionError:
            print("Could not connect to The Hylia.")
            print("Make sure you have a working internet connection.")

            if madeDir:
                os.rmdir(outPath)
            return

    doIt()
