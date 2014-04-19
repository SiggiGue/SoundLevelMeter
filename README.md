#Sound Level Meter for the browser with WebSockets
This repository contains an implementation of a simple sound level meter displayed in the browser.
[PySoundCard][] is used for sound card input and tornado WebSocket is used to reach through the data to the javascript  in the html page.

![LevelMeter](screenshot.png "Simple Level Meter in the browser")

##Getting started
Clone this repo, be shure to have the modules pycparser, cffi, pysoundcard and tornado to be installed.
If you are a windows user i recommend to use [WinPython][] or a compareable python distribution. With the package manager you can install windows binaries. The pycparser and cffi are easy to get from the [Unofficial Windows Binaries][] page from Christoph Gohlke. The tornsdo package is already installed on WinPython.

[WinPython]: http://winpython.sourceforge.net/
[Unofficial Windows Binaries]: http://www.lfd.uci.edu/~gohlke/pythonlibs/
[PySoundCard]: https://github.com/bastibe/PySoundCard

##Usage
Just run the file `slm.py`. This will pop up the browser and show the simple level meter. With the start and stop button you control the data stream. The settings button gives you the options to set the averaging time and to calibrate your sound level meter with a calibrator.
You can open the slm.html another time. This will connect to another WebSocket and you can specify different setings and view the measured levels in many browsers with different settings.


##Future
For the future there are some plans for supporting weightings like A, B, and C-weighting. Maybe the communication over the WebSocket will be refactored to support a fractional octave view...

Have fun!
