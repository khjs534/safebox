from matrix_keypad import RPi_GPIO
import twilio.twiml
import time
import RPi.GPIO as GPIO
import dropbox
import datetime
from twilio.rest import TwilioRestClient
from subprocess import call

# add your twilio SID and token here
dropbox_access_token = ""
ACCOUNT_SID = ""
AUTH_TOKEN = ""

# uncomment line below when putting in your AUTH
#client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
timestamp = datetime.datetime.now().strftime("%h-%m-%S")
filename = "opener-" + timestamp + ".jpg"

f = open("home/pi/Desktop/safebox/pic.jpg")
dropbox_client = dropbox.client.DropboxClient(dropbox_access_token)
response = dropbox_client.put_file(filename, f)
url = dropbox_client.media(response['path'])['url']



def digit():
  kp = RPi_GPIO.keypad()
  digitPressed = None
  while digitPressed == None:
    digitPressed = kp.getKey()
  return digitPressed

def access():
  code = ""
  while (len(code) < 4):
    code += str(digit())
  return code

def lock():
  servoGPIO = 17
  GPIO.setup(servoGPIO, GPIO.OUT)
  pwm = GPIO.PWM(servoGPIO, 50)
  pwm.start(7)
  time.sleep(0.5)
  pwm.ChangeDutyCycle(7)
  pwm.stop()

def unlock():
  servoGPIO = 17
  GPIO.setup(servoGPIO, GPIO.OUT)
  pwm = GPIO.PWM(servoGPIO, 50)
  pwm.start(12)
  time.sleep(0.5)
  pwm.ChangeDutyCycle(12)
  pwm.stop()

def message_admins(message, *url):
  admin_numbers = open('admin.txt', 'r')
  admin_numbers = admin_numbers.readline().rstrip().split(" ")
  if not url == None:
    for i in range(len(admin_numbers)):
      outgoing = client.messages.create(
        to = admin_numbers[i],
        # add your twilio number here
        from_ = "",
        body = message,
        media_url = url
      )
  else:
    for i in range(len(admin_numbers)):
      outgoing = client.messages.create(
        to = admin_numbers[i],
        # add your twilio number here
        from_ = "",
        body = message
      )


def take_picture():
  call("fswebcam --no-banner pic.jpeg", shell=True)

while True:
  code = ""
  if len(code) < 4:
    code = access()
  open_file = open("tracking.txt", 'r+')
  data_array = open_file.readline().split(" ")
  if code in data_array:
    unlock()
    message = "Safebox unlocked from keypad with code: " + code
     # uncomment line below when not testing
#    message_admins(message)
  elif code == "####":
    lock()
    message = "Safebox locked from keypad"
    # uncomment line below when not testing
#    message_admins(message)
  else:
    take_picture()
    message_admins(message, url)
