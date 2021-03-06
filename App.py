import os
import requests
import youtube_dl

class yt_downloader:
    def __init__(self):
        self.debug = False
        self.yt_url = ''
        self.outtmpl = ''
        self.thumbnail = ''
        self.folderPath = ''

        self.set_dir(f"{os.path.expanduser('~')}/Desktop/유튜브 다운로드")
        self.set_outtmpl()

    def print(self,*txt):
        if self.debug : print(*txt)

    def get_dir(self):
        self.print('폴더 열기')
        os.startfile(self.folderPath)
        return self.folderPath

    def set_dir(self, folderPath):
        try :
            if not os.path.isdir(folderPath):
                os.makedirs(folderPath)
                self.print('폴터 생성')
            self.folderPath = folderPath
            self.set_outtmpl()
        except :
            print(f'잘못된 경로 :\n{folderPath}')

    def set_outtmpl(self):
        url = self.yt_url
        # 저장할 이름 설정
        info_list = ['uploader', 'title']
        if 'list' in url: info_list.insert(0, 'playlist_title')
        info = f"\%({r')s_%('.join(info_list)})s"
        self.outtmpl = self.folderPath + info + '.%(ext)s'
        self.outtmpl = self.outtmpl.replace('NA_', '')
        self.print(self.outtmpl)

    def set_url(self,input_url):
        url = input_url.replace("'","").replace('"','').replace(" ","")

        # 유효성 검사
        if 'youtube.com/watch?v=' in url :
            if requests.get(url).status_code == 200 :
                self.print('입력된 주소 : '+url)
                self.yt_url = url
                self.set_outtmpl()

                url_id = url[url.find('?v=') + 3:].split('&list')[0]
                self.thumbnail = f'https://img.youtube.com/vi/{url_id}/maxresdefault.jpg'
            else : return
        else : return

    def get_thumbnail(self):
        self.print("썸네일 : ",self.thumbnail)
        return self.thumbnail

    def download_mp4(self):
        self.print('mp4 다운로드')
        urls = self.yt_url
        outtmpl = self.outtmpl

        try:
            ydl_opts = {
                'format': 'best/best',  # 가장 좋은 화질로 선택(화질을 선택하여 다운로드 가능)
                'outtmpl': outtmpl,  # 다운로드 경로 설정
                'writesubtitles': 'best',  # 자막 다운로드(자막이 없는 경우 다운로드 X)
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([urls])
        except Exception as e:
            self.print('올바르지 않은 주소',e)

    def download_mp3(self):
        self.print('mp3 다운로드')
        urls = self.yt_url
        outtmpl = self.outtmpl.replace('.%(ext)s', '.mp3')

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': outtmpl,  # 다운로드 경로 설정
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([urls])
        except Exception as e:
            self.print('올바르지 않은 주소',e)

if __name__ == '__main__':
    App = yt_downloader()
    App.debug = True

    url = input("youtube url을 입력하세요.")
#    url = 'http://youtube.com/watch?v=9bZkp7q19f0' # 단일 영상
#    url = 'https://www.youtube.com/watch?v=lr_NsUOpqbA&list=PLxqyJJGD5pCVEg-7XlPtLdyDU_AzwX8Yj' # 재생목록

    App.set_url(url)
    App.get_dir()
    App.get_thumbnail()
    App.download()
    App.download_mp3()

url = 'http://youtube.com/watch?v=9bZkp7q19f0'
url = 'https://www.youtube.com/watch?v=lr_NsUOpqbA&list=PLxqyJJGD5pCVEg-7XlPtLdyDU_AzwX8Yj'  # 재생목록

# 참고 자료
# ydl_opts : https://tech.dslab.kr/2019/09/10/python-youtube_dl/
# thumbnail : https://blog.kesuskim.com/2016/08/how-to-get-youtube-thumbnail/

######## output template :
# https://github.com/ytdl-org/youtube-dl/blob/master/README.md
# title (string): Video title
# creator (string): The creator of the video
# uploader (string): Full name of the video uploader
# uploader_id (string): Nickname or id of the video uploader
# playlist_title (string): Playlist title
# playlist_uploader (string): Full name of the playlist uploader
# ext (string): Video filename extension
# url (string): Video URL
# id (string): Video identifier
# channel (string): Full name of the channel the video is uploaded on
# alt_title (string): A secondary title of the video
# release_date (string): The date (YYYYMMDD) when the video was released
# timestamp (numeric): UNIX timestamp of the moment the video became available
# upload_date (string): Video upload date (YYYYMMDD)
# playlist (string): Name or id of the playlist that contains the video
# playlist_index (numeric): Index of the video in the playlist padded with leading zeros according to the total length of the playlist
# playlist_id (string): Playlist identifier
