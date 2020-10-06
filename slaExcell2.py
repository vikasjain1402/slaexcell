import openpyxl
import os
import datetime
from supportings import  workingdayscalc
from datalookup import tcsRoles

direc=os.getcwd()
filname="TCS.xlsx"
os.chdir(direc)
print(f"Loading File :{filname}....")
wb=openpyxl.load_workbook(filname)
sh=wb.worksheets[2]
print("Done")
InTCS=False
pre_Inc=None
final_data=dict()
in_data=None

for line in sh:
    if "Incident Number" == line[0].value:
        continue
    ig = line[4].value
    ag=line[12].value
    av=line[13].value
    mst=line[14].value
    met=line[15].value
    inc = line[0].value

    in_data=dict()


    if (av in tcsRoles) and( ag=="Assignment Group") and (ig in tcsRoles):
        InTCS=True
        if final_data.get(inc,None)==None:
            final_data[inc] = {}
            final_data[inc]['Duration'] = [{"st": mst, "et": met}]
        else:
            final_data[inc]['Duration'].append({"st": mst, "et": met})
        continue

    if (("Pending" == av) or ("Resolved" == av)) and InTCS:
        if av=="Resolved":
            final_data[inc]["Resolved"]=met-mst+final_data[inc].get("Resolved",datetime.timedelta(0))

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

dbugid=None
if dbugid is not None:
    print(final_data[debugid]['Duration'])
    print(final_data[debugid]['Pending'])
    print(final_data[debugid]['Resolved'].seconds)
    print(final_data[debugid]['Resolved'].days)
    input("press any key to resume")
excellist=[]
for i in final_data:
    totaltimeOutage=datetime.timedelta(0)

    for j in final_data[i]['Duration']:
        totaltimeOutage+=j['et']-j['st']

    totaltimeOutageexcweekend=0
    for j in final_data[i]['Duration']:
        totaltimeOutageexcweekend+=workingdayscalc(j['st'],j['et'])



    totaltime = 0
    for jj in final_data[i]['Pending']:
        totaltime+=workingdayscalc(jj['st'],jj['et'])

    totaltime1=datetime.timedelta(0)
    for jj in final_data[i]['Pending']:
        totaltime1+=jj['et']-jj['st']

    print(i,
          totaltime1.days+totaltime1.seconds/(24*3600),
          totaltimeOutage.days+totaltimeOutage.seconds/(24*3600),
          totaltimeOutageexcweekend,totaltime,final_data[i]["Resolved"].days+final_data[i]["Resolved"].seconds/(24*3600),sep="#")
    excellist.append([i,totaltime1.days+totaltime1.seconds/(24*3600),totaltimeOutage.days+totaltimeOutage.seconds/(24*3600),totaltimeOutageexcweekend,totaltime,final_data[i]["Resolved"].days+final_data[i]["Resolved"].seconds/(24*3600)])
filname="TCS_output.xlsx"
path=os.path.join(direc,filname)

os.chdir(direc)
print(f"\n Writing file {filname}...",end=" ")
wb = openpyxl.Workbook()
ws = wb.active
for i in excellist:
    ws.append(i)
wb.save(filname)
print("Done")
