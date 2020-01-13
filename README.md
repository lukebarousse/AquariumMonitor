# Smart Aquarium
## Project Goals
Host an external browser that allows outside access and control of:
- 1 or more cameras
- Aquarium Light Control
- Aquarium Feeder Control

Support Alexa control of:
- Aquarium Light
- Aquarium Feeder
------
## Needed Equipment
- Aquarium with installed light
- [Raspberry Pi Starter Kit 4GB RAM](https://www.amazon.com/gp/product/B07V5JTMV9/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1)
- [Pi Camera V2](https://www.amazon.com/gp/product/B01ER2SKFS/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
- [Pi Camera Extension Cable](https://www.amazon.com/gp/product/B07J57LQQS/ref=ppx_yo_dt_b_asin_title_o02_s01?ie=UTF8&psc=1)
- [Web Camera Logitech C270](https://www.amazon.com/gp/product/B004FHO5Y6/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
    - [List of Cameras Here](https://elinux.org/RPi_USB_Webcams)
- [Assorted Ribbon Cables](https://www.amazon.com/gp/product/B07GD2PGY4/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
- [IoT Relay - High Power for Lights](https://www.amazon.com/gp/product/B00WV7GMA2/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
- [Relay Module 5V - 4 Channel for Feeder](https://www.amazon.com/gp/product/B01HEQF5HU/ref=ox_sc_act_title_1?smid=A2WWHQ25ENKVJ1&psc=1)
- [Eheim Automatic Feeding Unit](https://www.amazon.com/Everyday-Feeder-Programmable-Automatic-Dispenser/dp/B001F2117I/ref=zg_bs_2975462011_1?_encoding=UTF8&psc=1&refRID=KGSNPF65ZRBQQRJKRDBH)
    - Electrical Wire to connect Relay to Feeder
    - Solder Gun and Wire to connect said wire
- [DS18B20 Waterproof Temperature Sensor](https://www.amazon.com/Waterproof-Temperature-Thermistor-Controller-Thermometer/dp/B01JKVRVNI/ref=sr_1_3?keywords=DS18b20&qid=1578248321&sr=8-3)
    - 10k Ohm Resistors
------
## Steps to Complete
### Legend
- Initial Setup
- MotionEyeOS Setup
- Dynamic DNS Setup
- GPIO Connections
- Alexa Control
------
### Initial Setup
- Set up Raspberry Pi with OS (Raspian)

------
### MotionEyeOS Setup
Source: [MotionEyeOS by ccrisan @ GitHub](https://github.com/ccrisan/motioneyeos "github")

#### MotionEyeOS Setup
Download the latest release of motioneyeos
[Select release here](https://github.com/ccrisan/motioneyeos/releases)  
Extract the image file from the archive  
Download writeimage.sh shell script (from motionEyeOS) that installs and configures your wifi and IP address
``` 
wget https://raw.githubusercontent.com/ccrisan/motioneyeos/master/writeimage.sh

# for Mac if you don't have wget (wget: command not found) install it
brew install wget
```
Insert Smart Card into mac, determine disk number
```
$ diskutil list
```
Determine disk number from command above (i.e. /dev/diskN) and unmount
```
$ diskutil unmountDisk /dev/diskX
```
Write the image file to your SD card.
```
 sudo sh ./writeimage.sh -d /dev/XXXX -i "/path/to/motioneyeos.img"

# IF starting up via WiFi you must add your network information to successfully start up
 sudo sh ./writeimage.sh -d /dev/disk3 -i "/Users/LukeBarousse/Downloads/motioneyeos-raspberrypi4-20190911.img" -n 'ATT8qCa7Vm:9vgf3=cu+rtr' -s "192.168.1.99/24:192.168.1.1:8.8.8.8"
```
When done, eject the disk
```
$ sudo diskutil eject /dev/rdiskN
```
View video on [http://localhost:8081](http://http://192.168.1.99/24:8081 "Local Home")  
Change admin password to something more secure  
Enable _Fast Network Camera_ option (NOTE: This disables motion detection/notification, pictures/movies, overlaid text.)  
Ensure the Default Gateway (192.168.1.1) is set to your Router's IP (192.168.1.xxx) address or your date/time will be wrong (i.e. 1-1-1970).

To shell into your pi from local computer
``` 
ssh admin@192.168.1.99
# type in password set above, if no password then leave blank and press enter
```
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
### Dynamic DNS & Port Forwarding
Source: [Duck DNS for Raspberry Pi](https://www.duckdns.org/install.jsp)

#### Setup Duck DNS Domain
Visit [Duck DNS](https://www.duckdns.org/install.jsp) and sign in  
Create a domain name  
WARNING: You must type the full address [http://domainname.duckdns.org](http://domainname.duckdns.org)  
Add your local IPv4 and IPv6 address

#### Setup Duck DNS to Update IP address
[Duck DNS Install](https://www.duckdns.org/install.jsp)  
Note: My IP address doesn't change frequently so I skipped this step.   
Directions below are for a Raspberry Pi:  
Make file for request
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
Source:[ Port Forward](https://portforward.com/ "Port Forward"), [Test Port Forward](https://www.yougetsignal.com/tools/open-ports/), 
[AT&T Uverse Router](https://www.att.com/support/article/u-verse-high-speed-internet/KM1123072), [AT&T Uverse How to Port Forward](https://www.youtube.com/watch?v=Aim81HD9_vk)

Note: Port forwarding is a way of making the pi accessible to computers on the internet
Login to your router  
Navigate to your routers port forwarding section (also called virtual server)  
Create the port forward entries in your router
- Protcol: ALL
- Internal Port: 8081
- External Port: 8081
- IP Address/Device: (Enter static IP address of Pi)
Test your ports are forwarded correctly, may have to restart router.
------
### GPIO Connections 

Sources:  
[Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)  
[MotionEyeOS Action Buttons](https://github.com/ccrisan/motioneyeos/wiki/Action-Buttons)  
![RPi GPIO Layout](https://www.raspberrypi.org/documentation/usage/gpio/images/GPIO.png)
Note: GPIO 2 & 3 available if I2C disabled, GPIO 14 & 15 available if serial is disabled

#### Light Connections - GPIO 21
Overview: Aquarium light plugged into IoT relay connected to GPIO pins of Pi.
Wire Pi to IOT Relay by M-F connection of GPIO 21 to positive input and GPIO ground to negative input of relay.  
Turn aquarium light on and plug aquarium receptacle in the 'normally OFF' receptacle.
Edit Action button scrips as described [here](https://github.com/ccrisan/motioneyeos/wiki/Action-Buttons)

#### Feeder Connections - GPIO 17  
Overview: Feeder wired to one channel of relay connected to GPIO pins of Pi.
Connect GPIO pins (Pi to Relay) 5V to Vcc, Ground to Gnd, and GPIO 17 to Channel Input.  
Solder two electrical wires to one the feeders push botton as pictured below.
Connect the other two ends of the wires to the N.O. and Com. terminals.  

![Fish Feeder Wiring](http://i1325.photobucket.com/albums/u626/jelazar67/WAMAS%20Articles/DIY%20Autofeeder/d51c2f28-e5c0-4d6f-b500-ad14b4b76b83_zps1a32b0d5.jpg)  

#### To Run Python Code
Create the file for button
```
nano /data/etc/up_1
```
Insert the path to the python file
```
#!/bin/bash
/usr/bin/python /data/etc/up.py
```
Make it executable
```
chmod +x /data/etc/up_1
```
Create python file
```
nano /data/etc/up.py
```
Enter your required code
```
#!/usr/bin/python

#Insert Python code here
```
Make it executable
```
chmod +x /data/etc/up.py
```
------
### Alexa Control

Note: Set this up only after all the steps above are fully complete  
Log into [_If This Than That_ (IFTTT.com)](https://ifttt.com/) and register your Amazon account.  
For each item (Lights ON, Feed Fish, etc.) assign an Alexa trigger as follows:  
The "This" will be an 'Alexa' command (e.g., Alexa trigger aquarium lights on)  
The "That" will be 'Webhooks', for this get the url of the buttons on the MotionEyeOS page (Meaning, go to your webpage with your cameras and copy the link location of the buttons for the respective python/GPIO task)  
------
### Temperature Setup (To Be Continued for this)

Source: [DIY Aquarium Controller](https://www.youtube.com/watch?v=76CD_waImoA&list=PLJDyE_1I8YfPQP4L8Mso2kDRItCbfq94s&index=5)
------
### Sources/Inspiration
- [SourceForge GPIO Python Code Basics](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/)
- [GitHub for MotionEyeOS](https://github.com/ccrisan/motioneyeos)
- [GitHub for LightOn/LightOff py file](https://github.com/skiwithpete/relaypi)
- [Spy your pet with a Raspberry Pi Camera Server by Michel Parreno](https://hackernoon.com/spy-your-pet-with-a-raspberry-pi-camera-server-e71bb74f79ea "Medium Article")
- [Duck DNS for Raspberry Pi](https://www.duckdns.org/install.jsp)
- [Fish Feeder Arduino Raspberry Pi Link](https://www.instructables.com/id/Fish-Feeder-Arduino-Raspberry-Pi-Link/)
- [Automatic Feeder for Aquacontroller](https://wamas.org/forums/blogs/entry/46-diy-automatic-feeder-for-aquacontroller/)
