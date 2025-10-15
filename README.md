# 7tv bot for Discord
This is a bot for 7TV/Twitch that monitors when editors change emotes in the active emote set for the monitored channels. It also has some functional commands for managing emotes in the server.\
This is a passion project/personal tool that I use. Forked from the original creator [WaterBoiledPizza](https://github.com/WaterBoiledPizza/7tv-bot-for-Discord) 

## Set up
**Tested in Python 3.13.7 as of 15/10/2025**
1) Download Python https://www.python.org/downloads/
- Any version of Python from 3.13+ should work, so getting the latest stable version is recommended
- Make sure to add Python to PATH
2) Download the files into a folder you choose
3) At the folder, click `setup.bat` to download the required libraries for the script.

## Make a bot
1) Go to https://discord.com/developers/applications
2) Click `[New Application]` and give your app a name
3) Accept the Terms of Service and click `[Create]`
4) At the Installation Tab
- Untick the `Installation Context` of `"User Install"`
- Under `Default Install Settings`
   - Add the scope `bot` then add the following permissions
        - Attach Files
        - Embed Links
        - Manage Expressions
        - Read Message History
        - Send Messages
        - Send Messages in Threads
        - View Channels
- Press `[Save Changes]`
6) At the bot tab, click `[Reset Token]`, then copy the bot token and put it into config.json.
    - Enable the following Privileged Gateway Intents
    	- Server Members Intent
    	- Message Content Intent
 - Press `[Save Changes]`
8) Invite the bot to your server
    - Select `OAuth2` and scroll down to the URL Generator
    - Check the "bot" box
    - Check the following permissions
        - General    
            - Manage Expressions
            - Create Expressions
            - View Channels
        - Text
    		- Send Messages
    		- Send Messages in Threads
    		- Embed Links
    		- Attach Files
    		- Read Message History
    - Make sure the integration type is "Guild Install"
9) Paste the link and accept/invite the bot to a server of your choosing

## Configuration
- Add the token of your bot in config.json
- Change the prefix as you want
- Change the size of the downloaded emote file (options are 1,2,3,4)
- Add dedicated discord channel for listening
    - Go to Discord settings. In Advanced tab, enable Developer mode
    - Right click your chosen discord channel, then copy ID
- Add 7tv user ID to listen. You can also do this later using the commands
    - Format:
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
    "commands_case_insensitive": true,
    "private_response": true,
    "subscribe_all_emote_sets": true,
    "SevenTV_category": "TOP_ALL_TIME",
    "SevenTV_exact_match": false,
    "listen_channel": xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx,
    "listeningUsers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]
}
```


## Run the bot
- Simply double click runbot.bat
- The script will add a tmp and an output folder if you don't have that already

## Sync the slash commands
- Type !sync in the discord with your bot in. Note: Only the bot owner can run this command
- Confirm the sync with Yes or Y
- This will run a global sync for your commands and allow you to start using slash commands. There is a maximum delay of 24 hours but you should only need to run this once unless you plan on making manual changes to the code

## Usage
You can use `/` (slash commands) or a prefix (e.g., `!`) for all of these commands except for `sync`. 

| Command                 | Description
|-------------------------|------------------------|
| `addemote <7TV Link> <*optional* emoji name>`    | Adds an emote to the server you are in using the provided 7TV Link     
| `removeemote <emote> or <emote name> `           | Remove a Discord emote from the server by specifying the name/emote                               
| `findemoteinchannel <channel name> <text>`       | Find emotes in a specific Twitch channel's 7TV emotes                          
| `searchemotes <text>`                            | Search for emotes using the name                                                                  
| `query7tvchannel <channel name>`                 | Looks up a 7TV channel based on the provided username                                 
| `addlistenchannel <channel name>`                | Add a Twitch channel to listen for 7TV emote updates                                         
| `removelistenchannel <channel name>`             | Remove a Twitch channel to stop listening for 7TV emote updates                          
| `listeningchannels`                              | Show Twitch channels that the bot is listening to for 7TV emote updates
| `servers`                                        | Lists the servers that the bot is in

### Sync the slash commands
`sync`: Syncs the Slash commands to Discord globally. Be careful not to spam this as it is rate-limited and slow to propagate changes


### Notes:
- Both **addlistenchannel** and **removelistenchannel** support live updates. The bot will start tracking new emotes without requiring a restart