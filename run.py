from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

def admin_check(sender_number):
  admin_number = open('admin.txt', 'r')
  admin_number = admin_number.readline()
  if admin_number == sender_number:
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

def add_tracking(value):
  tracking = open('tracking.txt', 'r+')
  tracking_array = tracking.readline().split(" ")
  if not value in tracking_array:
    tracking.write(value + " ")

def remove_tracking(value):
  tracking_file = open('tracking.txt', 'r+')
  tracking_array = tracking_file.readline().split(" ")
  if value in tracking_array:
    tracking_file.close()
    tracking_array.remove(value)
    tracking_string = " ".join(tracking_array)
    tracking_file = open('tracking.txt', 'w+')
    tracking_file.write(tracking_string + " ")
  
# def add_user(value):

# def remove_user(value):


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
          message = "safebox locked"
      elif command == "unlock":
          message = "safebox unlocked"
      else:
        if admin:
          if value == None:
            message = "no value given"
          else:
            if command == "add tracking":
              add_tracking(value)
              message = "tracking number " + value + " added"
            if command == "remove tracking":
              remove_tracking(value)
              message = "tracking number " + value + " removed"
            if command == "add user":
              add_user(value)
              message = "user " + value + " added"
            if command == "remove user":
              remove_user(value)
              message = "user " + value + " removed"
        else:
          message = "user not authorized"
    else:
      message = "user not authorized"
       



    # if incoming_message[0].lower() == 'set':
    #   database = open('database.txt', 'r+')
    #   tracking = database.readline().split(" ")
    #   if not incoming_message[1] in tracking:
    #     database.write(incoming_message[1] + " ")
    #     message = "access code set to: " + incoming_message[1]
    #   else:
    #     message = "number already exists"
    # elif incoming_message[0].lower() == 'unlock':
    #   database = open('database.txt', 'r+')
    #   data_array = database.readline().split(" ")
    #   if incoming_message[1] in data_array:
    #     message = "access granted"
    #     database.close()
    #     data_array.remove(incoming_message[1])
    #     data_string = " ".join(data_array)
    #     print data_string
    #     database_2 = open('database.txt', 'w+')
    #     database_2.write(data_string + " ")
    #   else:
    #     message = "access denied"
    # else:
    #   message = 'input not recognized'

    print incoming_message

    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
