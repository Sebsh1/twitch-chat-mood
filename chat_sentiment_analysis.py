from vod_chat_downloader import load_chat_data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from webscraping import get_vod_channel
from live_chat_reciever import get_chat_messages
from numpy import mean
from math import floor
import matplotlib.pyplot as plt
import sys, os, json
import argparse

def init_custom_vader():
    analyzer = SentimentIntensityAnalyzer()

    for entry in os.scandir("vader_extensions"):
        if entry.path.endswith(".txt"):
            with open(entry) as f: 
                data = f.read() 
                js = json.loads(data) 
                analyzer.lexicon.update(js)
    
    print(f"Updated VADER with content of vader_extensions")

    return analyzer

def analyse_vod_mood(video_id):
    channel_id, stream_date, chat_data = load_chat_data(video_id)    

    analyser = init_custom_vader()

    leans_at_time = {}
    unrecognized_chats = []
    timestep_interval = 1 

    for chat in chat_data:
        time = floor(chat[0] / 60 / timestep_interval)
        leaning = analyser.polarity_scores(chat[1])['compound']

        if chat[1].startswith('!'): # Likely to be chat commands
            continue

        if leaning == 0.0 and ' ' not in chat[1]:  # One word leanings of 0 are likely to be unrecognized emotes or other unrecognized words
            unrecognized_chats.append(chat[1])
        else:    
            if time in leans_at_time:
                leans_at_time[time].append(leaning)
            else:
                leans_at_time[time] = [leaning]
           
    avg_lean_at_time = {}
    for time in list(leans_at_time.keys()):
        avg_lean_at_time[time] = mean(leans_at_time[time])

    # Plotting
    fig, ax = plt.subplots()
    ax.bar(list(avg_lean_at_time.keys()), list(avg_lean_at_time.values()), bottom=0)
    ax.set_title(f"{channel_id}'s chat mood on {stream_date}")
    ax.set_ylabel('Mood')
    ax.set_xlabel(f'Time (in intervals of {timestep_interval} minute(s))')
    plt.show()
        
    # print("Unrecognized words/sentences:\n", unrecognized_chats)

def analyse_live_mood(channel_name):
    analyser = init_custom_vader()
    unrecognized_chats = []
    leans_at_time = {}
    timestep_interval = 1

    for time, msg in get_chat_messages(channel_name):
        time = floor(time / 60 / timestep_interval)
        leaning = analyser.polarity_scores(msg)['compound']

        if msg.startswith('!'): # Likely to be chat commands
            continue

        if leaning == 0.0 and ' ' not in msg:  # One word leanings of 0 are likely to be unrecognized emotes or other unrecognized words
            unrecognized_chats.append(msg)
        else:    
            if time in leans_at_time:
                leans_at_time[time].append(leaning)
            else:
                leans_at_time[time] = [leaning]
           
    avg_lean_at_time = {}
    for time in list(leans_at_time.keys()):
        avg_lean_at_time[time] = mean(leans_at_time[time])



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-vod', action='store')
    parser.add_argument('-live', action='store')
    args = parser.parse_args()
    
    if args.vod is not None and args.live is not None:
        print("You can't analyse a vod and a live channel at the same time")
    elif args.vod is not None:
        analyse_vod_mood(args.vod)
    elif args.live is not None:
        analyse_live_mood(args.live)
    else:
        print("Usage:\n chat_sentiment_analysis -vod [video_id] \nor\n chat_sentiment_analysis -live [channel_name]")
        sys.exit(1)


    