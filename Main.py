# Code By ChatGPT

# Menggunakan serial port (USB)
# instal terlebh dahulu module serial
# sintaks di terminal/powershell : pip install pyserial
# bila import serial masih tak terdeteksi, ikuti tutorial : https://www.youtube.com/watch?v=Pf-cGzOQmXU

import serial
import time

ser = serial.Serial('COM4', 9600)  # buka koneksi serial dengan port USB dan baudrate 9600

while True:
    if ser.in_waiting > 0:  # jika ada data yang tersedia di buffer
        data = ser.readline().decode().rstrip()  # baca data dari serial dan hapus karakter newline
        print(data)  # tampilkan data di console
    else:
        print("waiting data")
        time.sleep(5)



# install module :pip install pybluez (kemungkinan tidak bisa karena outdated)
# jika gagal silakan install dari : https://github.com/pybluez/pybluez
# untuk install manual silakan buka cmd pada folder instalasi dan ketikkan : py setup.py install
# kondisi : aku masih gagal instalasi
"""
import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

print("Menunggu koneksi pada channel %d..." % port)

client_sock, client_info = server_sock.accept()
print("Menghubungkan ke", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0:
            break
        print("Data diterima:", data.decode())
except OSError:
    pass

print("Koneksi ditutup")

client_sock.close()
server_sock.close()

"""

