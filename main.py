from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

###### Find/display artist's top 10

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists (yet)....")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token()
artist_name = "Hillsong"
artist = search_for_artist(token, artist_name)
artist_id = artist["id"]
songs = get_songs_by_artist(token, artist_id)
for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")

######
###### Find the key of a specific track
def search_for_track(token, track_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("No track with this name exists (yet)....")
        return None
    return json_result[0]

def get_key_of_track(token, track_id):
    major_key_map = {-1:"No match", 0: "C", 1:"C#/D♭", 2:"D", 3:"D#/E♭", 4:"E", 5:"F", 6:"F#/G♭", 7:"G", 8:"G#/A♭", 9:"A", 10:"A#/B♭", 11:"B", 12:"C"}
    minor_key_map = {-1:"No match", 0: "Cm", 1:"C#m/D♭m", 2:"Dm", 3:"D#m/E♭m", 4:"Em", 5:"Fm", 6:"F#m/G♭m", 7:"Gm", 8:"G#m/A♭m", 9:"Am", 10:"A#m/B♭m", 11:"Bm", 12:"Cm"}
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    key_num = json_result["key"]
    mode = json_result["mode"]
    key =  major_key_map[key_num] if mode == 1 else minor_key_map[key_num]
    return key

token = get_token()
song_name = "Monkey Type Beat"
track = search_for_track(token, song_name)
track_id = track["id"]
print("\"" + song_name + "\" is in the key of: " + get_key_of_track(token, track_id))
######





