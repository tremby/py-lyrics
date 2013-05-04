"""
Copyright 2009~2012 Bart Nagel (bart@tremby.net)

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program. If not, see <http://www.gnu.org/licenses/>.
"""

NAME = "lyrics"
VERSION = "2.0"
DESCRIPTION = """Python script making use of LyricWiki (lyrics.wikia.com) to pull 
lyrics from the web from the commandline"""
AUTHOR = "Bart Nagel"
AUTHOR_EMAIL = "bart@tremby.net"
URL = "http://github.com/tremby/py-lyrics"
LICENSE = "Gnu GPL v3"

import urllib
import sys
import os
import re
import subprocess
import lxml.html

def lyricwikicase(s):
	"""Return a string in LyricWiki case.
	Substitutions are performed as described at 
	<http://lyrics.wikia.com/LyricWiki:Page_Names>.
	Essentially that means capitalizing every word and substituting certain 
	characters."""

	words = s.split()
	newwords = []
	for word in words:
		newwords.append(word[0].capitalize() + word[1:])
	s = "_".join(newwords)
	s = s.replace("<", "Less_Than")
	s = s.replace(">", "Greater_Than")
	s = s.replace("#", "Number_") # FIXME: "Sharp" is also an allowed substitution
	s = s.replace("[", "(")
	s = s.replace("]", ")")
	s = s.replace("{", "(")
	s = s.replace("}", ")")
	s = urllib.urlencode([(0, s)])[2:]
	return s

def lyricwikipagename(artist, title):
	"""Return the page name for a set of lyrics given the artist and 
	title"""

	return "%s:%s" % (lyricwikicase(artist), lyricwikicase(title))

def lyricwikiurl(artist, title, edit=False, fuzzy=False):
	"""Return the URL of a LyricWiki page for the given song, or its edit 
	page"""

	if fuzzy:
		base = "http://lyrics.wikia.com/index.php?search="
		pagename = artist + ':' + title
		if not edit:
			url = base + pagename
			doc = lxml.html.parse(url)
			return doc.docinfo.URL
	else:
		base = "http://lyrics.wikia.com/"
		pagename = lyricwikipagename(artist, title)
	if edit:
		if fuzzy:
			url = base + pagename
			doc = lxml.html.parse(url)
			return doc.docinfo.URL + "&action=edit"
		else:
			return base + "index.php?title=%s&action=edit" % pagename
	return base + pagename

def __executableexists(program):
	"""Determine whether an executable exists"""

	for path in os.environ["PATH"].split(os.pathsep):
		exefile = os.path.join(path, program)
		if os.path.exists(exefile) and os.access(exefile, os.X_OK):
			return True
	return False

def currentlyplaying():
	"""Return a tuple (artist, title) if there is a currently playing song in 
	MPD or Rhythmbox, otherwise None.
	Raise an OSError if no means to get the currently playing song exist."""

	artist = None
	title = None

	mpc = __executableexists("mpc")
	rhythmbox = __executableexists("rhythmbox-client")

	if not mpc and not rhythmbox:
		raise OSError("neither mpc nor rhythmbox-client are available")

	if mpc:
		output = subprocess.Popen(["mpc", "--format", "%artist%\\n%title%"],
				stdout=subprocess.PIPE).communicate()[0].split("\n")
		if not output[0].startswith("volume: "):
			(artist, title) = output[0:2]

	if artist is None and rhythmbox:
		output = subprocess.Popen(
				["rhythmbox-client", "--no-start", "--print-playing", 
						"--print-playing-format=%ta\n%tt"],
				stdout=subprocess.PIPE).communicate()[0]
		if len(output) > 0 and output != "Not playing\n":
			(artist, title) = output.split("\n")[0:2]

	if artist is None or title is None:
		return None
	return (artist, title)

def getlyrics(artist, title, fuzzy=False):
	"""Get and return the lyrics for the given song.
	Raises an IOError if the lyrics couldn't be found.
	Raises an IndexError if there is no lyrics tag.
	Returns False if there are no lyrics (it's instrumental)."""

	try:
		doc = lxml.html.parse(lyricwikiurl(artist, title, fuzzy=fuzzy))
	except IOError:
		raise

	try:
		lyricbox = doc.getroot().cssselect(".lyricbox")[0]
	except IndexError:
		raise

	# look for a sign that it's instrumental
	if len(doc.getroot().cssselect(".lyricbox a[title=\"Instrumental\"]")):
		return False

	# prepare output
	lyrics = []
	if lyricbox.text is not None:
		lyrics.append(lyricbox.text)
	for node in lyricbox:
		if str(node.tag).lower() == "br":
			lyrics.append("\n")
		if node.tail is not None:
			lyrics.append(node.tail)
	return "".join(lyrics).strip()
