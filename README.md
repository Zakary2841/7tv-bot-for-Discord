# **HYBRID COMMANDS FORK**
Slash Commands will work with this fork. Please note that this is a live testing branch and that some functionality may not work as expected. If this happens please raise an issue and I will look into fixing the issue.

# 7tv bot for Discord

## Set up
1) Download Python https://www.python.org/downloads/
- Any version of Python should work, so getting the latest stable version is recommended
- Make sure to add Python to PATH
2) Download the files into a folder you destinated
3) At the folder, click `setup.bat` to download the required library for the script. 

## Make a bot
1) Go to https://discord.com/developers/applications
2) Click [New Application] and give your app a name.
3) At the bot tab, click [Add Bot], then copy the Token of the bot.
4) Enable the following Privileged Gateway Intents
	- Server Members Intent
	- Message Content Intent
5) Invite the bot to your server
    - OAuth2 -> URL Generator
    - Check the "bot" box
    - Check the following permissions
		- Manage Emojis and Stickers
		- Read Messages/View Channels
		- Send Messages
		- Send Messages in Threads
		- Embed Links
		- Attach Files
		- Read Message History

## Configuration
- Add the token of your bot in `config.json`
- Change the prefix as you want
- Change the size of the downloaded emote file
- Add dedicated discord channel for listening
    - Go to Discord settings. In Advanced tab, enable Developer mode
    - Right click your chosen discord channel, then copy ID
- Add 7tv user ID to listen. You can also do this using the commands
    - format:
    ```
    "listeningUsers": [
        "<7tv ID>", "<7tv ID>", ...
    ]
    ```
- Sample config:
```
{
    "TOKEN": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "prefix": "!",
    "output_folder": "out",
    "showemote_size": 4,
    "SevenTV_case_sensitive": false,
    "SevenTV_category": "TOP",
    "SevenTV_exact_match": false,
    "SevenTV_ignore_tags": true,
    "listen_channel": xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx,
    "listeningUsers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]
}
```

## Run the bot
- Simply click `runbot.bat`
* The script will add a `tmp` and an output folder if you don't have that already. 

## Sync the slash commands
- Type `!sync` in the discord with your bot in. Note: Only the bot owner can run this command
- Confirm the sync with `Yes` or `Y`
- This will run a global sync for your commands and allow you to start using slash commands. There is a maximum delay of 24 hours but you should only need to run this once

## Usage -  Also works for slash commands
- Posting a link to 7tv emote will show a gif version of the emote if it is WEBP format
    - only works with V2 urls, since V3 urls can show embeded emote in Discord
- !addemote \<link to 7tv emote\> \<\*optional\* emoji name\>
- !findemoteinchannel \<channel name\> \<text\>
- !searchemotes \<text\>
- !listeningchannels
- !deleteemote <emote\>

[In development]
- !addlistenchannel <channel name\>  \- Requires bot restart to start tracking
- !removelistenchannel <channel name\> \- Requires bot restart to stop tracking  \
\
These two commands require bot restart to start tracking. Will be updated in future to support live updates if possible 
