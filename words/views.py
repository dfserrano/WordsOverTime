from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
import random
from datetime import datetime, date, time, timedelta
import time
import csv

from .forms import MainForm
from .requesthandler import *
from .hash import *
from .models import *

GRANULARITY_WEEKLY = 'Week'
GRANULARITY_MONTHLY = 'Month'
GRANULARITY_YEARLY = 'Year'


# Create your views here.
def index(request):
    return render(request, 'words/index.html')
    #return HttpResponse("Hello world")

def success(request):
    #hashStr = gen_unique_hash(Graph, 15)
    hashStr = 23432
    
    #Get Form Data!
    if "startDate" in request.POST:
        startDateString = request.POST["startDate"]
        startDate = datetime.strptime(startDateString, '%Y-%m-%d')
    else:
        #error page
        startDateString = ''
    if "endDate" in request.POST:
        endDateString = request.POST["endDate"]
        endDate = datetime.strptime(endDateString, '%Y-%m-%d')
    else:
        #error
        endDateString = ''
    granularity = request.POST["granularity"]
    
    #Form data for n closest neighbors
    if "Nneighbor" in request.POST:
        n = int(request.POST["Nneighbor"])
    else:
        n = -1
    if "keywords" in request.POST:
        keyWords = request.POST["keywords"]
        keyWordsList = keyWords.split()
    else:
        #error
        keyWords = ''
        keyWordsList = [] 
    if "text_file" in request.FILES:
        textFile = request.FILES["text_file"]
    else:
        textFile = ''
    skipOrCBOW1 = request.POST["skipOrCBOW1"]
    #TODO: read in file and create list of strings from it
    #How to separate words?

    #Form data for cosine distance
    if "wordPairs" in request.POST:
        wordPair = request.POST["wordPairs"]
        wordPairList = wordPair.split()
    else:
        wordPair = ''
        wordPairList = []
    if "text_file2" in request.FILES:
        textFile2 = request.FILES["text_file2"]
    else:
        textFile2 = ''
    skipOrCBOW2 = request.POST["skipOrCBOW2"]
    #TODO: read in file and create list of strings from it
    #How to separate words?
    
    #Form data for tfidf
    if "tfidfWord" in request.POST:
        tfidfWord = request.POST["tfidfWord"]
    else:
        tfidfWord = ''
    
    #Form data for Pairwise Conditional Probabilities
    if "conditionalWord" in request.POST:
        conditionalWordPair = request.POST["conditionalWord"]
        conditionalWordPairList = conditionalWordPair.split()
    else:
        conditionalWordPair = ''
        conditionalWordPairList = []
    if "fileConditional" in request.FILES:
        fileConditional = request.FILES["fileConditional"]
    else:
        fileConditional = ''
    #TODO: read in file and create list of strings from it
    #How to separate words?

    #Form data from checkboxes
    if "Average valence" in request.POST:
        averageValence = request.POST["Average valence"]
    else:
        averageValence = 0
    if "Average arousal" in request.POST:
        averageArousal = request.POST["Average arousal"]
    else:
        averageArousal = 0
    if "5 Words Average valence" in request.POST:
        top5averageValence = request.POST["5 Words Average valence"]
    else:
        top5averageValence = 0
    if "5 Words Average arousal" in request.POST:
        top5averageArousal = request.POST["5 Words Average arousal"]
    else:
        top5averageArousal = 0

    #Form data for word frequency
    if "frequencyWord" in request.POST:
        wordFrequencyWords = request.POST["frequencyWord"]
        wordFrequencyList = wordFrequencyWords.split()
    else:
        wordFrequencyWords = ''
        wordFrequencyList = []
    if "wordFrequencyFile" in request.FILES:
        wordFrequencyFile = request.FILES["wordFrequencyFile"]
    else:
        wordFrequencyFile = ''
    #TODO: read in file and create list of strings from it
    #How to separate words?

    #Form data for relative word frequency
    if "relativeWord" in request.POST:
        relativeWords = request.POST["relativeWord"]
        relativeList = relativeWords.split()
    else:
        relativeWords = ''
        relativeList = []
    if "relativeFile" in request.FILES:
        relativeFile = request.FILES["relativeFile"]
    else:
        relativeFile = ''
    #TODO: read in file and create list of strings from it
    #How to separate words?

    #Form data for email
    if "userEmail" in request.POST:
        email = request.POST["userEmail"]
    else:
        #error
        email = ''
    #print(keyWordsList)
    
    requestList = []
    hashList = []

    #Handle N closest neighbor request
    if(n >= 0 and keyWordsList):
        closeHash = 1
        nClosestReq = NClosestNeighboursOverTimeRequest((startDate, endDate), granularity, keyWordsList[0], n, True)
        nClosestResult = nClosestReq.execute()
        nClosestResult.generateCSV(closeHash)
        hashList.append(closeHash)

    #Handle CosineDistance request        
    if (wordPairList):
        cosHash = 2
        cosReq = CosDistanceOverTimeRequest((startDate, endDate), granularity, wordPairList[0], wordPairList[1], True)
        cosResult = cosReq.execute()
        cosResult.generateCSV(cosHash)
        hashList.append(cosHash)

    #Handle tfidf request
    if (tfidfWord != ''):
        print("Doing stuff")
        tfidfHash = 3
        tfidfReq = TfidfOverTimeRequest((startDate, endDate), granularity, tfidfWord)
        tfidfResult = tfidfReq.execute()
        tfidfResult.generateCSV(tfidfHash)
        hashList.append(tfidfHash)

    #Handle Pairwise Probability request
    if (conditionalWordPairList):
        pairHash = 4
        pairReq = PairwiseProbabilitiesOverTimeRequest((startDate, endDate), granularity, conditionalWordPairList[0], conditionalWordPairList[1])
        pairResult = pairReq.execute()
        pairResult.generateCSV(pairHash)
        hashList.append(pairHash)

    #avgHash = 5
    #Handle Average Valence Request
    if (averageValence == '1'):
        avgValHash = 5        
        avgValReq = AverageValenceOverTimeRequest((startDate, endDate), granularity)
        avgValResult = avgValReq.execute()
        avgValResult.generateCSV(avgValHash)
        hashList.append(avgValHash)

    #Handle Average Arousal Request
    if (averageArousal == '1'):
        avgAroHash = 6  
        avgAroReq = AverageArousalOverTimeRequest((startDate, endDate), granularity)
        avgAroResult = avgAroReq.execute()
        avgAroResult.generateCSV(avgAroHash)
        hashList.append(avgAroHash)      
        print(hashList)  
        

    #Handle Average 5 Word Valence Request
    if (top5averageValence == '1'):
        avgVal5Hash = 7        
        avgVal5Req = AverageValenceFiveWordsOverTimeRequest((startDate, endDate), granularity)
        avgVal5Result = avgVal5Req.execute()
        avgVal5Result.generateCSV(avgVal5Hash)
        hashList.append(avgVal5Hash)   

 

    #Handle Average 5 Word Arousal Request
    if (top5averageArousal == '1'):
        avgAro5Hash = 8        
        avgAro5Req = AverageArousalFiveWordsOverTimeRequest((startDate, endDate), granularity)
        avgAro5Result = avgAro5Req.execute()
        avgAro5Result.generateCSV(avgAro5Hash) 
        hashList.append(avgAro5Hash)  
    
    #Handle Word Freqency (How?)
    if (wordFrequencyList):
        #Do stuff
        pass
    #Handle relative word frequency (How?)
    if (relativeList):
        #Do stuff
        pass
    
    #req = CosDistanceOverTimeRequest(hashStr, (startDate, endDate), 'Year', keyWordsList[0], keyWordsList[1], True)
    
    #result = req.execute()
    #result.generateCSV(hashStr)

    print(hashList)

    context = {}
    for index in range (0, len(hashList)):
        context["Hash%s" %index] = int(hashList[index])
    
    context["nHashes"] = len(hashList)

    return render(request, 'words/success.html', context)
    

