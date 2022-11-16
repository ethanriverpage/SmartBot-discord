import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import authmanager as auth
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

auth.startauthmanager()

""" def savedtracks():
    scope = "user-library-read"
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    savedtracks_results = sp.current_user_saved_tracks()

    def showtracks(savedtracks_results):
        for item in savedtracks_results['items']:
            track = item['track']
            return ("%32.32s %s" % (track['artists'][0]['name'], track['name']))

    
    showtracks(savedtracks_results)

    def show_next_tracks():
        savedtracks_results_next = sp.next(savedtracks_results)
        showtracks(savedtracks_results_next)

    show_next_tracks() """

def savedtracks():
    savedtracks_res = auth.savedtracks()
    def showtracks(savedtracks_res):
        for item in savedtracks_res['items']:
            track = item['track']
            return ("%32.32s %s" % (track['artists'][0]['name'], track['name']))
    
    showtracks(savedtracks_res)


