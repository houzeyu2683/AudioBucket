import os
import pandas
import yt_dlp
import shutil
import gradio

def getAudio(path: str) -> tuple:
    sheet = pandas.read_csv(path)
    tag = os.path.basename(path).replace(".csv", "")
    folder = os.path.join(".cache", tag)
    os.makedirs(folder, exist_ok=True)
    host = 'https://www.youtube.com/watch?v='
    length = len(sheet)
    progress = gradio.Progress()
    for index, item in progress.tqdm(sheet.iterrows(), total=length):
        # progress(index+1, total=length, desc="Download Audio Schedule") 
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
    audio = (path, status)
    return(audio)