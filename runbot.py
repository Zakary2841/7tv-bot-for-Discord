import discord
from discord.ext import commands
from discord import app_commands, Intents, Client, Interaction
import os
from io import BytesIO
from types import SimpleNamespace
from classes import Emote, Channel, UserNotFound, InvalidCharacters
import json
from search import searchemote
import asyncio
import websockets
import time

f = open('config.json')
cfg = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
TOKEN = cfg.TOKEN  #Gets TOKEN from config.json
folder_dir = cfg.output_folder
listenchannel_q = asyncio.Queue()
event = asyncio.Event()

if not os.path.exists(folder_dir):
    os.makedirs(folder_dir)
    print("Output folder created")

if not os.path.exists("tmp"):
    os.makedirs("tmp")
    print("Temporary folder created")
    
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = "!", intents = intents)

    async def setup_hook(self):
        event.set()
    
    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral = True)
        raise error

client = Bot()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await listenchannel_q.put(client.get_channel(cfg.listen_channel))
    event.set()
  
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(r'https://old.7tv.app/emotes/'):
        emoteID = message.content.split("/")[-1]
        e = Emote(emoteID,cfg.showemote_size)
        if hasattr(e.info, 'message'):
            await message.channel.send(e.message)
        else:
            e.download("tmp")
            with open(e.file_path, 'rb') as fp:
                await message.channel.send(file=discord.File(fp))
            os.remove(e.file_path)

    await client.process_commands(message)


@client.hybrid_command(name = "addemote", with_app_command = True, description = "Adds an emote using the provided 7TV Link")
@app_commands.describe(url='URL of the emote you want to add',
    emotename= 'The name you want to newly added emote to be called')
@commands.has_permissions(manage_emojis = True)
async def addemote(ctx, url: str, emotename: str = None):
    success = False
    guild = ctx.guild
    ename = "error"
    error = ""
    if ctx.author.guild_permissions.manage_emojis:
        await ctx.defer(ephemeral = True)
        emoteID = url.split("/")[-1]
        for i in reversed(range(1, 5)):
            print(f"Trying size {i}x...")
            e = Emote(emoteID,i)
            if hasattr(e.info, 'message'):
                await ctx.send(e.message)
            else:
                if emotename is None:
                    ename = e.info.name
                else: ename = emotename
                e.download("tmp")
                with open(e.file_path, 'rb') as fp:
                    try:
                        img_or_gif = BytesIO(fp.read())
                        b_value = img_or_gif.getvalue()
                        emoji = await guild.create_custom_emoji(image=b_value, name=ename)
                        print(f'Successfully added emote: <:{ename}:{emoji.id}>')
                        await ctx.send(f'Successfully added emote: <:{ename}:{emoji.id}>')
                        success = True

                    except Exception as err:
                        #print(f'File size of {i}x is too big!')
                        error = err
                        print(err)

                if os.path.exists(e.file_path):
                    os.remove(e.file_path)

                if success: break
        if not success:
            await ctx.send(f'Unable to add emote {ename}: {error}')


@client.hybrid_command(name = "deleteemote", with_app_command = True, description = "Delete a discord emote by specifying the name")
@app_commands.describe(emote='Name/Emote you want to delete')
@commands.has_permissions(manage_emojis = True)
async def deleteemote(ctx, emote: discord.Emoji):
    if ctx.author.guild_permissions.manage_emojis:
        await ctx.defer(ephemeral = True)
        try:
            await emote.delete()
            print(f'Successfully deleted: {emote}')
            await ctx.send(f'Successfully deleted: {emote}')
        except Exception as err:
            print(err)
            await ctx.send(err)


@client.hybrid_command(name = "findemoteinchannel", with_app_command = True, description = "Find an emote in a Twitch Channel")#
@app_commands.describe(channel='Channel you want to search emotes in',
    emote= 'Text you want to search for',
    exact='Do you want the text to match exactly?')
