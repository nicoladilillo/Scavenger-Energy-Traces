import csv
import sys
import bisect

curves = { 0 : "0"}
for curve_file_name in sys.argv[2:]:
    # extrapolate the quantity value from file name
    value = str(curve_file_name).split('_')[1].split('.')[0]
    # print(value)
    with open(curve_file_name, 'r') as file:
        MPP = 0
        # print(value)
        for line in file.readlines():
            I_V = line.split(",")
            I   = float(I_V[1].strip())
            V   = float(I_V[0].strip())
            P   = I*V
            if P > MPP:
                MPP = P
        # select MPP for curve
        curves[float(value)] = MPP

# sorted curve for increase irradiance
keys = []
items = []
for i in sorted(curves):
    keys.append(float(i))
    items.append(float(curves.get(i)))
size  = len(keys)

# elaborate power for each timestamp
# open csv to read and craeate result csv file
with open(str(sys.argv[1]),'r') as cvs_file_read, open("output.csv", 'w', newline='') as file_write:
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
        header[-1] = "Power"
        writer.writerow(header)

    # read each timestamp and start elaboration of power
    for row in csvreader:
        quantity = float(row[-1])
        # find the interval of quantity
        i = bisect.bisect_left(keys, quantity)
        # check if i is out of boundary and saturate result
        if i == size:
            y = items[-1]
        elif i == 0:
            y = 0
        else :
            # linear interpolation
            y = (items[i]-items[i-1])/(keys[i]-keys[i-1])*(quantity - keys[i-1]) + items[i-1]

        row[-1] = round(y,4)
        writer.writerow(row)