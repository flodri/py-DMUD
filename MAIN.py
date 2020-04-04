# to invite a bot, here's the way to make a link :
#    https://discordapp.com/oauth2/authorize?client_id={CLIENTID}&scope=bot&permissions={PERMISSIONINT}
#the permission int can be calculated on the dicord docs, I used this : 3397696

from pathlib import Path
from init import *

class room():
    """The class used to represent a room
    """
    def __init__(self,desc,exits=set(),players=set()):
        self.desc    = desc
        self.exits   = exits
        self.players = players
    def __repr__(self):
        return f'room(**{self.__dict__.__repr__()})'

class player():
    """The class used to represend a player
    """
    def __init__(self,idt,x,y,z,inst,pseudo):
        self.idt    = idt
        self.x      = x
        self.y      = y
        self.z      = z
        self.inst   = inst
        self.pseudo = pseudo
    def save(self):
        """Save player data
        """
        with open(f'players/{self.idt}.txt', 'w') as fichier:
            fichier.write(self.__repr__())
    def __repr__(self):
        return f'player(**{self.__dict__.__repr__()})'

def load_player(player_id):
    global players
    """load a player object in the players dict with the player_id key
    """
    with open(f'players/{player_id}.txt', 'r') as fichier:
        players[player_id]=eval(fichier.read())

def warn_coming(player_id):
    global toSend
    """if there is others players in the room player_id went,
    warn them player_id entered
    """
    p = players[player_id]
    msg = f'{players[player_id].pseudo} just entered the room.'
    for player_in_room in world[p.inst][p.x,p.y,p.z].players: #Never empty, there at least the who's now in
        if player_in_room!=player_id:toSend.append((player_in_room,msg))

def warn_leaving(player_id,d): #d for direction
    global toSend
    """if there was others players in the room player_id was,
    warn them player_id left
    """
    p = players[player_id]
    for player_in_room in world[p.inst][p.x,p.y,p.z].players: #Never empty, there's at least the one leaving
        if player_in_room!=player_id:
            #for just 2 string, + is faster than .join
            if   d==NORTH:toSend.append((player_in_room,players[player_id].pseudo+" just left to the north."))
            elif d==SOUTH:toSend.append((player_in_room,players[player_id].pseudo+" just left to the south."))
            elif d==EST  :toSend.append((player_in_room,players[player_id].pseudo+" just left to the est."))
            elif d==WEST :toSend.append((player_in_room,players[player_id].pseudo+" just left to the west."))  
            elif d==UP   :toSend.append((player_in_room,players[player_id].pseudo+" just left up."))
            elif d==DOWN :toSend.append((player_in_room,players[player_id].pseudo+" just left down."))          

def desc_room(player_id):
    """return a description of the room ready to be send to the player
    """
    p=players[player_id]
    if (p.x,p.y,p.z) in world[p.inst]:
        room = world[p.inst][p.x,p.y,p.z]
        r = [(p.x,p.y,p.z).__repr__(),'\n',room.desc]
        if len(room.players)>1: #since there's the player requesting the desc, it's always at least 1
            r.append('\nAre also present in the room :\n')
            others = room.players.copy()
            others.remove(player_id)
            for player_in_room in others:
                r.append(players[player_in_room].pseudo)
                r.append('\n')
        return ''.join(r)
    else :return "`! inexisting room !`\n(contact a admin, htf did you get here ?)"

def movement(player_id,d):
    """handle the movement logic of the player
    """
    global players,world
    p=players[player_id]
    if   d==NORTH:
        if NORTH in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.remove(player_id)
            players[player_id].y+=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "You can't go North."
    elif d==EST  :
        if EST in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.discard(player_id)
            players[player_id].x+=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "You can't go Est."
    elif d==SOUTH:
        if SOUTH in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.discard(player_id)
            players[player_id].y-=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "You can't go South."
    elif d==WEST :
        if WEST in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.discard(player_id)
            players[player_id].x-=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "You can't go West."
    elif d==UP   :
        if UP in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.discard(player_id)
            players[player_id].z+=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "You can't go Up."
    elif d==DOWN :
        if DOWN in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.discard(player_id)
            players[player_id].z-=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "You can't go Down."

