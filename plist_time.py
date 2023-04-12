from googleapiclient.discovery import build
import isodate
import os
import argparse

API_KEY = os.environ.get('YOUTUBE_API_KEY')
PLAYLIST = '<playlist_id>'


class plist:
    def __init__(self, pid) -> None:
        """
        Args:
        pid : Playlist ID
        """

        self.pid = pid
        self.youtube = build('youtube', 'v3', developerKey=API_KEY)

    def extractId(self):

        # Collects the ids of videos
        vidId = []

        # get 50 results of the playlist
        request = self.youtube.playlistItems().list(
            part='contentDetails',
            maxResults=50,
            playlistId=self.pid
        )

        # execute and get the video ids
        response = request.execute()

        for item in response['items']:
            id = item['contentDetails']
            id = id['videoId']
            vidId.append(id)

        # Get more ids if more videos are left
        while True:
            if 'nextPageToken' in response:
                request = self.youtube.playlistItems().list(
                    part='contentDetails',
                    maxResults=50,
                    playlistId=self.pid,
                    pageToken=response['nextPageToken']
                )

                response = request.execute()
                for item in response['items']:
                    id = item['contentDetails']
                    id = id['videoId']
                    vidId.append(id)
            else:
                break

        return vidId

    def calTime(self):
        totalTime = 0
        vidLis = self.extractId()

        for vid in vidLis:
            request = self.youtube.videos().list(
                part='contentDetails',
                id=vid
            )

            response = request.execute()

            time = response['items'][0]['contentDetails']['duration']

            totalTime += self.timeConvert(time)

        hours = int(totalTime//3600)
        min = int((totalTime % 3600)//60)

        return (hours, min)

    def timeConvert(self, time):
        time = isodate.parse_duration(time)
        sec = time.total_seconds()
        return sec


def main():

    parser = argparse.ArgumentParser(description="Calculates the total duration of a youtube playlist")
    parser.add_argument("-id", help="Id of the Playlist", type=str)
    args = parser.parse_args()
    pl = plist(args.id)
    h, m = pl.calTime()
    print('This playlist is : {} hours, {} minutes long!'.format(h, m))


if __name__ == '__main__':
    main()
