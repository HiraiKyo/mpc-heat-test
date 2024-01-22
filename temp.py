import serial

temp_current = 0
is_alive = True

def listen_temp(arduino_port, baudrate, timeout):
  arduino_serial = serial.Serial(arduino_port, baudrate=baudrate, timeout=timeout)
  while is_alive:
    line = arduino_serial.readline()
    temp = float(line.decode().replace("inner_temp=", ""))  
    global temp_current
    temp_current = temp
    
def get_temp():
  global temp_current
  return temp_current

def stop():
  global is_alive
  is_alive = False