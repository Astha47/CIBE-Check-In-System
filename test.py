import csv

DataMahasiswa = []

# Buka file CSV dan baca isinya
with open('src/IDMahasiswa.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    # Skip header
    next(reader, None)
    # Loop melalui baris-baris data
    for row in reader:
        # Tambahkan data ke dalam list
        DataMahasiswa.append(row)

# Cetak data


log = []
with open('src/log.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    # Skip header
    next(reader, None)
    # Loop melalui baris-baris data
    for row in reader:
        # Tambahkan data ke dalam list
        log.append(row)
print(log)

print()
import datetime

# Mendapatkan waktu lokal terkini
waktu_lokal = datetime.datetime.now()
print(waktu_lokal)
"""
for i in range(len(DataMahasiswa)):
    found = False
    if data == DataMahasiswa[i][0]:
        found = True
        indexFound = i
"""