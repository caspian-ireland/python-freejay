[![GitHub release](https://img.shields.io/github/release/caspian-ireland/python-freejay?include_prereleases=&sort=semver&color=blue)](https://github.com/caspian-ireland/python-freejay/releases/)
[![issues - python-freejay](https://img.shields.io/github/issues/caspian-ireland/python-freejay)](https://github.com/caspian-ireland/python-freejay/issues)
[![License](https://img.shields.io/badge/License-GPLv3-blue)](#license)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Python FreeJay

Python FreeJay is free DJ software that supports basic DJ functionality and
convenient audio download from YouTube.

Inspired by the 2000s party saver twoyoutubevideosandamotherfuckingcrossfader.com,
FreeJay is a desktop application built on open source tools, and aims to
provide a fast and painless solution for those times when all you have is a
laptop and an internet connection.

## Project Status
Project is: _in progress_

## Roadmap

The project is currently under development and various design decisions are
yet to be made. The core functionality will be built on the standard logic used
in mainstream DJ software.

### Initial release:

The initial release will provide a basic GUI built using
[tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter)
with audio playback implemented using [python-mpv](https://github.com/jaseg/python-mpv).

Features:
* 2 decks (audio players)
* Crossfader
* Play/pause, cue, stop, pitch, nudge, jog
* YouTube audio download

### Further down the line...

* 3-band EQ per channel/deck
* Waveform visualisation
* TUI, eventually replacing the tkinter GUI.
* BPM detection


## Installation

This project is still in development and is not ready for distribution. Install
instructions will be provided with initial release.

If you are interested in viewing the progress so far, you can try the following:
* I'm running Python 3.11.0, though earlier versions _may_ work
* Clone this repository
* Install dependencies using `pip install -r requirements.txt`
* Install `libmpv`. If you encounter difficulties check the
install instructions for [python-mpv](https://github.com/jaseg/python-mpv)


## Usage

This project is still in development and is not ready for distribution. Usage
instructions will be provided with initial release.


## Contributing

Not accepting code contributions until a basic application structure has been established.
Please feel free to submit suggestions via an
https://github.com/caspian-ireland/python-freejay/labels/enhancement issue.


## Code Style

[Black](https://github.com/psf/black)

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) or later.
