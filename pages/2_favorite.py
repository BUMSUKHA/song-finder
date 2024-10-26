import streamlit as st
import sqlite3
import spotipy
from youtubesearchpython import VideosSearch
from spotipy.oauth2 import SpotifyClientCredentials

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
st.set_page_config(page_title="RMS",page_icon="🎵",initial_sidebar_state="expanded")

# 데이터베이스 연결
conn = sqlite3.connect('./db.db')
cursor = conn.cursor()

client_id = "7ca31bb821a045fdbddca19677630a0f" 
client_secret = "b801c09b526e4087a35d59e87b471642"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
if st.session_state.get('logged_in', False):
    st.sidebar.title(f"Hello, {st.session_state.user['username']}")
    
    userid = st.session_state.user['userid']
    cursor.execute("SELECT songid FROM favorite WHERE userid = ?", (userid,))
    favorite_songs = cursor.fetchall()
    
    st.title("Your Favorite Songs")
    
    songid_list = [song[0] for song in favorite_songs]
        
    if songid_list:
        tracks = sp.tracks(songid_list)
        for track in tracks['tracks']:
            col1, col2 = st.columns(2)
            songid = track['id']
            with col1:
                st.image(track['album']['images'][0]['url'], caption=f"{track['artists'][0]['name']} - {track['name']}", width=300)
            with col2:
                st.write('')
                url = "https://open.spotify.com/track/"+str(track['id'])
                st.markdown(f'<a href="{url}"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/232px-Spotify_icon.svg.png" width=20> Click to move</a>',unsafe_allow_html=True)
                st.write(f"🎯 Track ID : {songid}")
                st.write(f"🎧 Track : {track['name']}")
                st.write(f"🗣️ Artist : {track['artists'][0]['name']}")
                st.write(f"📅 Release date : {track['album']['release_date']}")
                st.write(f"✨ Popularity : {track['popularity']}")
                if st.button(f"⭐ Remove from favorites", key=songid):
                    cursor.execute("DELETE FROM favorite WHERE userid = ? AND songid = ?", (userid, songid))
                    conn.commit()  # 데이터베이스에 변경사항 저장
                    st.success(f"Removed {track['name']} from your favorites!")
    else:
        st.info("You haven't added any songs to your favorites yet")
    
    conn.close()
else:
    st.info("Sign in is required.")