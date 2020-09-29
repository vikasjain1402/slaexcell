import openpyxl
import os
import datetime
from supportings import  workingdayscalc

path=os.path.join("/home/vikas/Desktop/",)
os.chdir(path)
wb=openpyxl.load_workbook("aaa.xlsx")
sh=wb.worksheets[0]

InTCS=False
pre_Inc=None
final_data=dict()
in_data=None
debug = "INC6925201"

for line in sh:
    ag=line[12].value
    av=line[13].value
    mst=line[14].value
    met=line[15].value
    inc = line[0].value

    in_data=dict()

    if ("TCS" in av) and ag=="Assignment Group":
        InTCS=True
        if final_data.get(inc,None)==None:
            final_data[inc] = {}
            final_data[inc]['Duration'] = [{"st": mst, "et": met}]
        else:
            final_data[inc]['Duration'].append({"st": mst, "et": met})
        continue

    if (("Pending" == av) or ("Resolved" == av)) and InTCS:
        if final_data.get(inc,None)==None:
            final_data[inc] = {}
            final_data[inc]['Pending'] = [{"st": mst, "et": met}]
        else:
            if final_data[inc].get('Pending',None)==None:
                final_data[inc]['Pending']=[]
                final_data[inc]['Pending'].append({"st": mst, "et": met})
            else:
                final_data[inc]['Pending'].append({"st": mst, "et": met})
        continue
    else:
        InTCS=False
        continue

for i in final_data:
    #if debug==i:
     #   input(f"{final_data[i]}pause press enter")
    totaltimeOutage=datetime.timedelta(0)
    for j in final_data[i]['Duration']:
        totaltimeOutage+=j['et']-j['st']

    totaltimeOutageexcweekend=0
    for j in final_data[i]['Duration']:
        totaltimeOutageexcweekend+=workingdayscalc(j['st'],j['et'])

    print(i,"Total Outage={:.2f}".format(totaltimeOutage.days+totaltimeOutage.seconds/(3600*24))," # ",totaltimeOutageexcweekend ,end=" Pending\Resolved=")

    totaltime = 0
    for jj in final_data[i]['Pending']:
        totaltime+=workingdayscalc(jj['st'],jj['et'])
        #if debug == i:
         #   input(f"{totaltime}pause press enter")
    print(totaltime)
    #print("={:.2f}".format(totaltime.days+totaltime.seconds/(3600*24)))


