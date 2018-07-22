import persistence, requests, re


def username_valid(username):
    return not persistence.check_if_username_exists(username)


def password_valid(password, password2):
    return password == password2


def form_valid(username, password):
    username_pattern = re.search("^[a-zA-Z0-9]*$", username)
    username_length = (len(username) >= 4 and len(username) <= 16)
    password_length = (len(password) >= 8 and len(password) <= 80)
    return username_pattern and username_length and password_length
        

def add_user(username, hashed_password):
    persistence.add_user(username, hashed_password)


def add_vote(data):
    persistence.add_vote(data["planetId"], data["planetName"], data["userId"])


def get_planets(page):
    return requests.get('https://swapi.co/api/planets/?page={}'.format(page)).json()


def get_statistics():
    return persistence.get_statistics()
