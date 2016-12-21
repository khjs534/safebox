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
phone_number = ""

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def digit():
  kp = RPi_GPIO.keypad()
  digitPressed = None
  while digitPressed == None:
    digitPressed = kp.getKey()
  led_keypress()
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
  GPIO.cleanup()

def unlock():
  servoGPIO = 17
  GPIO.setup(servoGPIO, GPIO.OUT)
  pwm = GPIO.PWM(servoGPIO, 50)
  pwm.start(12)
  time.sleep(0.5)
  pwm.ChangeDutyCycle(12)
  pwm.stop()
  GPIO.cleanup()

def message_admins(message, *url):
  admin_numbers = open('admin.txt', 'r')
  admin_numbers = admin_numbers.readline().rstrip().split(" ")
  if not url == None:
    for i in range(len(admin_numbers)):
      outgoing = client.messages.create(
        to = admin_numbers[i],
        from_ = phone_number,
        body = message,
        media_url = url
      )
  else:
    for i in range(len(admin_numbers)):
      outgoing = client.messages.create(
        to = admin_numbers[i],
        from_ = phone_number,
        body = message
      )

def take_picture():
  call("fswebcam --no-banner pic.jpeg", shell=True)

def led_keypress():
  ledGPIO = 27
  GPIO.setup(ledGPIO, GPIO.OUT)
  GPIO.output(ledGPIO, GPIO.HIGH)
  time.sleep(0.25)
  GPIO.output(ledGPIO, GPIO.LOW)

def blink_on():
  ledGPIO = 27
  GPIO.setup(ledGPIO, GPIO.OUT)
  pwm = GPIO.PWM(ledGPIO, 4)
  pwm.start(2)
  time.sleep(0.5)
  pwm.ChangeDutyCycle(2)

def blink_off():
  ledGPIO = 27
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(ledGPIO, GPIO.OUT)
  pwm = GPIO.PWM(ledGPIO, 4)
  pwm.stop()
  GPIO.cleanup()

class Buzzer(object):
 def __init__(self):
   GPIO.setmode(GPIO.BCM)  
   self.buzzer_pin = 5 #set to GPIO pin 5
   GPIO.setup(self.buzzer_pin, GPIO.IN)
   GPIO.setup(self.buzzer_pin, GPIO.OUT)
   print("buzzer ready")


 def buzz(self, pitch, duration):
  
  if(pitch==0):
   time.sleep(duration)
   return
  period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
  delay = period / 2     #calcuate the time for half of the wave  
  cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

  for i in range(cycles):
   GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
   time.sleep(delay)    #wait with pin 18 high
   GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
   time.sleep(delay)    #wait with pin 18 low

 def play(self, tune):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  x=0

  print("Playing tune ",tune)
  if(tune==1):
    pitches=[262,294,330,349,392,440,494,523, 587, 659,698,784,880,988,1047]
    duration=0.1
    for p in pitches:
      self.buzz(p, duration)
      time.sleep(duration *0.5)
    for p in reversed(pitches):
      self.buzz(p, duration)
      time.sleep(duration *0.5)

  elif(tune==2):
    pitches=[262,330,392,523,1047]
    duration=[0.2,0.2,0.2,0.2,0.2,0,5]
    for p in pitches:
      self.buzz(p, duration[x])
      time.sleep(duration[x] *0.5)
      x+=1
  elif(tune==3):
    pitches=[392,294,0,392,294,0,392,0,392,392,392,0,1047,262]
    duration=[0.2,0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.4]
    for p in pitches:
      self.buzz(p, duration[x])
      time.sleep(duration[x] *0.5)
      x+=1

  elif(tune==4):
    pitches=[1047, 988,659]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])
      time.sleep(duration[x] *0.5)
      x+=1

  elif(tune==5):
    pitches=[1047, 988,523]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])
      time.sleep(duration[x] *0.5)
      x+=1

  GPIO.setup(self.buzzer_pin, GPIO.IN)

buzzer = Buzzer()

while True:
  code = ""
  if len(code) < 4:
    code = access()
  open_file = open("tracking.txt", 'r+')
  data_array = open_file.readline().split(" ")
  if code in data_array:
    ledGPIO = 27
    GPIO.setup(ledGPIO, GPIO.OUT)
    pwm = GPIO.PWM(ledGPIO, 4)
    pwm.start(2)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(2)

    unlock()
    message = "Safebox unlocked from keypad with code: " + code
    message_admins(message)
  elif code == "####":
    ledGPIO = 27
    GPIO.setup(ledGPIO, GPIO.OUT)
    pwm = GPIO.PWM(ledGPIO, 4)
    pwm.start(2)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(2)

    lock()
    message = "Safebox locked from keypad"
    message_admins(message)
  else:
    ledGPIO = 27
    GPIO.setup(ledGPIO, GPIO.OUT)
    pwm = GPIO.PWM(ledGPIO, 4)
    pwm.start(2)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(2)
    buzzer.play(4)
    timestamp = datetime.datetime.now().strftime('%h-%m-%s')
    filename = "opener-" + timestamp + ".jpeg"
    take_picture()
    message = "ROBBER!!!!"
    f = open("pic.jpeg")
    dropbox_client = dropbox.client.DropboxClient(dropbox_access_token)
    response = dropbox_client.put_file(filename, f)
    url = dropbox_client.media(response['path'])['url']
    message_admins(message, url)    
  blink_off()
