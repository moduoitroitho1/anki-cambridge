# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 15:25:05 2020

@author: VU-PC
"""

#todo: word => a list search => all list search
#name type i or t or C pronun audio example definition level
#todo: audio
import requests
from bs4 import BeautifulSoup
import string
#import urllib
a = 'kick (HIT) A2 the action of kicking somethingDictionary example:She gave him a kick under the table to shut him up.Learner example:We [practiced] shooting, passing the ball to each other, and [taking a] corner kick. (Preliminary English Test; B1; German)  '
url = 'https://englishprofile.org/british-english/words/detail/3230'
b ='kick · verb I or T \uf028 /kɪk/Full view'
d='ID_00003329_05'


def smallNameList(url):
    '''input: url
        output: a list with all words in page and their number theo tuple'''
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html5lib')
        #print(soup.prettify())
        #nameList = []
        names = soup.findAll(class_='info sense')
        #print(names)
        for name in names:
            getName = name.get_text()
            print(getName)
            idName = name['id']
        print(getName,idName)
    except:
        pass
#url = input('enter: ')
#findName(url)

### Get NAME, LEVEL, DEFFO, EXAMPLE
def smallInfo(text):
    wordInfo = ()
    standard = string.ascii_uppercase
    compare = list()
    for letter in standard:
        let_pos = text.find(letter)
        if let_pos != -1:
            compare.append((letter,let_pos))
        else: continue
    min_pos = 10000
    for (letter,let_pos) in compare:
        if let_pos <= min_pos: 
            min_pos = let_pos
    if text[min_pos-1] =='(':
        end_pos = text.find(')')
        wordLevel = text[end_pos+2:end_pos+4]
    else:
        wordLevel = text[min_pos:min_pos+2]
    wordLevel_pos = text.find(wordLevel)
    wordName = text[:wordLevel_pos-1]
    dict_pos = text.find('Dictionary example')
    start_pos = len(wordName)+len(wordLevel)+2
    learn_pos = text.find('Learner example')
    wordDef = text[start_pos:dict_pos]
    wordExamples = text[dict_pos+19:learn_pos-1]
    wordeList1 = wordExamples.split('.')
    wordeList2 = []
    for example in wordeList1:
        examplePeriod = example + '.'
        wordeList2.append(examplePeriod)
    wordInfo = (wordName,wordLevel,wordDef,wordeList2)
    return wordInfo


def bigNameList(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html5lib')
        bigName = []
        #print(soup.prettify())
        #nameList = []
        names = soup.findAll(class_='pos_header')
        #print(names)
        for name in names:
            getName = name.get_text()
            bigName.append(getName)
        return print(bigName)
    except:
        pass 

def bigInfo(text):
    textSplit = text.split()
    wordInfo = ()
    wordName = textSplit[0]
    audio_pos = text.find('\uf028')
    start_pos = len(wordName)+3
    wordType = text[start_pos:audio_pos]
    wordPro = text[audio_pos+2:]
    #print(wordPro)
    if 'Full view' in wordPro:
        full_pos = wordPro.find('Full view')
        wordPro = wordPro[:full_pos]
    wordInfo = (wordName, wordType,wordPro)
    return wordInfo
bigInfo(b)

def navigation(url,divID):
    '''Input: div
        Output: parent div'''
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html5lib')
    div = soup.find(id=divID)
    #print(div)
    #print(div.parent.parent['class'])

    if div.parent.parent['class']==['pos_section']:
        mom_sec = div.parent.parent
        momdad = mom_sec.find(class_='pos_header')
        print( momdad)
    else:
        pa_div = div.parent
        #print(pa_div)
        #print(pa_div.previous_sibling)
        pre_div = pa_div
        #print(pre_div)
        #print(pre_div['class'])
        '''m = ' '.join(pre_div['class'])
        print(type(m))'''
        '''while pre_div['class']!=['pos_section']:
            pre_div = pa_div.previous_sibling
            pa_div =pre_div
            print(pa_div) 
        mom_sec = pa_div
        momdad = mom_sec.find(class_='pos_header')
        print(momdad)'''
        print(pa_div.previous_sibling)
        pre_div = pa_div.previous_sibling
        print(pre_div)
        pa_div =pre_div
        print(pa_div) 
navigation(url,d)
    
def wordInfo(url,divID):
    '''Input: divID
    Output: tuple with all info of the word'''
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html5lib')
    div = soup.find(id=divID)
    pad_div = div.parent
    momdad = navigation(url,divID)
    momText = momdad.get_text()
    momInfo = bigInfo(momText)
    smallText = pad_div.get_text()
    chiInfo = smallInfo(smallText)
    wordsInfo = (momInfo+chiInfo)
    print(wordsInfo)
    
#wordInfo(url,d)

            
            
        
    
    