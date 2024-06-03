import speech_recognition as sr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading
import time

SPOTIPY_CLIENT_ID = '1d438e52214b4acf8350a767b19d7a59'
SPOTIPY_CLIENT_SECRET = 'b4ac261cf83c470a830fb358ab84208c'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-modify-playback-state user-read-playback-state"))

# Speech recognition setup
recognizer = sr.Recognizer()

# Set up the listener for media key events


# Retrieves active device info from spotify
def get_active_device():
    devices = sp.devices()
    
    active_device = None
    for device in devices['devices']:
        if device['is_active']:
            active_device = device
            break
    
    return active_device

#Play track with voice
def play_spotify():
    active_device = get_active_device()
    if active_device:
        sp.start_playback(device_id=active_device['id'])
    else:
        print("No active device found.")

#Pause track with voice
def pause_spotify():
   active_device = get_active_device()
   if active_device:
        sp.pause_playback(device_id=active_device['id'])
   else:
        print("No active device found.")

#Skip track with voice
def skip_track():
    active_device = get_active_device()
    if active_device:
        sp.next_track(device_id=active_device['id'])
    else:
        print("No active device found.")

#Previous track with voice
def prev_track():
    active_device = get_active_device()
    if active_device:
        sp.previous_track(device_id=active_device['id'])
    else:
        print("No active device found.")

#Voice commands
def process_command(command):
    if "play" in command:
        play_spotify()
    elif "pause" in command:
        pause_spotify()
    elif "skip" in command:
        skip_track()
    elif "previous" in command:
        prev_track()

#Asigns the audio source and initializes the listening program.
def listen_and_recognize():
    while True:
        with sr.Microphone() as source:
            print("Say something:")
            recognizer.energy_threshold = 4000
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            if any(keyword in command for keyword in ["play", "pause", "skip", "previous"]):
                process_command(command)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")

if __name__ == "__main__":
    while True:
        listen_and_recognize()
        
