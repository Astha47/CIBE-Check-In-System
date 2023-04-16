import time
import serial

port = 'COM9'  # ganti dengan nama port yang sesuai
baudrate = 9600

# inisialisasi koneksi serial
ser = serial.Serial(port, baudrate)
ser.flushInput()

# kirimkan "allow" dan "deny" bergantian dengan jarak 2 detik
while True:
    ser.write(b'allow\n')
    print('Mengirim allow')
    time.sleep(2)
    
    ser.write(b'deny\n')
    print('Mengirim deny')
    time.sleep(2)
