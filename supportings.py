import datetime
et=datetime.datetime.now()
st=datetime.datetime.now()-datetime.timedelta(seconds=14*3600)

def maxmin(dated,maxi=True):
    y,m,d=dated.year,dated.month,dated.day
    if maxi==True:
        maxminval=datetime.datetime(y,m,d,23,59,59,99999)
    else:
        maxminval = datetime.datetime(y, m, d, 00, 00, 00, 00000)
    return maxminval


def workingdayscalc(sd,et):

    days=0
    d1=datetime.timedelta(days=1)
    if et.date()==sd.date():
        if et.weekday()<5:
            return (et-sd).seconds/(24*3600)
        else:
            return 0
    days+=((maxmin(sd,maxi=True)-sd).seconds)/(24*3600) if sd.weekday()<5 else 0
    days+=((et-maxmin(et, maxi=False)).seconds)/(24 * 3600) if et.weekday()<5 else 0
    sd+=d1
    sd=maxmin(sd,maxi=False)
    et=maxmin(et,maxi=False)
    while sd<et:
        if sd.weekday()<5:
            days+=1
        sd+=d1

    return days

if __name__=="__main__":
    st=datetime.datetime(2020, 6, 24, 16, 12, 4)
    et=datetime.datetime(2020, 6, 25, 4, 57, 5)
    print(workingdayscalc(st, et))
    st=datetime.datetime(2020, 6, 25, 4, 57, 5)
    et=datetime.datetime(2020, 6, 25, 5, 47, 13)
    print(workingdayscalc(st, et))
    st=datetime.datetime(2020, 6, 25, 5, 47, 13)
    et=datetime.datetime(2020, 7, 1, 4, 0, 18)
    print(workingdayscalc(st, et))
    st=datetime.datetime(2020, 6, 25, 6, 7, 46)
    et=datetime.datetime(2020, 6, 26, 3, 38, 24)
    print(workingdayscalc(st, et))
    st=datetime.datetime(2020, 6, 26, 3, 38, 24)
    et=datetime.datetime(2020, 7, 1, 4, 0, 18)
    print(workingdayscalc(st, et))
