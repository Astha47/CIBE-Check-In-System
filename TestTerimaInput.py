import serial
import time
import os

# Konfigurasi serial port
port = "COM9"
baudrate = 9600
ser = serial.Serial(port, baudrate)

bacaan = 0
while True:
    bacaan += 1
    # Baca data dari serial port
    data = str(ser.readline().decode().strip())
    if data:
        os.system('cls')
        print("Ada data ke-",bacaan)
        # Bersihkan buffer masukan sebelum membaca data
        print("Membaca data")
        ser.flushInput()
        print("Data berhasil dibaca")
        # Tampilkan data ke layar
        print(data)
    else:
        # Tampilkan pesan "waiting" jika tidak ada data
        print("waiting")
    data = ''

    # Jeda 2 detik
