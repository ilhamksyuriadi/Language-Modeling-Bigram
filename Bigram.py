# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 11:26:27 2018

@author: ilhamksyuriadi
"""

import xlrd
import nltk
import re

#load from excel file
rawArticles = xlrd.open_workbook('artikel.xlsx')
A = rawArticles.sheet_by_index(0)

#load to data to list
articles = []
for i in range(A.nrows):
    title = A.cell_value(i,1)
    lowedTitle = title.lower()
    par = A.cell_value(i,2)
    lowedPar = par.lower()
    articles.append([A.cell_value(i,0), lowedTitle, lowedPar])

#tokenize by sentence
tokenSent = []
for i in range(len(articles)):
    token = nltk.sent_tokenize(articles[i][2])
    title = re.sub('[^a-z]',' ',str(articles[i][1]))
    tokenSent.append([articles[i][0],title])
    for j in range(len(token)):
        par = re.sub('[^a-z]',' ',str(token[j]))
        tokenSent.append([articles[i][0],par])

#tokenize by word, word frequency, raw bigram and bigram frequency       
freqWord = {} #dictionary for frequency word
freqBigram = {} #dictionary for frequency bigram
probBigram = {} #dictionary for probability bigram
listBigram = []
totalCount = 0
allToken = []
for i in range(len(tokenSent)):
    token = nltk.word_tokenize(tokenSent[i][1])
    for j in range(len(token)):
        if token[j] in freqWord:
            freqWord[token[j]] += 1
        else:
            freqWord[token[j]] = 1
            allToken.append(token[j])
        totalCount += 1
    lBigram = []
    for i in range(len(token)-1):
        lBigram.append((token[i],token[i+1]))
    #lBigram = list(nltk.bigrams(tokenSent[i][1].split()))
    for k in range(len(lBigram)):
        listBigram.append([lBigram[k][0],lBigram[k][1]])
        word = lBigram[k][0] + " " + lBigram[k][1]
        if word in freqBigram:
            freqBigram[word] += 1
            probBigram[word] = freqBigram[word] / freqWord[lBigram[k][0]]
        else:
            freqBigram[word] = 1
            probBigram[word] = freqBigram[word] / freqWord[lBigram[k][0]]
                        
#testing with 10 word
testWord = []
for i in range(10):
    word = str(input("Masukan kata : "))
    testWord.append(word)
predictWord = []
for i in range(len(testWord)):
    expWord = []
    wordProb = []
    if testWord[i] not in freqWord:
        expWord.append("null")
    else:
        for j in range(len(listBigram)):
            if testWord[i] == listBigram[j][0]:
                expWord.append([listBigram[j][0],listBigram[j][1]])
    for k in range(len(expWord)):
        if expWord[k] == "null":
            wordProb.append([0,"null"])
        else:
            word = expWord[k][0] + " " + expWord[k][1]
            wordProb.append([freqBigram[word],expWord[k][1]])
            
    wordProb.sort()
    predictWord.append(wordProb[len(wordProb)-1][1])
for i in range(len(testWord)):
    print("")
    print("Kata     : ", testWord[i])
    if predictWord[i] != "null":
        print("Prediksi : ", predictWord[i])
    else:
        print("Prediksi tidak tersedia, kata tidak ada dalam dokumen")



            
            
            
            
            
            
            
            