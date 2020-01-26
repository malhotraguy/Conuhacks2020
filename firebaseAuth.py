import pyrebase
from firebase_admin import db

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

def pushDB(username,name,zendeskAppId,zendeskAppUId,quizNumbers, overlappedEvents,going):
    """
    ----------------------------------------
    Inserts given data into firebase db
    ---------------------------------------
    :param username: string
    :param name: string
    :param zendeskAppId: string
    :param zendeskAppUId: string
    :param quizNumbers: list
    :param overlappedEvents: list
    --------------------------------------
    :return: result - boolean
    """
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
        'name':name,
        'zendeskAppID':zendeskAppId,
        'zendeskAppUId':zendeskAppUId,
        'quizNumbers':quizNumbersFinal,
        'overlappedEvents':overlappedEventsFinal,
        'event':''
    }
    result = db.child(username).set(data)
    return result

def fetchDB(username,fields):
    """
    -------------------------------
    Fetch data about a specific person
    -------------------------------
    :param username: string
    :param fields: list
    ------------------------------
    :return data: dict
    """
    x = {}
    for field in fields:
        i = db.child(username).child(field).get().val()
        x.update({field: i})
    return x

def search(event):
    """
    -------------------------------------
    searches for people going to the same event
    ----------------------------------------
    :param event: string
    ----------------------------------------
    :return: ID and UID
    """

def changeStatus(username, event):
    """
    -------------------------------------
    searches for people going to the same event
    ----------------------------------------
    :param username: string
    :param event: string
    ----------------------------------------
    :return: done: boolean
    """
    done = False
    userEvent = db.child(username).child("event").get().val()
    if userEvent == "":
        db.child(username).child("event").set(event)
        done = True
    return done

#a function that goes through all the users and gives the specific users UID and ID based upon GOING to same event.

#pushDB("heyThere","Rahul","abc123","123abc",[10,50,100], ["skating","coffee"],None)
# nah = fetchDB("heyThere",["name","zendeskAppID"])
# print(nah)

print(changeStatus("heyThere","soccer"))
