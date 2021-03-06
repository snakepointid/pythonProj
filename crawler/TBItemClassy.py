# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 11:21:07 2016

@author: changlue.she
"""
from urllib  import urlopen
from bs4 import BeautifulSoup
from crawler.downloadPage import TBpage
'''get the first class categories'''
html  = urlopen('https://www.tmall.com/')
bsObj = BeautifulSoup(html.read()) 
firstClassContents =  bsObj.find('ul',{'class':'normal-nav clearfix'}).findAll('li')
firstClassList = []
for firstClassContent in firstClassContents:
    tmp = "/".join([line.text for line in firstClassContent.findAll('a')])
    firstClassList.append(tmp)

'''get the second,third and brand class categories'''
loopTime = 0
allClass = []
bsObj = BeautifulSoup(TBpage)
secondClassContents = bsObj.findAll('div',{'class':'pannel-con j_CategoryMenuPannel'})
for idx,secondClassContent in enumerate(secondClassContents):    
    '''first loop to get second class content and first class items'''
    firstclass = firstClassList[idx]  
    cateDetailContents = secondClassContent.findAll('div',{'class':'hot-word-line'})
    for cateDetailContent in cateDetailContents:
        '''second loop to get tird class content and second class items'''
        secondClass = cateDetailContent.find('div',{'class':'title-text'}).text      
        thirdClassContents = cateDetailContent.find('div',{'class':'line-con'}).findAll('a')       
        for thirdClassContent in thirdClassContents:
            '''
            third loop to get brand content and third class items
            but, maybe there is not brand in a third class,so use try
            and except to handle those error
            '''
            loopTime+=1
            try:
                thirdClass = thirdClassContent.text                               
                allClass.append([firstclass,secondClass,thirdClass])
            except:
                print 'there are no brands here',loopTime
#------------------------------------------------------------------------------
'''pick save and load the brands'''
import cPickle
dirs = "C:\\Users\\Administrator.NBJXUEJUN-LI\\Desktop\\project\\Python\\NLP\\savedObject\\JD_TB\\"
cPickle.dump(allClass,open(dirs+"tbBrands.pkl","wb")) 
allClassLoad = cPickle.load(open(dirs+"tbBrands.pkl","rb"))
for brands in allClassLoad:
    print '->'.join(brands)
#------------------------------------------------------------------------------
'''save the brands into csv'''
import pandas as pd
BrandDF = pd.DataFrame(allClassLoad)
BrandDF.to_csv('C:\\Users\\Administrator.NBJXUEJUN-LI\\Desktop\\project\\MSXF\\feature construct\\doc\\TBClassification.csv',encoding='gbk')