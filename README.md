##SafeBox Project

Developers: Bradley Simmons, Danny Kalemba, Sean Kung

###PROBLEM:
The problem that we aimed to solve is that with the rise of internet shopping there has been a rise in package theft.

###PURPOSE:
To learn more about interconnected systems via MCU programming. We wanted to achieve this by created a box that would have a locking mechanism controlled by a MCU (raspberry pi, or arduino yun).

###Overview:
We thought to use a common piece of information between the package carrier and the user so they could both easily open the Safebox. In the context of our project we thought of using the last four digits of the tracking number on the package.

We wanted to add easier functionality for the user by integrating the Twilio API. This way a user could send ordinary text messages to control the Safebox as well as receive text notification about status changes from the Safebox.

To successfully use our common piece of information to gain access to the SafeBox we required a keypad. The delivery person can then enter the last 4 digits of the tracking number on the package to open the Safebox. The SafeBox will only open if the 4 digits entered are on a list of tracking numbers. They can then lock it by pushing "####".

Everytime the safe is opened, all users listed on the ADMIN list will receive a notification that the SafeBox was opened.

Admins have access to many commands. To send a command to Safebox, the command is simply texted to the user's Twillio number. The current admin commands are the following:

* add tracking {4 digit number, ex. 0000}
* remove tracking {4 digit number, ex. 0000}
* add user {ex. +11112223333} (note when adding phone numbers you must include '+' and the country code)
* remove user {+11112223333} (note when adding phone numbers you must include '+' and the country code)
* lock
* unlock

If an admin was unable to pick up a package or if a package is meant for someone else in the household, Safebox has a list of users. User commands are limited to 'lock' and 'unlock'. If a user sends a command to Safebox an admin will be notifed that the Safebox was opened via a text command from the phone number it was sent from.



###DEPENDENCIES:
* Hardware
  * Raspberry Pi
  * Keypad
  * Servo Motor(s)
  * LEDs
  * Piezo Electric Buzzer
  * Sturdy Box

* Software
  * Python
  * Twilio API
  * Dropbox API
  * Linux
  * Flask
  * Ngrok

###LICENSE:
  [MIT](https://github.com/khjs534/safebox/blob/master/LICENSE)

