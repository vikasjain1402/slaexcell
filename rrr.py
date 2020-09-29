import openpyxl
import os
import datetime
path=os.path.join("/home/vikas/Desktop/",)
os.chdir(path)
wb=openpyxl.load_workbook("aaa.xlsx")
sh=wb.worksheets[0]
'''
finaldata=[{"incident_number":"123355",
            "pending":       [dict()],
            "Duration":     [dict()]
            }]
'''

finaldata=[]
InTcs=False
pre_inc=sh[0][0]
print(pre_inc)
for line in sh:
    ag=line[12].value
    av=line[13].value
    mst=line[14].value
    met=line[15].value
    inc = line[0].value
    while inc==pre_inc:


    in_data={}
    in_data["Incident Number"]=inc

    if ("TCS" in av):
        try:
            in_data['Duration'].append({"st":mst,"et":met})
        except:
            in_data['Duration']=[{"st": mst, "et": met}]
    if ("Pending" in av or "Resolved" in av) and InTcs:
        try:
            in_data['Pending'].append({"st":mst,"et":met})
        except:
            in_data['Pending']=[{"st": mst, "et": met}]
    else:
        InTcs=False

finaldata.append(in_data)


print(finaldata[1:5])