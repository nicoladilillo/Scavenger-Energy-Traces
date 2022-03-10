import sys
import bisect
import re

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

    # write Tco of I vs deltaT
    with open("TEG_I_vs_deltaT_Tco"+Toc+".txt",'w') as fw:
        fw.write("deltaT, I\n")
        # start from first value of Tho when I is not zero
        for Tho in range(int(Toc) + 20, 200, 5):
            # find the interval of Tho
            i = bisect.bisect_left(Tho_I_Toc, Tho)
            # linear interpolation
            if i == len(I_Toc):
                I_app = I_Toc[i-1]
            else:
                I_app = (I_Toc[i]-I_Toc[i-1])/(Tho_I_Toc[i]-Tho_I_Toc[i-1])*(Tho - Tho_I_Toc[i-1]) + I_Toc[i-1]
            
            # write new result file        
            fw.write(str(str(Tho-int(Toc)) +  ", " + str(round(I_app, 3)) + "\n"))

    # write Tco of V vs deltaT
    with open("TEG_V_vs_deltaT_Tco"+Toc+".txt",'w') as fw:
        fw.write("deltaT, V\n")
        # start from first value of Tho when V is not zero
        for Tho in range(int(Toc) + 20, 200, 5):
            # find the interval of Tho
            i = bisect.bisect_left(Tho_V_Toc, Tho)
            # linear interpolation
            if i == len(V_Toc):
                V_app = V_Toc[i-1]
            else:
                V_app = (V_Toc[i]-V_Toc[i-1])/(Tho_V_Toc[i]-Tho_V_Toc[i-1])*(Tho - Tho_V_Toc[i-1]) + V_Toc[i-1]
            
            # write new result file
            fw.write(str(str(Tho-int(Toc)) +  ", " + str(round(V_app, 3)) + "\n"))

