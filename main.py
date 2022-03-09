# conda activate myenv
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import tensorflow
import random
import json 
import pickle
import os
import nltk
import datetime
from datetime import date
import speech_recognition as sr
from tensorflow.python.framework import ops
# nltk.download('punkt')
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Last resort 🔽
# engine.setProperty('voice', voices[0].id)

# Like stphen hawking 🔽
# engine.setProperty('voice', voices[11].id)

# Pretty good 🔽
engine.setProperty('voice', voices[10].id)

import speech_recognition as sr


def talk(message):
    engine.say(message)

    engine.runAndWait()

    


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return numpy.array(bag)

def chat():
    print("** Start talking with bot (Type quit to stop) **")
    os.system('afplay reactive.wav')
    engine.say(' You can start talking with bot (Type quit to stop)')
    engine.runAndWait()
    while True:
        
        inp = input("You: ")
        if inp.lower()== "quit" or inp.lower()== "close" or inp.lower()== "end" or inp.lower()== "exit":
            break
        
        results = modal.predict([bag_of_words(inp, words)])
        result_index = numpy.argmax(results)


        tag =  labels[result_index]
        print("It is in "+tag+" tag")
        if result_index > 0.7:
            print('Confidence in the answer - ', result_index)
            for tg in data['intents']:
                if tg['tag'] == tag:
                    response = random.choice(tg['responses'])
            
            if tag == "time_search":
                now = datetime.datetime.now().ctime()
                response = response + now[0:16]
                # response = now.strftime("%d/%m/%Y, %H:%M:%S")
            print(response)
            talk(response)
        else:
            print("Sorry, I did not understand")


def listen():
    r = sr.Recognizer()
    r.energy_threshold = 3000  
    r.dynamic_energy_threshold = True  
    with sr.Microphone() as source:
        audio = r.listen(source)
        mes = r.recognize_google(audio)
        print("**Done Listening**")
        print("Took value: "+mes)

if __name__ == "__main__":
    stemmer = LancasterStemmer()

    with open("intents.json") as file:
        data = json.load(file)

    try:
        with open("data.pickle", "rb") as f:
            words, labels, training, output = pickle.loads(f)
    except:
        words = []
        labels = []
        docs_y = []
        docs_x = []

    
        for intent in data['intents']:
            for pattern in intent['patterns']:
                wrds = nltk.word_tokenize(pattern)

                words.extend(wrds)

                docs_x.append(wrds)
                docs_y.append(intent['tag'])

                if intent['tag'] not in labels:
                    labels.append(intent['tag'])

        words = [stemmer.stem(w.lower()) for w in words if w != "?"]
        words = sorted(list(set(words)))
        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag = []
            wrds = [stemmer.stem(w) for w in doc]
            print(wrds)
            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

        training = numpy.array(training)
        output = numpy.array(output)
        with open("data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)

    ops.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    # hidden layer
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    # Output layer
    net = tflearn.fully_connected(net, len(output[0]),activation="softmax")

    net = tflearn.regression(net)
    modal = tflearn.DNN(net)

    try:
        modal.load("modal.tflearn")
    except:
        modal.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
        modal.save("modal.tflearn")

    chat()
    # listen()