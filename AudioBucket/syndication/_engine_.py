import feedparser
import os
import pandas
import urllib.parse
import requests

class Engine:

    def __init__(self, link: str, storage: str) -> None:
        self.link = link
        self.storage = storage
        return

    def pullCatalog(self) -> bool:
        chunk = {'title': [], 'name': [], 'length': [], 'link': [], 'format': []}
        response = feedparser.parse(self.link)
        for channel in response['entries']:
            assert len(channel['enclosures'])==1
            item = channel['enclosures'][0]
            content = os.path.dirname(item['href'])
            code = os.path.basename(item['href'])
            chunk['title'] += [channel['title']]
            chunk['name'] += [os.path.basename(content)]
            chunk['link'] += [urllib.parse.unquote(code)]
            chunk['length'] += [item['length']]
            chunk['format'] += [code[str(code).rfind('.')+1:]]
            continue
        catalog = pandas.DataFrame(chunk)
        path = os.path.join(self.storage, 'catalog.csv')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        catalog.to_csv(path, index=False)
        self.catalog = catalog
        return(True)
    
    def pullArchive(self) -> bool:
        length = len(self.catalog)
        folder = os.path.join(self.storage, 'archive')
        os.makedirs(folder, exist_ok=True)
        for index, item in self.catalog.iterrows():
            path = os.path.join(folder, f"{item['name']}.{item['format']}")
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