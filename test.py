

import requests

lichess = "https://lichess.org/api/user/"
chessdotcom = ""
api = ""

def getdata(username):
    response = requests.get(lichess+username+"/perf/blitz")
    if response.status_code == 200:
        result = response.json()
        print(result)
        print(result['perf']['glicko']['rating'])
        print(result['stat']['highest']['int'])
    else:
        print("error")


if __name__=="__main__":
    getdata("thunderbird28")
