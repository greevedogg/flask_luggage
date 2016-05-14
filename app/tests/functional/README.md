Requirements:

* JDK 1.7
* Selenium Server 2.53
* Appium

# Setup

## Overview

Currently it's set up to work with Selenium Grid for desktop browsers and Appium separately for mobile. At some point we should
merge the two so that Appium runs as a Selenium Grid node, but the problem I was having is that I couldn't get the
simulator to come up when setting it up as a grid node. If Appium is used standalone then the simulator works just fine.

## Commands

    $ java -jar selenium-server-standalone-2.53.0.jar -role hub


    $ java -jar selenium-server-standalone-2.53.0.jar -role node -nodeConfig /path/to/app/tests/functional/bootstrap/desktop-selenium-grid.json


    $ appium
