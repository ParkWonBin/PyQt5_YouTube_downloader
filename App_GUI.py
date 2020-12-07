from App import yt_downloader

if __name__ == '__main__':
    print('GUI')
    App = yt_downloader()
    App.set_url(input("youtube url을 입력하세요."))
    App.get_dir()
    App.download_mp3()