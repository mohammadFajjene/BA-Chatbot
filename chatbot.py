import random
import json
import pickle
import spacy
import numpy as np
import nltk
import mysql.connector
import main
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from states import ChatbotStates as cs

myDB = mysql.connector.connect(
  host="localhost",
  user="root",
  password="000000"
)

myCursor = myDB.cursor()
myCursor.execute("use mydatabase")
subjectQuery = 'select name from subject'
myCursor.execute(subjectQuery)
subjectList = []
for index,_tuple in enumerate(list(myCursor.fetchall())):
    subjectList.append(_tuple[0].lower())

# print(subjectList)

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.model')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    print(res)
    ERROR_THRESHOULD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOULD]
    results.sort(key=lambda x: x[1], reverse=True)
    print(results)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag']==tag:
            result = random.choice(i['responses'])
            break
    return result




print('GO! bot is running')
greetingsList = ["hello", "hey", "Welcome to Chatbot", "greetings", "Welcome dear,","nice day, "]
nlp = spacy.load('en_core_web_sm')

while True:
    chatbotState = cs()
    currentState = chatbotState.current_state.identifier
    print(currentState)
    print(random.choice(greetingsList)+" my name is Alice, What 's your name?")
    message = input("")
    doc = nlp(message)
    person_name = doc.ents[0].text
    print('Welcome '+ person_name + ' How are you?')
    message = input("")
    print("Ok, Do you want to know about subjects ? ")
    message = input("")
    if 'yes' in message:
        print('ok, ' + person_name + ' let\'s go')
        nextstate = 'subjects'
        chatbotState.run((currentState + '_to_' + nextstate).__str__())
        currentState = chatbotState.current_state.identifier
        # print(currentState)
        print('please tell me which subject you want to know ?')
        message = input("")
        message = clean_up_sentence(message)
        for item in message:
            if any(item in word for word in subjectList):
                subjectQuery = 'select * from subject where name like \'%'+item+'%\''
                myCursor.execute(subjectQuery)
                subjectList = []
                print(list(myCursor.fetchall()))
            else:
                print('could not recognize, can you retype subject name please?')
                # for index, _tuple in enumerate(list(myCursor.fetchall())):
                #     subjectList.append(_tuple[0].lower())



    # ints = predict_class(message)
    # res = get_response(ints, intents)
    # print(res)

