import html
import random
import requests

CHUCK_QUOTE_CACHE = [
    "Chuck Norris killed two stones with one bird.",
    "In an average living room there are 1,242 objects Chuck Norris could use to kill you, including the room itself.",
    "What was going through the minds of all of Chuck Norris' victims before they died? His shoe.",
    "Chuck Norris doesn't do Burn Down charts, he does Smack Down charts.",
    "Dark spots on the Moon are the result of Chuck Norris' shooting practice.",
    "When you're Chuck Norris, anything + anything is equal to 1. One roundhouse kick to the face.",
    "Chuck Norris's show is called Walker: Texas Ranger, because Chuck Norris doesn't run.",
    "Chuck Norris's keyboard has the Any key.",
    "Fool me once, shame on you. Fool Chuck Norris once and he will roundhouse kick you in the face.",
    "Once Chuck Norris signed a cheque and the bank bounced.",
    "Sticks and stones may break your bones, but a Chuck Norris glare will liquefy your kidneys.",
    "The square root of Chuck Norris is pain. Do not try to square Chuck Norris, the result is death.",
    "Chuck Norris wipes his ass with chain mail and sandpaper.",
    "Chuck Norris can't test for equality because he has no equal.",
    "Chuck Norris doesn't say \"who's your daddy\", because he knows the answer",
    "Chuck Norris' programs never exit, they terminate.",
    "Once you go Norris, you are physically unable to go back.",
    "Chuck Norris can write infinite recursion functions and have them return.",
    "Chuck Norris can taste lies.",
    "Since 1940, the year Chuck Norris was born, roundhouse kick related deaths have increased 13,000 percent.",
    "Chuck Norris's first program was kill -9.",
    "Chuck Norris's database has only one table, 'Kick', which he DROPs frequently.",
    "Chuck Norris doesn't bowl strikes, he just knocks down one pin and the other nine faint.",
    "Chuck Norris doesn't win, he allows you to lose.",
    "Chuck Norris can write to an output stream.",
    "MacGyver can build an airplane out of gum and paper clips. Chuck Norris can kill him and take it.",
    "Chuck Norris can access the DB from the UI.",
    "Chuck Norris does not need to know about class factory pattern. He can instantiate interfaces.",
    "Chuck Norris' sperm can be seen with the naked eye. Each one is the size of a quarter.",
    "Chuck Norris can win a game of Connect Four in only three moves.",
    "Chuck Norris doesn't play god. Playing is for children.",
    "Chuck Norris's keyboard doesn't have a Ctrl key because nothing controls Chuck Norris.",
    "Chuck Norris will never have a heart attack. His heart isn't nearly foolish enough to attack him.",
    "Chuck Norris doesn't step on toes. Chuck Norris steps on necks.",
    "Chuck Norris got his drivers license at the age of 16. Seconds.",
    "When God said, \"let there be light\", Chuck Norris said, \"say 'please'.\""
]


def get_random_quote() -> str:
    return random.choice(CHUCK_QUOTE_CACHE)


def quote_online() -> str:
    response = ''

    try:
        result = requests.get('https://api.icndb.com/jokes/random')

        if result.status_code == requests.codes.ok:
            payload = result.json()

            if 'value' in payload and 'joke' in payload['value']:
                response = html.unescape(payload['value']['joke'])
            else:
                response = payload['value']
    except requests.exceptions.ConnectionError as e:
        pass

    return response
