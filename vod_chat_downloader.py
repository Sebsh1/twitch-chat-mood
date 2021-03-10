import json
import requests
import sys

client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'

chat_data = []

def collect_chat_data(data):
    for comment in data['comments']:
        if comment['source'] != 'chat':
            continue
        if comment['commenter'] == 'Nightbot' or comment['commenter'] == "Moobot":
            continue
        chat_data.append([comment['content_offset_seconds'], comment['message']['body']])

def load_chat_data(video_id):
    session = requests.Session()
    session.headers = { 'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json' }

    response = session.get('https://api.twitch.tv/v5/videos/' + video_id + '/comments', timeout=10)
    response.raise_for_status()
    data = response.json()

    stream_date = data['comments'][0]['created_at'].split('T')[0]
    channel_id = data['comments'][0]['channel_id']

    collect_chat_data(data)

    cursor = None
    if '_next' in data:
        cursor = data['_next']

    print("Loading VOD chat data... (This might take a while for long VODs and/or if chat was moving fast)")

    while cursor:
        response = session.get('https://api.twitch.tv/v5/videos/' + video_id + '/comments?cursor=' + cursor, timeout=10)
        response.raise_for_status()
        data = response.json()

        collect_chat_data(data)

        if '_next' in data:
            cursor = data['_next']
        else:
            cursor = None

    print(f"Finished loading {len(chat_data)} chat messages")

    return channel_id, stream_date, chat_data
