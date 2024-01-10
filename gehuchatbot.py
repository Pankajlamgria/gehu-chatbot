import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import json 
from textblob import TextBlob
from gtts import gTTS
import vlc
import datetime
import csv

class gehu:
    def __init__(self):
        self.trainx=[]
        self.trainy=[]
        f=open("./data/train/training.json")
        resfile=open("./data/responses/response.json")
        data=json.load(f)
        self.responses=json.load(resfile)
        
        currenttime=datetime.datetime.now()
        csvfile=open("./data/history.csv","a+")
        csvwriter=csv.writer(csvfile)
        csvwriter.writerow([currenttime])
        csvfile.close()
        
        for key in data:  
            for i in data[key]:
                self.trainx.append(i)
                self.trainy.append(key)
        self.vectorizer=TfidfVectorizer()
        traneddata=self.vectorizer.fit_transform(self.trainx)
        self.clf=svm.SVC(kernel="linear")
        self.clf.fit(traneddata,self.trainy)
        
    def findemotion(self,userInput):
        userInput=userInput.lower()
        tb_text=TextBlob(userInput)
        tb_text.correct()
        userInput=str(tb_text)
        testx=self.vectorizer.transform([userInput])
        return self.clf.predict(testx)
    def showhistory(self):
        csvfile=open("./data/history.csv","r")
        csvreader=csv.reader(csvfile)
        self.botresp=""
        str=""
        for line in csvreader:
            if(len(line)==1):
                str=str+f"\nDate:{line[0]}"
            elif(len(line)==2):
                str=str+f"\nUser:{line[0]}"
                str=str+f"\nBot:{line[1]}"
        return str
           
    def clearHistory(self):
        self.botresp=""
        csvfile=open("./data/history.csv","w")
        csvfile.close()    
        
    def generateres(self,req):
        tag=self.findemotion(req)
        if(tag[0]=='history'):
            return self.showhistory()
        elif(tag[0]=='deletehistory'):
            self.clearHistory()
            return random.choice(self.responses['deletehistory'])
        else:
            self.botresp=random.choice(self.responses[f'{tag[0]}'])
            csvfile=open("./data/history.csv","a+")
            csvwriter=csv.writer(csvfile)
            csvwriter.writerow([req,self.botresp])
            csvfile.close()
            return self.botresp
                  
    def speaktheoutput(self):
        tts=gTTS(self.botresp,lang='en',slow=False)
        tts.save("./data/speak.mp3")
        p=vlc.MediaPlayer("./data/speak.mp3")
        p.play()
    
