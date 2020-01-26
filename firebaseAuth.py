
"""
from firebase import firebase

fb = firebase.FirebaseApplication("https://conuhacks2020-6dc7f.firebaseio.com/", None)

data = {
    'name': 'Edmund',
    'skills': 'python,java,HTML',
    'quiz answers': 'dog,purple,yes',
    'overlapped events': 'piano,math,coffee'
}
result = fb.post('conuhacks2020-6dc7f', data)
print(result)
"""
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDXhXKICYn2uGx4uqZSvRqAQz8_X-btRJ4",
    "authDomain": "conuhacks2020-6dc7f.firebaseapp.com",
    "databaseURL": "https://conuhacks2020-6dc7f.firebaseio.com",
    "projectId": "conuhacks2020-6dc7f",
    "storageBucket": "conuhacks2020-6dc7f.appspot.com",
    "messagingSenderId": "434422996113"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

username = ""
name = "" #alpha
zendeskAppId = 0 #alphanumeric
zendeskAppUId = 0 #alphanumeric
skills = ''
quizNumbers = ''

data = {
    'username':username,
    'name':name,
    'zendeskAppId':zendeskAppUId,
    'skills':'',
    'quizNumbers':'',
    'overlappedEvents':'',
}
db.push(data)
