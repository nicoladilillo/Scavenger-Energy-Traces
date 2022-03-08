import csv
import random

# elaborate power for each timestamp
# open file to read and to write
with open("TEG_trace.csv",'r') as cvs_file_read, open("SolarCell1_trace.csv", 'w', newline='') as file_write:
    # read header, if it exists
    has_header = csv.Sniffer().has_header(cvs_file_read.read(1024))
    cvs_file_read.seek(0)
    
    #open csv to read
    csvreader = csv.reader(cvs_file_read)
    #open csv to write
    writer = csv.writer(file_write)

    #if there is header read first line ans save it
    if has_header:
        header = next(csvreader)
        writer.writerow(header)

    # read each timestamp and start elaboration of power
    for row in csvreader:
        # write a random value between 0 and 1000
        row[-1] = str(round(random.random()*1000, 3))
        # write new row
        writer.writerow(row)