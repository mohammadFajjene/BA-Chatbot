import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import mysql.connector
import random
from statemachine import StateMachine, State
import json
import spacy
lemmatizer = WordNetLemmatizer()

# database connector
myDB = mysql.connector.connect(
  host="localhost",
  user="root",
  password="000000"
)
myCursor = myDB.cursor()
myCursor.execute("use mydatabase")


# create return variables list
ret_var = []


# reading primitive intents
intents = json.loads(open('C:\\Users\\surface\\PycharmProjects\\pythonProject1\\intents.json').read())
subjectListTokenized =[]
departmentListTokenized = []
examListTokenized =[]
doctorListTokenized =[]
trimmedDoctorName = []

# departments attributes
departmentsAttr = ['contact', 'email', 'phone', 'fax', 'address', 'opening hours']

# subject attributes
subjectsAttr = ['level', 'points', 'hours', 'lecturer', 'language']

# exams attributes
examsAttr = ['date', 'day', 'time', 'tester','room']

# doctors attributes
doctorsAttr = ['function', 'mobile', 'email']

ignore_letters = ['?', '!', '.', 'msc.', ',', ':', '(', ')', '-', '/', 'i', 'of', 'and', 'to', 'dr.', 'prof.', 'm.', 'sc.', 'prof', 'm.sc.', 'dr.-', 'ii', 'dr.', 'II', 'I', 'III']



# adding departments names to patterns
departmentQuery = 'select name from departmentstable'
myCursor.execute(departmentQuery)
departmentList = []
for index, _tuple in enumerate(list(myCursor.fetchall())):
    departmentList.append(_tuple[0].lower())
    departmentList.append(_tuple[0].lower()[0:4])
departmentList.extend(departmentsAttr)
departmentList.append('departments')
for department in departmentList:
    departmentListTokenized.extend(nltk.word_tokenize(department))
intents["intents"][1]["patterns"] = departmentListTokenized






# adding subjects names to patterns
subjectQuery = 'select name from subject'
myCursor.execute(subjectQuery)
subjectList = []
for index,_tuple in enumerate(list(myCursor.fetchall())):
    subjectList.append(_tuple[0].lower())
    subjectList.append(_tuple[0].lower()[0:6])
subjectList.extend(subjectsAttr)
for subject in subjectList:
    subjectListTokenized.extend(nltk.word_tokenize(subject))
for i, subject in enumerate(subjectListTokenized):
    if subjectListTokenized[i] in ignore_letters:
        del(subjectListTokenized[i])

intents["intents"][2]["patterns"] = subjectList#Tokenized



# adding exams names to patterns
examQuery = 'select name from exam'
myCursor.execute(examQuery)
examList = []
for index,_tuple in enumerate(list(myCursor.fetchall())):
    #if (_tuple[0].lower() not in subjectList):
        examList.append(_tuple[0].lower())
        #examList.append(_tuple[0].lower()[0:4])
examList.extend(examsAttr)
for exam in examList:
    examListTokenized.extend(nltk.word_tokenize(exam))
#for i, exam in enumerate(examListTokenized):
    #if examListTokenized[i] in ignore_letters:
        #del(subjectListTokenized[i])

intents["intents"][3]["patterns"] = examList#Tokenized

# adding doctors names to patterns
doctorQuery = 'select name from doctors'
myCursor.execute(doctorQuery)
doctorList = []
for index,_tuple in enumerate(list(myCursor.fetchall())):
   # if (_tuple[0].lower()):
        doctorList.append(_tuple[0].lower())
        doctorList.append(_tuple[0].lower()[0:5])
doctorList.extend(doctorsAttr)
#doctorList.append('doctors')
for doctor in doctorList:
    doctorListTokenized.extend(nltk.word_tokenize(doctor))
for i, doctor in enumerate(doctorListTokenized):
     if doctorListTokenized[i] in ignore_letters:
         del(doctorListTokenized[i])
#     if len(doctorListTokenized[i]) > 5:
#         trimmedDoctorName.append(doctorListTokenized[i][0:5])
# doctorListTokenized.extend(trimmedDoctorName)
intents["intents"][4]["patterns"] = doctorListTokenized

# open intents file to write in
with open("intents_.json", "w") as intents_:
    json.dump(intents, intents_, indent=4)











subjectName =set()
subjectAttribute = []

