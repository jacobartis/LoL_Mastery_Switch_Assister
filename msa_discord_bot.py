import discord
import json
from PIL import Image 
from os.path import exists
from discord.utils import get
from discord.ext import commands
import mastery_switch_assister as msa

#Creates the bot and sets its prefixes and intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["\\","~"],intents = intents)

#command to add summoners to the pool
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="add",help = "Adds summoners to the pool (You can add mutiple at once by surrounding them in quotes).")
async def add_summoners(ctx, names):
    try:
        assert(str(names))
        names_list = names.split()
        summoners = []
        for name in names_list:
            summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
            assert(summoner != None)
            summoners.append(summoner)
        champ_pool.add_summoners(summoners)
        await ctx.channel.send("**added summoners:** "+names)
        save_file()
        
    except Exception as e:
        await ctx.channel.send("Error adding summoner "+names+": "+str(e))

#Handles errors for adding summoners
@add_summoners.error
async def add_summoners_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please include a summoner name to add")
    except Exception as e:
        await ctx.channel.send("Error showing add summoner error message: "+str(e))

#command to disable summoners from the pool
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="disable",help = "Disable summoners in the pool, can be enabled again using enable or enable_all commands (You can disable mutiple summoners at once by surrounding them in quotes).")
async def disable_summoners(ctx, names):
    try:
        assert(str(names))
        names_list = names.split()
        summoners = []
        for name in names_list:
            summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
            assert(summoner != None)
            summoners.append(summoner)
        champ_pool.disable_summoners(summoners)
        await ctx.channel.send("**Disabled summoners:** "+names)
        save_file()
    except Exception as e:
        await ctx.channel.send("Error disabling "+names+": "+str(e))

#Handles errors for disable summoners
@disable_summoners.error
async def disable_summoners_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please include a summoner name to disable")
    except Exception as e:
        await ctx.channel.send("Error showing disable summoner error message: "+str(e))


#command to remove summoners from the pool
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="remove",help = "Remove summoners in the pool (You can remove mutiple summoners at once by surrounding them in quotes).")
async def remove_summoners(ctx, names):
    try:
        assert(str(names))
        names_list = names.split()
        summoners = []
        for name in names_list:
            summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
            assert(summoner != None)
            summoners.append(summoner)
        champ_pool.remove_summoners(summoners)
        await ctx.channel.send("**Removed summoners:** "+names)
        save_file()
    except Exception as e:
        await ctx.channel.send("Error removing "+names+": "+str(e))

#Handles errors for removing summoners
@remove_summoners.error
async def remove_summoners_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please include a summoner name to remove")
    except Exception as e:
        await ctx.channel.send("Error showing remove summoner error message: "+str(e))


#command to enable summoners from the pool
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="enable",help = "Enable disabled summoners in the pool (You can enable mutiple summoners at once by surrounding them in quotes).")
async def enable_summoners(ctx, names):
    try:
        assert(str(names))
        names = names.split()
        summoners = []
        for name in names:
            summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
            assert(summoner != None)
            summoners.append(summoner)
        champ_pool.enable_summoners(summoners)
        await ctx.channel.send("**Enabled "+names+":** "+str(e))
        save_file()
    except Exception as e:
        await ctx.channel.send("Error enabling "+names+": "+str(e))

#Handles errors for enabling summoners
@enable_summoners.error
async def enable_summoners_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please include a summoner name to enable.")
    except Exception as e:
        await ctx.channel.send("Error showing enable summoner error message: "+str(e))


#command to enable all summoners in the pool
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="enable_all",help = "Enables all disabled summoners in the pool.")
async def enable_all_summoners(ctx):
    try:
        champ_pool.enable_all_summoners()
        await ctx.channel.send("**Enabled all summoners!**")
        save_file()
    except Exception as e:
        await ctx.channel.send("Error enabling summoners: "+str(e))

#Handles errors for enabling summoners
@enable_all_summoners.error
async def enable_all_summoners_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Huh?")
    except Exception as e:
        await ctx.channel.send("Error showing enable all summoner error message: "+str(e))


#command to set the pool mastery value
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="mastery",help = "Sets the mastery value of the pool.")
async def set_mastery(ctx, value):
    try:
        assert(int(value))
        champ_pool.set_mastery(int(value))
        await ctx.channel.send("**Set mastery to:** "+value)
        save_file()
    except Exception as e:
        await ctx.channel.send("Error setting mastery: "+str(e))

#command to show the pool mastery value
@set_mastery.error
async def show_mastery(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("**Current mastery:** "+str(champ_pool.mastery))
    except Exception as e:
        await ctx.channel.send("Error showing mastery: "+str(e))


#command to show the current pool or the pool of given summoner(s)
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="show",help = "Shows the current pool or the pool of given summoner(s).")
async def show_pool(ctx, names):
    try:
        assert(str(names))
        names_list = names.split()
        pool = []
        for name in names_list:
            pool.append("**"+name+"**"+":")
            summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
            assert(summoner != None)
            pool.extend(summoner.get_champs_over_value(champ_pool.mastery))
        await ctx.channel.send("__**Champ pool for summoner(s) "+str(names)+":**__ \n"+"\n".join(pool))
    except Exception as e:
        await ctx.channel.send("Error showing champ pool of "+names+": "+str(e))

