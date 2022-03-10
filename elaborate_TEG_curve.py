import sys
import bisect

# parameters
max_Tho   = 200
min_delta = 20

# start dictionary with all possible deltaT, then discharged the empty one
I_dictionary = {k: [] for k in range(min_delta, max_Tho, 5)}
V_dictionary = {k: [] for k in range(min_delta, max_Tho, 5)}

# pass all value of Tco of digilatize curve and elaborate it
for Toc in sys.argv[1:]:
    # opena Tco digitalize cuve of load current and load voltage
    with open("TEG_I_Tco"+Toc+".txt",'r') as I_read, open("TEG_V_Tco"+Toc+".txt", 'r') as V_read:
        next(I_read)
        I_Toc     = []
        Tho_I_Toc = []
        for row in I_read:
            app = row.split(', ')
            Tho_I_Toc.append(float(app[0]))
            I_Toc.append(float(app[1]))

        next(V_read)
        V_Toc     = []
        Tho_V_Toc = []
        for row in V_read:
            app = row.split(', ')
            Tho_V_Toc.append(float(app[0]))
            V_Toc.append(float(app[1]))
    

    Toc = int(Toc)

    # elaborate I vs deltaT
    # start from first value of Tho when I is not zero
    for Tho in range(Toc + min_delta, max_Tho, 5):
        # find the interval of Tho
        i = bisect.bisect_left(Tho_I_Toc, Tho)
        # linear interpolation
        if i == len(I_Toc):
            I_app = I_Toc[i-1]
        else:
            I_app = (I_Toc[i]-I_Toc[i-1])/(Tho_I_Toc[i]-Tho_I_Toc[i-1])*(Tho - Tho_I_Toc[i-1]) + I_Toc[i-1]
        
        # save value to corresponding delta       
        I_dictionary[Tho-Toc].append(round(I_app, 3))

    # elaborate V vs deltaT
    # start from first value of Tho when V is not zero
    for Tho in range(Toc + min_delta, max_Tho, 5):
        # find the interval of Tho
        i = bisect.bisect_left(Tho_V_Toc, Tho)
        # linear interpolation
        if i == len(V_Toc):
            V_app = V_Toc[i-1]
        else:
            V_app = (V_Toc[i]-V_Toc[i-1])/(Tho_V_Toc[i]-Tho_V_Toc[i-1])*(Tho - Tho_V_Toc[i-1]) + V_Toc[i-1]
        
        # save value to corresponding delta
        V_dictionary[Tho-Toc].append(round(V_app, 3))

# create file for dela quantity (I, V)
for deltaT in I_dictionary.keys():
    if len(I_dictionary[deltaT]) > 0:
        zip_object = zip(I_dictionary[deltaT], V_dictionary[deltaT])
        with open("TEG_"+str(deltaT)+".txt",'w') as I_V_curve:
            I_V_curve.write("A, V\n")
            for I, V in zip_object:
                I_V_curve.write(str(I) + ", " + str(V) + "\n")
