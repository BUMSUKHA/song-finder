import base64
import requests
import json

def parse_features(features):
    import pandas as pd
    df = pd.DataFrame(features, index=[0])
    df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
    return df_features
