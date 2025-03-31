import os
import yt_dlp
import pandas
import shutil

class Engine:

    def __init__(self, link: str, storage: str) -> None:
        self.link = link
        self.storage = storage
        return

    def pullCatalog(self) -> bool:
        option = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(option) as session:
            response = session.extract_info(self.link, download=False)
            pass
        information = response['entries']
        title = [item['title'] for item in information]
        name = [item['id'] for item in information]
        duration = [item['duration'] for item in information]
        catalog = pandas.DataFrame({"name": name, 'title': title,'duration': duration})
        path = os.path.join(self.storage, 'catalog.csv')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        catalog.to_csv(path, index=False)
        self.catalog = catalog
        return(True)

    def readCatalog(self, path: str) -> bool:
        self.catalog = pandas.read_csv(path)
        return(True)

    def pullArchive(self) -> bool:
        folder = os.path.join(self.storage, 'archive')
        os.makedirs(folder, exist_ok=True)
        host = 'https://www.youtube.com/watch?v='
        length = len(self.catalog)
        for index, item in self.catalog.iterrows():
            name = item['name']
            link = f'{host}{name}'
            path = os.path.join(folder, f"{name}.%(ext)s")
            option = {
                'format': 'bestaudio/best',
                'outtmpl': path,
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav'
                }],
                'paths': {
                    'temp': f'.cache/{name}'
                }
            }
            session = yt_dlp.YoutubeDL(option)
            try:
                session.download([link])
                pass
            except:
                session.close()
                continue
            session.close()
            print(f"Progress: [{index+1}|{length}]", end='\r')
            continue
        shutil.rmtree('.cache', ignore_errors=True)
        print(f"Progress: [{length}|{length}]")
        total = len(os.listdir(folder))
        print(f"Total: [{total}|{length}]")
        return(True)

    pass

