from collections import *
import math
import time
import sys

f=open("hmmmodel.txt","w")

def unique_keys(k):
    res=[]
    res1=[]
    for i in k:
        res.append(i.split("|")[-1])
        res1.append(i.split("|")[0])
    r=set(res)
    rr=set(res1)
    return r,rr

def write_to_file(type,pp):
    k=pp.keys()
    f=open("hmmmodel.txt","a")
    for i in k:
        f.write(type+":"+i+":"+str(pp[i])+"\n")
    f.close()

def make_prob(type,p):
    k=p.keys()
    res={}
    states,o1=unique_keys(k)
    for st in states:
        if type=="O":
            fil_k=[x for x in k if x.endswith("|"+st)]
        else:
            fil_k=[x for x in k if x.endswith("|"+st)]
        total=0
        #total=sum([float(p[i])
        if type=="O":
            total=len(o1)
            s=0
        else:
            total=0
            s=1
        for i in fil_k:
            total+=float(p[i])
            #print p[i]
        #print st+":"+str(len(fil_k))
        for f in fil_k:
            res[f]=math.log(float(p[f])/float(total))
        if type=="O":
            res["***|"+st]=math.log(float(1)/float(total))
        else:
            res["****|"+st]=math.log(float(1)/float(total))
    for st in states:
        f=[res[x] for x in res if x.endswith("|"+st)]
        #print st+"!"+str(sum(f))
    write_to_file(type,res)
    return res

start=time.time()
count_t=defaultdict(lambda:0)
count_o=defaultdict(lambda:1)
with open("catalan_corpus_train_tagged.txt","r") as f:
    lines=f.readlines()
for l in lines:
    tokens=l.split()
    pre=tokens[0].split("/")[-1]
    count_t[pre+"|q0"]+=1
    for t in tokens[1:]:
        temp=t.split("/")
        cur=temp[-1]
        word="/".join(temp[:-1])
        count_o[word+"|"+cur]+=1
        count_t[cur+"|"+pre]+=1
        pre=cur
prob_t=make_prob("T",count_t)
prob_o=make_prob("O",count_o)
end=time.time()
print str(end-start)
f.close()
