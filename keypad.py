from matrix_keypad import RPi_GPIO

# kp = RPi_GPIO.keypad()

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
    print code
  return code

print access()
