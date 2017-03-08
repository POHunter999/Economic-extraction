# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:00:06 2017

@author: POHunter
"""


import pandas as pd
import jieba
import jieba.posseg as pseg
import jieba.analyse
jieba.initialize()
jieba.load_userdict("cidian.txt") # file_name为自定义词典的路径
#分割句子，输入一段话或一篇文章
def cut_sentence(words):
    #words = (words).decode('utf8') 如果是从编码为 utf8 的 txt 文本中直接输入的话，需要先把文本解码成 unicode 来处理
    start = 0
    i = 0  #记录每个字符的位置
    sents = []
    punt_list = '!?:;~。！？；～'  #string 必须要解码为 unicode 才能进行匹配
    for word in words:
        if word in punt_list:
            sents.append(words[start:i+1])
            start = i + 1  #start标记到下一句的开头
            i += 1
        else:
            i += 1  #若不是标点符号，则字符位置继续前移
    if start < len(words):
        sents.append(words[start:])  #这是为了处理文本末尾没有标点符号的情况
    return sents

#在字符串中寻找目标位置，输入为一段话和目标字符
def findStrPosition(sentences,search):       
    start = 0
    lis=[]    
    while  True:     
        index = sentences.find(search, start)     
             
        if index == -1:     
            break    
   
        lis.append(index)
        start = index  + 1 
    return lis#输出为保存位置的列表
#在列表中寻找目标位置，输入（列表，目标）
def findSortedPosition(theList, target): 
    index=[]
    for i in  range(len(theList)):
        if theList[i]==target:
            index.append(i)
    return index  #输出为保存位置的列表

#寻找所需信息的位置    
def findData(fenci,flag):
    the="".join(flag)#将词性列表合成一个字符串
    #对不同的所需信息位置进行抽取，对所需信息提前进行标注，保存在Dataframe结构中
    nmm=findStrPosition(the,'nmm')
    nmmDF=pd.DataFrame(nmm,columns=["location"])
    nmmDF['type']='nmm'
        
    vmx=findStrPosition(the,'vmx')
    vmxDF=pd.DataFrame(vmx,columns=["location"])
    vmxDF['type']='vmx'
           
    nvmm=findStrPosition(the,'vmm')
    nvmmDF=pd.DataFrame(nvmm,columns=["location"])
    nvmmDF['type']='nvmm'
    
#将三种Dataframe合成一个并返回
    final=(nmmDF.append(nvmmDF)).append(vmxDF)
    
    return final#final为保存需要信息大概位置的变量        
#主函数输入一句话   
def main(sentences):
#利用分词工具进行分词及词性标注
    a=pseg.cut(sentences)
    
    fenci=[]#用于保存分词信息
    flag=[]#用于保存词性信息
    df=pd.DataFrame()
    df2=pd.DataFrame()
    
    #将分词和词性读入两个列表用以后用
    for w in a:
        fenci.append(w.word)
        flag.append(w.flag[0])
        
    final=findData(fenci,flag)#调用findData函数输出final
    
    ts=""#构造空字符串，保存实体

#遍历final中保存的所有位置    
    for line in final.itertuples():
        
        zhuti1="".join(fenci[int(line[1])-2:int(line[1])])#包含所提取信息的一部分主体
        zhuti2="".join(fenci[int(line[1]):int(line[1]+1)])#包含所提取信息的另一部分主体
        num="".join(fenci[int(line[1])+1:int(line[1])+3])#所抽取的数值信息
        tag1=jieba.analyse.extract_tags(zhuti1,1)#在第一部分主体中提取核心词tag1
        tag2=jieba.analyse.extract_tags(zhuti2,1)#在第二部分主体中提取核心词tag2
        
        if len(tag1)==1 and len(tag2)==1: 
            if tag1[0] in shiti:
                ts=tag1[0]
                temp=pd.DataFrame([[ tag1[0],num]],columns=["项目", tag2[0] ])
                df=df.append(temp)
                com=pd.DataFrame([[ tag1[0]+tag2[0] ,num]],columns=["项目","值" ])
                df2=df2.append(com)
            elif tag2[0] in shiti:
                ts=tag2[0]
                temp=pd.DataFrame([[ tag2[0],num]],columns=["项目", tag1[0] ])
                df=df.append(temp)
                com=pd.DataFrame([[ tag2[0]+tag1[0] ,num]],columns=["项目","值" ])
                df2=df2.append(com)
            elif not(tag1[0] in shiti or tag2[0] in shiti):
                location=int(line[1])
                while not(fenci[location] in shiti):
                    location=location-1
                    if location==-1:
                        tempshiti=ts
                        break
                    tempshiti=fenci[location]                                        
                if tag1[0] in shuxing:
                    com=pd.DataFrame([[tempshiti+tag2[0]+tag1[0] ,num]],columns=["项目","值" ])
                    df2=df2.append(com)
                elif tag2[0] in shuxing:
                    com=pd.DataFrame([[tempshiti+tag1[0]+tag2[0] ,num]],columns=["项目","值" ])
                    df2=df2.append(com)
        '''
        if line[2]=='nmm':
            zhuti="".join(fenci[int(line[1])-3:int(line[1])+1])
            num="".join(fenci[int(line[1])+1:int(line[1])+3])
            tags=jieba.analyse.extract_tags(zhuti,2)                                
            #print("".join(fenci[int(line[1])-3:int(line[1])+3]) + 'nmm' )
            temp=pd.DataFrame([[ str(tags[1]),num]],columns=["项目", tags[0] ])
            df=df.append(temp)
        elif line[2]=='nvmm':                
            zhuti="".join(fenci[int(line[1])-3:int(line[1])+1])
            num="".join(fenci[int(line[1])+1:int(line[1])+3])
            tags=jieba.analyse.extract_tags(zhuti,2)                
            #print("".join(fenci[int(line[1])-2:int(line[1])+3])+'nvmm')
            temp=pd.DataFrame([[ str(tags[1]),num]],columns=["项目", tags[0]  ])  
            df=df.append(temp)
        elif line[2]=='vmx':
            print("".join(fenci[int(line[1]):int(line[1])+3])+'vmx')
        '''
    return  df,df2
#去除列表中的空值           
def not_empty(s): return s and s.strip()
#去除列表末尾的\n
def dropn(s):    
    for i in range(len(s)):
        s[i]=s[i].strip('\n')        
    return s
    
    
file = open('input.txt','r')#目标文本
shi=open('shiti.txt','r')#人工定义的实体
shu=open('shuxing.txt','r')#人工定义的属性



text = file.readlines()#该列表按段读入目标文章
shiti= shi.readlines()#该列表存储实体
shuxing=shu.readlines()#该列表存储属性


text=list(filter(not_empty, text))
text=dropn(text)
shiti=list(filter(not_empty, shiti))
shiti=dropn(shiti)
shuxing=list(filter(not_empty, shuxing))
shuxing=dropn(shuxing)


dff1=pd.DataFrame()
dff2=pd.DataFrame()
for sentences in text:    
    df1,df2=main(str(sentences))
    dff1=dff1.append(df1)
    dff2=dff2.append(df2)
    
first = dff1['项目']
dff1.drop(labels=['项目'], axis=1,inplace = True)
dff1.insert(0, '项目', first)
dff1.to_csv("dff1.csv")

first = dff2['项目']
dff2.drop(labels=['项目'], axis=1,inplace = True)
dff2.insert(0, '项目', first)
dff2.to_csv("dff2.csv")
        
    