def cmd_interpreter(player_id,text,msg):
    """Implement the folowing commands in order :
    logout  : disconnect the player
    -       : send what folows to others in the room
    look    : return the room description
    who     : return a list of who's online
    n/north : if possible, move the player in said direction
    e/est   : if possible, move the player in said direction
    s/south : if possible, move the player in said direction
    w/west  : if possible, move the player in said direction
    u/up    : if possible, move the player in said direction
    """
    global players,world,toSend
    if (text == "link start"):
        p = players[player_id]
        world[p.inst][p.x,p.y,p.z].players.add(player_id)
        return ("`**WELCOME !**`\n> Based on py-DMUD by Flodri (discord : Flodri#5261). See <https://github.com/flodri/py-DMUD>\n\n" + desc_room(player_id))
    elif (text == "logout") and (player_id in connected):
        p = players[player_id]
        world[p.inst][p.x,p.y,p.z].players.discard(player_id)
        connected.discard(player_id)
        return ("`Successfully logged out.`")

    ### The '-' command :
    if text.startswith('-'):
        p = players[player_id]
        sendTo = world[p.inst][p.x,p.y,p.z].players.copy()
        sendTo.discard(player_id)
        if len(sendTo)==0:return "Nobody can hear you as you are alone."
        else:
            msg=f'`{players[player_id].pseudo} : {str(msg.content)[1:]}`'
            for player_in_room in sendTo:toSend.append((player_in_room,msg))
            return msg
        
    ### The look command :
    elif text=='look':
        return desc_room(player_id)

    ### The who command :
    elif text=='who':
        who=[]
        for p in connected:who.append(players[p].pseudo)
        return str(len(who))+'\n'+'\n'.join(who)
    
    ### The movements commands :
    d=False
    if   text in{'n','north'}:d=NORTH
    elif text in{'e','est'  }:d=EST
    elif text in{'s','south'}:d=SOUTH
    elif text in{'w','west' }:d=WEST
    elif text in{'u','up'   }:d=UP
    elif text in{'d','down' }:d=DOWN
    if d:return movement(player_id,d)

    #if the command is not recognised :
    return '?'



##################################
#End of def, start of game logic :
##################################



with open('world.txt', 'r') as fichier:
    world.update(eval(fichier.read()))

Path('./players').mkdir(exist_ok=True)    
for p in os.listdir('./players'):
    load_player(p[:-4])

async def background_toSend():
    """Send regularly the messages stored in toSend to the corresponding players
    """
    global toSend
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            if len(toSend)!=0:
                print(toSend)
                for m in toSend[:]:
                    await players_channels[m[0]].send(m[1])
                    toSend.remove(m)#can't use pop and the index as toSend can be modified during the await    
            await asyncio.sleep(0.5) #Repeat after 0.5 s
        except:
            print("!!!!!!! backgroud_toSend is crashing !!!!!!!'\n")
            await asyncio.sleep(0.1)
            pass

@client.event #event decorator/wrapper
async def on_ready():
    print(f'Logged on as {client.user}')

@client.event #event decorator/wrapper
async def on_message(message):
    
    try : #To have a idea of what's going on,
          #to comment out if you actually have some amount of activity on your mud
        print(message.content)
    except : print("##### !!! UN-PRINTABLE !!! #####")
    
    if message.author != client.user:#otherwise it answer itself (-_-")
        msg = str(message.content)
        
        if str(message.channel)[0:20]=='Direct Message with ':
            player_id = str(message.author.id)
            text = str(message.content)
            if text=="link start":
                #Already registered :
                if player_id in players:
                    if player_id in connected:
                        await message.channel.send("you're already connected to your avatar.")
                    else:
                        players_channels[player_id] = message.channel
                        connected.add(player_id)
                        async with message.channel.typing():
                            await message.channel.send(cmd_interpreter(message))  
                        
                #First connexion :
                else:
                    players_channels[player_id] = message.channel
                    #No charactere creation as is, if you want one you should put it here
                    #instead of the cmd_interpreter(message) part
                    players[player_id]=player(player_id,0,0,0,0,str(message.author))
                    connected.add(player_id)
                    async with message.channel.typing():
                        await message.channel.send(cmd_interpreter(player_id,text,message))

            #If not "link start" and the player is co, we interprete :
            elif player_id in connected:
                async with message.channel.typing():
                    await message.channel.send(cmd_interpreter(player_id,text,message))
            #If not "link start" is not co, we check if we're creating a caracter, if yes interprete acordingly
            #otherwise ignore :
            #elif etat.get(player_id) <=-1:
            #    async with message.channel.typing():
            #        await message.channel.send(crea_FR(message))

        elif str(message.author) in admins:#admins is a set, so hashtable make this pretty fast
            if ("!quit" == msg) :
                #Disconnect your bot.
                await message.channel.send('Disconnecting.')
                await client.close()
                sys.exit()
                
            elif ("!save" == msg):
                #Save everything.
                for p in players:p.save()
                with open('world.txt', 'w') as fichier:
                    fichier.write(world.__repr__())
                await message.channel.send('Save completed.')
                    
            elif ("!save quit" == msg):
                #Save everything, then disconnect your bot.
                for p in players:p.save()
                with open('world.txt', 'w') as fichier:
                    fichier.write(world.__repr__())
                await message.channel.send('Save completed.\nDisconnecting')
                await client.close()
                sys.exit()
            
            elif msg.startswith('!admin '):
                #add a admin to your game, if he's already admin remove him
                pseudo = msg[7:]
                if pseudo in admins:
                    admins.remove(pseudo)
                    with open('admins.txt', 'w') as fichier:
                        fichier.write(admins.__repr__())
                else:
                    admins.add(pseudo)
                    with open('admins.txt', 'w') as fichier:
                        fichier.write(admins.__repr__())
                    await message.channel.send(f'{pseudo} is now a admin.')
            
        else:
            if ("!who" == msg):
                #print the pseudo of everyone online in the mud.
                who=[]
                for p in connected:who.append(players[p].pseudo)
                message.channel.send(str(len(who))+'\n'+'\n'.join(who))
                
#client.loop.create_task(background_task())
client.loop.create_task(background_toSend())

client.run(TOKEN)
