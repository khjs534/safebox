from flask import Flask, request, redirect
import twilio.twiml
import time
import RPi.GPIO as GPIO

app = Flask(__name__)

def admin_check(sender_number):
  admin_number = open('admin.txt', 'r')
  admin_number = admin_number.readline().split(" ")
  if sender_number in admin_number:
    return True
  else:
    return False

def user_check(sender_number):
  user_numbers = open('users.txt', 'r')
  user_numbers = user_numbers.readline().split(" ")
  if sender_number in user_numbers:
    return True
  else:
    return False

def command_return(incoming_message):
  if incoming_message[0].lower() == "add" and incoming_message[1].lower() == "tracking":
    return "add tracking"
  elif incoming_message[0].lower() == "remove" and incoming_message[1].lower() == "tracking":
    return "remove tracking"
  elif incoming_message[0].lower() == "add" and incoming_message[1].lower() == "user":
    return "add user"
  elif incoming_message[0].lower() == "remove" and incoming_message[1].lower() == "user":
    return "remove user"
  elif incoming_message[0].lower() == "lock":
    return "lock"
  elif incoming_message[0].lower() == "unlock":
    return "unlock"
  else:
    return "command not supported"

def add(value, file):
  open_file = open(file, 'r+')
  data_array = open_file.readline().split(" ")
  if not value in data_array:
    open_file.write(value + " ")

def remove(value, file):
  open_file = open(file, 'r+')
  data_array = open_file.readline().split(" ")
  if value in data_array:
    open_file.close()
    data_array.remove(value)
    data_string = " ".join(data_array)
    open_file = open(file, 'w+')
    open_file.write(data_string + " ")

def lock():
  GPIO.setmode(GPIO.BOARD)
  servoPin = 11
  GPIO.setup(servoPin, GPIO.OUT)
  pwm = GPIO.PWM(servoPin, 50)
  pwm.start(7)
  time.sleep(0.5)
  pwm.ChangeDutyCycle(7)
  pwm.stop()

def unlock():
  GPIO.setmode(GPIO.BOARD)
  servoPin = 11
  GPIO.setup(servoPin, GPIO.OUT)
  pwm = GPIO.PWM(servoPin, 50)
  pwm.start(12)
  time.sleep(0.5)
  pwm.ChangeDutyCycle(12)
  pwm.stop()

@app.route("/", methods=['GET', 'POST'])
def incoming():

    incoming_message = request.values.get('Body', None).split(" ")
    sender_number = request.values.get('From', None)


    admin = admin_check(sender_number)
    user = user_check(sender_number)
    command = command_return(incoming_message)

    if len(incoming_message) > 2:
      value = incoming_message[2]
    else:
      value = None

    if admin or user:
      if command == "command not supported":
        message = "command not supported"
      elif command == "lock":
          lock()
          message = "safebox locked"
      elif command == "unlock":
          unlock()
          message = "safebox unlocked"
      else:
        if admin:
          if value == None:
            message = "no value given"
          else:
            if command == "add tracking":
              add(value, 'tracking.txt')
              message = "tracking number " + value + " added"
            if command == "remove tracking":
              remove(value, 'tracking.txt')
              message = "tracking number " + value + " removed"
            if command == "add user":
              add(value, 'users.txt')
              message = "user " + value + " added"
            if command == "remove user":
              remove(value, 'users.txt')
              message = "user " + value + " removed"
        else:
          message = "user not authorized"
    else:
      message = "user not authorized"

    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
