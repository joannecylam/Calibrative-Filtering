#!/usr/bin/env python
import numpy as np
import math

MAX_USER=544
MAX_MOV=1682
aver_rate=[]
s=[]
e_score=0



x = np.array(np.loadtxt('train.dat',delimiter='\t'))

def initialize_matrix(row, col):
    y=[]
    for i in range (0, row):                               
        new = []                 
        for j in range (0, col):     
            new.append(0)         
        y.append(new)  
    return y

def fillup(x, y,row,col):
    #x = np.array(np.loadtxt('test.dat',delimiter='\t'))
    for i in range (0,row):
        userid=int(x[i][0])-1
        movieid=int(x[i][1])-1
        score=float(x[i][2])
        y[userid][movieid]=score
    return y

def average_rating(x,row,col):
    currentuser=1
    accum_score=0
    counter=0
    arr=[]
    for i in range (0,row):
        userid=int(x[i][0])
        
        score = float(x[i][2])
        
        
        if(currentuser==userid):
            accum_score += float(score)
            counter+=1
        else:
            average = accum_score/counter
            arr.append(average)
            accum_score=float(score)
            counter=1
            currentuser+=1
    average = accum_score/counter
    arr.append(average)
    return arr

def similarity(y,aver_rate,MAX_USER,MAX_MOV):
    s=[]
    m=0
    mi=0
    mj=0
    n=0
    for i in range (0,MAX_USER):
        new = []
        for j in range (0, MAX_USER):
            for k in range(0,MAX_MOV):
                if y[i][k] != 0 and y[j][k]!=0 :
                    n += (y[i][k]-aver_rate[i])*(y[j][k]-aver_rate[j])
                    mi += pow((y[i][k]-aver_rate[i]),2)
                    mj += pow((y[j][k]-aver_rate[j]),2)
            if(n>0):
                tem=n/(math.sqrt(mi)*math.sqrt(mj))
                new.append(tem)
                n=0
                mi=0
                mj=0
                tem=0
            else:
                new.append(0)
                n=0
                mi=0
                mj=0
                tem=0
        s.append(new)
    return s    
def compute_e_score(MAX_USER,f,y,aver_rate,s,userid,movieid):
    escore=0
    n=0
    m=0
    for i in range (0,MAX_USER):
        if y[i][movieid] > 0:
            n+=s[userid][i]*(y[i][movieid]-aver_rate[i])
            m+=s[userid][i]
    if (m>0):
        escore=aver_rate[userid]+n/m
    else:
        escore=aver_rate[userid]
    
    f.write(str(escore) +'\n')
    print(escore)

row = x.shape[0]
col = x.shape[1]
y = initialize_matrix(MAX_USER,MAX_MOV)
y = fillup(x, y,row,col)
aver_rate=average_rating(x,row,col)
s = similarity(y,aver_rate,MAX_USER,MAX_MOV)

f=open('E.test.rs.txt','w')

testdata = np.array(np.loadtxt('test.dat',delimiter='\t'))
for w in range(0,testdata.shape[0]):
    user= int(testdata[w][0])-1
    movie=int(testdata[w][1])-1
    compute_e_score(MAX_USER,f,y,aver_rate,s,user,movie)