departmentName = set()
departmentAttribute = []

examName = set()
examAttribute = []

doctorName = set()
doctorAttribute = []



# responses to greetings state
def predict_greetings(sentence):
    ret_var.clear()
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    person_name = doc.ents[0].text
    ret_var.append('Welcome ' + person_name + ', I spelt your name correctly?')
    print(person_name)
    ret_var.append('Can you retype your name please?')
    ret_var.append("Ok, How can I help you ? ")
    ret_var.append(person_name)
    return ret_var



# responses to subjects state
def pridect_subjects(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    subjectNameBag = [0] * len(subjectListTokenized)
    subjectAttrBag = [0] * len(subjectsAttr)
    for w in sentence_words:
        for i, word in enumerate(subjectListTokenized):
            if (word == w) & (w not in ignore_letters) & (w not in subjectsAttr):
                subjectName.add(w)
                subjectNameBag[i] = 1

        for i, word in enumerate(subjectsAttr):
            if (word == w) & (w not in ignore_letters):
                subjectAttribute.append(w)
                subjectAttrBag[i] = 1

    np.array(subjectNameBag)
    np.array(subjectAttrBag)

    subjectNameEmpty = 0
    subjectAttributeEmplty = 0
    if subjectName==set():
        # print('empty set')
        subjectNameEmpty = 1
    if len(subjectAttribute)==0:
        # print('empty list')
        subjectAttributeEmplty = 1

    if subjectAttributeEmplty & subjectNameEmpty:
        ret_var.clear()
        ret_var.append('could not recognize your question, can you retype?')
        return ret_var
    elif subjectNameEmpty:
        ret_var.clear()
        ret_var.append('Can you type subject name please?')
        return ret_var
    elif subjectAttributeEmplty:
        ret_var.clear()
        ret_var.append('what do you want to know about ' + list(subjectName)[0].__str__() + '?')
        return ret_var
    else:
        ret_var.clear()
        subjectAttribute.append('name')
        subjectQuery = 'select ' + ','.join(subjectAttribute)
        subjectQuery = subjectQuery + ' from subject where name like \'%'+list(subjectName)[0].__str__()[0:8]+'%\''
        myCursor.execute(subjectQuery)
        fetchedAttribute = myCursor.fetchall()
        # print(subjectAttribute)
        #lecturerIndex = subjectAttribute.index('lecturer')
        #print(fetchedAttribute[0][lecturerIndex])
        #singleLecturer = fetchedAttribute[0][lecturerIndex]

        if len(fetchedAttribute) > 1:
            res = ''
            for index, attr in enumerate(fetchedAttribute):
                res = res + (attr[-1].__str__() + ': ' + index.__str__()) + ', '

            ret_var.append(res)
            ret_var.append('There are more than one subject found in that name, please insert the index of subject that you want.\n')

        fetchedList = []
        for j in range(len(fetchedAttribute)):
            res = ''
            for i in range(len(subjectAttribute)-1):
                res = res + (subjectAttribute[i] + ': ' + fetchedAttribute[j][i]) + ', '
                print(res)
            fetchedList.append(res)
        ret_var.append(fetchedList)
        ret_var.append('was my answer correct ?')
        ret_var.append('I am sorry, can you retype your question please ?')
        ret_var.append('Thank you, glad to hear that.')
        ret_var.append('how can I help you ?')
        subjectAttribute.clear()
        subjectName.clear()
        return ret_var


# responses to departments state
def predict_departments(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    departmentNameBag = [0] * len(departmentListTokenized)
    departmentAttrBag = [0] * len(departmentsAttr)
    for w in sentence_words:
        for i, word in enumerate(departmentListTokenized):
            if (word == w) & (w not in ignore_letters) & (w not in departmentsAttr):
                departmentName.add(w)
                departmentNameBag[i] = 1

        for i, word in enumerate(departmentsAttr):
            if (word == w) & (w not in ignore_letters):
                departmentAttribute.append(w)
                departmentAttrBag[i] = 1

    np.array(departmentNameBag)
    np.array(departmentAttrBag)

    departmentNameEmpty = 0
    departmentAttributeEmplty = 0
    if departmentName == set():
        # print('empty set')
        departmentNameEmpty = 1
    if len(departmentAttribute) == 0:
        # print('empty list')
        departmentAttributeEmplty = 1

    if departmentAttributeEmplty & departmentNameEmpty:
        ret_var.clear()
        ret_var.append('could not recognize your question, can you retype?')
        return ret_var
    elif departmentNameEmpty:
        ret_var.clear()
        ret_var.append('Can you type department name please?')
        return ret_var
    elif departmentAttributeEmplty:
        ret_var.clear()
        ret_var.append('what do you want to know about ' + list(departmentName)[0].__str__() + '?')
        return ret_var
    else:
        ret_var.clear()
        departmentQuery = 'select ' + ','.join(departmentAttribute)
        departmentQuery = departmentQuery + ' from departmentstable where name like \'%'+list(departmentName)[0].__str__()+'%\''
        print('xxxxxx', list(departmentName)[0].__str__()[0:4])
        myCursor.execute(departmentQuery)
        fetchedAttribute = myCursor.fetchall()

        fetchedList = []
        res = ''
        for i in range(len(departmentAttribute)):
            res = res + (departmentAttribute[i] + ': ' + fetchedAttribute[0][i]) + ', '
        fetchedList.append(res)
        ret_var.append(fetchedList)
        ret_var.append('was my answer correct ?')
        ret_var.append('I am sorry, can you retype your question please ?')
        ret_var.append('Thank you, glad to hear that.')
        ret_var.append('how can I help you ?')
        departmentAttribute.clear()
        departmentName.clear()
        return ret_var



# responses to exams state
def predict_exams(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    examNameBag = [0] * len(examListTokenized)
    examAttrBag = [0] * len(examsAttr)
    for w in sentence_words:
        for i, word in enumerate(examListTokenized):
            if (word == w) & (w not in ignore_letters) & (w not in examsAttr):
                examName.add(w)
                examNameBag[i] = 1

        for i, word in enumerate(examsAttr):
            if (word == w) & (w not in ignore_letters):
                examAttribute.append(w)
                examAttrBag[i] = 1

    np.array(examNameBag)
    np.array(examAttrBag)

    examNameEmpty = 0
    examAttributeEmplty = 0
    if examName == set():
        # print('empty set')
        examNameEmpty = 1
    if len(examAttribute) == 0:
        # print('empty list')
        examAttributeEmplty = 1

    if examAttributeEmplty & examNameEmpty:
        ret_var.clear()
        ret_var.append('could not recognize your question, can you retype?')
        return ret_var
    elif examNameEmpty:
        ret_var.clear()
        ret_var.append('Can you type exam name please?')
        return ret_var
    elif examAttributeEmplty:
        ret_var.clear()
        ret_var.append('what do you want to know about ' + list(examName)[0].__str__() + '?')
        return ret_var
    else:
        ret_var.clear()
        examAttribute.append('name')
        examQuery = 'select ' + ','.join(examAttribute)
        examQuery = examQuery + ' from exam where name like \'%'+list(examName)[0].__str__()[0:7]+'%\''
        myCursor.execute(examQuery)
        fetchedAttribute = myCursor.fetchall()

        if len(fetchedAttribute) > 1:
            res = ''
            for index, attr in enumerate(fetchedAttribute):
                res = res + (attr[-1].__str__() + ': ' + index.__str__()) + ', '
            ret_var.append(res)
            ret_var.append('There are more than one exam found in that name, please insert the index of exam that you want.\n')

        fetchedList = []
        for j in range(len(fetchedAttribute)):
            res = ''
            for i in range(len(examAttribute)-1):
                res = res + (examAttribute[i] + ': ' + fetchedAttribute[j][i]) + ', '
            fetchedList.append(res)

        ret_var.append(fetchedList)
        ret_var.append('was my answer correct ?')
        ret_var.append('I am sorry, can you retype your question please ?')
        ret_var.append('Thank you, glad to hear that.')
        ret_var.append('how can I help you ?')
        examAttribute.clear()
        examName.clear()
        return ret_var




# responses to doctors state
def predict_doctors(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    doctorNameBag = [0] * len(doctorListTokenized)
    doctorAttrBag = [0] * len(doctorsAttr)
    for w in sentence_words:
        for i, word in enumerate(doctorListTokenized):
            if (word == w) & (w not in ignore_letters) & (w not in doctorsAttr):
                doctorName.add(w)
                doctorNameBag[i] = 1

        for i, word in enumerate(doctorsAttr):
            if (word == w) & (w not in ignore_letters):
                doctorAttribute.append(w)
                doctorAttrBag[i] = 1

    np.array(doctorNameBag)
    np.array(doctorAttrBag)

    doctorNameEmpty = 0
    doctorAttributeEmplty = 0
    if doctorName == set():
        # print('empty set')
        doctorNameEmpty = 1
    if len(doctorAttribute) == 0:
        # print('empty list')
        doctorAttributeEmplty = 1

    if doctorAttributeEmplty & doctorNameEmpty:
        ret_var.clear()
        ret_var.append('could not recognize your question, can you retype?')
        return ret_var
    elif doctorNameEmpty:
        ret_var.clear()
        ret_var.append('Can you type doctor name please?')
        return ret_var
    elif doctorAttributeEmplty:
        ret_var.clear()
        ret_var.append('what do you want to know about Dr. ' + list(doctorName)[0].__str__()[-1:-4] + '?')
        return ret_var
    else:
        ret_var.clear()
        doctorAttribute.append('name')
        doctorQuery = 'select ' + ','.join(doctorAttribute)
        doctorQuery = doctorQuery + ' from doctors where name like \'%'+list(doctorName)[0].__str__()[-7:]+'%\''
        myCursor.execute(doctorQuery)
        fetchedAttribute = myCursor.fetchall()

        if len(fetchedAttribute) > 1:
            res = ''
            for index, attr in enumerate(fetchedAttribute):
                res = res + (attr[-1].__str__() + ': ' + index.__str__()) + ', '
            ret_var.append(res)
            ret_var.append(
                'There are more than one doctor found in that name, please insert the index of doctor that you want.\n')

        fetchedList = []
        for j in range(len(fetchedAttribute)):
            res = ''
            for i in range(len(doctorAttribute) - 1):
                res = res + (doctorAttribute[i] + ': ' + fetchedAttribute[j][i]) + ', '
            fetchedList.append(res)

        ret_var.append(fetchedList)
        ret_var.append('was my answer correct ?')
        ret_var.append('I am sorry, can you retype your question please ?')
        ret_var.append('Thank you, glad to hear that.')
        ret_var.append('how can I help you ?')
        doctorAttribute.clear()
        doctorName.clear()
        return ret_var

# responses to doctors state
def predict_goodbye(sentence):
    ret_var.clear()
    sentence_words = nltk.word_tokenize(sentence)
    if ('bye' or 'goodbye') in sentence_words:
        ret_var.append('Thank you for using Chatbot, goodbye..')



# create chatbot class
class ChatbotStates(StateMachine):

    # defining states
    greetings = State('Greeting', initial=True)
    departments = State('Departments')
    subjects = State('Subjects')
    exams = State('Exams')
    doctors = State('Doctors')
    goodbye = State('Goodbye')

    # defining transitions
    greetings_to_departments = greetings.to(departments)
    greetings_to_subjects = greetings.to(subjects)
    greetings_to_exams = greetings.to(exams)
    greetings_to_doctors = greetings.to(doctors)
    greetings_to_goodbye = greetings.to(goodbye)

    departments_to_subjects = departments.to(subjects)
    departments_to_exams = departments.to(exams)
    departments_to_doctors = departments.to(doctors)
    departments_to_goodbye = departments.to(goodbye)

    subjects_to_departments = subjects.to(departments)
    subjects_to_exams = subjects.to(exams)
    subjects_to_doctors = subjects.to(doctors)
    subjects_to_goodbye = subjects.to(goodbye)

    exams_to_departments = exams.to(departments)
    exams_to_subjects = exams.to(subjects)
    exams_to_doctors = exams.to(doctors)
    exams_to_goodbye = exams.to(goodbye)

    doctors_to_departments = doctors.to(departments)
    doctors_to_subjects = doctors.to(subjects)
    doctors_to_exams = doctors.to(exams)
    doctors_to_goodbye = doctors.to(goodbye)

    # define states functions
    def on_greetings(self, message):
        return predict_greetings(message)


    def on_departments(self, message):
        return predict_departments(message)


    def on_subjects(self, message):
        return pridect_subjects(message)


    def on_exams(self, message):
        return predict_exams(message)


    def on_doctors(self, message):
        return predict_doctors(message)

    def on_goodbye(self, message):
        return 'Thank you for using Chatbot, goodbye ..'