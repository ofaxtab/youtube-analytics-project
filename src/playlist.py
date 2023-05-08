import json
import os
import isodate

import pprint
from googleapiclient.discovery import build

from src.video import Video

class PlayList:
    youtube = None

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        PlayList.youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        self.playlist_data = PlayList.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                   part='contentDetails,snippet',
                                                                   maxResults=50,
                                                                   ).execute()
        self.video_ids: list[str] = [item['contentDetails']['videoId'] for item in self.playlist_data['items']]


        self.channel_id = self.playlist_data['items'][0]['snippet']['channelId']
        self.outer_playlist_data = self.youtube.playlists().list(channelId=self.channel_id,
                                     part='contentDetails,snippet,player',
                                     maxResults=50,
                                     ).execute()
        for item in self.outer_playlist_data['items']:
            if item['id'] == self.playlist_id:
                self.title = item['snippet']['title']


        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

        #self.title = pl.outer_playlist_data['items']

    @property
    def total_duration(self):
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)
                                               ).execute()
        all_duration = None
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            if not all_duration:
                all_duration = duration
            else:
                all_duration += duration
        return all_duration

    def show_best_video(self):
        all_stats = [Video(video_id) for video_id in self.video_ids]
        return max(all_stats, key=lambda x: x.likes).video_url

if __name__ == '__main__':
    pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
    # pprint.pprint(pl.outer_playlist_data)
    #pprint.pprint(pl.playlist_data)
    print(pl.title)
    print(pl.url)
    print(pl.video_ids)
    # pprint.pprint(str(pl.total_duration))
    # pprint.pprint(pl.playlist_data)
    print(pl.show_best_video())

    # pprint.pprint(pl.playlist_data['items'][0]['snippet']['channelId'])
