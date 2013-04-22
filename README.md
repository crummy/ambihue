ambihue
=======

Ambient Hue Lighting Controller

This python script examines pixels on your main screen and sets your #2 Phillips Hue light to the average of those colours.

This is intended to provide a an experience similar to the amBX lighting system: http://www.ambx.com/

Requirements:
* Uses PIL to grab your screen

Limitations:
* Might only work with windowed/fullscreen windowed programs?

Usage:
* python gamehue.py <hubIP> <lightID>

Credit:
* Thanks to studioimaginaire; I use their Python interface for the Hue hub.
