# to invite a bot, here's the way to make a link :
#    https://discordapp.com/oauth2/authorize?client_id={CLIENTID}&scope=bot&permissions={PERMISSIONINT}
# the permission int can be calculated on the dicord docs, I used this : 3397696

from pathlib import Path
from init import *


class room_obj():
    """The class used to represent a room.
    desc is a str containing the room description.
    exits is a set containing the exits,
    they are represented by the cardinal constants in init.py.
    players is a set containing the id of players in the room.
    """
    def __init__(self, desc, exits=None, players=None):
        self.desc = desc
        # see https://github.com/flodri/py-DMUD/issues/9
        if exits   is None: self.exits   = set()
        else: self.exits   = exits
        if players is None: self.players = set()
        else: self.players = players

    def check_exit(self, d, inst, x, y, z):
        """Check if the exits actually lead to a existing room.
        Return True if yes, otherwise return False.
        """
        if   d == NORTH: y += 1
        elif d == EST  : x += 1
        elif d == SOUTH: y -= 1
        elif d == WEST : x -= 1
        elif d == UP   : z += 1
        elif d == DOWN : z -= 1
        if (inst in world) and ((x, y, z) in world[inst]): return True
        return False

    def warn_coming(self, player_id):
        global toSend
        """if there is others players in the room player_id went,
        warn them player_id entered
        """
        p = players[player_id]
        for player_in_room in self.players:
            toSend.append((player_in_room, f'{players[player_id].pseudo} just entered the room.'))

    def warn_leaving(self, player_id, d):  # d for direction
        global toSend
        """if there was others players in the room player_id was,
        warn them player_id left
        """
        for player_in_room in self.players:  # if .players is empty, the for loop is not executed
            toSend.append((player_in_room, f"{players[player_id].pseudo} just left {directions_to_text[d]}"))

    def __repr__(self):
        return f'room_obj(**{self.__dict__.__repr__()})'


class player_obj():
    """The class used to represend a player.
    idt is the discord id of the player, since it's guarented to be unique, it's re-used
    x,y, and z are int and represent the position of the player
    inst can be what you whant and correspond the instance id the player is in.
    pseudo is a str which represent the pseudonym of the player
    """
    def __init__(self, idt, x, y, z, inst, pseudo):
        self.idt    = idt
        self.x      = x
        self.y      = y
        self.z      = z
        self.inst   = inst
        self.pseudo = pseudo

    def save(self):
        """Save player data,
        by default in the players folder under a file with the player id.
        """
        with open(f'players/{self.idt}.txt', 'w') as fichier:
            fichier.write(self.__repr__())

    def disconnect(self):
        world[self.inst][self.x, self.y, self.z].players.discard(self.idt)
        connected.discard(self.idt)

    def __repr__(self):
        return f'player_obj(**{self.__dict__.__repr__()})'


class menu_cmd_info():
    """A container to help with the admin menu type command like !create,
    since it's "fragmented" commands it need to stock some data

    (yes, I know about named tuple, but modifying value in them is bothersome and
    I didn't felt like using a dict, so a class it is :p)
    """
    def __init__(self, menu_command, channel, waiting_for, inst, x, y, z):
        self.menu_command = menu_command
        
        self.channel      = channel
        self.waiting_for  = waiting_for
        self.inst         = inst
        self.x            = x
        self.y            = y
        self.z            = z


def load_player(player_id):
    global players
    """load a player object in the players dict with the player_id key
    """
    with open(f'players/{player_id}.txt', 'r') as fichier:
        players[player_id] = eval(fichier.read())


def desc_room(player_id):
    """return a description of the room ready to be send to the player
    """
    p = players[player_id]
    if (p.x, p.y, p.z) in world[p.inst]:
        room = world[p.inst][p.x, p.y, p.z]
        r = [(p.x, p.y, p.z).__repr__(), '\n', room.desc]
        if len(room.players) > 1:  # since there's the player requesting the desc, it's always at least 1
            r.append('\nAre also present in the room :\n')
            others = room.players.copy()
            others.remove(player_id)
            for player_in_room in others:
                r.append(players[player_in_room].pseudo)
                r.append('\n')
        return ''.join(r)
    else: return "`! inexisting room !`\n(contact a admin, htf did you get here ?)"


