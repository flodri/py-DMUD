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
EST = 2
SOUTH = 3
WEST = 4
UP = 5
DOWN = 6

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

client = discord.Client()