def graph(request, hash):
    filePath = '/mnt/vol/csvs'
    keyWords = ["bird", "thing"]
    valuesList = [(2009, 0.8, 'bird'), (2010, 0.8, 'bird'), (2009, 0.1, 'thing'), (2010, 0.1, 'thing')]
    yValues = []
    xValues = []
    xAxis = ''
    yAxis = ''
    thing = []
    #with open('test.csv', 'r') as csvfile:
    #    reader = csv.DictReader(csvfile)
    #    xAxis = reader.fieldnames[0]
    #    yAxis = reader.fieldnames[1]
    #    for row in reader:
    #        xValues.append(row[xAxis])
    #        thing = row[yAxis]
    #        yValues.append(thing[1])
    #        keyWords.append(thing[0])

    testDict = {}
    yValuesList = []
    for word in keyWords:
        testDict[word] = []
        yTempValues = []
        for thing in valuesList:
            print(thing)
            if(thing[2] == word):
                testDict[word].append(thing[1])
                yTempValues.append(thing[1])
                xValues.append(thing[0])
        yValuesList.append(yTempValues)
    
    print(keyWords)

    print(yValuesList)

    #print (testDict)
    #numWords = len(keyWords)
    #yValuesList= []
    #for i in range(0, numWords):
    #    yValuesList.append

    #xAxis = result.xTitle
    #yAxis = result.yTitle
    #xAxis = "Date"
    #yAxis = "Valence"
    #xValues = [1,2,3,4,5]
    #yValues = [1,2,3,4,5]
    #keyWords = ['hello', 'hi']
    word1 = "Hello"
    word2 = "Hi"
    #w1x = [1,6,3,4]
    #w1y = [1,3,6,7]
    #w2x = [2,5,6,7]
    #w2y = [1,4,7,9]
    context = {
        'xAxis': xAxis,
        'yAxis': yAxis,
        #'word1': word1,
        #'word2': word2, 
        'xValues': xValues,
        #'w1x': w1x,
        #'w1y': w1y,
        #'w2x': w2x,
        #'w2y': w2y,
        'keywords': keyWords,
        'yValues': yValues
    }
    return render(request, 'words/graph2.html', context)
 
#class IndexView(generic.DetailView):
  #template_name = "words/index.html"
  
def results(request):
  if request.method == 'POST':
    form = ContactForm(request.POST) 
    if form.is_valid():
      data = myform.cleaned_data
      #process data with field = data['field']
      #generate a Request object (see requesthandler.py)
  return HttpResponseRedirect()
