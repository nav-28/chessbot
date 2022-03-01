import discord
import random
import json
import requests

lichess = "https://lichess.org/api/user/"
chessdotcom = ""
err_msg = "!stats <site> username"
err_emb = discord.Embed(title="Chess Stats")
err_emb.add_field(name=f"Commands", value=err_msg, inline=False)
err_limit = discord.Embed(title="Chess Bot")
err_limit.add_field(name=f"Error", value="Please wait for 1 minute. API is rate limited.", inline=False)


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
           await message.delete()
           return
        if msg[1] == 'lichess':
           reply, result  = lichessresponse(msg[2])
           if result == -1 or result == 0:
               await message.reply(embed=err_limit)
           else:
               emd = create_embed(msg[2],reply)
               await message.reply(embed=emd)
        return
    
def create_embed(title, msg):
    emd = discord.Embed(title=title+" Stats")
    emd.add_field(name=f"Bullet", value=msg[0], inline=False)
    emd.add_field(name=f"Blitz", value=msg[1], inline=False)
    return emd


def gettoken():
    f = open("token", "r")
    return(f.readline())


def api_lichess(username, gametype):
    response = requests.get(lichess+username+"/perf/"+gametype)
    reply = "current:"
    if response.status_code == 200:
        result = response.json()
        reply+= str(int(result['perf']['glicko']['rating']))
        reply += " "
        reply += str(int(result['stat']['highest']['int']))
        return reply, 1
    elif response.status_code == 429:
        return reply, 0
    else:
        return reply, -1


# TODO: handle if no highest is there
def lichessresponse(username):
    msg, ret = api_lichess(username, "bullet")
    if ret == -1 or ret == 0:
        return msg, -1
    msg2, ret = api_lichess(username, "blitz")
    if ret == -1 or ret == 0:
        return msg, -1

    return [msg, msg2], 1




if __name__ == "__main__":
    token = gettoken()
    client.run(token) 
