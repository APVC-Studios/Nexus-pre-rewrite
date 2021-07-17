#Imports
import discord
import os
import time
import json
import urllib
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from datetime import datetime, timezone, date
from discord.ext import commands
#Data
client = commands.Bot(command_prefix='$')
tokenLocation = "token.txt"
client.remove_command("help")
f = open("Version.txt", "r")
version = f.read()
f.close()
with open('Status.json') as f:
    statusData = json.load(f)

#CSR
channels = [
    [,"https://discord.com/api/webhooks//-"], 
    [,"https://discord.com/api/webhooks//-"],
    [,"https://discord.com/api/webhooks//-"],
]
#a

async def isAdmin(userID):
    temp = False
    with open("userConfig.json") as f:
        data = json.load(f)
        for k in data["admins"]:
            if data["admins"][k] == userID:
                temp = True
    return temp

async def isBlacklisted(userID):
    temp = False
    with open("userConfig.json") as f:
        data = json.load(f)
        for k in data["blacklisted"]:
            if data["blacklisted"][k] == userID:
                temp = True
    return temp

async def updateLastMessage(msg):
    createdAt = str(msg.created_at)
    author = msg.author.name
    with open("lastsent.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        data[author] = createdAt

        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile)
        jsonFile.truncate()
async def onlineToEmbed(jsonData):
    try:
        data = jsonData

        # A very hacky but working solution for the bug with not being able to set colors is below
        sixteenIntegerHex = int(data["color"].replace("#", ""), 16)
        readableHex = int(hex(sixteenIntegerHex), 0)

        embed = discord.Embed(title=data["title"], description=data["description"], color=readableHex)
        
        if data["showFields"]:
            for key in data["fields"]:
                field = data["fields"][key]
                embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])

        if data["showAuthor"]:
            embed.set_author(name=data["author"]["name"], url=data["author"]["url"])
            if data["author"]["avatar"]:
                embed.set_author(name=data["author"]["name"], url=data["author"]["url"], icon_url=data["author"]["avatar"])

        if data["showFooter"]:
            embed.set_footer(text=data["footer"]["text"])
            if data["footer"]["image"]:
                embed.set_footer(text=data["footer"]["text"],icon_url=data["footer"]["image"])

        if data["image"]:
            embed.set_image(url=data["image"])

        if data["thumbnail"]:
            embed.set_thumbnail(url=data["thumbnail"])

        return embed
    except Exception as e:
        embed = discord.Embed(title="An error occured!", description="The JSON file may be incorrectly configured, of an incorrect filetype or corrupted. Please check the file and try again.\n\n```{0}```".format(e), color=0xff0000)
        return embed
async def jsonToEmbed(jsonFile):
    if jsonFile.endswith('.json'):
        try:
            with open(jsonFile) as f:
                data = json.load(f)
                print(data["title"])
                
                # A very hacky but working solution for the bug with not being able to set colors is below
                sixteenIntegerHex = int(data["color"].replace("#", ""), 16)
                readableHex = int(hex(sixteenIntegerHex), 0)

                embed = discord.Embed(title=data["title"], description=data["description"], color=readableHex)
                
                if data["showFields"]:
                    for key in data["fields"]:
                        field = data["fields"][key]
                        embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])

                if data["showAuthor"]:
                    embed.set_author(name=data["author"]["name"], url=data["author"]["url"])
                    if data["author"]["avatar"]:
                        embed.set_author(name=data["author"]["name"], url=data["author"]["url"], icon_url=data["author"]["avatar"])

                if data["showFooter"]:
                    embed.set_footer(text=data["footer"]["text"])
                    if data["footer"]["image"]:
                        embed.set_footer(text=data["footer"]["text"],icon_url=data["footer"]["image"])

                if data["image"]:
                    embed.set_image(url=data["image"])

                if data["thumbnail"]:
                    embed.set_thumbnail(url=data["thumbnail"])

                return embed
        except Exception as e:
            embed = discord.Embed(title="An error occured!", description="The JSON file may be incorrectly configured, of an incorrect filetype or corrupted. Please check the file and try again.\n\n```{0}```".format(e), color=0xff0000)
            return embed
    else:
        embed = discord.Embed(title="An error occured!", description="The submitted file is not a json file!", color=0xff0000)
        return embed

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game(statusData["Text"])
    await client.change_presence(status=statusData["StatusType"], activity=game)
    guild = client.get_guild(805226004250492929)
    for invite in await guild.invites():
        if invite.inviter == client.user or invite.inviter.id == 487746760530460674: #If created by bot or created by Digi:
            return
        await invite.delete()

