# Twitch Chat Mood Analyser

This tool visualises the sentiment in twitch chat over time.
It does so by using [VADER](https://github.com/cjhutto/vaderSentiment) extended with custom dictionaries to capture the sentiment of twitch emotes and other words unique to twitch chat.

In it's current state it only recognizes a subset of the default Twitch emotes and a subset of the emotes introduced by the BetterTTV extension.
All other emotes (including channel specific ones) are considered 'neutral', unless specified in a dictionary file in vader_extensions.
The values for the custom 'words' are chosen by me, and if you disagree feel free to propose changes, inclusion of new 'words' or entire new dictionaries for channels.

## Usage

You must have a Twitch account and request an authentication token from https://twitchapps.com/tmi/ before use. 

Enter your Twitch nickname and token into the "twitch_api_cred.txt" file.

Run `python chat_sentiment_analysis -vod [video_id]` to analyse a VOD where video_id is the number in the URL of the twitch VOD.

Run `python chat_sentiment_analysis -live [channel_name]` to analyse a live chat in real time where channel_name is the name of the channel's chat.

Use `-m` to specify a specific minute interval for the bars, default is 5.

Use `-d` to enter debugging mode, where unrecognized (single word, neutral) chats are displayed. Useful for finding things to add to the vader dictionaries. 

## TODO

    * Live chat plotting window not responding, but still works fine. 
    * Get channel name through Twitch API using channel_id instead of scraping it, since scraping seems volatile (and slower)
    * Expand VADER dictionaries
