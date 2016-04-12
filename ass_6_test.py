import time
def unique_keys(k):
    res=[]
    for i in k:
        res.append(i.split("|")[-1])
    r=set(res)
    return r

def probobs(p,s,e):
    if s+"|"+e in p:
        return float(p[s+"|"+e])
    elif "***|"+e in p:
        return float(p["***|"+e])
    else:
        return -9999999

def probtran(p,s,e):
    if s+"|"+e in p:
        return float(p[s+"|"+e])
    else:
        return -9999999

def hmm(p_t,p_o,w,pre,p_pre):
    states=p_t.keys()
    next=[x.split("|")[0] for x in states if x.endswith("|"+pre)]
    m_val=-9999999
    cur=next[0]
    for s in next:
        tran=probtran(p_t,s,pre)
        obs=probobs(p_o,w,s)
        if tran==0:
            continue
        val=p_pre+tran+obs
        if val>m_val:
            cur=s
            m_val=val
    return cur,m_val

start=time.time()
with open("hmm_feature.txt","r") as f:
    prob_t={}
    prob_o={}
    line=f.readlines()
    for l in line:
        x=l.split(":")
        if x[0]=="T":
            prob_t[x[1]]=x[2]
        elif x[0]=="O":
            prob_o[x[1]]=x[2]
states=unique_keys(prob_t.keys())
out=open("output.txt","w")
with open("catalan_corpus_dev_raw.txt","r") as f:
    lines=f.readlines()
    for l in lines:
        temp=[]
        f_states=[]
        words=l.split()
        p_state="q0"
        p_val=0
        for w in words:
            p_state,p_val=hmm(prob_t,prob_o,w,p_state,p_val)
            temp.append(w+"/"+p_state)
        out.write(" ".join(temp)+"\n")
end=time.time()
print end-start

