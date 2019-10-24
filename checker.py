import os, sys

def checkerf(filename, problemid):
    #print(filename, problemid)
    os.system('python3 %s < problems/%d.in > problems/%d_t.out'%(filename,problemid,problemid))
    data1 = open('problems/%d_t.out'%problemid).read()
    data2 = open('problems/%d.out'%problemid).read()
    os.remove('problems/%d_t.out'%problemid)
    if data1 == data2:
        return 'ACCEPTED'
    else:
        return 'WRONG ANSWER'
