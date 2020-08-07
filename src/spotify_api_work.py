
client_id = "f54bef3c9a844c348e3d8d0d8cafefe1"
client_secret = "eb15a4eefe804edba006bcec248a87e0"
redirect_uri = 'https://intel.com/' #lol idk what this is they just made me chose one


import requests
import json
import base64
import numpy as np

method = 'post'

playlist_id = '0sxxPBp8iOUBSuoj1pPkUl'
#encode client_id : client_secret to base 64
to_encode = '{}:{}'.format(client_id, client_secret)
creds_encoded = base64.b64encode(to_encode.encode())


auth_data = {'grant_type' : 'client_credentials'}
auth_header = {'Authorization' : 'Basic {}'.format(creds_encoded.decode())}


#make request to spotify to get access token
auth_url = 'https://accounts.spotify.com/api/token'

r = requests.post(auth_url, data = auth_data, headers = auth_header)

response = r.json()

#access token expires in an hour once you get it
access_token = response['access_token']


def extract_many_songs_features(playlist_dict):
    '''
    sends song ids to spotify api in GET request to get the features of the song back in the response
    takes in song_id which is a string
    '''
    
    count = 0
    audio_features_url = 'https://api.spotify.com/v1/audio-features?ids='
    feature_list = []
    feature_dict = {}
    total = len(playlist_dict)
    
    total_count = 0
    for song,id_num in playlist_dict.items():
        total_count +=1
        if count < 50:
            audio_features_url+= id_num
            if count!=49:
                audio_features_url+= ','
            count +=1
        if count < 50 and total_count == total:
            features_header = {'Authorization' : 'Bearer {}'.format(access_token)}
            r_features = requests.get(audio_features_url, headers = features_header)
            feat_response = r_features.json()

            feature_list += feat_response['audio_features']
            count = 0
            audio_features_url = 'https://api.spotify.com/v1/audio-features?ids=' + id_num + ','

        elif count == 50:
            features_header = {'Authorization' : 'Bearer {}'.format(access_token)}
            r_features = requests.get(audio_features_url, headers = features_header)
            feat_response = r_features.json()

            feature_list += feat_response['audio_features']
            count = 0
            audio_features_url = 'https://api.spotify.com/v1/audio-features?ids=' + id_num + ','
    
    index = 0
    for song in playlist_dict.keys():
        if index < len(feature_list):
            feature_dict[song] = feature_list[index]
        index+=1
    return feature_dict


def get_playlist_tracks(playlist_id):
    '''
    goes into spotify database to grab the tracks from our playlist which we will use as our dataset
    '''
     
    header = {'Authorization': 'Bearer {}'.format(access_token)}
    track_list = []
    track_dict = {}

    query_params = '?fields=total&limit=1'
    get_url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
    r = requests.get(get_url, headers = header)
    tracks = r.json()
    calls = tracks['total']//100 + 1
    for i in range(calls):
        query_params = '?fields=items.track.name,items.track.id&offset={}'.format(str(i*100))
        get_url = 'https://api.spotify.com/v1/playlists/{}/tracks{}'.format(playlist_id, query_params)
        r = requests.get(get_url, headers = header)
        tracks = r.json()
        track_list.append(tracks['items'])
    for j in track_list:
        for item in j:
            name = item['track']['name']
            id_num = item['track']['id']
            track_dict[name] = id_num

    return track_dict
    # return track_dict



playlist_tracks = get_playlist_tracks(playlist_id)
features = extract_many_songs_features(playlist_tracks)


imp_features = {}
for song in features:
    imp_features[song] = {'danceability': features[song]['danceability'], 'energy': features[song]['energy'], 'valence' : features[song]['valence']}

