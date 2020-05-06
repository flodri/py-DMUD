"""
Where we load the world, declare the global var, some const,...
"""
import sys
import asyncio
import os
import discord
from math import *
from random import *
from time import *

NORTH = 1
EST   = 2
SOUTH = 3
WEST  = 4
UP    = 5
DOWN  = 6

global CREA_ROOM_INFO
CREA_ROOM_INFO = None #for the !create command
WAITING_DESC  = 0
WAITING_EXITS = 1
        
short_to_directions={'n':NORTH,'e':EST,'s':SOUTH,'w':WEST,'u':UP,'d':DOWN}#for the !exits command
directions_to_emoji={NORTH:'⬆️',EST:'➡️',SOUTH:'⬇',WEST:'⬅️',UP:'⏫',DOWN:'⏬'}#for the reactions
directions_to_text={NORTH:'**North**',EST:'**Est**',SOUTH:'**South**',WEST:'**West**',UP:'**Up**',DOWN:'**Down**'}
reaction_to_command={'⬆️':'n','➡️':'e','⬇':'s','⬅️':'w','⏫':'u','⏬':'d'}#to translate the reactions into commands

#### ! put your discord bot token here : ! ###
TOKEN = ''

global players_channels
players_channels = {}

global world
world = {}

global toSend
toSend = []

global players
players = {}

global connected
connected = set()

global admins
admins = set()

client = discord.Client()
