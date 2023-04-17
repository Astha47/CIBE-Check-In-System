# Menggunakan serial port (USB)
# instal terlebh dahulu module serial
# sintaks di terminal/powershell : pip install pyserial
# bila import serial masih tak terdeteksi, ikuti tutorial : https://www.youtube.com/watch?v=Pf-cGzOQmXU

import serial
import time
import csv
import datetime
import os

# Mendapatkan waktu lokal terkini
waktu_lokal = datetime.datetime.now()

# INISIASI VARIABEL
MaxCapacity = 26
MaxNonFTSL = 9

ser = serial.Serial('COM9', 9600)  # buka koneksi serial dengan port USB dan baudrate 9600

def menulisLogs(nim,logs):
    # Mencari keberadaan logs
    logsStatus = False
    idlogs = 0
    for i in range(len(logs)):
        if logs[i][0] == nim:
            if (logs[i][2]) == '':
                logs[i][2] = str(datetime.datetime.now())
                logsStatus = True
                break
    
    if logsStatus == False:
        logs += [[nim,str(datetime.datetime.now()),'']]
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

os.system('cls')

while True:
    print("CIBE Check-In System V-Alpha")
    print("Silakan tempelkan kartu Anda!")
    print()
    id = ser.readline().decode('latin-1').strip()  # baca data dari serial 
    if id:  # jika ada data yang tersedia di buffer
        os.system('cls')
        print("CIBE Check-In System V-Alpha")
        
        print("============================")
        print("Kartu terbaca")
        #print(id)  # tampilkan data di console
        print()
        print("Memverifikasi data....")
        print("============================")

        #Bagian validasi dan pengecekan

        # Load Data Utama ID
        DataMahasiswa = loadData('IDMahasiswa.csv',False)

        #DEBUG
        #print("Data Mahasiswa : ",DataMahasiswa)

        # Load Data Log
        log = loadData('log.csv',True)

        #DEBUG
        #print('Log awal : ',log)
        
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


            #print("log =",log)
            for i in range(len(log)):

                # DEBUG
                #print("panjang log = ",len(log))
                #print("pengecekan baris ke-",i,"dijalanlan.")

                for j in range(2):
                    if log[i][j] == id:
                        # Hapus ID
                        log[i][j] = ''
                        log[i][2] = ''

                        # Menuliskan log pada file
                        tulis_matriks_ke_file(log,'src/log.csv')

                        # Tuliskan pesan pada layar
                        print('Logout berhasil, sampai berjumpa lagi',datamasuk[2]+'!')

                        # DEBUG
                        #print('ID Terdapat dalam log!')
                        #print('lokasi baris = ',i)
                        #print('lokasi kolom = ',j)
                        status = 'Registered'

                        # Menulis logs
                        logs = menulisLogs(datamasuk[1],logs)

                        # Kirim data untuk menjalankan aktuator bernilai allow
                        ser.write(b'allow\n')

                        # DEBUG
                        #print("log = ", log)

                        # Menunggu Sensor Pendeteksi / Input Tombol
                        passSensor = ser.readline().decode().strip()
                        print("passSensor = ",passSensor)
                        if passSensor:
                            os.system('cls')
            
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

                # DEBUG
                #print("Jumlah total : ",JumlahTotal)

                if datamasuk[3] == "FTSL":
                    if JumlahTotal <MaxCapacity:
                        log += [[id,'','FTSL']]
                        print('Selamat datang',datamasuk[2],'di Co-Working Space CIBE')
                        # Kirim data untuk menjalankan aktuator bernilai allow
                        ser.write(b'allow\n')

                        # Menunggu Sensor Pendeteksi / Input Tombol
                        passSensor = ser.readline().decode().strip()
                        if passSensor:
                            os.system('cls')
                    else:
                        log += [['',id,'FTSL']]
                        print('waiting')
                        # Kirim data untuk menjalankan aktuator bernilai allow
                        ser.write(b'allow\n')



                        # Menunggu Sensor Pendeteksi / Input Tombol
                        passSensor = ser.readline().decode().strip()
                        if passSensor:
                            os.system('cls')
                    
                    # Menulis logs
                    logs = menulisLogs(datamasuk[1],logs)

                    # DEBUG
                    #print("logs = ",logs)
                else:
                    if JumlahTotal < MaxCapacity and JumlahNonFTSL < MaxNonFTSL:

                        # Tambahkan LOG
                        log += [[id,'','Non-FTSL']]
                        # Tulis LOG pada penyimpanan
                        tulis_matriks_ke_file(log,'src/log.csv')
                        # Pesan pada layar
                        print()
                        print('Dipersilahkan masuk, selamat datang',datamasuk[2]+"!")
                        # Kirim data untuk menjalankan aktuator bernilai allow
                        ser.write(b'allow\n')

                        # Tulis data masuk pada logs
                        # Menulis logs
                        logs = menulisLogs(datamasuk[1],logs)
                        # DEBUG
                        #print("logs = ",logs)
                        #print("log  = ",log)

                        # Menunggu Sensor Pendeteksi / Input Tombol
                        passSensor = ser.readline().decode().strip()
                        if passSensor:
                            os.system('cls')
                    else:
                        print('ditolak')
                        # Kirim data untuk menjalankan aktuator bernilai deny
                        ser.write(b'deny\n')
                        time.sleep(3)
                        os.system('cls')

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
            print()
            print('ID Tidak dikenali, Coba lagi!')
            print('Akses masuk ditolak')
            # Kirim data untuk menjalankan aktuator bernilai deny
            ser.write(b'deny\n')
            time.sleep(3)
            os.system('cls')

        
    else:
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