@commands.has_permissions(manage_emojis = True)
async def findemoteinchannel(ctx, channel: str, emote: str, exact= False):
    print(f"FindEmoteQuery = Channel:{channel} Emote:{emote}")
    await ctx.defer(ephemeral = True)
    try:
        c = Channel(channel)
    except UserNotFound:
        await ctx.send("User not found. Please check the username and try again")
    else:
        elist = c.findEmotes(emote, exact)
        message = f'{channel} has {len(elist)} {emote} emote(s):'
        for i in elist:
            print(f"Found {i.name}")
            message += f"\n[{i.name}](https://7tv.app/emotes/{i.id})"

        embed = discord.Embed(
            title= "Search completed!",
            description= message,
            colour= discord.Colour.from_rgb(40,177,166)
    )

        embed.set_thumbnail(url="https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_e02650251d204198923de93a0c62f5f5/static/light/3.0")
        embed.set_footer(text="You can also add the emotes to your server as emoji by: !addemote <emote url>")
        await ctx.send(embed= embed)


@client.hybrid_command(name = "searchemotes", with_app_command = True, description = "Search for emotes using the name")
@app_commands.describe(emote='Name/Emote you want to search for')
@commands.has_permissions(manage_emojis = True)
async def searchemotes(ctx, emote: str):
    message = ""
    if ctx.author.guild_permissions.manage_emojis:
        await ctx.defer(ephemeral = True)
        elist = searchemote(emote)
        message += f'Found {len(elist)} emote(s) that contain "{emote}":'
        for i in elist:
            print(f"Found {i.name}")
            message += f"\n[{i.name}](https://7tv.app/emotes/{i.id})"

        embed = discord.Embed(
            title= "Search completed!",
            description= message,
            colour= discord.Colour.from_rgb(40,177,166)
        )

        embed.set_thumbnail(url="https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_e02650251d204198923de93a0c62f5f5/static/light/3.0")
        embed.set_footer(text="You can also add the emotes to your server as emoji by: !addemote <emote url>")
        await ctx.send(embed= embed)


@client.hybrid_command(name = "addlistenchannel", with_app_command = True, description = "Add a Twitch channel to listen for 7TV emote updates. (Requires restart)")
@app_commands.describe(channel='Name of the channel you want to add to the listening channels')
@commands.has_permissions(manage_emojis = True)
async def addlistenchannel(ctx, channel: str):
    if ctx.author.guild_permissions.manage_emojis:
        await ctx.defer(ephemeral = True)
        await event.wait()
        await asyncio.sleep(1)
        try:
            c = Channel(channel)
        except UserNotFound:
            msg = f"The channel {channel} is not found. Please check the spelling and try again."
            print(msg)
            await ctx.send(msg)
            event.set()
            return
        except InvalidCharacters:
            msg = f"The query {channel} contains invalid characters. Please only use A-Z and numbers."
            print(msg)
            await ctx.send(msg)
            event.set()
            return
        if c.id in cfg.listeningUsers:
            msg = f"The channel {channel} already exists in this list!"
            print(msg)
            await ctx.send(msg)
        else:
            try:
                cfg.listeningUsers.append(c.id)
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(cfg.__dict__, f, ensure_ascii=False, indent=4)
                print((f'Added {channel} to listening channels'))
                await ctx.send(f'Added {channel} to listening channels')
            except Exception as err:
                print(err)
                await ctx.send(err)
                event.set()
        event.set()


@client.hybrid_command(name = "removelistenchannel", with_app_command = True, description = "Remove a Twitch channel to listen for 7TV emote updates. (Requires restart)")
@app_commands.describe(channel='Name of the channel you want to remove from the listening channels')
@commands.has_permissions(manage_emojis = True)
async def removelistenchannel(ctx, channel: str):
    if ctx.author.guild_permissions.manage_emojis:
        await ctx.defer(ephemeral = True)
        await event.wait()
        await asyncio.sleep(1)
        try:
            c = Channel(channel)
        except UserNotFound:
            msg = f"The channel {channel} is not found. Please check the spelling and try again."
            print(msg)
            await ctx.send(msg)
            event.set()
            return
        except InvalidCharacters:
            msg = f"The query {channel} contains invalid characters. Please only use A-Z and numbers."
            print(msg)
            await ctx.send(msg)
            event.set()
            return
        if c.id in cfg.listeningUsers:
            try:
                cfg.listeningUsers.remove(c.id)
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(cfg.__dict__, f, ensure_ascii=False, indent=4)
                msg = f'Removed {channel} from listening channels'
                print(msg)
                await ctx.send(msg)
            except Exception as err:
                print(err)
                await ctx.send(err)
                event.set()
        else:
            msg = f"The channel {channel} does not exist in this list!"
            print(msg)
            await ctx.send(msg)
        event.set()


