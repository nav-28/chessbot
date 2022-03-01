

import requests

lichess = "https://lichess.org/api/user/"
chessdotcom = "https://api.chess.com/pub/player/{username}/stats"
api = ""

def getdata(username):
    response = requests.get(lichess+username+"/perf/blitz")
    if response.status_code == 200:
        result = response.json()
        print(result['perf']['glicko']['rating'])
        if result['perf']['glicko']['provisional'] == True:
            print("Provisional")
        try:
            print(result['stat']['highest']['int'])
        except KeyError as e:
            print("No highest")
    elif response.status_code == 429:
        # API is rate limited
        return msg, 0
    else:
        # username error
        return msg,



def chessdotcom_response(username):
    reply = "Bullet: "
    link = chessdotcom.replace("{username}", username)
    response = requests.get(link)
    if response.status_code == 200:
        result = response.json()
        # get bullet
        try:
            reply += str(result['chess_bullet']['last']['rating'])
            reply += " Best: "
            reply += str(result['chess_bullet']['best']['rating'])
        except KeyError as e:
            reply += "Not Available"

        reply2= "Blitz: "
        # get blitz
        try:

            reply2 += str(result['chess_blitz']['last']['rating'])
            reply2 += " Best "
            reply2 += str(result['chess_blitz']['best']['rating'])

        except KeyError as e:
            reply2 += "Not Available"

        return [reply, reply2], 1


    elif response.status_code == 429:
        # api rate limited
        return reply, 0
    else:
        return reply, -1
    return

if __name__=="__main__":
    msg, res = chessdotcom_response("thunderbird28")