@client.command()
async def help(ctx):
    await ctx.message.delete()
    embedVar = discord.Embed(title="Help", description="Bot version {0}.\nConfig for {1}.\n isBlacklisted:{2}. isAdmin:{3}".format(version, ctx.message.author.display_name, await isBlacklisted(ctx.message.author.id), await isAdmin(ctx.message.author.id)), color=0x03fc13)
    f = open("Commands.txt", "r")
    embedVar.add_field(name="Commands.txt", value=f.read(), inline=False)
    f.close()
    f = open("Changelog.txt", "r")
    embedVar.add_field(name="Changelog.txt", value=f.read(), inline=False)
    f.close()
    embedVar.set_footer(text="DiscordPy version {0}".format(discord.__version__), icon_url="https://i.imgur.com/RPrw70n.jpg")
    await ctx.send(embed=embedVar)

@client.command()
async def loadembed(ctx,key):
    if await isAdmin(ctx.author.id):
        await ctx.message.delete()
        try:
            json_url = urllib.request.urlopen("")
            EmbedList = json.loads(json_url.read())
            json_url = urllib.request.urlopen(EmbedList[key])
            print(EmbedList[key])
            newEmbed = json.loads(json_url.read())
            embed = await onlineToEmbed(newEmbed)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("An error has occured!\n\n```{0}```".format(e))
    else:
        ctx.reply("You lack the permissions to use this command!", mention_author=False)

# This doesn't work, don't uncomment it. It isn't even that usefull
# @client.command()
# async def lastactive(ctx):
#     if await isAdmin(ctx.author.id):
#         with open("lastsent.json") as f:
#             data = json.load(f)
#             num = 1
#             string = []
#             for k in data:
#                 if len(string[num] + k + " : " + data[k]).len > 2000:
#                     num = num + 1
#                 string[num] = string[num] + k + " : " + data[k]
#             embed = discord.Embed(title="Listing data...", description="Note that not all members might be listed.")
#             embed.add_field(name="Field 1", value=string[1], inline=False)
#             if string[2]:
#                 embed.add_field(name="Field 2", value=string[2], inline=False)
#             if string[3]:
#                 embed.add_field(name="Field 3", value=string[3], inline=False)
#             await ctx.reply(embed=embed, mention_author=False)

            
#     else:
#         ctx.reply("You lack the permissions to use this command!", mention_author=False)


@client.command()
async def showjson(ctx):
    if ctx.message.attachments:
        if ctx.message.attachments[0].filename.endswith('.json'):
            await ctx.message.attachments[0].save("TempEmbed.json")
            y = ctx.message.attachments[0]
            print("Downloading {0} as TempEmbed.json".format(y.filename))
            while True:
                print("Server size: {0} | Local size: {1}".format(y.size,os.path.getsize("TempEmbed.json")))
                if os.path.getsize("TempEmbed.json") == y.size:
                    print("Finished downloading TempEmbed.json")
                    break
            embVar = await jsonToEmbed("TempEmbed.json")
            await ctx.reply(embed=embVar, mention_author=False)
        else:
            await ctx.reply('{0} is not a json file!'.format(ctx.message.attachments[0].filename), mention_author=False)
    else:
        await ctx.reply('Please attach a file!', mention_author=False)

