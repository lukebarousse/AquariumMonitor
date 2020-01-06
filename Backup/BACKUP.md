### Camera Setup  (Removed and replaced with MotionEYEos) 
####Main Source: [Spy your pet with a Raspberry Pi Camera Server by Michel Parreno](https://hackernoon.com/spy-your-pet-with-a-raspberry-pi-camera-server-e71bb74f79ea "Medium Article")

#### Enable Camera
Enable camera configuration via Raspberry Pi options. In terminal run:
```
$ sudo raspi-config
```
Choose "camera" and select "Enable support for Raspberry Pi Camera". Reboot when prompted.

Test the camera:
```
$ raspistill -o cam.jpg
```
#### Enable Motion
First update the pi:
```
$ sudo apt-get update
$ sudo apt-get upgrade
```
Install Motion and activate driver:
```
$ sudo apt-get install motion
$ sudo modprobe bcm2835-v4l2      # v4l2 is an 'L', not the number 1
```
Active the driver by adding the following to modules:
```
$ sudo nano /etc/modules

# at the end modules add the following:
bcm2835-v4l2
```
Set as daemon (run in background) and start automatically:
```
$ sudo nano /etc/default/motio

# CTL+W and search for start_motion_daemon and activate it:
start_motion_daemon=yes
```
#### Configure Motion
Create a backup of config file:
```
$ sudo cp /etc/motion/motion.conf /etc/motion/motion.conf.bak
```
Edit the source config file:
``` 
$ sudo nano /etc/motion/motion.conf

# Allow motion to run the daemon we've set earlier
daemon on

# Set the logfile (important to debug motion if you webservers crashes)
logfile /tmp/motion.log

# we want to be able to access the stream outside off the Pi's localhost
stream_localhost off

# disable pictures and movies saving
output_pictures off 
ffmpeg_output_movies off

# set the framerate of the stream (100 for higher quality)
framerate 100

# set the width and height of your video
width 640
height 480

# control de port 8080 by default
webcontrol_port 8081

# careful ! don't set the stream_port just like the webcontrol port

# Add this line in the file for password authentication for camera server
webcontrol_authentication username:password
```
NOTE: Select compatible resolution for the PI as the stream won't start if you don't
Optional: Save Motion Detection Pictures
```
## define the number of images saved when a movement is detected
output_pictures on
pre_capture 1
post_capture 1

## define the folder where captures are going (don't forget the chmod rights if necessary)
target_dir /<path_of_your_choice> 
```
#### Testing Camera Locally
Start the motion server:
```
$ sudo service motion start 
```