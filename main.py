import spotipy
import time
import logging
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from yandex_music import Client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()
load_dotenv()
#TOKEN  = os.getenv('TOKEN')
scope = "user-library-read user-library-modify"

def on_code(code):
    print(f'Откройте {code.verification_url} и введите код: {code.user_code}')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

track_ids = []
chunk_size = 1
client = Client()
token = client.device_auth(on_code=on_code)
client.init()
client.request.set_timeout(60)
liked_tracks = client.users_likes_tracks()


for track in liked_tracks.tracks:
    artist = track.fetch_track().artists[0].name,
    title_name = track.fetch_track().title
    search_result = sp.search(q=f"track:{title_name} artist:{artist}",limit=1, type="track")
    if search_result['tracks']['items']:
        track_id = search_result['tracks']['items'][0]['id']
        spot_artist = search_result['tracks']['items'][0]['artists'][0]['name']
        spot_name_track = search_result['tracks']['items'][0]['name']
        track_ids.append(track_id)
        logger.info(f"Ya Artist: {artist} Ya Title Name: {title_name} ||| Spot ID: {track_id} Spot Artist: {spot_artist} Spotify Title Name: {spot_name_track}")
    else:
        logger.warning(f"This track was not found in Spotify: {artist} - {title_name}")
        continue
    time.sleep(0.5)

  
chunks = [track_ids[i:i + chunk_size] for i in range(0, len(track_ids), chunk_size)]

for chunk in chunks[::-1]:
    save_track = sp.current_user_saved_tracks_add(tracks=chunk)
    time.sleep(1)

logger.info("Done")