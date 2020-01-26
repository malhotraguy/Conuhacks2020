
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

def push(username,name,zendeskAppId,zendeskAppUId,skills,quizNumbers, overlappedEvents):
    """
    ----------------------------------------
    Inserts given data into firebase db
    ---------------------------------------
    :param username: string
    :param name: string
    :param zendeskAppId: string
    :param zendeskAppUId: string
    :param skills: list
    :param quizNumbers: list
    :param overlappedEvents: list
    --------------------------------------
    :return: result - boolean
    """
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    skillsFinal = ''
    for i in range(len(skills)):
        if i != (len(skills)-1):
            skillsFinal += str(skills[i]) + ","
        else:
            skillsFinal += str(skills[i])

    quizNumbersFinal = ''
    for i in range(len(quizNumbers)):
        if i != (len(quizNumbers)-1):
            quizNumbersFinal += str(quizNumbers[i]) + ","
        else:
            quizNumbersFinal += str(quizNumbers[i])
    overlappedEventsFinal = ''
    for i in range(len(overlappedEvents)):
        if i != (len(overlappedEvents)-1):
            overlappedEventsFinal += str(overlappedEvents[i]) + ","
        else:
            overlappedEventsFinal += str(overlappedEvents[i])
    data = {
        'username':username,
        'name':name,
        'zendeskAppID':zendeskAppId,
        'zendeskAppUId':zendeskAppUId,
        'skills':skillsFinal,
        'quizNumbers':quizNumbersFinal,
        'overlappedEvents':overlappedEventsFinal,
    }
    result = db.push(data)
    return result
ok = pushDB("luix5540", "Edmund", "abcd1234", "1234abcd", ["python","java","HTML"], [10,50,100], ["skating","coffee"])
print(ok)
