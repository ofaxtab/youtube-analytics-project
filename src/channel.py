import json
import os

from googleapiclient.discovery import build
import isodate

class Channel:
    """Класс для ютуб-канала"""
    youtube = None

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.api_key = os.getenv('YT_API_KEY')
        Channel.youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        self.channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.__channel_id = self.channel['items'][0]['id']
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.total_subscribers = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.total_views = self.channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, filename: str):
        with open(filename, 'w', encoding='utf8') as file:
            file.write(json.dumps(self.channel, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
