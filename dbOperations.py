import pyrebase
# from firebase_admin import db

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


def push_db(username, name, zendesk_app_id, zendesk_app_uid, quiz_metrics, ranked_events="", chosen_event="", volunteer_points=0):
    """
    ----------------------------------------
    Inserts given data into firebase db
    ---------------------------------------
    :param username: string
    :param name: string
    :param zendesk_app_id: string
    :param zendesk_app_uid: string
    :param quiz_metrics: list
    :param ranked_events: list
    :param volunteer_points: int
    --------------------------------------
    :return: result - boolean
    """
    data = {
        'name': name,
        'zendesk_app_id': zendesk_app_id,
        'zendesk_app_uid': zendesk_app_uid,
        'quiz_metrics': quiz_metrics,
        'ranked_events': ranked_events,
        'chosen_event': chosen_event,
        'volunteer_points': volunteer_points

    }
    result = db.child(username).set(data)
    return result


def fetchDB(username, fields):
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


def searchEvent(event):
    """
    -------------------------------------
    searches for people going to the same event
    ----------------------------------------
    :param event: string
    ----------------------------------------
    :return: people: dict
    """
    people = {}

    x = db.child().get().val()
    print(x.values())

    for i in x.values():
        temp = []
        if i["event"] == event:
            user = i["name"]
            temp.append(i["zendesk_app_id"])
            temp.append(i["zendesk_app_uid"])
            people.update({user: temp})
    return people


def changeStatus(username, field_to_change,field_value):
    """
    -------------------------------------
    searches for people going to the same event
    ----------------------------------------
    :param username: string
    :param event: string
    ----------------------------------------
    :return: done: boolean
    """
    db.child(username).child(field_to_change).set(field_value)
    return True


# a function that goes through all the users and gives the specific users UID and ID based upon GOING to same event.
if __name__ == "__main__":
    push_db("heyThere", "Rahul", "abc", "123", [0, 10, 50], ["apple", "bananas"], "soccer", 0)
