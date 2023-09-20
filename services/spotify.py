from dotenv import load_dotenv
load_dotenv()
import base64
import os
import requests
from requests import post
import json
import secret
import random


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = secret.spotify_token

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_artist_ID(artist_name):
    url = f"{secret.spotify_artist_ID}{artist_name}&type=artist"
    headers = get_auth_header(get_token())

    response = requests.get(url=url, headers=headers)
    json_result = json.loads(response.content)
    id = json_result["artists"]["items"][0]["id"]

    return id


def get_suggested_artists(artist_id):
    try:
        url = f"{secret.spotify_related}{artist_id}/related-artists"
        headers = get_auth_header(get_token())

        response = requests.get(url=url, headers=headers)
        json_result = json.loads(response.content)

        artists = []

        for artist in json_result["artists"]:
            artist_name = artist["name"]
            image_url = artist["images"][0]["url"]
            link = artist["external_urls"]["spotify"]
            artists.append(artist_name + " - " + image_url + " - " + link)
            # limit to 6 artists
            if len(artists) >= 6:
                break

        print("Spotify success")
        return artists

    except Exception as e:
        print("Spotify Error - Getting related artists", e)


# finds random related artist -> finds random related from related
# to increase variability
# could play around with random count values/tempurature
def get_random_suggested_artist(artist_id, count=0):
    if count >= 2:
        return get_suggested_artists(artist_id)

    try:
        url = f"{secret.spotify_related}{artist_id}/related-artists"
        headers = get_auth_header(get_token())

        response = requests.get(url=url, headers=headers)
        json_result = json.loads(response.content)

        artists = []

        for artist in json_result["artists"]:
            artist_name = artist["name"]
            artists.append(artist_name)

        # select a random artist from list of related
        random_artist = random.choice(artists)
        id = get_artist_ID(random_artist)

        return get_random_suggested_artist(id, count + 1)

    except Exception as e:
        print("Spotify Error - Getting random related artists", e)





# https://api.spotify.com/v1/artists/{ID}/top-tracks
# https://api.spotify.com/v1/search?q=kanye_west&type=artist
# https://api.spotify.com/v1/artists/{id}/related-artists