#!/usr/bin/env python

from distutils.core import setup
import lyrics

with open("README.md") as file:
	long_description = file.read()

setup(
		name=lyrics.NAME,
		version=lyrics.VERSION,
		description=lyrics.DESCRIPTION,
		long_description=long_description,
		author=lyrics.AUTHOR,
		author_email=lyrics.AUTHOR_EMAIL,
		url=lyrics.URL,
		license=lyrics.LICENSE,

		py_modules=["lyrics"],
		scripts=["lyrics"],
		)
