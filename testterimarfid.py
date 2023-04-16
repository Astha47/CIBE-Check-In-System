import serial
import time

# Konfigurasi serial port
port = "COM9"
baudrate = 9600
print("reading")
ser = serial.Serial(port, baudrate)

bacaan = 0
while True:
    bacaan += 1
    # Baca data dari serial port
    data = ser.readline().decode('latin-1').strip()
    if data:
        print("Ada data ke-",bacaan)
        # Bersihkan buffer masukan sebelum membaca data
        #ser.flushInput()
        # Tampilkan data ke layar
        print(data)
    else:
        # Tampilkan pesan "waiting" jika tidak ada data
        print("waiting")
    data = ''

    # Jeda 2 detik

