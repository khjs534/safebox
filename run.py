from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def incoming():

    incoming_message = request.values.get('Body', None).split(" ")
    message_sender = request.values.get('From', None)

    if incoming_message[0].lower() == 'set':
      database = open('database.txt', 'r+')
      tracking = database.readline().split(" ")
      if not incoming_message[1] in tracking:
        database.write(incoming_message[1] + " ")
        message = "access code set to: " + incoming_message[1]
      else:
        message = "number already exists"
    elif incoming_message[0].lower() == 'unlock':
      database = open('database.txt', 'r+')
      data_array = database.readline().split(" ")
      if incoming_message[1] in data_array:
        message = "access granted"
        database.close()
        data_array.remove(incoming_message[1])
        data_string = " ".join(data_array)
        print data_string
        database_2 = open('database.txt', 'w+')
        database_2.write(data_string + " ")
      else:
        message = "access denied"
    elif " ".join(incoming_message.lower()) == 'open the pod bay doors hal':
      message = 'i\'m sorry dave, i\'m afraid i can\'t do that'
    else:
      message = 'input not recognized'

    print incoming_message

    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
