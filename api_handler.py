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



        Public:




    """
    # load environmental variables from (only) .env file
    load_dotenv()

    __client_id = os.getenv("CLIENT_ID")
    __client_secret = os.getenv("CLIENT_SECRET")

    token_url = "https://accounts.spotify.com/api/token"
    search_url = "https://api.spotify.com/v1/search"
    artist_url = "https://api.spotify.com/v1/artists/"

    def __init__(self):
        self.__get_token()

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
