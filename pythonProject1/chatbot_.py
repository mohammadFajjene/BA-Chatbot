import json
import pickle
import spacy
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from states import ChatbotStates as cs


# create chatbot class
class Chatbot():

    # initiating variables
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open('intents_.json').read())
        self.nlp = spacy.load('en_core_web_sm')
        self.words = pickle.load(open('C:\\Users\\surface\\PycharmProjects\\pythonProject1\\words.pkl', 'rb'))
        self.classes = pickle.load(open('C:\\Users\\surface\\PycharmProjects\\pythonProject1\\classes.pkl', 'rb'))
        self.model = load_model('C:\\Users\\surface\\PycharmProjects\\pythonProject1\\chatbotmodel.model')
        self.chatbotState = cs()

    # tokenize and lemmetize words
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    # create bag of words
    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)

        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1

        return np.array(bag)

    # predict current state
    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOULD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOULD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list


    # return current state
    def get_response(self, intents_list, intents_json):
        state = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['state']==state:
                result = i['state']
                break
        return result

    # receive message from  frontend
    def ask(self, message):

        currentState = self.chatbotState.current_state.identifier
        # if len(message.split())==1:
        #     ints = self.predict_class(message.lower()[0:5])
        # else:
        ints = self.predict_class(message.lower())
        # print(message.lower())
        # print(len(message.lower().split()))
        nextState = self.get_response(ints, self.intents)
        if (nextState != currentState):
            self.chatbotState.run((currentState + '_to_' + nextState).__str__())
            currentState = nextState
        # print(currentState)
        res = getattr(self.chatbotState, 'on_'+currentState.__str__())(message.lower())
        print(currentState)
        print(currentState)
        return res


