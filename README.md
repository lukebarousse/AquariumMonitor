# README.md

## Smart Aquarium Project Goals
Host an external browser that allows outside access and control of:
- 1 or more cameras
- Aquarium Light Control
- Aquarium Feeder Control
- Temperature Monitor

Support Alexa internal control of:
- Aquarium Light
- Aquarium Feeder

## Needed Equipment
- Aquarium filled with Fish and properly lighted
- [Raspberry Pi Starter Kit 4GB RAM](https://www.amazon.com/gp/product/B07V5JTMV9/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1)
- [Pi Camera V2](https://www.amazon.com/gp/product/B01ER2SKFS/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
- [Pi Camera Extension Cable](https://www.amazon.com/gp/product/B07J57LQQS/ref=ppx_yo_dt_b_asin_title_o02_s01?ie=UTF8&psc=1)
- [Web Camera Logitech C270](https://www.amazon.com/gp/product/B004FHO5Y6/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
- [Assorted Ribbon Cables](https://www.amazon.com/gp/product/B07GD2PGY4/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
- [IoT Relay - High Power for Lights](https://www.amazon.com/gp/product/B00WV7GMA2/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
- [Relay Module 5V - 4 Channel for Feeder](https://www.amazon.com/gp/product/B01HEQF5HU/ref=ox_sc_act_title_1?smid=A2WWHQ25ENKVJ1&psc=1)
- [Eheim Automatic Feeding Unit](https://www.amazon.com/Everyday-Feeder-Programmable-Automatic-Dispenser/dp/B001F2117I/ref=zg_bs_2975462011_1?_encoding=UTF8&psc=1&refRID=KGSNPF65ZRBQQRJKRDBH)
- [DS18B20 Waterproof Temperature Sensor](https://www.amazon.com/Waterproof-Temperature-Thermistor-Controller-Thermometer/dp/B01JKVRVNI/ref=sr_1_3?keywords=DS18b20&qid=1578248321&sr=8-3)
    - 10k Ohm Resistors

## Steps to Compete
### Legend
- Initial Setup
- MotionEyeOS Setup
- Dynamic DNS Setup
- GPIO Connections
- Alexa Control

------
### Initial Setup
- Set up Raspberry Pi with OS (Raspian)
- Set up SSH with a local computer
- (Optional) Setup VNS with local computer
- Enable WiFi
- Setup a static IP address
------
### MotionEyeOS Setup
Source: [MotionEyeOS by ccrisan @ GitHub](https://github.com/ccrisan/motioneyeos "github")

#### MotionEyeOS Flash and Install
Download the latest stable release of motioneyeos  
[Select release here](https://github.com/ccrisan/motioneyeos/releases)

Extract the image file from the archive

Write the image file to your SD card.
```
 ./writeimage.sh -d /dev/XXXX -i "/path/to/motioneyeos.img"

# OR use the following to also set the static IP address (I choose 99 in this case)
./writeimage.sh -d /dev/mmcblk0 -i "/path/to/motioneyeos.img" -s "192.168.1.99/24:192.168.1.1:8.8.8.8"
```

View video on [http://localhost:8081](http://localhost:8081 "Local Home")
#### Enable Light & Feeder Action Button

Create bash script for turning light on(off) & feeding as follows:  
(Note: only certain action button names are permitted, also use 1 for camera 1 & 2 for camera 2, etc.)
``` 
$ nano /data/etc/light_on_1
```
_Simple GPIO Example_   
Add the following and input the correct GPIO number:
``` 
#!/bin/bash

GPIO=XX
test -e /sys/class/gpio/gpio$GPIO || echo $GPIO > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio$GPIO/direction
echo 1 > /sys/class/gpio/gpio$GPIO/value

# OR execute through python code(Not Tested)
#!/bin/sh
python3 /path/to/the/LightOn.py
```
To turn off light create file `/data/etc/light_off_1` and change `echo 1 > ...` to `echo 0 > ...`.

_HTML Request Example_  
Add the following:
``` 
#!/bin/bash

URL="http://192.168.1.123/webhook/alarm/"
METHOD="POST"
TIMEOUT="5"
curl -X $METHOD --connect-timeout $TIMEOUT "$URL" > /dev/null
```

Make the script executable
``` 
$ chomod +x /data/etc/light_on_1
```

------
### Dynamic DNS Setup
Source: [Duck DNS for Raspberry Pi](https://www.duckdns.org/install.jsp)

#### Setup Duck DNS
Note: I chose Duck DNS based on a recommendation from a friend /Xe138  
Make file for request:
``` 
$ sudo mkdir duckdns
$ sudo cd duckdns
$ sudo vi duck.sh
```
Copy the text below and insert (hit the i key to insert, ESC and arrows to move cursor).  
Note: Change 'domain' and 'token'. Can hardcode IP, best to leave blank.
``` 
echo url="https://www.duckdns.org/update?domains=exampledomain&token=a7c4d0ad-114e-40ef-ba1d-d217904a50f2&ip=" | curl -k -o ~/duckdns/duck.log -K -
```
Save file (ESC then :wq! then Enter)
Make duck.sh executable
```
$ sudo chmod 7000 duck.sh
```
Use cron to make script run every 5 minutes
``` 
$ sudo crontab -e

# insert the following at bottom of crontab
*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
```
Test the script
``` 
$ sudo ./duck.sh
```
Verify if attempt was successful (OK is good, KO is bad)
``` 
$ sudo cat duck.log
```
#### Setup Port Forwarding
Source: [Port Forward](https://portforward.com/ "Port Forward"), 
[AT&T Router](https://portforward.com/atnt/6800g/ "ATT 6800g")

Note: Port forwarding is a way of making the pi accessible to computers on the internet
Login to your router  
Navigate to your routers port forwarding section (also called virtual server)  
Create the port forward entries in your router
- Internal Port: 8081
- External Port: 8081
- Protcol: ALL
- IP Address/Device: (Enter static IP address of Pi)
Test your ports are forwarded correctly, may have to restart router.
------
### GPIO Connections 

Source: [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)
![RPi GPIO Layout](https://www.raspberrypi.org/documentation/usage/gpio/images/GPIO.png)
Note: GPIO 2 & 3 available if I2C disabled, GPIO 14 & 15 available if serial is disabled

#### Light Connections - GPIO 21
Overview: Aquarium light plugged into IoT relay connected to GPIO pins of Pi.
Wire Pi to IOT Relay by M-F connection of GPIO 21 to positive input and GPIO ground to negative input of relay.  
Turn aquarium light on and plug aquarium receptacle in the 'normally OFF' receptacle.

#### Feeder Connections - GPIO 17  
Overview: Feeder wired to one channel of relay connected to GPIO pins of Pi.
Connect GPIO pins (Pi to Relay) 5V to Vcc, Ground to Gnd, and GPIO 17 to Channel Input.  
Solder two electrical wires to one the feeders push botton as follows:  
![Fish Feeder Wiring](http://i1325.photobucket.com/albums/u626/jelazar67/WAMAS%20Articles/DIY%20Autofeeder/d51c2f28-e5c0-4d6f-b500-ad14b4b76b83_zps1a32b0d5.jpg)  
Connect the other two ends of the wires to the N.O. and Com. terminals.
------

### Alexa or Google Control (Future)

------

### Temperature Setup (Future)

Source: [DIY Aquarium Controller] (https://www.youtube.com/watch?v=76CD_waImoA&list=PLJDyE_1I8YfPQP4L8Mso2kDRItCbfq94s&index=5)

------
### Sources/Inspiration
- [SourceForge GPIO Python Code Basics](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/)
- [GitHub for MotionEyeOS](https://github.com/ccrisan/motioneyeos)
- [GitHub for LightOn/LightOff py file](https://github.com/skiwithpete/relaypi)
- [Spy your pet with a Raspberry Pi Camera Server by Michel Parreno](https://hackernoon.com/spy-your-pet-with-a-raspberry-pi-camera-server-e71bb74f79ea "Medium Article")
- [Duck DNS for Raspberry Pi](https://www.duckdns.org/install.jsp)
- [Fish Feeder Arduino Raspberry Pi Link](https://www.instructables.com/id/Fish-Feeder-Arduino-Raspberry-Pi-Link/)
- [Automatic Feeder for Aquacontroller](https://wamas.org/forums/blogs/entry/46-diy-automatic-feeder-for-aquacontroller/)
