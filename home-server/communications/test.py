int_encdoe = b'3'
import serial
ser = serial.Serial( '/dev/rfcomm0', 115200)
ser.write(b'3')
