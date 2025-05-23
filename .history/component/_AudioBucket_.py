import pandas
import yt_dlp
import gradio
import datetime
import hashlib
import os
import shutil

class Table:

    def __init__(self) -> None:
        return
    
    def getResponse(self, link: str, query: str) -> tuple:
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
        sheet = pandas.DataFrame(
            {"name": name, 'title': title, 'duration': duration}
        )
        sheet = sheet.dropna().reset_index(drop=True)
        code = str(datetime.datetime.now()).encode()
        tag = hashlib.sha512(code).hexdigest()[:8]
        path = f'.cache/{tag}.csv'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        assert isinstance(sheet, pandas.DataFrame)
        status = gradio.update(visible=True)
        if(query==""): 
            sheet.to_csv(path, index=False)
            response = (sheet, path, status, status)
            return(response)
        sheet = sheet.query(query, engine='python')
        sheet.to_csv(path, index=False)
        response = (sheet, path, status, status)
        return(response)
    
    pass


class Audio:
    
    def __init__(self) -> None:
        return
    
    def getResponse(self, path: str)-> tuple:
        sheet = pandas.read_csv(path)
        tag = os.path.basename(path).replace(".csv", "")
        folder = os.path.join(".cache", tag)
        os.makedirs(folder, exist_ok=True)
        host = 'https://www.youtube.com/watch?v='
        length = len(sheet)
        progress = gradio.Progress()
        for index, item in progress.tqdm(sheet.iterrows(), total=length):
            name = item['name']
            link = f'{host}{name}'
            option = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(folder, f"{name}.%(ext)s"),
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav'
                }],
                'postprocessor_args': [
                    '-ar', '16000'
                ],
                'paths': {
                    'temp': os.path.join('.cache', name)
                }
            }
            session = yt_dlp.YoutubeDL(option)
            try:
                session.download([link])
                pass
            except:
                session.close()
                shutil.rmtree(os.path.join('.cache', name), ignore_errors=True)
                continue
            session.close()
            shutil.rmtree(os.path.join('.cache', name), ignore_errors=True)
            print(f"Progress: [{index+1}|{length}]", end='\r')
            continue
        print(f"Progress: [{length}|{length}]")
        total = len(os.listdir(folder))
        print(f"Total: [{total}|{length}]")
        shutil.make_archive(base_name='package', format='zip', root_dir=folder)
        path = os.path.join(folder, "package.zip")
        shutil.move('./package.zip', path)
        status = gradio.update(visible=True)
        response = (path, status)
        return(response)
    
    pass

class AudioBucket:

    def __init__(self, service: gradio.Blocks) -> None:
        self.service = service
        return

    def getComponent(self) -> gradio.Blocks:
        title = 'AudioBucket'
        theme = gradio.themes.Ocean()
        archive = {}
        view = {}
        with gradio.Blocks(title=title, theme=theme) as interface:
            gradio.HTML(f"<h1 style='text-align: center;'>{title}</h1>")
            variant = "default"
            with gradio.Row(variant=variant):
                variant = "default"
                with gradio.Column(variant=variant):
                    source = gradio.Textbox(label="Enter Source")
                    query = gradio.Textbox(label="Enter Query")
                    getTable = gradio.Button(value="Get Table")
                    archive['table'] = gradio.File(
                        label="Download Table", 
                        interactive=False, 
                        visible=False
                    )
                    getAudio = gradio.Button(value='Get Audio', visible=False)
                    archive['audio'] = gradio.File(
                        label="Download Audio", 
                        interactive=False, 
                        visible=False
                    )
                    pass
                value = pandas.DataFrame(
                    {"name": [], "title": [], "duration": []}
                )
                view['table'] = gradio.Dataframe(
                    value, 
                    max_height=500, 
                    wrap=True, 
                    show_row_numbers=True
                )
                getTable.click(
                    fn=Table().getResponse, 
                    inputs=[source, query], 
                    outputs=[view['table'], archive['table'], archive['table'], getAudio]
                )
                pass
            progress = gradio.HTML("<br><br>")
            getAudio.click(
                fn=Audio().getResponse,
                inputs=[archive['table']],
                outputs=[archive['audio'], archive['audio']],
                show_progress_on=progress
            )
            pass
        component = interface
        return(component)

    pass