## SafeBox Project


Developers: Bradley, Danny, Sean

PURPOSE:
To learn more about interconnected systems via MCU programming and python script
execution.

Overview:
The project consists of using the twilio API to send commands to an arduino running twilio-python library.
Given a certain command the arduino will lock, or unlock.

The SafeBox will also have a keypad that a delivery person can open via the last 4 digits of the tracking number on the package.
They can then lock it by pushing "####". The SafeBox will only open if the 4 digits entered are on a list of tracking numbers.

Everytime the safe is opened, any ADMIN ranked users will receive a notification that the SafeBox was opened.

Admin users have access to more commands:
addTracking
rmTracking
addUser
rmUser
lock
unlock

Users have less access:
lock
unlock

DEPENDENCIES:
* Hardware
  * Arduino Yun
  * Keypad
  * Servo Motor(s)

* Software
  * Python
  * Twilio API
  * Arduino IDE

CONTRIBUTIONS & LICENSING:
  TBD

