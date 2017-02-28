#encoding=utf-8
"""
Created on Tue Feb 28 10:31:55 2017

@author: POHunter
"""
sentences=" 2015年，全省加快转变农业发展方式，全力打造高原特色现代农业，全年全省农林牧渔业总产值保持了稳定增长，粮食产量再创新高。2015年全省农林牧渔业总产值完成3383.09亿元，同比增长6.0%；完成增加值2098.19亿元，增加值总量在全国排第14位，同比增长6.0%，其中：农业增加值1230.75亿元，增长5.7%；林业增加值216.11亿元，增长10.3%；牧业增加值559.98亿元，增长4.3%；渔业增加值48.88亿元，增长8.8%。农林牧渔服务业增加值42.48亿元，增长10.2%。2015年，全省粮食生产实现了总量增及单产同步增长态势，粮食产量为1876.4万吨，比2014年增产15.7万吨，增长0.84%，实现连续十三年增长粮食综合平均单产278.8公斤，比2014年增加3.6公斤，同比增长1.3%。2015年，全省高原特色农业形势良好，特色经济作物量效齐升，茶叶、水果、花卉等价格上涨明显，橡胶、咖啡及核桃种植面积和产量继续保持全国第一，粮油、肉类、蔬菜、水产品等都获得较好收成。"
import pandas as pd
import jieba
import jieba.posseg as pseg
jieba.load_userdict("cidian.txt") # file_name为自定义词典的路径

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


def findStrPosition(sentences,search):       
    start = 0
    lis=[]    
    while  True:     
        index = sentences.find(search, start)     
    # if search string not found, find() returns -1     
    # search is complete, break out of the while loop
             
        if index == -1:     
            break    
    #print( "%s found at index %d"  % (search, index) )     
    # move to next possible start position     
        lis.append(index)
        start = index  + 1 
    return lis

def findSortedPosition(theList, target): 
    index=[]
    for i in  range(len(theList)):
        if theList[i]==target:
            index.append(i)
    return index  
    
def findData(fenci,flag):
    the="".join(flag)
    
    nmm=findStrPosition(the,'nmm')
    nmmDF=pd.DataFrame(nmm)
    nmmDF['type']='nmm'
        
    vmx=findStrPosition(the,'vmx')
    vmxDF=pd.DataFrame(vmx)
    vmxDF['type']='vmx'
           
    nvmm=findStrPosition(the,'vmm')
    nvmmDF=pd.DataFrame(nvmm)
    nvmmDF['type']='nvmm'
    
    final=(nmmDF.append(vmxDF)).append(nvmmDF)
    '''
    for i in nmm:
        print("".join(fenci[i-2:i+3]))
    for i in vmx:
        print("".join(fenci[i:i+3]))
    for i in nvmm:
        print("".join(fenci[i-1:i+4]))
    '''    
    return final        
    
def main(sentences):

    a=pseg.cut(sentences)
    fenci=[]
    flag=[]
    for w in a:
        fenci.append(w.word)
        flag.append(w.flag[0])

    final=findData(fenci,flag)
    final=final.sort_values([0])
    final.columns=["location","type"]

    for line in final.itertuples():
        if line[2]=='nmm':
            print("".join(fenci[line[1]-2:line[1]+3]))
        elif line[2]=='vmx':
            print("".join(fenci[line[1]:line[1]+3]))
        else:
            print("".join(fenci[line[1]-2:line[1]+4]))
           

file = open('input.txt','r')
words = file.readlines()
aaa = cut_sentence(words)
for i in aaa:
    main(str(i))

        
            
    
    
    

