# Internet-Xmas-Tree
Internet-Controlled Christmas tree lights using PHP and Python.

**Farnsworth:** What-mas?

**Fry:** Christmas. You know? X-M-A-S.

**Leela:** Oh, you mean Xmas. You must be using an archaic pronunciation. Like when you say "ask" instead of "aks".

# Example Usage

[Demo reel of various patterns.](https://www.youtube.com/watch?v=5M3lig-fI4s)

<img src="images/redgreen.jpg" alt="Picture of tree in use with Xmas colors" />

<img src="images/bluegreen.jpg" alt="Picture of tree in use with Seahawks colors" />

<img src="images/sketchywiring.jpg" alt="Picture of sketchy looking wiring setup from first version" />

[Old example of Web Interface](https://youtu.be/gIETAGKKV80).

![Screenshot of Webpage](http://puu.sh/m7AJj/7616c63f76.png "Screenshot of Webpage")

# Install and Usage

## Dependencies

Requires the [rpi\_ws281x python package by jgarff](https://github.com/jgarff/rpi_ws281x).
Ensure that your led strip is working properly first. This package contains example files to do so.

Requires a webserver that supports php. I used apache.

Either clone the repository or download a ZIP with the contents.

## Setup

Clone or extract the files to a directory of your choosing. Point your webserver to the `web` folder. Verify that the server is working properly by attempting to set a color.

At the top of `xmasWeb.py` the variables `LED_BRIGHTNESS` and `LED_COUNT` should be modified to match the setup. Start the python program with `sudo python xmasWeb.py`.

**Why run as root?**

The Pi requires programs that make changes to the GPIO be run as root.

Once the program is started, the led strip should light up with the correct color and pattern.

**If it doesn't work**, try ensuring that permissions for the folder are set properly for the user `www-data` or whatever your webserver uses. Ensure that both the web server and python script are running.

# Authors
Uses [jscolor](http://jscolor.com/) under the [GNU GPL license v3](http://www.gnu.org/licenses/gpl-3.0.en.html) for the color picker on the HTML form page.

Everything else by Chris Johnston 12/23/2015
