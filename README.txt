Version : 0.3.2 (10-06-2020) 

To run this you'll need :
- to have a discord bot and put his token in the init.py file (some help on that here : https://discordpy.readthedocs.io/en/latest/discord.html)
- to have python 3.7 or more and the discord.py library

When you have all of this simply run the MAIN.py file.

If you want access to admin commands put your full discord pseudo in the admins set in admins.txt
(you'll be able to add admins with the !admin comand after that)

If you need more informations or help,
here is the wiki : https://github.com/flodri/py-DMUD/wiki
and here is my discord server : https://discord.gg/gbEdcxW

Changelog :
0.3.2 (10-06-2020):
  - A lot of cleaning of MAIN.py to make it easier to read and more PEP8 compliant, thanks pycodestyle
  - every exit var has been renamed exit_ to avoid redefining built-in
  - added the !prefixe command, which change the prefixe for server commands and save it
0.3.1 (09-06-2020):
  - added the disconnect methode to the player_obj class, which simplify some part of the code
  - make sure everyone is disconnected when the game start to avoid people being unexpectedly connected
    if your game crashed
  - added the check_exit methode to the room_oj class
  - now check if exits actually lead somewhere before moving a player
  - the admin !exits and !desc commands are now menu based. Not that there is much to select,
    but it's more intuitive to use since it's now similar to the behavior of !create, 
    and allow to see the previous descriptions and exits which facilitate editing.
  - the admin !create command now have a option to automatically create the corresponding oposites
    exits in the adjacent rooms, simplifying the building process.
0.3.0 (06-05-2020):
  - "!create" now send a warning when there is already a room at the specified coordinates instead of overwriting it.
  - added the "!del" command, it delete a room and all exits leading to it
  - fixed some Typo in the admins commands messages
  - greatly improved the readability (and a bit the perf) of the warn_leaving and warn_coming functions
  - warn_coming() and warn_leaving() are now methodes of the room() class
    which avoid fetching the room in the world dict multiples times, resulting in better perf.
  - greatly improved the readability of the movement() function
  - renamed the room and player class to room_obj and player_obj to avoid confusion in some part of the code
  - added the discord specific ability to emulate commands with reactions, which allow navigation of the world
    with only the mouse/touchscreen (this is the real gem of this update), thanks to Itsformetowrite for the idea.
0.2.4 (05-05-2020):
  - fixed the "!save" and "!save" quit commands
0.2.3 (30-04-2020):
  - fixed a bug which prevented players from connecting again after logging out
  - added the help command which return a link to the default command list of py-DMUD
  (I don't know why I didn't add it sooner)
  - some more documentation for the room and player class
0.2.2 (30-04-2020):
  - fixed the server !who command
0.2.1 (22-04-2020)
  - some cleaning, and the who and !who commands are now faster and more readable
0.2.0 (06-04-2020)
  - I finally added the only update I kinda promised, OLC stuff, to be precise :
    - a !create command, to create a room to the passed coordinates
    - a !exits command to change a room exits
    - a !desc command to change a room desc
    - a !look command, to allow a admin to see the room as if he was a player inside it
  - fixed some mistakes on init which made most admin commands bug
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
