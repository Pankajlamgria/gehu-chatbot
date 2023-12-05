import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from nltk import WordNetLemmatizer

class gehu:
    def __init__(self):
        lemmatizer=WordNetLemmatizer()
        self.stopword=stopwords.words('english')
        self.trainx=[]
        self.trainy=[]
        f=open("./data/train/greet.json")
        resfile=open("./data/responses/response.json")
        data=json.load(f)
        self.responses=json.load(resfile)
        for key in data:  
            for i in data[key]:
                i=i.lower()
                tokenwords=word_tokenize(i)
                newSetence=[]
                for words in tokenwords:
                    if(words not in self.stopword):
                        words=lemmatizer.lemmatize(words)
                        newSetence.append(words)
                self.trainx.append(' '.join(newSetence))
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
        tokenwords=word_tokenize(userInput)
        newSentence=[]
        for word in tokenwords:
            if word not in self.stopword:
                newSentence.append(word)
        userInput=(' '.join(newSentence))
        testx=self.vectorizer.transform([userInput])
        return self.clf.predict(testx)
    def startthebot(self):
        print(f"Bot:{random.choice(self.responses['greet'])}")
        req=input("User:")
        tag=self.findemotion(req)
        while(tag[0]!="quit"):
            print(f"Bot:{tag[0]} {random.choice(self.responses[f'{tag[0]}'])}")
            req=input("User:")
            tag=self.findemotion(req)
        print(f"Bot:{tag[0]} {random.choice(self.responses['quit'])}")

            
obj=gehu()
gehu.startthebot(obj)