@client.command()
async def ping(ctx):
    await ctx.message.delete()
    print("Running test command!")
    embedVar = discord.Embed(title="Pong!", description="Got a reply in {0}".format(round(client.latency, 1)), color=0x4287f5,timestamp=datetime.now())
    msg = await ctx.send(embed=embedVar)
    await msg.delete(delay=5)

@client.command()
async def getinvite(ctx, *, reason):
    reason = " ".join(reason[:])
    invite = await ctx.channel.create_invite(max_age=86400, reason=reason, max_uses=1, unique=True)
    channel = client.get_channel(809735202518859817)
    
    now = datetime.now(tz=timezone.utc)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    embed = discord.Embed(title="New invite generated!", description="Invite was generated by {0} on {1} with the reason \"{2}\"\nInvite url:||{3}||".format(ctx.author.name,dt_string,str(reason),str(invite)), color=0x4bf542)
    await channel.send(embed=embed) #"Test message {0}").format(invite)#
    DM = await ctx.author.create_dm()
    embed = discord.Embed(title="Here's your invite!", description="This invite has a single use and expires in a day.\n\nInvite URL: ||{0}||\n\nNote that abusing the invite system will get you blacklisted!".format(str(invite)), color=0x4bf542)
    await DM.send(embed=embed)
    await ctx.reply('Check your DM\'s!', mention_author=False)

   
@client.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found\n\n```Discord.py reported: {0}```".format(error))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to do that!\n\n```Discord.py reported: {0}```".format(error))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument!\n\n```Discord.py reported: {0}```".format(error))
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument!\n\n```Discord.py reported: {0}```".format(error))
    elif isinstance(error, commands.CommandError) or isinstance(error,commands.CommandInvokeError):
        await ctx.message.add_reaction('❌')
        try:
            await ctx.send("An error has occured!\n\n```Discord.py reported: {0}```".format(error)) #This error can possibly go past Discord's character limit. Better safe then sorry.
        except:
            await ctx.send("An error has occured!")
    else: 
        await ctx.send("An unknown error has occured!")

@client.event
async def on_invite_create(invite):
    if not invite.inviter == client.user and not invite.inviter.id == 487746760530460674 and invite.guild.id == 805226004250492929: #Ignore the bot, Digi and anything that isn't the main server
        await invite.delete(reason="Automated invite invalidation.")
        DM = await invite.inviter.create_dm()
        await DM.send("Making invites is disabled in \"Approach Vector Studios\". Please use the `$getinvite` command instead!")

@client.event
async def on_message(message):
    #message.content.lower()
    if message.author == client.user or message.author.bot or await isBlacklisted(message.author.id):
        await client.process_commands(message)
        return
    channel = message.channel.id
    await updateLastMessage(message)
    #print(channel)
    for x in channels:
        #print(x[0])
        if x[0] == int(channel):
            for x in channels:
                if not x[0] == int(channel):
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(x[1], adapter=AsyncWebhookAdapter(session))
                        msgContent = message.content
                        if message.attachments:
                            for y in message.attachments: 
                                #tempFile = urllib.request.urlretrieve(y.url, "temp/{0}".format(y.filename))
                                await y.save('temp/{0}'.format(y.filename))
                                print("Downloading temp/{0}".format(y.filename))
                                while True:
                                    print("Server size: {0} | Local size: {1}".format(y.size,os.path.getsize('temp/{0}'.format(y.filename))))
                                    if os.path.getsize('temp/{0}'.format(y.filename)) == y.size:
                                        print("Finished downloading temp/{0}".format(y.filename))
                                        msgContent = msgContent + "\n{0}".format(y.url)
                                        break
                        await webhook.send(msgContent, username=message.author.display_name, avatar_url=message.author.avatar_url, allowed_mentions=discord.AllowedMentions.none())
    await client.process_commands(message)
    

f = open(tokenLocation, "r")
client.run(f.read())
f.close()
