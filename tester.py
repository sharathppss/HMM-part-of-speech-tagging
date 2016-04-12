from collections import *

out=open("result.txt","w")
correct=defaultdict(int)
total=defaultdict(int)
c=0
t=0
f2=open("catalan_corpus_dev_tagged.txt","r")
with open("output.txt","r") as f1:
   l1=f1.readlines()
   l2=f2.readlines()
   for i in range(len(l1)):
       inp1=l1[i]
       inp2=l2[i]
       p1=inp1.split()
       p2=inp2.split()
       if len(p1)!=len(p2):
           print "ERROR"+str(p1)
       for i in range(len(p1)):
           if p1[i].split("/")[-1]==p2[i].split("/")[-1]:
               correct[p1[i].split("/")[-1]]+=1
               c+=1
               out.write(p1[i]+"|"+p2[i]+"|"+"correct"+"\n")
           else:
               out.write(p1[i]+"|"+p2[i]+"|"+"wrong"+"\n")
           total[p2[i].split("/")[-1]]+=1
           t+=1
           #total+=1
for x in total.keys():
    print x+":"+str((float(correct[x])/float(total[x])))+":"+str(correct[x])+":"+str(total[x])
print c,t
x=float(c)/float(t)
print x