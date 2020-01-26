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

def pushDB(username,name,zendeskAppId,zendeskAppUId,quizNumbers, overlappedEvents,event):
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
        'zendeskAppUID':zendeskAppUId,
        'quizNumbers':quizNumbersFinal,
        'overlappedEvents':overlappedEventsFinal,
        'event':event
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
    :return: people: list
    """
    people = {}

    x = db.child().get().val()
    print(x.values())

    for i in x.values():
        temp = []
        if i["event"] == event:
            user = i["name"]
            temp.append(i["zendeskAppID"])
            temp.append(i["zendeskAppUID"])
            people.update({user:temp})
    return people


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

pushDB("heyThere","Rahul","abc","123",[0,10,50], ["apple","bananas"],"soccer")
# nah = fetchDB("heyThere",["name","zendeskAppID"])
# print(nah)
#print(search("soccer"))
#print(changeStatus("heyThere","soccer"))
