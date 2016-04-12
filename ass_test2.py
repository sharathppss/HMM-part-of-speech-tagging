# -*- coding: utf-8 -*-
import operator
import time
from collections import *
from collections import deque

def unique_keys(k):
    res=[]
    for i in k:
        if(i.startswith("****")):
            continue
        res.append(i.split("|")[0])
    r=set(res)
    return r

def back_track(back,mp,wlen,words):
    res=deque()
    pre=mp
    res.appendleft(words[wlen-1]+"/"+pre)
    for i in range(wlen-1,0,-1):
        pre=back[i][pre]
        res.appendleft(words[i-1]+"/"+pre)
    return res

def bias_estimate(xx):
    if xx[0].isupper():
        return 6,"NP"
    elif len([c for c in xx if c.isdigit()])>len(xx)/2:
        return 6,"ZZ"
    elif [u for u in xx.split("_") if u in ["gener","febrer","març","abril","maig","juny","juliol","agost","setembre","octubre","novembre","desembre"]]!=[]:
        return 6,"WW"
    elif xx in ["AixÃ²","tal","AÃ§Ã²"]:
        return 6,"PD"
    return 0,"XX"

def hmm(p_t,p_o,words,Q,next,WA):
    prob={}
    back={}
    temp1=defaultdict(lambda :-99999)
    temp2={}
    for q in Q:
        #temp1[q]=probtran(p_t,q,"q0")+probobs(p_o,words[0],q)
        #temp1[q]=(float(p_t[q+"|"+"q0"]) if q+"|"+"q0" in p_t else float(p_t["****|q0"]))+(float(p_o[words[0]+"|"+q]) if words[0]+"|"+q in p_o else -99999)
        temp1[q]=(float(p_t[q+"|"+"q0"]))+(float(p_o[words[0]+"|"+q]))
        temp2[q]="q0"
    prob[0]=temp1
    back[0]=temp2
    for t in range(1,len(words)):
        temp1={}
        temp2={}
        ptt=prob[t-1]
        wt=words[t]
        r,s=bias_estimate(str(wt))
        wt_q=wt+"|"
        WQ=WA[wt]
        if WQ==[]:
            WQ=Q
        for q in WQ:
            if q in WA[wt]:
                x=p_o[wt_q+q]
            else:
                x=p_o["***|"+q]
            if q==s:
                x+=r
            #temp1[q],temp2[q]=maxprob(prob,p_t,p_o,q,t,Q,words)
            max_val=-999999999999
            m_q="XX"
            #x=p_o[wt_q+q]# if words[t]+"|"+q in p_o else -99999)
            #N=next[q]
            N=ptt.keys()
            q_n=q+"|"
            for qq in N:
                val=x+ptt[qq]+p_t[q_n+qq]# if q+"|"+qq in p_t else float(p_t["****|"+qq]))
                if val >max_val:
                    max_val=val
                    m_q=qq
            temp1[q]=max_val
            temp2[q]=m_q
        prob[t]=temp1
        back[t]=temp2
    most_prob_state=max(prob[len(words)-1].iteritems(), key=operator.itemgetter(1))[0]
    return back_track(back,most_prob_state,len(words),words)

def tran_mat(p,states):
    res=defaultdict(list)
    k=p.keys()
    for i in k:
        g=i.split("|")
        if g[0]=="****":
            continue
        res[g[-1]]+=[g[0]]
    return res

def unique_words(p,states):
    res=defaultdict(list)
    k=p.keys()
    for i in k:
        g=i.split("|")
        if g[0]=="***":
            continue
        res["|".join(g[:-1])]+=[g[-1]]
    return res

def run():
    stime=time.time()
    with open("hmmmodel.txt","r") as f:
        prob_t=defaultdict(lambda:-99999)
        prob_o=defaultdict(lambda:-99999)
        line=f.readlines()
        for l in line:
            x=l.split(":")
            if x[0]=="T":
                prob_t[":".join(x[1:-1])]=float(x[-1])
            elif x[0]=="O":
                prob_o[":".join(x[1:-1])]=float(x[-1])
    out=open("output.txt","w")
    Q=unique_keys(prob_t.keys())
    W=unique_words(prob_o,Q)
    next=tran_mat(prob_t,Q)
    #next=[x.split("|")[0] for x in Q if x.endswith("|"+q)]
    with open("catalan_corpus_dev_raw.txt","r") as f:
        lines=f.readlines()
        for l in lines:
            words=l.split()
            res=hmm(prob_t,prob_o,words,Q,next,W)
            out.write(" ".join(res)+"\n")
    etime=time.time()
    print str(etime-stime)

run()