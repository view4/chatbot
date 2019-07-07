"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random

swear_words=["fuck","shit","prick","cunt", "dumbass","asshole","twat"]

curse_response=["you diseased rhinocerus' pisel", "You're so ugly you make the mirror cry", "screw you", "get lost", "fuck you","u twat"]
stock_responses=["Hello, you may call me Boto, Gad, Hobart, I go by many names.","If you're having a bad day, and you wish to vent, then we can have a curse out match (I won't tell anyone)", "Ask me the weather??", "How are you feeling?", "What is your favourite food","okay, thank you"]

used_stock=[]
used_curses=[]

joke="A man walks into a bar.....ouch"
animations=["afraid", "bored", "confused","crying","dancing","dog","excited", "giggling","heartbroke","inlove","laughing","money","no","ok","takeoff","waiting"]


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    rsp=process_msg(user_message)
    return json.dumps({"animation": choose_mation(), "msg": rsp})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": "You are not my friend"})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

def process_msg(msg):
    if check_if_swore(msg):
        return choose_curse(curse_response)
    elif msg=="how are you?":
        return "fine thanks"
    elif msg[-1]=="?":
        return "My repotoire of understanding is slightly low- je ne comprends pas"
    elif asked_joke(msg):
        return tell_joke()
    elif asked_for_weather(msg):
        return "HaHaHa, the weather you ask, pffft,I ain't that advanced"
    else:
        return choose_stock()




def check_if_swore(msg):
    words=msg.split()
    for word in words:
        if word in swear_words:
            return True
    return False



def choose_curse(type):
    global curse_response
    global used_curses
    length=len(curse_response)-1
    if length==-1:
        curse_response=used_stock
    index=random.randint(0,length)
    rsp=curse_response[index]
    used_curses.append(rsp)
    del curse_response[index]
    return rsp

def choose_stock():
    global stock_responses
    global used_stock
    length=len(stock_responses)-1
    if length==-1:
        stock_responses=used_stock
    index=random.randint(0,length)
    rsp=stock_responses[index]
    used_stock.append(rsp)
    del stock_responses[index]
    return rsp

def choose_mation():
    length=(len(animations))-1
    index=random.randint(0,length)
    return animations[index]
def asked_joke(msg):
    if "joke" in msg:
        return True
    else:
        return False
def tell_joke():
    return joke


def asked_for_weather(msg):
    if "weather" in msg:
        return True
    else:
        return False


if __name__ == '__main__':
    main()

