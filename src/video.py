import os
import pprint

from googleapiclient.discovery import build


class Video:
    youtube = None
    """Класс предназначен для получения информации о видео с ютуба"""

    def __init__(self, video_id: str):
        Video.youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        self.video_data = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                      id=video_id
                                                      ).execute()

        self.video_id = video_id
        self.title = self.video_data['items'][0]['snippet']['title']
        self.video_url = f'https://youtu.be/{self.video_id}'
        self.views = self.video_data['items'][0]['statistics']['viewCount']
        self.likes = self.video_data['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_data = super().youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()

        self.video_url = f'https://www.youtube.com/watch?v={self.video_id}&list={self.playlist_id}'
        self.playlist_url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
