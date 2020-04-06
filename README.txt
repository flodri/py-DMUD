Version : 0.2.0 (06-04-2020) 

To run this you'll need :
- to have a discord bot and put his token in the init.py file (some help on that here : https://discordpy.readthedocs.io/en/latest/discord.html)
- to have python 3.7 or more and the discord.py library

When you have all of this simply run the MAIN.py file.

If you want access to admin commands put your full discord pseudo in the admins set in admins.txt
(you'll be able to add admins with the !admin comand after that)

Changelog :
0.2.0 (06-04-2020)
  - I finally added the only update I kinda promised, OLC stuff, to be precise :
    - a !create command, to create a room to the passed coordinates
    - a !exits command to change a room exits
    - a !desc command to change a room desc
    - a !look command, to allow a admin to see the room as if he was a player inside it
  - fixed me being stupid and not initialising some stuff wich made most admin commands bug
0.1.6 (04-04-2020) 
  - thanks to rrebrick who made me notice it, there's no need anymore to type your bot username in some part of MAIN.py
0.1.5 (31-03-2020):
  - fixed a stupid error in the warn_leaving function which was making it useless
  - added some comments/modified docstring to help document
0.1.4 (30-03-2020)
  - fixed a bug with the "!save quit" command
  - added feedback to all admin commands
  - added the "!admins pseudo" command which add/remove admins without having to edit admins.txt
0.1.3 (29-03-2020)
  - no need to create the players folder anymore thanks to rrebrick
0.1.2 (24-03-2020)
  - fixed a typo in background_toSend in MAIN.py which made it bug
  - fixed a missing exit in the world.txt demo
  - changed the desc_room function in MAIN.py to remove oneself from the desc when it display with others inside
0.1.1 (24-03-2020)
  - fixed typo in init.py
0.1 (22/03/2020)
  - This thing now exist
