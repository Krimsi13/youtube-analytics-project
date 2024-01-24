from datetime import timedelta
import isodate
from src.API import API


class PlayList(API):

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_response = self.youtube.playlists().list(id=self.playlist_id,
                                                               part='snippet,contentDetails',
                                                               maxResults=50,
                                                               ).execute()
        self.title = self.playlist_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()

    @property
    def total_duration(self):
        duration_list = []
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_list.append(duration)

        return timedelta(seconds=sum(td.total_seconds() for td in duration_list))

    def show_best_video(self):
        likes = 0
        url_on_vid = str()
        for video in self.video_response['items']:
            current_likes: int = video['statistics']['likeCount']
            if int(current_likes) > int(likes):
                url_on_vid = video['id']
                likes = current_likes
        return f"https://youtu.be/{url_on_vid}"
