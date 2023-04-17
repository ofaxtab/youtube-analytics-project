import json
import os

from googleapiclient.discovery import build
import isodate

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