@client.hybrid_command(name = "listeningchannels", with_app_command = True, description = "Show Twitch channels that the bot is listening to for 7TV emote updates.")
@commands.has_permissions(manage_emojis = True)
async def listeningchannels(ctx):
    msg = "Currently listening: "
    if ctx.author.guild_permissions.manage_emojis:
        await ctx.defer(ephemeral = True)
        if cfg.listeningUsers:
            msg = "Currently listening: "
            lc = [Channel.lookup7TVUser(i) for i in cfg.listeningUsers]
            for i in lc[:-1]:
                msg += f'{i}, '
            msg += f'{lc[-1]}. '
    await ctx.send(msg,ephemeral=False)


@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx):
    print(f"User {ctx.message.author} ID:{ctx.message.author.id} ran command. Asking for confirmation")
    def check(msg): # checking if it's the same user and channel
        return msg.author == ctx.author and msg.channel == ctx.channel
    try:
        msg = ("Are you sure you want to run a global sync?")
        print(msg)
        await ctx.send(msg)        
        response = await client.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError: # returning after timeout
        msg = (f"No response from {ctx.message.author}. Cancelling sync.")
        print(msg)
        await ctx.send(msg)        
        return
    if response.content.lower() not in ("yes", "y"): # lower() makes everything lowercase to also catch: YeS, YES etc.
        msg = (f"User {ctx.message.author} did not enter 'Yes' or 'Y'. Cancelling sync.")
        print(msg)
        await ctx.send(msg)        
        return
    print(f"User {ctx.message.author} ran 'sync' (Global) " )
    await ctx.defer(ephemeral = True)
    #await client.tree.sync()
    msg = (f"Synced slash commands globally for {client.user}.")
    print(msg)
    await ctx.send(msg)        

async def listen():
    accessPt = "wss://events.7tv.io/v3"
    listenchannel = await listenchannel_q.get()
    title = ""
    message = ""
    color = discord.Colour.from_rgb(40, 177, 166)
    e = None
    eurl = ""
    while True:
        if listenchannel:
            async with websockets.connect(accessPt) as ws:
                for i in cfg.listeningUsers:
                    await ws.send(json.dumps({
                    "op": 35,
                    "d": {
                        "type": "emote_set.update",
                        "condition": {
                            # valid fields in the condition depend on the subscription type
                            # though in most cases except creations, object_id is acceptable
                            # to filter for a specific object.

                            "object_id": i
                        }
                    }
                    }))
                while event.is_set():
                    msg = await ws.recv()
                    parsed = json.loads(msg)
                    parsed = parsed['d']
                    if "body" in parsed:
                        title = Channel.lookup7TVUser(parsed['body']['id'])
                        if "pushed" in parsed['body']:
                            e = Emote(parsed['body']['pushed'][0]['value']['id'],3)
                            message = f"Added emote {parsed['body']['pushed'][0]['value']['name']}:\nhttps://7tv.app/emotes/{e.id}"
                            color = discord.Colour.from_rgb(40, 177, 166)

                        elif "pulled" in parsed['body']:
                            e = Emote(parsed['body']['pulled'][0]['old_value']['id'],3)
                            message = f"Removed emote {parsed['body']['pulled'][0]['old_value']['name']}:\nhttps://7tv.app/emotes/{e.id}"
                            color = discord.Colour.from_rgb(177, 40, 51)

                        if e.isAnimated:
                            eurl = f"https://cdn.7tv.app/emote/{e.id}/3x.gif"
                        else:
                            eurl = f"https://cdn.7tv.app/emote/{e.id}/3x.png"

                        embed = discord.Embed(
                            title=title,
                            description=message,
                            colour=color
                        )

                        embed.set_thumbnail(
                            url=eurl)
                        embed.set_footer(
                            text="You can also add the emotes to your server by doing: !addemote <emote url>")
                        await listenchannel.send(embed=embed)

                while not event.is_set():
                    await asyncio.sleep(5)
        await asyncio.sleep(5)


loop = asyncio.get_event_loop()


async def run_bot():
    try:
        await client.start(TOKEN)
    except Exception:
        await client.close()


def run_in_thread():
    fut = asyncio.run_coroutine_threadsafe(listen(), loop)
    fut.result()  # wait for the result


async def main():
    await asyncio.gather(
        run_bot(),
        asyncio.to_thread(run_in_thread)
    )


loop.run_until_complete(main())