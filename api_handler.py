"""
spotify-automation-v2
spotify_automation_v2/api_handler.py
Handles the tasks related to spotify api
"""

import os
import json
import base64
from dotenv import load_dotenv
from requests import post, get
from python_datalogger import DataLogger


class SpotifyHandler:
    """
    Handles the tasks related to spotify api and process user requests accordingly.

    Attributes:
    ----------

        Private:

            __client_id : spotify client id data
            __client_secret : spotify client secret data


    Methods:
    -------

        Private:
            __get_token : requests temporary access tokens from spotify api
            __get_auth_header : returns an authorization header


        Public:
            search_for_artist : search for artists id using given artist name
            get_songs_by_artist : gets a list of top songs by the given artist



    """
    # load environmental variables from (only) .env file
    load_dotenv()

    __client_id = os.getenv("CLIENT_ID")
    __client_secret = os.getenv("CLIENT_SECRET")

    token_url = "https://accounts.spotify.com/api/token"
    search_url = "https://api.spotify.com/v1/search"
    artist_url = "https://api.spotify.com/v1/artists/"

    def __init__(self):
        """Creates a new instance of the SpotifyHandler class"""
        self.__token = self.__get_token()
        self.__auth_header = SpotifyHandler.__get_auth_header(token=self.__token)
        self.__artist_id = None

    @classmethod
    @DataLogger.logger
    def __get_token(cls) -> str:
        """
        Gets a temporary token from spotify api
        :return: an access token
        """
        auth_string = SpotifyHandler.__client_id + ":" + SpotifyHandler.__client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        results = post(SpotifyHandler.token_url, headers=headers, data=data)
        json_result = json.loads(results.content)
        return json_result["access_token"]

    @staticmethod
    @DataLogger.logger
    def __get_auth_header(token: str) -> dict[str:str]:
        """
        returns an authorization header
        :param token: token to access spotify api
        :return: authorization header
        """
        return {"Authorization": "Bearer " + token}

    @DataLogger.logger
    def search_for_artist(self, artist_name: str) -> None:
        """
        Search for an artist id using a given artist name
        :param artist_name: str: name of the artist
        :return: str: id of the artist
        """
        query = f"?q={artist_name}&type=artist&limit=1"
        query_url = SpotifyHandler.search_url + query
        results = get(query_url, headers=self.__auth_header)
        json_result = json.loads(results.content)
        if len(json_result["artists"]["items"]) == 0:
            print("No such artist !")
            return None
        else:
            self.__artist_id = json_result["artists"]["items"][0]["id"]

    @DataLogger.logger
    def get_songs_by_artist(self) -> any:
        """
        Gets a list of songs by the specified artist
        :return: dictionary of songs information
        """
        if self.__artist_id is not None:
            url = f"{SpotifyHandler.artist_url}{self.__artist_id}/top-tracks?country=US"
            results = get(url, headers=self.__auth_header)
            json_result = json.loads(results.content)

            tracks = json_result["tracks"]
            for idx, song in enumerate(tracks):
                print(f"{(idx + 1)}. {song['name']}")

            # return json_result

        else:
            return None
