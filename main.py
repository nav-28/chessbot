import discord
import random
import json
import requests

lichess = "https://lichess.org/api/user/{username}/perf/"
lichess_profile = "https://lichess.org/@/"
chessdotcom = "https://api.chess.com/pub/player/{username}/stats"
chesscom_profile = "https://chess.com/member/"
err_msg = "!stats <site> username"
err_emb = discord.Embed(title="Chess Stats")
err_emb.add_field(name=f"Commands", value=err_msg, inline=False)
err_limit = discord.Embed(title="Chess Bot")
err_limit.add_field(name=f"Error", value="Please wait for 1 minute. API is rate limited.", inline=False)
err_user = discord.Embed(title="Chess Bot")
err_user.add_field(name=f"Error", value="Incorrect Username", inline=False)


client = discord.Client()


@client.event
async def on_ready():
    print("now running", client)

@client.event
async def on_message(message):
    if message.content.startswith('!stats'):
        msg = message.content.split()
        if len(msg) != 3:
           await message.reply(embed=err_emb)
           return

       # handle lichess
        if msg[1] == 'lichess':
           reply, result  = lichess_response(msg[2])
           if result == 0:
               await message.reply(embed=err_limit)
           elif result == -1:
               await message.reply(embed=err_user)
           else:
               emd = create_embed(msg[2],reply, 0)
               await message.reply(embed=emd)

        # handle chessdotcom
        elif msg[1] == 'chesscom':
            reply, result = api_chesscom(msg[2])
            if result == 0:
                await message.reply(embed=err_limit)
            elif result == -1:
                await message.reply(embed=err_user)
            else:
                emd = create_embed(msg[2], reply, 1)
                await message.reply(embed=emd)
        else:
            await message.reply(embed=err_msg)
        return
    
def create_embed(username, msg, site):
    profile_link = ""
    if site == 0:
        profile_link += lichess_profile + username
    else:
        profile_link += chesscom_profile + username
    emd = discord.Embed(title=username+" Stats")
    emd.add_field(name=f"Bullet", value=msg[0], inline=True)
    emd.add_field(name=f"Blitz", value=msg[1], inline=True)
    emd.add_field(name=f"Profile Link", value=profile_link, inline=False)
    return emd


def gettoken():
    f = open("token", "r")
    return(f.readline())


def api_lichess(username, gametype):
    link = lichess.replace("{username}", username)
    response = requests.get(link+gametype)
    reply = "current:"
    if response.status_code == 200:
        result = response.json()
        # get current rating
        reply+= str(int(result['perf']['glicko']['rating']))
        # check if provisional
        if result['perf']['glicko']['provisional'] == True:
            reply += "? "
        else:
            reply += " "
        # check if highest available
        reply+= "Highest: "
        try:

            reply += str(int(result['stat']['highest']['int']))
        except KeyError as e:
            reply += "Not Available"

        return reply, 1


    elif response.status_code == 429:
        return reply, 0
    else:
        return reply, -1


def lichess_response(username):
    msg, ret = api_lichess(username, "bullet")
    if ret == 0:
        return msg, 0
    elif ret == -1:
        return msg, -1
    msg2, ret = api_lichess(username, "blitz")
    if ret == 0:
        return msg, 0
    elif ret == -1:
        return msg, -1

    return [msg, msg2], 1

def api_chesscom(username):
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
            reply2 += " Best: "
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





if __name__ == "__main__":
    token = gettoken()
    client.run(token) 
