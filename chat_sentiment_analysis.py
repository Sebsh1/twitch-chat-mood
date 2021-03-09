from vod_chat_downloader import load_chat_data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from numpy import mean
from math import floor
import matplotlib.pyplot as plt
import sys, os, json

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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} [video_id]')
        print("video_id is the number in the URL of a VOD")
        sys.exit(1)

    video_id = sys.argv[1]
    chat_data = load_chat_data(video_id)

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
    
    print("Unrecognized words/sentences:\n", unrecognized_chats)

    fig, ax = plt.subplots()
    ax.bar(list(avg_lean_at_time.keys()), list(avg_lean_at_time.values()), bottom=0)
    ax.set_title('Chat Sentiment on DATE')
    ax.set_ylabel('sentiment')
    ax.set_xlabel('time')
    plt.show()