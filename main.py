"""
spotify-automation-v2
spotify_automation_v2/main.py
Allows you to access and retrieve information using spotify api
"""
from api_handler import SpotifyHandler

handle = SpotifyHandler()
handle.search_for_artist(artist_name="Good Kid")
handle.get_top_songs_by_artist()
