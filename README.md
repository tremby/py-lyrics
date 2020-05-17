Lyrics
======

Output lyrics from LyricWiki for a given song or the currently playing song in 
MPD.

Dependencies
------------

Python packages:

- lxml
- cssselect

Optional binaries:

- mpc to get the currently playing song from MPD

Installation
------------

Follow the usual Python paradigm

    sudo python setup.py install

or just run it directly

    ./lyrics

Usage
-----

See the help output

    lyrics --help

for details. In its simplest form, `lyrics`, get the currently playing song from 
MPD if possible, then fetch its lyrics from LyricWiki and output 
them to stdout. The mode can be changed with various switches to open a browser 
to the lyrics page or the edit lyrics page, or to output either URL to stdout.

Or the artist and title can be given, such as `lyrics Rammstein Los` or `lyrics 
Periphery "Ow My Feelings"`.

Bugs
----

Probably. Reports or patches are welcome, on the Github tracker.

Authors
-------

Bart Nagel <bart@tremby.net>
and [others](https://github.com/tremby/py-lyrics/graphs/contributors)

Download
--------

- [From Github](https://github.com/tremby/py-lyrics)
