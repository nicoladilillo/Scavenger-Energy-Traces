import csv
import sys
import bisect
import re

# calculate exponent according to order of magnitude of unit
def order_of_magnitude(unit):
    magnitude = 10**(0)
    order = re.findall("[mup]", unit)

    if len(order) >= 1:
        if order[0] == 'm':
            magnitude = 10**(-3)
        elif order[0] == 'u':
            magnitude = 10**(-6)
        elif order[0] == 'p':
            magnitude = 10**(-9)

    return magnitude

# calculate the MPP for each curve file
curves = { 0 : "0"}
for curve_file_name in sys.argv[2:]:
    # extrapolate the quantity value from file name
    value = str(curve_file_name).split('_')[1].split('.')[0]
    # print(value)
    with open(curve_file_name, 'r') as file:
        # elaboate order of magnitude for current and voltage
        header = next(file)
        header = header.split(',')
        current_order = order_of_magnitude(header[0].strip())
        voltage_order = order_of_magnitude(header[1].strip())
        # select MPP for each curve, power is consider in Watt
        MPP = 0
        for line in file.readlines():
            I_V = line.split(",")
            I   = float(I_V[1].strip())
            V   = float(I_V[0].strip())
            P   = I*V
            if P > MPP:
                MPP = P
        # adapt power to order of magnitude, the final unit will be W
        curves[float(value)] = MPP*current_order*voltage_order

# save name of product
product_name = curve_file_name.split('_')[0]

# sorted curve for increase irradiance
keys = []
items = []
for i in sorted(curves):
    keys.append(float(i))
    items.append(float(curves.get(i)))
size = len(keys)

# elaborate power for each timestamp
# open file to read and to write
with open(str(sys.argv[1]),'r') as cvs_file_read, open(product_name + "_output.csv", 'w', newline='') as file_write:
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
        header[-1] = "Power[W]"
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

        # change value of quantity with power value, saved in exponential way
        row[-1] = "{:0.4e}".format(y)
        # write new row
        writer.writerow(row)