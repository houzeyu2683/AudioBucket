import feedparser
import os
import pandas
import urllib.parse
import requests
import hashlib

class Engine:

    def __init__(self, link: str, storage: str) -> None:
        self.link = link
        self.storage = storage
        return

    def pullCatalog(self) -> bool:
        chunk = {'title': [], 'name': [], 'link': [], 'duration': [], 'suffix': []}
        response = feedparser.parse(self.link)
        for channel in response['entries']:
            assert len(channel['enclosures'])==1
            title = channel['title']
            name = hashlib.md5(str(title).encode()).hexdigest()
            if('item'):
                item = channel['enclosures'][0]
                pass
            node = str(item['href']).rfind('https://')
            link = urllib.parse.unquote(item['href'][node:])
            duration = item['length']
            suffix = link[str(link).rfind('.')+1:]
            chunk['title'] += [title]
            chunk['name'] += [name]
            chunk['link'] += [link]
            chunk['duration'] += [duration]
            chunk['suffix'] += [suffix]
            continue
        catalog = pandas.DataFrame(chunk)
        path = os.path.join(self.storage, 'catalog.csv')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        catalog.to_csv(path, index=False)
        self.catalog = catalog
        return(True)

    def readCatalog(self, path: str) -> bool:
        self.catalog = pandas.read_csv(path)
        return(True)
        
    def pullArchive(self) -> bool:
        length = len(self.catalog)
        folder = os.path.join(self.storage, 'archive')
        os.makedirs(folder, exist_ok=True)
        for index, item in self.catalog.iterrows():
            path = os.path.join(folder, f"{item['name']}.{item['suffix']}")
            try:
                response = requests.get(item['link'])
                pencil = open(path, "wb")
                for data in response.iter_content(chunk_size=1024):
                    pencil.write(data)
                    continue
                pencil.close()
                pass
            except:
                pencil.close()
                continue
            print(f"Progress: [{index+1}|{length}]", end='\r')
            continue
        print(f"Progress: [{index+1}|{length}]")
        total = len(os.listdir(folder))
        print(f"Progress: [{total}|{length}]")
        return(True)

    pass