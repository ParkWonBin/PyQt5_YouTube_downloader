import os
import youtube_dl

class yt_downloader:
    def __init__(self):
        # 저장 위치 설정 ##############
        self.folderName = "유튜브 다운로드"
        self.folderPath = f"{os.path.expanduser('~')}/Desktop/{self.folderName}/"
        self.yt_url = 'http://youtube.com/watch?v=9bZkp7q19f0'

    def mkdir(self):
        folderPath = self.folderPath
        if not os.path.isdir(folderPath):
            os.makedirs(folderPath)
            print('폴터 생성')
        else:
            os.startfile(folderPath)
            print('폴더 열기')
        ##############################

    def set_url(self,urls):
        self.yt_url = urls
        # 'http://youtube.com/watch?v=9bZkp7q19f0' # 영상
        # 'https://www.youtube.com/watch?v=lr_NsUOpqbA&list=PLxqyJJGD5pCVEg-7XlPtLdyDU_AzwX8Yj' # 재생목록

    def download(self):
        urls = self.yt_url
        Path = self.folderPath

        try:
            ydl_opts = {
                'format': 'best/best',  # 가장 좋은 화질로 선택(화질을 선택하여 다운로드 가능)
                'outtmpl': Path+'%(title)s.%(ext)s',  # 다운로드 경로 설정
                'writesubtitles': 'best',  # 자막 다운로드(자막이 없는 경우 다운로드 X)
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl : ydl.download([urls])
        except  Exception as e:
            print('올바르지 않은 주소')
            print(e)

if __name__ == '__main__':
    App = yt_downloader()
    App.set_url(input("youtube url을 입력하세요."))
    App.mkdir()
    App.download()