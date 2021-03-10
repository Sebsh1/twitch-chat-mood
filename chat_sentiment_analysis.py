from vod_chat_downloader import load_chat_data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from webscraping import get_vod_channel
from live_chat_reciever import get_chat_messages
from numpy import mean
from math import floor
import matplotlib
import matplotlib.pyplot as plt
import sys, os, json, argparse, datetime, threading


def init_custom_vader():
    # Load pre-trained classifier
    analyzer = SentimentIntensityAnalyzer()

    # Expand with custom dictionaries
    count = 0
    for entry in os.scandir("vader_extensions"):
        if entry.path.endswith(".txt"):
            with open(entry) as f: 
                data = f.read() 
                js = json.loads(data) 
                analyzer.lexicon.update(js)
                count += 1

    print(f"Updated VADER with content of {count} dictionaries in vader_extensions")
    return analyzer

def analyse_vod_mood(video_id, timestep):
    channel_id, stream_date, chat_data = load_chat_data(video_id)

    analyser = init_custom_vader()
    leans_at_time = {}
    if args.debug:
        unrecognized_chats = []
    
    for chat in chat_data:

        # Disperse timings into intervals
        time = floor(chat[0] / 60 / int(timestep))

        # Classify
        leaning = analyser.polarity_scores(chat[1])['compound']

        # Discard chat commands
        if chat[1].startswith('!'): 
            continue

        # Store leaning, unless likely to be unrecognized emote
        if leaning == 0.0 and ' ' not in chat[1]:
            if args.debug:
                unrecognized_chats.append(chat[1])
            else: 
                continue
        else:    
            if time in leans_at_time:
                leans_at_time[time].append(leaning)
            else:
                leans_at_time[time] = [leaning]
           
    # Data for plotting
    avg_lean_at_time = {}
    for time in list(leans_at_time.keys()):
        avg_lean_at_time[time] = mean(leans_at_time[time])

    # Plotting
    fig, ax = plt.subplots()
    ax.bar(list(avg_lean_at_time.keys()), list(avg_lean_at_time.values()), color="grey")
    ax.set_title(f"{channel_id}'s chat's mood on {stream_date}")
    ax.set_ylabel('Mood (from -1 to 1)')
    ax.set_xlabel(f'Time (in intervals of {timestep} minute(s))')
    plt.show()
        
    # For inspection and future expansion of dictionaries
    if args.debug:
        print("Unrecognized emotes/words/sentences:\n", unrecognized_chats)

def analyse_live_mood(channel_name, timestep):
    analyser = init_custom_vader()
    leans_at_time = {}
    avg_lean_at_time = {}
    if args.debug:
        unrecognized_chats = []

    # Interval control
    start_time_interval = None
    prev_time = 0

    # Plotting
    matplotlib.use('tkAgg')
    plt.ioff()
    fig, ax = plt.subplots()
    ax.bar(list(avg_lean_at_time.keys()), list(avg_lean_at_time.values()), color="grey")
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    ax.set_title(f"{channel_name}'s chat's mood on {today}")
    ax.set_ylabel('Mood (from -1 to 1)')
    ax.set_xlabel(f'Time (in intervals of {timestep} minute(s))')
    ax.relim()
    ax.autoscale_view(True,True,True)
    plt.draw()
    plt.pause(0.001)

    for time, msg in get_chat_messages(channel_name):

        # Disperse timings into intervals
        if start_time_interval is None:
            time = floor(time / 60 / int(timestep))
            start_time_interval = time
            time = 0
        else: 
            time = floor(time / 60 / int(timestep)) - start_time_interval

            # New interval
            if time != prev_time:
                print("----------------NEW INTERVAL STARTED----------------")
                # Update data
                avg_lean_at_time[prev_time] = mean(leans_at_time[prev_time])

                # Update plot
                ax.cla()
                ax.bar(list(avg_lean_at_time.keys()), list(avg_lean_at_time.values()), color="grey")
                plt.draw()
                plt.pause(0.001)

                prev_time = time

        # Discard chat commands
        if msg.startswith('!'):
            continue

        leaning = analyser.polarity_scores(msg)['compound']
        print(leaning, "  -  ", msg)

        # Store leaning unless likely to be unrecognized emote
        if leaning == 0.0 and ' ' not in msg:
            if args.debug:
                unrecognized_chats.append(msg)
            else: 
                continue
        else:    
            if time in leans_at_time:
                leans_at_time[time].append(leaning)
            else:
                leans_at_time[time] = [leaning]
           
    # For inspection and future expansion of dictionaries
    if args.debug:
        print("Unrecognized emotes/words/sentences:\n", unrecognized_chats)

    # Stop plot from disapearing
    plt.show()

if __name__ == "__main__":

    # Argument support
    parser = argparse.ArgumentParser()
    parser.add_argument('-vod', action='store')
    parser.add_argument('-live', action='store')
    parser.add_argument('-m', "--minutes", action='store')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    
    # Setting time intervals for bars
    if args.minutes is not None:
        timestep = args.minutes
    else: 
        timestep = 5

    # Choosing main mode
    if args.vod is not None and args.live is not None:
        print("You can't analyse a vod and a live channel at the same time")
    elif args.vod is not None:
        analyse_vod_mood(args.vod, timestep)
    elif args.live is not None:
        analyse_live_mood(args.live, timestep)
    else:
        print("Usage:\n chat_sentiment_analysis -vod [video_id] \nor\n chat_sentiment_analysis -live [channel_name]")
        sys.exit(1)


    