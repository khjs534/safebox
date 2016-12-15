from twilio.rest import TwilioRestClient

# put your own credentials here
# credemtials removed for git push
ACCOUNT_SID = "ACCOUNT_SID"
AUTH_TOKEN = "AUTH_TOKEN"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

message = client.messages.create(to="+17739729168", from_="+17734668069",
                                 body="Hello there!")
