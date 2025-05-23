import gradio
import pandas
import shutil
import os
import yt_dlp
import datetime
import hashlib
import feedparser
import requests

class Audio:

    def __init__(self, user: str) -> None:
        self.user = user
        return

    def renderComponent(self) -> None:
        gradio.HTML(f"<h1 style='text-align: center;'>Audio</h1>")
        variant = "default"
        with gradio.Row(variant=variant):
            variant = "default"
            with gradio.Column(variant=variant):
                source = gradio.Textbox(label="Enter Source")
                condition = gradio.Textbox(label="Enter Condition")
                search = gradio.Button(value="Search")
                self.archive['table'] = gradio.File(
                    label="Download Table", 
                    interactive=False, 
                    visible=False
                )
                collect = gradio.Button(value='Collect', visible=False)
                self.archive['package'] = gradio.File(
                    label="Download Audio", 
                    interactive=False, 
                    visible=False
                )
                pass
            column = {"title": [], "duration": [], "name": [], "link": []}
            value = pandas.DataFrame(column)
            self.view['table'] = gradio.Dataframe(
                value, 
                max_height=500, 
                wrap=True, 
                show_row_numbers=True
            )
            pass
        self.view['progress'] = gradio.HTML("<br><br>")
        search.click(
            fn=self.search, 
            inputs=[source, condition], 
            outputs=[
                self.view['table'], 
                self.archive['table'], 
                self.archive['table'], 
                collect
            ]
        )
        collect.click(
            fn=self.collect,
            inputs=[self.archive['table']],
            outputs=[self.archive['package'], self.archive['package']],
            show_progress_on=self.view['progress']
        )
        return

    def search(self, link: str, query: str) -> tuple:
        if('youtube' in link and 'playlist' in link):
            option = {
                'quiet': True,
                'extract_flat': True,
                'force_generic_extractor': True,
                'no_warnings': True
            }
            with yt_dlp.YoutubeDL(option) as session:
                response = session.extract_info(link, download=False)
                information = response['entries']
                title = [item['title'] for item in information]
                name = [item['id'] for item in information]
                duration = [item['duration'] for item in information]
                pass
            host = 'https://www.youtube.com/watch?v='
            link = [f'{host}{item}' for item in name]
            table = pandas.DataFrame({
                "name": name, 
                'title': title, 
                'duration': duration, 
                'link': link
            })
            pass
        else:
            channel = getattr(feedparser.parse(link), 'entries')
            queue = []
            for episode in channel:
                assert isinstance(episode, dict)
                existence = episode.get('enclosures', None)
                if(existence==[]): continue
                duration = episode.get('itunes_duration', None)
                title = episode.get("title", None)
                item = dict(episode.get('enclosures')[0])
                name = hashlib.sha256(str(item.get("href")).encode()).hexdigest()[:8]
                link = item.get('href')
                value = {
                    'title': title,
                    'duration': duration,
                    'name': name,
                    'link': link
                }
                queue += [value]
                continue
            table = pandas.DataFrame(queue)
            pass
        table = table.dropna().reset_index(drop=True)
        if(True):
            history = os.path.join(".cache", self.user)
            _ = shutil.rmtree(history, ignore_errors=True)
            os.makedirs(history, exist_ok=True)
            code = str(datetime.datetime.now()).encode()
            tag = hashlib.sha512(code).hexdigest()[:8]
            path = os.path.join(history, f'{tag}.csv')
            if(query!=""): 
                table = table.query(query, engine='python')
                table = table.reset_index(drop=True)
                pass
            table.to_csv(path, index=False)
            pass
        status = gradio.update(visible=True)
        response = (table, path, status, status)
        return(response)

    def collect(self, path: str) -> tuple:
        tag = str(os.path.basename(path)).replace(".csv", "")
        folder = os.path.join('.cache', self.user, tag)
        os.makedirs(folder, exist_ok=True)
        table = pandas.read_csv(path)
        length = len(table)
        progress = gradio.Progress()
        for index, item in progress.tqdm(table.iterrows(), total=length):
            if('youtube' in item['link']):
                memory = os.path.join(folder, item['name'])
                option = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(folder, f"{item['name']}.%(ext)s"),
                    'quiet': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav'
                    }],
                    'postprocessor_args': [
                        '-ar', '16000'
                    ],
                    'paths': {
                        'temp': memory
                    }
                }
                session = yt_dlp.YoutubeDL(option)
                try:
                    session.download([item['link']])
                    pass
                except:
                    session.close()
                    shutil.rmtree(memory, ignore_errors=True)
                    print(f"Progress: [{index+1}|{length}]", end='\r')
                    continue
                session.close()
                shutil.rmtree(memory, ignore_errors=True)
                pass
            else:
                response = requests.get(item['link'], stream=True)
                if(response.status_code!=200):
                    print(f"Progress: [{index+1}|{length}]", end='\r')
                    continue
                target = os.path.join(folder, f"{item['name']}.wav")
                stream = open(target, 'wb')
                for chunk in response.iter_content(chunk_size=8192):
                    _ = stream.write(chunk)
                    continue
                stream.close()
                pass
            print(f"Progress: [{index+1}|{length}]", end='\r')
            continue
        print(f"Progress: [{length}|{length}]")
        total = len(os.listdir(folder))
        print(f"Total: [{total}|{length}]")
        if(True):
            shutil.make_archive(
                base_name='package', 
                format='zip', 
                root_dir=folder
            )
            path = os.path.join(folder, "package.zip")
            shutil.move('./package.zip', path)
            pass
        status = gradio.update(visible=True)
        response = (path, status)
        return(response)

    archive = {'table': None, 'package': None}
    view = {'table': None, 'progress': None}
    pass