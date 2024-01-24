import os
from googleapiclient.discovery import build


class API:
    API_KEY: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)
