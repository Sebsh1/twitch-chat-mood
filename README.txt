# Twitch Chat Mood Analyser
This tool visualises the sentiment in twitch chat over time.
It does so by using [VADER](https://github.com/cjhutto/vaderSentiment) extended with custom dictionaries to capture the sentiment of twitch emotes and other words unique to twitch chat.
In it's current state it only recognizes a subset of the default Twitch emotes and a subset of the emotes introduced by the BetterTTV extension.
All other emotes (including channel specific ones) are considered 'neutral', unless specified in a dictionary file in vader_extensions.
The values for the custom 'words' are chosen by me, and if you disagree feel free to propose changes or inclusion of new 'words' or entire new dictionaries for other channels

## Use
Run python chat_sentiment_analysis [video_id]
where video_id is the number in the URL of the twitch VOD

It might complain about missing the vader_lexicon. If it does just download it using way suggested in the terminal or manually download it from [here](http://www.nltk.org/nltk_data/) and place it in one of the locations it looked for it.

## Things still to do
    - Hook it up to live twitch chat
    - Make it grab date, channel and possibly 'current game' from twitch api for graphing