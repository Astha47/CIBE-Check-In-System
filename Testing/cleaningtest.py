def pembersihLog(log):
    newLog = []
    for row in log:
        if row[2] != '':
            print(row[2])
            newLog += [row]
    return newLog

log = [['in','waiting','status'],['dasdad','sdadasd','asdasd'],['','',''],['dasda','','asdadad']]

newlog = pembersihLog(log)
print(newlog)