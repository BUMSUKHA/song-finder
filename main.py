import streamlit as st 
import spotipy
from youtubesearchpython import VideosSearch
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import spotifyAPI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.set_page_config(page_title="RMS",page_icon="🎵",initial_sidebar_state="expanded")

# 데이터 베이스 연결
conn = sqlite3.connect('./db.db')
cursor = conn.cursor()

client_id = "7ca31bb821a045fdbddca19677630a0f" 
client_secret = "b801c09b526e4087a35d59e87b471642"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_recommendations(track_name):
    results = sp.search(q=track_name, type='track')
    track_uri = results['tracks']['items'][0]['uri']

    recommendations = sp.recommendations(seed_tracks=[track_uri])['tracks']
    return recommendations

def get_track(track_name):
    results = sp.search(q=track_name, type='track')
    track = results['tracks']['items'][0]
    return track

st.title("🎧 Song finder")
song_detail, Recommendations = st.tabs(["🔍 Song detail", "🔮 Recommendations"])

if st.session_state.get('logged_in', False):
    st.sidebar.title(f"Hello, {st.session_state.user['username']}")
    
track_name = st.sidebar.text_input("Enter a song name:", value="APT.")

col1, col2, col3 = st.columns(3)

if track_name:
    try:   
        track = get_track(track_name)
        
        st.sidebar.image(track['album']['images'][1]['url'], caption=f"{track['artists'][0]['name']} - {track['album']['name']}")
        
        if st.session_state.get('logged_in', False):
            if st.sidebar.button("⭐Add a favorite"):
                songid = track['id']
                userid = st.session_state.user['userid']

                # 즐겨찾기 중복 체크
                cursor.execute("SELECT * FROM favorite WHERE userid = ? AND songid = ?", (userid, songid))
                favorite_exists = cursor.fetchone()

                if favorite_exists:
                    st.sidebar.error("This song is already in your favorites!")
                else:
                    # 즐겨찾기 추가 쿼리
                    cursor.execute("INSERT INTO favorite (userid, songid) VALUES (?, ?)", (userid, songid))
                    conn.commit()  # 데이터베이스에 변경 사항 저장
                    st.sidebar.success("Song added to your favorites!")
                    
                conn.close()
        
        # API req 아껴두기
        # recommendations = get_recommendations(track_name)
        
        with song_detail:
            st.subheader("Your song :")
            st.write(f"🗣️ {track['artists'][0]['name']} - {track['name']}")
            url = "https://open.spotify.com/track/"+str(track['id'])
            st.markdown('<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/232px-Spotify_icon.svg.png" width=20> '+url,unsafe_allow_html=True)
            yt = st.button('🎞️ Find on Youtube')
            
            if yt:
                try:
                    videos_search = VideosSearch(f"{track['name']} - {track['artists'][0]['name']}", limit=1)
                    result = videos_search.result()
                    video_url = result['result'][0]['link']
                    st.video(video_url)
                except:
                    st.write('Did not find the track on Youtube')
                    
            ft = st.checkbox('Feature plot',value=True)
            
            if ft:     
                track_features = sp.audio_features([track['id']])
                features = spotifyAPI.parse_features(track_features)
                
                st.write(features)
                labels= list(features)[:]
                stats= features.mean().tolist()

                angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

                stats=np.concatenate((stats,[stats[0]]))
                angles=np.concatenate((angles,[angles[0]]))

                fig=plt.figure(figsize = (18,18))
                ax = fig.add_subplot(221, polar=True)
                ax.plot(angles, stats, 'o-', linewidth=2, label = "Features", color= 'gray')
                ax.fill(angles, stats, alpha=0.25, facecolor='gray')
                ax.set_thetagrids(angles[0:7] * 180/np.pi, labels , fontsize = 13)
                ax.set_rlabel_position(250)
                plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
                plt.ylim(0,1)
                plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))

                st.pyplot(fig)

                if st.checkbox('What do those features mean?'):
                    st.write("**acousticness**: 트랙이 어쿠스틱일 가능성을 0.0에서 1.0까지의 값으로 나타낸 신뢰도 지표입니다.")
                    st.write("**danceability**: 템포, 리듬의 안정성, 비트 강도, 그리고 전체적인 규칙성을 포함한 음악적 요소의 조합을 바탕으로 트랙이 춤추기에 얼마나 적합한지를 설명합니다. 값이 0.0에 가까울수록 덜 춤추기 좋고, 1.0에 가까울수록 가장 춤추기 좋습니다.")
                    st.write("**energy**: 에너지는 0.0에서 1.0까지의 값으로, 강도와 활동성에 대한 인식적 측정을 나타냅니다. 일반적으로 에너지가 높은 트랙은 빠르고, 시끄럽고, 강렬하게 느껴집니다. 예를 들어 데스 메탈은 에너지가 높고, 바흐 프렐류드는 낮은 점수를 받습니다. 이 속성에 기여하는 지각적 요소에는 동적 범위, 인식된 음량, 음색, 발현율, 그리고 일반적인 엔트로피가 포함됩니다.")
                    st.write("**instrumentalness**: 트랙에 보컬이 포함되지 않았는지를 예측합니다. 여기서 'Ooh'와 'Aah' 소리는 보컬로 간주되지 않습니다. 랩이나 말하는 트랙은 명백히 보컬로 취급됩니다. instrumentalness 값이 1.0에 가까울수록 보컬이 없을 가능성이 큽니다. 값이 0.5를 넘으면 보통 기악곡을 나타내지만, 값이 1.0에 가까울수록 신뢰도가 높아집니다.")
                    st.write("**liveness**: 녹음에 청중이 있는지 여부를 탐지합니다. liveness 값이 높을수록 트랙이 라이브로 연주되었을 가능성이 높습니다. 0.8 이상의 값은 트랙이 라이브로 연주되었을 가능성이 크다는 강한 신호입니다.")
                    st.write("**speechiness**: 트랙에서 말하는 소리가 감지되는 정도를 나타냅니다. 녹음이 말하기에 가까울수록 이 속성 값은 1.0에 가까워집니다. 값이 0.66 이상이면 전적으로 말로 이루어진 트랙일 가능성이 높습니다. 값이 0.33과 0.66 사이면 음악과 말이 섞여 있을 가능성이 있으며, 랩 음악 같은 경우도 포함됩니다. 0.33 이하의 값은 대부분 음악 또는 말과 상관없는 트랙을 나타냅니다.")
                    st.write("**valence**: 트랙에서 전달되는 음악적 긍정성을 0.0에서 1.0까지 측정한 값입니다. 값이 높을수록 긍정적인 감정(예: 기쁨, 환희)을, 값이 낮을수록 부정적인 감정(예: 슬픔, 분노)을 전달합니다.")

            
        with Recommendations:
            for i, track in enumerate(recommendations):
                st.image(track['album']['images'][0]['url'], caption=f"{track['artists'][0]['name']} - {track['name']}", width=300)
    except:
        st.error("429 Client Error: Too Many Requests")
else:
    st.info("Plaese write the name of the song you'd like to search for")