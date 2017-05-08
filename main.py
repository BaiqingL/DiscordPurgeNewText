import discord#,discord.util
import threading
import os.path
import shlex
 
client=discord.Client()
watch_delete=[]
 
@client.event
async def on_ready():
    print("Logged in as "+client.user.name)
 
@client.event
async def on_message(msg):
    global watch_delete
    # delete message if in channel purge list
    if msg.channel.id in watch_delete:
        await client.delete_message(msg)
 
token=None
if not os.path.isfile("./token"):
    token=input("Token file not found. Please enter bot token: ")
    open('token','w').write(token)
else:
    with open('token','r') as tf:
        token=tf.read()
 
class InputThread(threading.Thread):
    def __init__(self,client):
        threading.Thread.__init__(self)
        self.client=client
 
    def dispatch(self,args):
        global watch_delete
        # return if not enough args
        if len(args)<2: return
 
        # iterate channels
        for cid in args[1:]:
            # purge channel
            if args[0]=="purge":
                chan=discord.utils.get(client.get_all_channels(),id=cid)
                self.client.purge_from(chan)
            # watch for new messages and delete
            elif args[0]=="delete-new":
                watch_delete.append(cid)
 
    def run(self):
        while True:
            args=shlex.split(input())
            self.dispatch(args)
 
ipt=InputThread(client)
ipt.start()
client.run(token)