def desc_room_admin(inst, x, y, z):
    """return a description of the room ready to be send to a admin
    """
    if (x, y, z) in world[inst]:
        room = world[inst][x, y, z]
        r = [(x, y, z).__repr__(), '\n', room.desc]
        if len(room.players) > 0:  # there can be nobody, since a admin is not physicaly present in the world
            r.append('\nAre also present in the room :\n')
            for player_in_room in room.players:
                r.append(players[player_in_room].pseudo)
                r.append('\n')
        return ''.join(r)
    else: return "`! inexisting room !`"


def movement(player_id, d):
    """handle the movement logic of the player
    """
    global players, world
    player = players[player_id]
    room = world[player.inst][player.x, player.y, player.z]
    if d in room.exits:
        if room.check_exit(d, player.inst, player.x, player.y, player.z):  # while building lot of exits where leading nowhere, which caused problems, so it's better to not assume that there isn't any error with the build exits.
            room.players.remove(player_id)
            room.warn_leaving(player_id,d)
            if   d == NORTH: player.y += 1
            elif d == EST  : player.x += 1
            elif d == SOUTH: player.y -= 1
            elif d == WEST : player.x -= 1
            elif d == UP   : player.z += 1
            elif d == DOWN : player.z -= 1
            room = world[player.inst][player.x, player.y, player.z]
            room.warn_coming(player_id)
            room.players.add(player_id)
            return desc_room(player_id),[directions_to_emoji[d] for d in room.exits]
        else: return f"The room in {directions_to_text[d]} direction doesn't seem to exist.\nPlease contact a admin.", False
    else: return f"You can't go {directions_to_text[d]}.", False


def cmd_interpreter(player_id, text, msg):
    """Implement the folowing commands in order :
    logout  : disconnect the player
    -       : send what folows to others in the room
    look    : return the room description
    who     : return a list of who's online
    help    : return a link to the default command list of py-DMUD
    n/north : if possible, move the player in said direction
    e/est   : if possible, move the player in said direction
    s/south : if possible, move the player in said direction
    w/west  : if possible, move the player in said direction
    u/up    : if possible, move the player in said direction
    d/down  : if possible, move the player in said direction
    """
    global players, world, toSend
    if (text == "link start"):
        p = players[player_id]
        room = world[p.inst][p.x, p.y, p.z]
        room.players.add(player_id)
        print(room)
        return ("`**WELCOME !**`\n> Based on py-DMUD by Flodri (discord : Flodri#5261). See <https://github.com/flodri/py-DMUD>\n\n" + desc_room(player_id)), [directions_to_emoji[d] for d in room.exits]
    elif (text == "logout") and (player_id in connected):
        players[player_id].disconnect()
        return "`Successfully logged out.`", False

    ### The '-' command :
    if text.startswith('-'):
        p = players[player_id]
        sendTo = world[p.inst][p.x, p.y, p.z].players.copy()
        sendTo.discard(player_id)
        if len(sendTo) == 0: return "Nobody can hear you as you are alone.", False
        else:
            msg = f'`{players[player_id].pseudo} : {str(msg.content)[1:]}`'
            for player_in_room in sendTo: toSend.append((player_in_room, msg))
            return msg, False

    ### The look command :
    elif text == 'look':
        return desc_room(player_id), False  # TODO, change the False by the actual emojis

    ### The who command :
    elif text == 'who':
        who_list = [players[player_id].pseudo for player_id in connected]
        return str(len(who_list))+'\n'+'\n'.join(who_list), False
    
    ### The help command :
    elif text == 'help':
        return'https://github.com/flodri/py-DMUD/wiki/command-list', False
    
    ### The movements commands :
    d=False
    if   text in {'n', 'north'}: d = NORTH
    elif text in {'e', 'est'  }: d = EST
    elif text in {'s', 'south'}: d = SOUTH
    elif text in {'w', 'west' }: d = WEST
    elif text in {'u', 'up'   }: d = UP
    elif text in {'d', 'down' }: d = DOWN
    if d: return movement(player_id, d)

    ### if the command is not recognised :
    return '?', False



