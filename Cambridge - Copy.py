# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 20:03:49 2020

@author: VU-PC
"""

import xlsxwriter
### SET UP
import requests
from bs4 import BeautifulSoup
import urllib
import os
#print(soup.prettify())


### Find PRONUNCIATION
def pronun(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html5lib')
        uspro = soup.find(class_='us dpron-i')
        prono1 = uspro.find(class_='pron dpron').get_text()
        return prono1
    except: pass

### Find DEFFINITION and INFO and NAME
def info(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html5lib')
        info = soup.find(class_='def-info ddef-info')
        #realin = info.find(class_=['epp-xref dxref A1','epp-xref dxref A2','epp-xref dxref B1','epp-xref dxref B2','epp-xref dxref C2','epp-xref dxref C2')
        realin = info.find(class_='epp-xref').get_text()
        #print(realin)
        return realin
    except:
        pass

def namem(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html5lib')
        name = soup.find(class_='headword tw-bw dhw dpos-h_hw')
        if name is None:
            name = soup.find(class_='headword hdb tw-bw dhw dpos-h_hw')
            real_name = name.find(class_='hw dhw').get_text()
        else:
            real_name = name.get_text()
        #print(real_name)
        return real_name
    except:
        pass
    
def deffi(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html5lib')
        overall = soup.find(class_='pr dsense')
        if overall is None:
            mean = soup.find(class_='def ddef_d db').get_text()
        else:
            mean = overall.find(class_='def ddef_d db').get_text()
        #print(mean)
    except: pass
    return mean

### Find EXAMPLES
def example_get(url):
    
        example_list =[]
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html5lib')
        exams = soup.find(class_='def-body ddef_b')
        exas = exams.find_all(class_='examp dexamp')
        for example in exas:
            e = example.get_text()
            example_list.append(e)
            
        for example in exas:
            e = example.get_text()
            bold_tag = example.find_all(class_='b db')
            for bold in bold_tag:
                pText = bold.parent.parent.get_text()
                pos_pa = example_list.index(pText)
            
                bold_text = bold.get_text()
                boldWithTag = '<b><i>'+bold_text+'</i></b>'
                le = e.split(bold_text)
                #print(le)
                jo = le[0]+boldWithTag+le[1]
                #print(jo)
                example_list[pos_pa] = jo
        #print(example_list)
        return '<br/>'.join(example_list)
    
#example_get('https://dictionary.cambridge.org/vi/dictionary/english/do') 
   
### Down MP3
def downmp3(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html5lib')
        uspro = soup.find(class_='us dpron-i')
        mp3 = uspro.find(class_='daud')
        #mplink = mp3.find(type='audio/mpeg')
        mplink = mp3.find('source')
        finlink = 'https://dictionary.cambridge.org'+(mplink['src'])
        mp3_name = url.split('english/')[1]+'.mp3'
        #print(mp3_name)
        fullfilename = os.path.join(r'C:\Users\VU-PC\AppData\Roaming\Anki2\User 1\collection.media',mp3_name)
        urllib.request.urlretrieve(finlink, fullfilename)
        return mp3_name
    except: pass

### Down PICTURE
def downpic(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html5lib')
        image = soup.find(class_='dimg')
        amimg = image.find('amp-img')
        linkam = 'https://dictionary.cambridge.org'+amimg['src']
        #print(linkam)
        img_name = url.split('english/')[1]+'.jpg'
        #print(img_name)
        fullfilename = os.path.join(r'C:\Users\VU-PC\AppData\Roaming\Anki2\User 1\collection.media',img_name)
        urllib.request.urlretrieve(linkam,fullfilename)
        return img_name
    except: pass

#CREATE FILE
workbook = xlsxwriter.Workbook(input('enter file name: ')+'.xlsx')
worksheet = workbook.add_worksheet()
wrap_format = workbook.add_format({'text_wrap': True})

ans = input('enter text: ')
ansList = ans.split(',')
#print(ansList)
row = 0
col = 0
insertList = []

for i in range(len(ansList)):
    tempList = [1,2,3]
    a='https://dictionary.cambridge.org/vi/dictionary/english/'+ansList[i]
    print(a)

    
    try:
        tempList[0] = namem(a)+'<br/>'+example_get(a)
        
    except: tempList[0]='non'
    #print(tempList[0])
    try:
        tempList[1] = info(a)+'<br/>'+namem(a)+'<br/>'+deffi(a)+'<br/>'+'<img src="'+downpic(a)+'">'
    except:
        try: 
            tempList[1] = info(a)+'<br/>'+namem(a)+'<br/>'+deffi(a)
        except:
            try:
                tempList[1] = namem(a)+'<br/>'+deffi(a)+'<br/>'+'<img src="'+downpic(a)+'">'
            except:
                try:
                    tempList[1] = namem(a)+'<br/>'+deffi(a)
                except:
                    try:
                        tempList[1] = namem(a)
                    except: 
                        try:
                            tempList[1] = ansList[1]
                        except: tempList[1] = 'non'
    #print(tempList[1])
    try:
        tempList[2] = pronun(a)+'<br/>'+'[sound:'+str(downmp3(a))+']'
    except:
        try:
            tempList[2] = pronun(a)
        except:
            tempList[2]='non'
    #print(tempList[2])
    insertList.append(tempList)
    insertList[i] = tempList
    #print(insertList)
print(insertList)
#insertSet = set(insertList)

for e,d,p in insertList:
    worksheet.write(row, col, e, wrap_format)
    worksheet.write(row, col + 1, d, wrap_format)
    worksheet.write(row, col + 2, p, wrap_format)
    row += 1
    
workbook.close()


