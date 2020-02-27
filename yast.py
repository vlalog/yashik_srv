import requests
import json
import config as cn
from flask import *

srv = Flask(__name__)
srv.debug = True

def sendToScreen(video_url):
    
    # Auth and getting Session_id

    auth_data = {
            'login': cn.login, 
            'passwd': cn.paswd
            }

    s = requests.Session()
    s.get("https://passport.yandex.ru/")
    s.post("https://passport.yandex.ru/passport?mode=auth&retpath=https://yandex.ru", data=auth_data)
    Session_id = s.cookies["Session_id"]
    token = s.get('https://frontend.vh.yandex.ru/csrf_token').text
    devices_online_stats = s.get("https://quasar.yandex.ru/devices_online_stats").text
    devices = json.loads(devices_online_stats)["items"]

    
    headers = {
        "x-csrf-token": token,
    }

    data = {
        "msg": {
            "provider_item_id": video_url,
            "player_id":"youtube"
        },
        "device": devices[0]["id"]
    }



    # Sending command with video to device
    res = s.post("https://yandex.ru/video/station", data=json.dumps(data), headers=headers)

    return res.text
    

        
    
@srv.route('/', methods=['GET'])
def urlreq():
   return '''
   <a href="/login">auth</a>
   <form action="/play" method="POST">
  <p>URL: <input type="text" name=url></input></p>
  <input type="submit">
  </form>
    '''
    
@srv.route('/play', methods=['POST'])
def play():
    url = request.form['url']
    try:
        return str(sendToScreen(url)) + '<a href="/">Go to home</a>'
    except:
        return "ERR. Check auth data (login:password):" + cn.login + ':' + cn.paswd + '<br><a href="/login">Auth</a><br><a href="/">Go to home</a>'

@srv.route('/login', methods=['GET'])
def loginpage():
    return '''
<form action="/auth" method="POST">
<p>Login: <input type="text" name=login></p>
<p>Password: <input type="password" name=paswd></p>
<input type="submit">
'''

@srv.route('/auth', methods=['POST'])
def save_auth_data():
    try:
        cn.login = request.form['login']
        cn.paswd = request.form['paswd']
        return 'sucsess <a href="/">back</a>'
    except:
        return 'error <a href="/auth">Try again</a>'


if __name__ == '__main__':
    srv.run(host='0.0.0.0', port='8080')