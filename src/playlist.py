import json
import os
import isodate

import pprint
from googleapiclient.discovery import build

from src.video import Video


class PlayList:
    youtube = None

    def __init__(self, playlist_id: str):
        self._playlist_id = playlist_id
        PlayList.youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        self._playlist_data = PlayList.youtube.playlistItems().list(playlistId=self._playlist_id,
                                                                    part='contentDetails,snippet',
                                                                    maxResults=50,
                                                                    ).execute()
        self._video_ids: list[str] = [item['contentDetails']['videoId'] for item in self._playlist_data['items']]

        self._channel_id = self._playlist_data['items'][0]['snippet']['channelId']
        self._outer_playlist_data = self.youtube.playlists().list(channelId=self._channel_id,
                                                                  part='contentDetails,snippet,player',
                                                                  maxResults=50,
                                                                  ).execute()
        for item in self._outer_playlist_data['items']:
            if item['id'] == self._playlist_id:
                self.title = item['snippet']['title']

        self.url = f'https://www.youtube.com/playlist?list={self._playlist_id}'

    @property
    def total_duration(self):
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                        id=','.join(self._video_ids)
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
        all_stats = [Video(video_id) for video_id in self._video_ids]
        return max(all_stats, key=lambda x: x.likes).video_url