##################################
#End of def, start of game logic :
##################################



with open('world.txt', 'r') as fichier:
    world.update(eval(fichier.read()))
    
with open('admins.txt', 'r') as fichier:
    admins = (eval(fichier.read()))

Path('./players').mkdir(exist_ok=True)
for p in os.listdir('./players'):
    load_player(p[:-4])

# Make sure everyone is disconnect, so if your game crashed,
# people aren't still connected when they don't expect it
for player_id in players:
    players[player_id].disconnect()


async def background_toSend():
    """Send regularly the messages stored in toSend to the corresponding players
    """
    global toSend
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            if len(toSend)!= 0:
                print(toSend)
                for m in toSend[:]:
                    await players_channels[m[0]].send(m[1])
                    toSend.remove(m)  # can't use pop and the index as toSend can be modified during the await
            await asyncio.sleep(0.5)  # Repeat after 0.5 s
        except:
            print("!!!!!!! backgroud_toSend is crashing !!!!!!!'\n")
            await asyncio.sleep(0.1)


@client.event  # event decorator/wrapper
async def on_ready():
    print(f'Logged on as {client.user}')


@client.event  # event decorator/wrapper
async def on_reaction_add(reaction, user):
    """If a player add a reaction, emule the corresponding command
    """
    if user != client.user:
        message = reaction.message
        if str(message.channel)[0:20] == 'Direct Message with ':
            text = reaction_to_command.get(reaction.emoji)
            if text is None: await message.channel.send('?')
            else:
                player_id = str(user.id)
                if player_id in connected:
                    to_return, reactions = cmd_interpreter(player_id, text, message)
                    async with message.channel.typing():
                        msg = await message.channel.send(to_return)
                    if reactions:
                        for emoji in reactions: await msg.add_reaction(emoji)


