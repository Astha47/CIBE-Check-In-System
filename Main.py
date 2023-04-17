# Code By ChatGPT

# Menggunakan serial port (USB)
# instal terlebh dahulu module serial
# sintaks di terminal/powershell : pip install pyserial
# bila import serial masih tak terdeteksi, ikuti tutorial : https://www.youtube.com/watch?v=Pf-cGzOQmXU

import serial
import time
import csv
import datetime

# Mendapatkan waktu lokal terkini
waktu_lokal = datetime.datetime.now()

# INISIASI VARIABEL
MaxCapacity = 26
MaxNonFTSL = 9

ser = serial.Serial('COM9', 9600)  # buka koneksi serial dengan port USB dan baudrate 9600

def menulisLogs(id,logs):
    # Mencari keberadaan logs
    logsStatus = False
    idlogs = 0
    for i in range(len(logs)):
        if logs[i][0] == id:
            if logs[i][2]:
                logs[i][2] = str(datetime.datetime.now())
                logsStatus = True
                break
    
    if logsStatus == False:
        logs += [[id,str(datetime.datetime.now()),'']]
    tulis_matriks_ke_file(logs,'src/logs.csv')

def tulis_matriks_ke_file(matrix, name_file):
    with open(name_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in matrix:
            writer.writerow(row)

def loadData(name,header):
    data = []
    with open('src/'+name) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            if header:
                # Loop melalui baris-baris data
                for row in reader:
                    # Tambahkan data ke dalam list
                    data.append(row)
            else:
                next(reader, None)
                # Loop melalui baris-baris data
                for row in reader:
                    # Tambahkan data ke dalam list
                    data.append(row)
    return data



while True:
    id = ser.readline().decode('latin-1').strip()  # baca data dari serial 
    if id:  # jika ada data yang tersedia di buffer
        print("Ada data")
        print(id)  # tampilkan data di console
        print("membaca data")

        #Bagian validasi dan pengecekan

        # Load Data Utama ID
        DataMahasiswa = loadData('IDMahasiswa.csv',False)
        print("Data Mahasiswa : ",DataMahasiswa)

        # Load Data Log
        log = loadData('log.csv',True)
        #print('Log : ',log)
        
        # Load Data Logs
        logs = loadData('logs.csv',True)
        #print('Logs : ',logs)

        # Mencari validasi ID
        for i in range(len(DataMahasiswa)):
            found = False
            if id == DataMahasiswa[i][0]:
                found = True
                datamasuk = DataMahasiswa[i]
                break
        
        # Mencari ID di log
        if found:
            # Cari di log masuk

            # Initializing status
            status = 'Unregistered'


            print("log =",log)
            for i in range(len(log)):
                for j in range(2):
                    if log[i][j] == id:
                        # Hapus ID
                        log[i][j] == ''
                        log[i][2] == ''
                        status = 'Registered'
                        # Menulis logs
                        #logs = menulisLogs(id,logs) ===================
                        # Kirim data untuk menjalankan aktuator bernilai allow
                        ser.write(b'allow\n')
            
            if status == 'Unregistered':
                # Hitung jumlah orang yang ada di dalam
                JumlahFTSL = 0
                JumlahNonFTSL = 0
                for i in range(len(log)):
                    if log[i][2] == "FTSL":
                        JumlahFTSL += 1
                    elif log[i][2] == "Non-FTSL":
                        JumlahNonFTSL += 1
                JumlahTotal = JumlahFTSL + JumlahNonFTSL

                if datamasuk[3] == "FTSL":
                    if JumlahTotal <MaxCapacity:
                        log += [[id,'','FTSL']]
                        print('Mendapat tempat duduk')
                        # Kirim data untuk menjalankan aktuator bernilai allow
                        ser.write(b'allow\n')
                    else:
                        log += [['',id,'FTSL']]
                        print('waiting')
                        # Kirim data untuk menjalankan aktuator bernilai allow
                        ser.write(b'allow\n')
                    logs += [[id,str(datetime.datetime.now()),'']]
                else:
                    if JumlahTotal < MaxCapacity and JumlahNonFTSL < MaxNonFTSL:
                        log += [[id,'','Non-FTSL']]
                        print('Dipersilahkan masuk, selamat datang',datamasuk[2])
                        # Kirim data untuk menjalankan aktuator bernilai allow
                        ser.write(b'allow\n')
                    else:
                        print('ditolak')
                        # Kirim data untuk menjalankan aktuator bernilai deny
                        ser.write(b'deny\n')

            elif status == 'Registered':
                # Mengecek apakah ada orang di waiting
                AdaWaiting = False
                idWaiting = 0
                for i in range(len(log)):
                    if log[i][1]:
                        AdaWaiting = True
                        idWaiting = i
                        break
                if AdaWaiting:
                    log += [[log[idWaiting][1],'',log[idWaiting][2]]]
                    log[idWaiting][1] = ''
                    log[idWaiting][2] = ''

            #tulis_matriks_ke_file(log,'src/log.csv') ============
        else:
            print('ID Tidak dikenali')
            print('ditolak')
            # Kirim data untuk menjalankan aktuator bernilai deny
            ser.write(b'deny\n')

        
    else:
        print("waiting data")
        time.sleep(1)

#debug


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

