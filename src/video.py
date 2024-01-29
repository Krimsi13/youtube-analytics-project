from src.API import API


class Video(API):

    def __init__(self, id_vid):
        try:
            self.id_vid = id_vid
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=id_vid
                                                             ).execute()
            self.title = self.video_response['items'][0]['snippet']['title']
            self.url_on_vid = f"https://www.youtube.com/watch?v={self.id_vid}"
            self.view_count_vid = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_response = None
            self.title = None
            self.view_count_vid = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, id_vid, playlist_id):
        super().__init__(id_vid)
        self.playlist_id = playlist_id