#Handles errors for showing the pool
@show_pool.error
async def show_pool_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("__**Current pool:**__ \n"+"\n".join(champ_pool.get_pool()))
    except Exception as e:
        await ctx.channel.send("Error showing champ pool: "+str(e))


#               Current WIP
#command to show the current pool
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="show_img",help = "Shows icons of current pool.")
async def show_pool_img(ctx):
    try:
        await ctx.channel.send("__**Current pool:**__ \n")
        for url in champ_pool.get_pool_img():
            await ctx.channel.send(url)
#        for byts in champ_pool.get_pool_img():
#            img = Image.open(byts.read())
#            img.save(byts,format='PNG')
#            img.read()
#            byts.seek(0)
#            byts.read()
#            await ctx.channel.send(discord.File(img))
    except Exception as e:
        await ctx.channel.send("Error showing pool images: "+str(e))

#Handles errors for showing the pool
@show_pool_img.error
async def show_pool_img(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("__**Current pool:**__ \n"+"\n".join(champ_pool.get_pool()))
    except Exception as e:
        await ctx.channel.send("Error showing champ pool as images: "+str(e))


#command to show the current pool as a summoner
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="show_as",help = "Shows the current pool as a summoner (removes their champs from the pool).")
async def show_pool_as(ctx,names):
    try:
        assert(str(names))
        summoners = []
        names_list = names.split()
        for name in names_list:
            summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
            assert(summoner != None)
            summoners.append(summoner)
        await ctx.channel.send("__**Current pool as "+str(names)+":**__ \n"+"\n".join(champ_pool.get_pool_as(summoners)))
    except Exception as e:
        await ctx.channel.send("Error showing as: "+str(e))

#Handles errors for showing the pool as a summoner
@show_pool_as.error
async def show_pool_as_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please include a summoner name to show pool as.")
    except Exception as e:
        await ctx.channel.send("Error showing champ pool as error : "+str(e))


#command to show all summoners 
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="summoners",help = "Shows all summoners in the pool (even disabled ones).")
async def show_summoners(ctx):
    try:
        names = []
        for summoner in champ_pool.all_summoners:
            names.append(summoner.name)
        await ctx.channel.send("__**Current summoners:**__ \n"+"\n".join(names))
    except Exception as e:
        await ctx.channel.send("Error showing summoners: "+str(e))

#Handles errors for showing the current summoners
@show_summoners.error
async def show_summoners_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Huh?")
    except Exception as e:
        await ctx.channel.send("Error showing summoners error: "+str(e))


#command to show the enabled summoners
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="summoners_enabled",help = "Shows enabled summoners in the pool.")
async def show_summoners_enabled(ctx):
    try:
        names = []
        for summoner in champ_pool.enabled_summoners:
            names.append(summoner.name)
        await ctx.channel.send("__**Enabled summoners:**__ \n"+"\n".join(names))
    except Exception as e:
        await ctx.channel.send("Error showing enabled summoners: "+str(e))

#Handles errors for showing the enabled summoners
@show_summoners_enabled.error
async def show_summoners_enabled_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Huh?")
    except Exception as e:
        await ctx.channel.send("Error showing enabled summoners error: "+str(e))


#command to show the disabled summoners
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="summoners_disabled",help = "Shows disabled summoners in the pool.")
async def show_summoners_disabled(ctx):
    try:
        names = []
        for summoner in champ_pool.all_summoners:
            if summoner in champ_pool.enabled_summoners:
                continue
            names.append(summoner.name)
        await ctx.channel.send("__**Disabled summoners:**__ \n"+"\n".join(names))
    except Exception as e:
        await ctx.channel.send("Error showing disabled summoners: "+str(e))

#Handles errors for showing the disabled summoners
@show_summoners_disabled.error
async def show_summoners_disabled_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Huh?")
    except Exception as e:
        await ctx.channel.send("Error showing disabled summoners error: "+str(e))


#command to clear all summoners from the pool
@commands.bot_has_permissions(send_messages=True,read_messages=True)
@bot.command(name="clear",help = "Removes all summoners from the pool.")
async def clear(ctx):
    try:
        champ_pool.clear_summoners()
        await ctx.channel.send("**Removing all summoners!**")
        save_file()
    except Exception as e:
        await ctx.channel.send("Error clearing summoners: "+str(e))

#Handles errors for clearing the champ pool
@clear.error
async def clear_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Huh?")
    except Exception as e:
        await ctx.channel.send("Error showing clear error: "+str(e))


def save_file():
    with open("summoners.json","w") as file:
        file.write(json.dumps(champ_pool.as_dict(), indent=4))

champ_pool = msa.Champ_Pool()


#Reads the Riot key from RiotApiKey.txt
file = open("RiotApiKey.txt")
riot_key = file.readline()
file.close()

try:
    s_file = None
    with open("summoners.json") as file:
        s_file = json.load(file)

    for name in s_file["summoners"]:
        summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
        champ_pool.add_summoners([summoner])

    for name in s_file["disabled"]:
        summoner = msa.Summoner(name,msa.get_champ_data(),riot_key)
        champ_pool.disable_summoners([summoner])
    champ_pool.set_mastery(s_file["mastery"])
except Exception as e:
    print("Error loading file: "+str(e))

#Reads the discord key from DiscordApiKey.txt and runs the corisponding bot
file = open("DiscordApiKey.txt","r")
bot.run(file.readline())
file.close()