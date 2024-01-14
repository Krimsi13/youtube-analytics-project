import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    API_KEY: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, js):
        with open(js, "w", encoding="utf-8") as f:
            f.write(f"id канала: {self.channel_id}\n")
            f.write(f"Название канала: {self.title}\n")
            f.write(f"Описание канала: {self.description}\n")
            f.write(f"Cсылка на канал: {self.url}\n")
            f.write(f"Количество подписчиков: {self.subscriber_count}\n")
            f.write(f"Количество видео: {self.video_count}\n")
            f.write(f"Общее количество просмотров: {self.view_count}\n\n")
