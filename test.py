import csv
# Load Data Utama ID
DataMahasiswa = []
with open('src/IDMahasiswa.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    next(reader, None)
    # Loop melalui baris-baris data
    for row in reader:
        # Tambahkan data ke dalam list
        DataMahasiswa.append(row)
print(DataMahasiswa)

# Load Data Log
log = []
with open('src/log.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    # Loop melalui baris-baris data
    for row in reader:
        # Tambahkan data ke dalam list
        log.append(row)
print(log)

# Load Data Logs
logs = []
with open('src/logs.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    # Loop melalui baris-baris data
    for row in reader:
        # Tambahkan data ke dalam list
        logs.append(row)
print(logs)