@client.event  # event decorator/wrapper
async def on_message(message):
    global MENU_CMD_INFO

    try :  # To have a idea of what's going on,
           # to comment out if you actually have some amount of activity on your mud
        print(message.content)
    except : print("##### !!! UN-PRINTABLE !!! #####")

    if message.author != client.user:  #otherwise it answer itself (-_-")
        msg = str(message.content)

        if str(message.channel)[0:20]=='Direct Message with ':
            player_id = str(message.author.id)
            text = str(message.content)
            if text == "link start":
                # Already registered :
                if player_id in players:
                    if player_id in connected:
                        await message.channel.send("you're already connected to your avatar.")
                    else:
                        players_channels[player_id] = message.channel
                        connected.add(player_id)
                        async with message.channel.typing():
                            to_return, reactions = cmd_interpreter(player_id, text, message)
                        msg = await message.channel.send(to_return)
                        if reactions:
                            for emoji in reactions: await msg.add_reaction(emoji)

                # First connexion :desc,exits=set(),players=set())
                else:
                    players_channels[player_id] = message.channel
                    # No charactere creation as is, if you want one you should put it here
                    # instead of the cmd_interpreter(message) part
                    players[player_id] = player_obj(player_id, 0, 0, 0, 0, str(message.author))
                    connected.add(player_id)
                    async with message.channel.typing():
                        to_return, reactions = cmd_interpreter(player_id, text, message)
                    msg = await message.channel.send(to_return)
                    if reactions:
                        for emoji in reactions: await msg.add_reaction(emoji)

            # If not "link start" and the player is co, we interprete :
            elif player_id in connected:
                async with message.channel.typing():
                    to_return, reactions = cmd_interpreter(player_id, text, message)
                msg = await message.channel.send(to_return)
                if reactions:
                    for emoji in reactions: await msg.add_reaction(emoji)
            #If not "link start" is not co, we check if we're creating a caracter, if yes interprete acordingly
            #otherwise ignore :
            #elif etat.get(player_id) <=-1:
            #    async with message.channel.typing():
            #        await message.channel.send(crea_FR(message))

        elif str(message.author) in admins:  #admins is a set, so hashtable make this pretty fast

            if (not MENU_CMD_INFO is None) and (message.channel == MENU_CMD_INFO.channel):
                if MENU_CMD_INFO.menu_command == MENU_CMD_CREA_ROOM:
                    if MENU_CMD_INFO.waiting_for == WAITING_DESC:
                        world[MENU_CMD_INFO.inst][MENU_CMD_INFO.x, MENU_CMD_INFO.y, MENU_CMD_INFO.z] = room_obj(msg)
                        MENU_CMD_INFO.waiting_for = WAITING_EXITS
                        await message.channel.send(f'The room now have the following description :\n{msg}\n\nWhat should be the exits ? (n,e,s,w,u,d)')
                    elif MENU_CMD_INFO.waiting_for == WAITING_EXITS:
                        exits = msg.split(',')
                        world[MENU_CMD_INFO.inst][MENU_CMD_INFO.x, MENU_CMD_INFO.y, MENU_CMD_INFO.z].exits = {short_to_directions[d] for d in exits}
                        MENU_CMD_INFO.waiting_for = WAITING_CREATE_OPOSITE_EXITS
                        await message.channel.send(f'The room now have the following exits :\n{exits}\n\nDo you want me to create automaticaly the coresponding exits in the adjacent room ?\n    1) yes\n    2) no')
                    elif MENU_CMD_INFO.waiting_for == WAITING_CREATE_OPOSITE_EXITS:
                        if msg == '1':
                            INST = MENU_CMD_INFO.inst
                            X = MENU_CMD_INFO.x
                            Y = MENU_CMD_INFO.y
                            Z = MENU_CMD_INFO.z
                            for exit_ in world[INST][X, Y, Z].exits:
                                if   exit_ == NORTH:
                                    if (X, Y+1, Z) in world[INST]: world[INST][X, Y+1, Z].exits.add(SOUTH)
                                elif exit_ == EST  :
                                    if (X+1, Y, Z) in world[INST]: world[INST][X+1, Y, Z].exits.add(WEST)
                                elif exit_ == SOUTH:
                                    if (X, Y-1, Z) in world[INST]: world[INST][X, Y-1, Z].exits.add(NORTH)
                                elif exit_ == WEST :
                                    if (X+1, Y, Z) in world[INST]: world[INST][X+1, Y, Z].exits.add(EST)
                                elif exit_ == UP   :
                                    if (X, Y, Z+1) in world[INST]: world[INST][X, Y, Z+1].exits.add(DOWN)
                                elif exit_ == DOWN :
                                    if (X, Y, Z-1) in world[INST]: world[INST][X, Y, Z-1].exits.add(UP)
                            MENU_CMD_INFO = None
                        elif msg == '2': MENU_CMD_INFO = None
                        else: return 'Please enter either 1 for yes, or 2 for no.'
                        await message.channel.send('Done.')
                elif MENU_CMD_INFO.menu_command == MENU_CMD_CHANGE_DESC:
                    if MENU_CMD_INFO.waiting_for == WAITING_DESC:
                        INST = MENU_CMD_INFO.inst
                        X = MENU_CMD_INFO.x
                        Y = MENU_CMD_INFO.y
                        Z = MENU_CMD_INFO.z
                        world[INST][X, Y, Z].desc = msg
                        MENU_CMD_INFO = None
                        await message.channel.send(f'The room at {INST} {X},{Y},{Z} now have the following description :\n{msg}')
                elif MENU_CMD_INFO.menu_command == MENU_CMD_CHANGE_EXITS:
                    if MENU_CMD_INFO.waiting_for == WAITING_EXITS:
                        try:
                            exits = msg.split(',')
                            INST = MENU_CMD_INFO.inst
                            X = MENU_CMD_INFO.x
                            Y = MENU_CMD_INFO.y
                            Z = MENU_CMD_INFO.z
                            world[INST][X, Y, Z].exits = {short_to_directions[d] for d in exits}
                            MENU_CMD_INFO = None
                            await message.channel.send(f'The room at {INST} {X},{Y},{Z} now have the following exits :\n{exits}')
                        except: await message.channel.send('Incorrect syntax.\nexits must be a list like follow :\nn,e,s,w,u,d')

            elif ("!quit" == msg):
                # Disconnect your bot.
                await message.channel.send('Disconnecting.')
                await client.close()
                sys.exit()

            elif ("!save" == msg):
                # Save everything.
                for p in players: players[p].save()
                with open('world.txt', 'w') as fichier:
                    fichier.write(world.__repr__())
                await message.channel.send('Save completed.')

            elif ("!save quit" == msg):
                # Save everything, then disconnect your bot.
                for p in players: players[p].save()
                with open('world.txt', 'w') as fichier:
                    fichier.write(world.__repr__())
                await message.channel.send('Save completed.\nDisconnecting')
                await client.close()
                sys.exit()

            elif msg.startswith('!admin '):
                # add a admin to your game, if he's already admin remove him
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

            elif msg.startswith('!create '):
                coord = msg[8:]
                try:
                    coords = coord.split(',')
                    INST = int(coords[0])
                    X = int(coords[1])
                    Y = int(coords[2])
                    Z = int(coords[3])
                    if (world.get(INST) is None) or (world[INST].get((X, Y, Z)) is None):
                        MENU_CMD_INFO = menu_cmd_info(MENU_CMD_CREA_ROOM, message.channel, WAITING_DESC, INST, X, Y, Z)
                        await message.channel.send(f'A room as been created in {INST} {X},{Y},{Z}, what should the description be ?')
                    else: await message.channel.send(f"The room at {INST} {X},{Y},{Z} already exist,\nyou may change it's description or exits with the !desc and !exits commands.")
                except: await message.channel.send('Incorrect syntax.')

            elif msg.startswith('!desc '):
                # syntax : !desc inst,x, y, z desc
                # change the description of the room at inst,x, y, z
                coord = msg[6:]
                try:
                    coords=coord.split(',')
                    INST = int(coords[0])
                    X = int(coords[1])
                    Y = int(coords[2])
                    Z = int(coords[3])
                    if (INST in world) and ((X, Y, Z) in world[INST]):
                        MENU_CMD_INFO = menu_cmd_info(MENU_CMD_CHANGE_DESC, message.channel, WAITING_DESC, INST, X, Y, Z)
                        await message.channel.send(f'The current description is this :```\n{world[INST][X,Y,Z].desc}```\nWhat should be the new one ?')
                    else: await message.channel.send('Incorrect coordinates.\nThis room does not exist.')
                except: await message.channel.send('Incorrect syntax.')

            elif msg.startswith('!exits '):
                # syntax : !exits inst,x, y, z exits
                # change the exits of the room at inst,x, y, z
                coord = msg[7:]
                try:
                    coords = coord.split(',')
                    INST = int(coords[0])
                    X = int(coords[1])
                    Y = int(coords[2])
                    Z = int(coords[3])
                    if (INST in world) and ((X, Y, Z) in world[INST]):
                        MENU_CMD_INFO = menu_cmd_info(MENU_CMD_CHANGE_EXITS, message.channel, WAITING_EXITS, INST, X, Y, Z)
                        await message.channel.send(f"The current exits are as follow :\n`{','.join([directions_to_short[d] for d in world[INST][X,Y,Z].exits])}`\nWhat should be the new exits ?")
                    else: await message.channel.send('Incorrect coordinates.\nThis room does not exist.')
                except: await message.channel.send('Incorrect syntax.')

            elif msg.startswith('!look '):
                # syntax : !look inst,x, y, z
                # send what a player would see of the room
                coord = msg[6:]
                try:
                    coords=coord.split(',')
                    await message.channel.send(desc_room_admin(int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])))
                except: await message.channel.send('Incorrect syntax.\n(!look inst,x,y,z)')

            elif msg.startswith('!map '):
                try: inst_id = int(msg[5:])
                except: inst_id = msg[5:]
                if inst_id in world:
                    X_MAX = 0
                    X_MIN = 0
                    Y_MAX = 0
                    Y_MIN = 0
                    for room_id in world[inst_id]:
                        x, y, z = room_id
                        if x > X_MAX: X_MAX = x
                        if x < X_MAX: X_MIN = x
                        if y > Y_MAX: Y_MAX = y
                        if y < Y_MIN: Y_MIN = y
                    length = abs(X_MIN) + 1 + abs(X_MAX)
                    height = abs(Y_MIN) + 1 + abs(Y_MAX)
                    matrix = [['.' for l in range(length)] for h in range(height)]
                    # we complete the matrix with rooms :
                    for room_id in world[inst_id]:
                        x, y, z = room_id
                        matrix[y+abs(Y_MIN)][x+abs(X_MIN)]='R'
                    to_r = ["```\n y\n ^_>x\n\n"]

                    # The line and Y axis :
                    index = Y_MAX
                    for line in matrix[::-1]:
                        if index >= 0: to_r.append(f" {index} {' '.join(line)}\n")
                        else: to_r.append(f"{index} {' '.join(line)}\n")
                        index -= 1

                    # The X axis :
                    to_r.append('  ')
                    index = X_MIN
                    for l in range(length):
                        if index < 0: to_r.append(str(index))
                        else: to_r.append(' '+str(index))
                        index+=1

                    to_r.append('```')
                    to_r = ''.join(to_r)

                    # if it's more thans 2000 caracts, well first gg it's a big map, but second we have a probem
                    # because if just one line is more than 2000 caracts, the map can't be send to discord.
                    # otherwise we can split and send multiple message.
                    if len(to_r) >= 2000:
                        print(to_r)
                        await message.channel.send('Your map is too big, and I have yet to write a correct spliter to send it in multiple part on discord,\nSo for now it have been printed on your terminal.')
                    else: await message.channel.send(to_r)
                else: await message.channel.send(f'{inst_id} is not a existing instance')

            elif msg.startswith('!del '):
                # syntax : !del inst, x, y, z
                # delete the room at inst,x, y, z and remove exits leading to it
                coord = msg[5:]
                try:
                    coords = coord.split(',')
                    INST = int(coords[0])
                    X = int(coords[1])
                    Y = int(coords[2])
                    Z = int(coords[3])
                    if (world.get(INST) is None) or (world[INST].get((X, Y, Z)) is None):
                        await message.channel.send(f'There is no room at {INST} {X},{Y},{Z}.')
                    else:
                        exits = world[INST][X, Y, Z].exits
                        del world[INST][X, Y, Z]
                        for exit_ in exits:
                            if   exit_ == NORTH: world[INST][X, Y+1, Z].exits.discard(SOUTH)
                            elif exit_ == EST  : world[INST][X+1, Y, Z].exits.discard(WEST)
                            elif exit_ == SOUTH: world[INST][X, Y-1, Z].exits.discard(NORTH)
                            elif exit_ == WEST : world[INST][X-1, Y, Z].exits.discard(EST)
                            elif exit_ == UP   : world[INST][X, Y, Z+1].exits.discard(DOWN)
                            elif exit_ == DOWN : world[INST][X, Y, Z-1].exits.discard(UP)
                        await message.channel.send(f'The room at {INST} {X},{Y},{Z} has been deleted.')
                except: await message.channel.send('Incorrect syntax.')

        else:
            if ("!who" == msg):
                # print the pseudo of everyone online in the mud.
                who_list = [players[player_id].pseudo for player_id in connected]
                await message.channel.send(str(len(who_list))+'\n'+'\n'.join(who_list))

#client.loop.create_task(background_task())
client.loop.create_task(background_toSend())

client.run(TOKEN)
