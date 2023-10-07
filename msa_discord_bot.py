import discord
from discord.utils import get
from discord.ext import commands
import mastery_switch_assister as msa

#Creates the bot and sets its prefixes and intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["\\","~"],intents = intents)

#command to add summoners to the pool
@commands.has_role("moderator")
@bot.command(name="add",help = "Adds summoners to the pool (You can add mutiple at once by surrounding them in quotes).")
async def add_summoners(ctx, names):
    try:
        assert(str(names))
        names = names.split()
        summoners = []
        for name in names:
            summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
            assert(summoner != None)
            summoners.append(summoner)
        champ_pool.add_summoners(summoners)
        await ctx.channel.send("added summoners: "+str(names))
    except Exception as e:
        await ctx.channel.send("error lol: "+str(e))

#command to dissable summoners from the pool
@commands.has_role("moderator")
@bot.command(name="disable",help = "Disable summoners in the pool, can be enabled again using enable or enable_all commands (You can disable mutiple summoners at once by surrounding them in quotes).")
async def add_summoners(ctx, names):
    try:
        assert(str(names))
        names = names.split()
        summoners = []
        for name in names:
            summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
            assert(summoner != None)
            summoners.append(summoner)
        champ_pool.disable_summoners(summoners)
        await ctx.channel.send("Disabled summoners: "+str(names))
    except Exception as e:
        await ctx.channel.send("error lol: "+str(e))

#command to remove summoners from the pool
@commands.has_role("moderator")
@bot.command(name="remove",help = "Remove summoners in the pool (You can remove mutiple summoners at once by surrounding them in quotes).")
async def add_summoners(ctx, names):
    try:
        assert(str(names))
        names = names.split()
        summoners = []
        for name in names:
            summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
            assert(summoner != None)
            summoners.append(summoner)
        champ_pool.remove_summoners(summoners)
        await ctx.channel.send("Removed summoners: "+str(names))
    except Exception as e:
        await ctx.channel.send("error lol: "+str(e))

#command to enable summoners from the pool
@commands.has_role("moderator")
@bot.command(name="enable",help = "Enable dissabled summoners in the pool (You can enable mutiple summoners at once by surrounding them in quotes).")
async def add_summoners(ctx, names):
    try:
        assert(str(names))
        names = names.split()
        summoners = []
        for name in names:
            summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
            assert(summoner != None)
            summoners.append(summoner)
        champ_pool.enable_summoners(summoners)
        await ctx.channel.send("Enabled summoners: "+str(names))
    except Exception as e:
        await ctx.channel.send("error lol: "+str(e))

#command to enable all summoners in the pool
@commands.has_role("moderator")
@bot.command(name="enable_all",help = "Enables all dissabled summoners in the pool.")
async def add_summoners(ctx):
    try:
        champ_pool.enable_all_summoners()
        await ctx.channel.send("Enabled all summoners!")
    except Exception as e:
        await ctx.channel.send("error lol: "+str(e))

#command to set the pool mastery value
@commands.has_role("moderator")
@bot.command(name="mastery",help = "Sets the mastery value of the pool.")
async def set_mastery(ctx, value):
    try:
        assert(int(value))
        champ_pool.set_mastery(int(value))
        await ctx.channel.send("set mastery to: "+value)
    except:
        await ctx.channel.send("error lol")

#command to show the current pool
@commands.has_role("moderator")
@bot.command(name="show",help = "Shows the current pool.")
async def show_pool(ctx):
    try:
        await ctx.channel.send("Current pool: "+str(champ_pool))
    except Exception as e:
        await ctx.channel.send("error lol: "+str(e))

#command to show the current pool as a player
@commands.has_role("moderator")
@bot.command(name="show_as",help = "Shows the current pool as a summoner (removes their champs from the pool).")
async def show_pool_as(ctx,name):
    try:
        assert(str(name))
        summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
        assert(summoner != None)
        await ctx.channel.send("Current pool as "+str(name)+": "+str(champ_pool.get_pool_as(summoner)))
    except Exception as e:
        await ctx.channel.send("error lol: "+str(e))

#command to show all summoners 
@commands.has_role("moderator")
@bot.command(name="summoners",help = "Shows all summoners in the pool (even disabled ones).")
async def show_summoners(ctx):
    try:
        names = []
        for summoner in champ_pool.all_summoners:
            names.append(summoner.name)
        await ctx.channel.send("Current summoners: "+str(names))
    except Exception as e:
        await ctx.channel.send("error lol: "+str(e))

#command to show the enabled summoners
@commands.has_role("moderator")
@bot.command(name="summoners_enabled",help = "Shows enabled summoners in the pool.")
async def show_summoners(ctx):
    try:
        names = []
        for summoner in champ_pool.enabled_summoners:
            names.append(summoner.name)
        await ctx.channel.send("Enabled summoners: "+str(names))
    except Exception as e:
        await ctx.channel.send("error lol: "+str(e))

#command to show the disabled summoners
@commands.has_role("moderator")
@bot.command(name="summoners_disabled",help = "Shows disabled summoners in the pool.")
async def show_summoners(ctx):
    try:
        names = []
        for summoner in champ_pool.all_summoners:
            if summoner in champ_pool.enabled_summoners:
                continue
            names.append(summoner.name)
        await ctx.channel.send("Disabled summoners: "+str(names))
    except Exception as e:
        await ctx.channel.send("error lol: "+str(e))

champ_pool = msa.Champ_Pool([],0)

#Reads the Riot key from RiotApiKey.txt
file = open("RiotApiKey.txt")
riot_key = file.readline()
file.close()
#Reads the discord key from DiscordApiKey.txt and runs the corisponding bot
file = open("DiscordApiKey.txt","r")
bot.run(file.readline())
file.close()